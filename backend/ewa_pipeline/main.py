import json
import warnings
from pathlib import Path

import click
from dotenv import load_dotenv
from rich.console import Console

# Suppress Pydantic serialization noise that fires on every LLM call when
# use_responses_api=True + with_structured_output(include_raw=True).
warnings.filterwarnings(
    "ignore",
    message="Pydantic serializer warnings",
    category=UserWarning,
    module="pydantic",
)

console = Console()


def _load_env_and_config(config_path: str = "config.yaml"):
    load_dotenv()
    from ewa_pipeline.config import load_config

    return load_config(Path(config_path))


@click.group()
def cli():
    """EWA Deep Analyzer - SAP EarlyWatch Alert analysis pipeline."""


def _print_completion(result, cost_tracker, output_path: Path, doc_name: str) -> None:
    health_color = {"Critical": "red", "Warning": "yellow", "Healthy": "green"}.get(
        result.overall_system_health, "white"
    )
    total_cost = cost_tracker.to_dict(document_name=doc_name)["totals"]["cost_usd"]
    console.print(
        f"\n[bold green]Done![/bold green] "
        f"Overall health: [{health_color}]{result.overall_system_health}[/{health_color}] | "
        f"{sum(len(da.findings) for da in result.domain_analyses)} findings | "
        f"{len(result.cross_references)} cross-references\n"
        f"Report saved to: [bold]{output_path}[/bold]\n"
        f"Cost: ${total_cost:,.2f}"
    )


@cli.command()
@click.option("--doc", "doc_path", required=True, type=click.Path(exists=True), help="Path to EWA .doc document")
@click.option("--output", default="output/analysis.xlsx", show_default=True, help="Output Excel path")
@click.option("--config", "config_path", default="config.yaml", show_default=True, help="Config YAML path")
@click.option("--verbose", is_flag=True, help="Show detailed progress")
@click.option("--skip-index", is_flag=True, help="Reuse existing _tree.json if present")
@click.option("--skip-analysis", is_flag=True, help="Reuse existing _result.json")
def analyze(doc_path: str, output: str, config_path: str, verbose: bool, skip_index: bool, skip_analysis: bool):
    """Run the full EWA analysis pipeline for a .doc document."""
    config = _load_env_and_config(config_path)
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    from ewa_pipeline.services.pipeline import run_pipeline

    def _cli_progress(event):
        stage = event.stage.replace("_", " ").title()
        line = f"[cyan]{stage}[/cyan]: {event.label}"
        if event.detail:
            line += f" ({event.detail})"
        console.print(line)

    result, cost_tracker, artifacts = run_pipeline(
        config=config,
        output_path=output_path,
        input_path=Path(doc_path),
        skip_index=skip_index,
        skip_analysis=skip_analysis,
        verbose=verbose,
        skills_dir=Path("skills"),
        progress_callback=_cli_progress,
    )
    console.print(f"  Result saved to [bold]{artifacts.result_path}[/bold]")
    console.print(f"  Cost report saved to [bold]{artifacts.cost_path}[/bold]")
    _print_completion(result, cost_tracker, output_path, artifacts.doc_name)


@cli.command()
@click.option("--result", required=True, type=click.Path(exists=True), help="Path to _result.json from a previous run")
@click.option("--tree", "tree_path", required=True, type=click.Path(exists=True), help="Path to _tree.json from Phase 0")
@click.option("--output", default="output/analysis.xlsx", show_default=True, help="Output Excel path")
@click.option("--config", "config_path", default="config.yaml", show_default=True, help="Config YAML path")
def excel(result: str, tree_path: str, output: str, config_path: str):
    """Regenerate Excel from saved analysis artifacts."""
    config = _load_env_and_config(config_path)
    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    from ewa_pipeline.report import excel_generator
    from ewa_pipeline.report.schemas import AnalysisResult
    from ewa_pipeline.tracking.cost_tracker import CostTracker

    console.print(f"[cyan]Loading[/cyan]: {Path(result).name}")
    analysis_result = AnalysisResult.model_validate_json(Path(result).read_text(encoding="utf-8"))
    with open(tree_path, encoding="utf-8") as f:
        tree = json.load(f)

    cost_tracker = CostTracker(pricing=config.pricing_dict())
    cost_path = output_path.parent / f"{output_path.stem}_cost.json"

    console.print("[cyan]Phase 3[/cyan]: generating Excel workbook...")
    excel_generator.generate(analysis_result, output_path, tree=tree)

    cost_tracker.save(cost_path, document_name=Path(result).stem)
    console.print(f"  Cost report saved to [bold]{cost_path}[/bold]")

    health_color = {"Critical": "red", "Warning": "yellow", "Healthy": "green"}.get(
        analysis_result.overall_system_health, "white"
    )
    total_cost = cost_tracker.to_dict(document_name=Path(result).stem)["totals"]["cost_usd"]
    console.print(
        f"\n[bold green]Done![/bold green] "
        f"Overall health: [{health_color}]{analysis_result.overall_system_health}[/{health_color}] | "
        f"{sum(len(da.findings) for da in analysis_result.domain_analyses)} findings\n"
        f"Report saved to: [bold]{output_path}[/bold]\n"
        f"Cost: ${total_cost:,.2f}"
    )


@cli.command()
@click.option("--host", default="127.0.0.1", show_default=True, help="Host for the web app")
@click.option("--port", default=8000, show_default=True, type=int, help="Port for the web app")
def web(host: str, port: int):
    """Run the web UI and API."""
    import uvicorn

    uvicorn.run("ewa_analyzer.web:app", host=host, port=port, reload=False)


@cli.command()
@click.option("--doc", "doc_path", required=True, type=click.Path(exists=True), help="Path to EWA .doc document")
@click.option("--config", "config_path", default="config.yaml", show_default=True, help="Config YAML path")
def index(doc_path: str, config_path: str):
    """Parse a .doc document and build the document tree for debugging."""
    _load_env_and_config(config_path)

    from converters.compact_html_converter import convert_html_to_compact_html
    from converters.doc_html_converter import convert_doc_to_html
    from ewa_pipeline.indexer.html_tree_builder import build_document_tree_from_html
    from ewa_pipeline.indexer.tree_navigator import get_analyzable_sections, tree_to_summary

    doc_file = Path(doc_path)
    data_dir = doc_file.parent
    compact_path = data_dir / f"{doc_file.stem}.html"

    console.print(f"[cyan]Converting[/cyan]: {doc_file.name} -> compact HTML...")
    html_path = convert_doc_to_html(doc_file, data_dir / f"{doc_file.stem}_html", prefer_word_com=False)
    convert_html_to_compact_html(html_path, compact_path)

    console.print("[cyan]Indexing[/cyan]: building HTML document structure...")
    tree = build_document_tree_from_html(compact_path, data_dir)

    sections = get_analyzable_sections(tree)
    console.print(f"  Analyzable sections: {len(sections)}")
    console.print(f"\n{tree_to_summary(tree)}")


@cli.command("alert-trial")
@click.option("--result", "result_path", required=True, type=click.Path(exists=True), help="Path to _result.json from a previous run")
@click.option("--out-prefix", required=True, help="Start of the output file names, e.g. output/trial")
@click.option("--keep", default=0.8, show_default=True, type=float, help="Decision-1 probability that counts as a match")
@click.option("--possible", default=0.5, show_default=True, type=float, help="Probability that counts as a possible match")
@click.option("--workers", default=4, show_default=True, type=int, help="Parallel calls to Decision-1")
@click.option("--config", "config_path", default="config.yaml", show_default=True, help="Config YAML path")
@click.option("--labels", "labels_path", default=None, type=click.Path(exists=True), help="Summary CSV with correct_finding_ids filled in; prints a scoreboard")
@click.option("--reuse-scores", is_flag=True, help="Read <prefix>_d1_scores.json instead of calling the model")
def alert_trial(result_path: str, out_prefix: str, keep: float, possible: float, workers: int,
                config_path: str, labels_path: str | None, reuse_scores: bool):
    """Offline trial: Decision-1 vs word overlap for matching SAP alerts to findings."""
    import shutil
    import time

    from ewa_pipeline.agents import decision_client
    from ewa_pipeline.report import alert_match_trial as trial

    config = _load_env_and_config(config_path)
    config = config.model_copy(update={"decision_enabled": True})

    result = json.loads(Path(result_path).read_text(encoding="utf-8"))
    pairs = trial.build_pairs(result)
    if not pairs:
        raise click.ClickException("No SAP alerts or no findings in this result file.")

    prefix = Path(out_prefix)
    prefix.parent.mkdir(parents=True, exist_ok=True)
    scores_path = Path(f"{prefix}_d1_scores.json")
    pairs_csv = Path(f"{prefix}_alert_pairs.csv")
    summary_csv = Path(f"{prefix}_alert_summary.csv")

    # Read the user's labels first, so nothing below can lose them.
    labels = trial.read_labels(Path(labels_path)) if labels_path else None

    if reuse_scores:
        if not scores_path.exists():
            raise click.ClickException(f"Cannot reuse scores: {scores_path} does not exist.")
        saved = json.loads(scores_path.read_text(encoding="utf-8"))
        scores = {}
        for pair in pairs:
            key = (pair["alert_no"], pair["finding_id"])
            scores[key] = saved.get(f"{key[0]}|{key[1]}")
        console.print(f"Reused scores from {scores_path} (no calls made)")
    else:
        def ask(question, options, context):
            return decision_client.decide(question, options, context, config=config)

        started = time.perf_counter()
        scores = trial.score_pairs(pairs, ask, workers=workers)
        seconds = time.perf_counter() - started
        errors = sum(1 for v in scores.values() if v is None)
        scores_path.write_text(
            json.dumps({f"{a}|{f}": v for (a, f), v in scores.items()}, indent=2), encoding="utf-8"
        )
        console.print(
            f"Calls made: {len(pairs)} | errors: {errors} | seconds: {seconds:.1f} | "
            f"characters sent: {trial.request_chars(pairs):,}",
            markup=False,
        )
        if errors == len(pairs):
            raise click.ClickException("Every call failed. Check the endpoint, key and Decision-1 access.")

    wo_picks = trial.pick_word_overlap(pairs)
    d1_by_alert, d1_by_pair = trial.pick_decision(pairs, scores, keep=keep, possible=possible)

    if trial.summary_has_labels(summary_csv):
        stamp = time.strftime("%Y%m%d_%H%M%S")
        backup = summary_csv.with_name(f"{summary_csv.stem}_labelled_backup_{stamp}{summary_csv.suffix}")
        shutil.copy2(summary_csv, backup)
        console.print(f"Existing labels kept in {backup}", markup=False)

    trial.write_pairs_csv(pairs_csv, pairs, d1_by_pair)
    trial.write_summary_csv(summary_csv, pairs, wo_picks, d1_by_alert, scores)
    console.print(f"Wrote {scores_path if not reuse_scores else 'scores (reused)'}, {pairs_csv}, {summary_csv}", markup=False)

    if labels is not None:
        console.print(trial.format_scoreboard(trial.scoreboard(labels, wo_picks, d1_by_alert)), markup=False)


@cli.command("alert-replay")
@click.option("--result", "result_path", required=True, type=click.Path(exists=True), help="Path to _result.json from a previous run")
@click.option("--tree", "tree_path", required=True, type=click.Path(exists=True), help="Path to the report's compact_tree.json")
@click.option("--scores", "scores_path", required=True, type=click.Path(exists=True), help="Saved <prefix>_d1_scores.json from alert-trial")
@click.option("--labels", "labels_path", required=True, type=click.Path(exists=True), help="Summary CSV with correct_finding_ids filled in")
@click.option("--keep", default=None, type=float, help="Match cut-off (default: DECISION_KEEP from config)")
@click.option("--possible", default=None, type=float, help="Possible-match cut-off (default: DECISION_POSSIBLE from config)")
@click.option("--config", "config_path", default="config.yaml", show_default=True, help="Config YAML path")
def alert_replay(result_path: str, tree_path: str, scores_path: str, labels_path: str,
                 keep: float | None, possible: float | None, config_path: str):
    """Offline check: replay saved Decision-1 scores with and without the report-heading check.

    Makes no AI calls and writes no files.
    """
    from ewa_pipeline.report import alert_match_trial as trial

    if keep is None or possible is None:
        config = _load_env_and_config(config_path)
        keep = config.decision_keep if keep is None else keep
        possible = config.decision_possible if possible is None else possible

    def load(path: str) -> dict:
        return json.loads(Path(path).read_text(encoding="utf-8-sig"))

    board = trial.replay_board(
        load(result_path), load(tree_path), load(scores_path),
        trial.read_labels(Path(labels_path)), keep, possible,
    )
    console.print(f"Replay at keep={keep}, possible={possible}", markup=False)
    console.print(trial.format_replay(board), markup=False)


if __name__ == "__main__":
    cli()
