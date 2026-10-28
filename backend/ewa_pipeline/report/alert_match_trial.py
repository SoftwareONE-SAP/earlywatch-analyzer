"""Offline trial: does Decision-1 match SAP alerts to our findings better than word overlap?

Nothing here is used by the live pipeline. It reads a saved _result.json, asks
Decision-1 about every (SAP alert, finding) pair, and writes CSV files so a
person can mark the right answers and compare the two methods.
"""
from __future__ import annotations

import csv
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any, Callable

from ewa_pipeline.agents.alert_decision import CRITERIA, EVIDENCE_LIMIT, QUESTION, decision_state  # noqa: F401
from ewa_pipeline.report.reconciliation import ALERT_MATCH_THRESHOLD, _alert_score, _words, reconcile
from ewa_pipeline.report.schemas import AnalysisResult, SapServiceSummary

PAIR_COLUMNS = [
    "alert_no", "alert_rating", "alert_text", "finding_id", "section_title", "severity",
    "finding_title", "jaccard", "jaccard_rank", "d1_p", "d1_rank", "d1_verdict",
]
SUMMARY_COLUMNS = [
    "alert_no", "alert_rating", "alert_text", "wo_pick", "wo_score", "d1_pick", "d1_p",
    "d1_extra_matches", "d1_possibles", "top_candidates", "proposed_correct_ids",
    "correct_finding_ids",
]

Ask = Callable[[str, dict, Any], dict]


def build_pairs(result: dict) -> list[dict]:
    """One row per (SAP alert, finding). Alert numbers start at 1. No pre-filter."""
    analysis = AnalysisResult.model_validate(result)
    summary = SapServiceSummary.model_validate(result.get("sap_summary") or {})
    findings = [(a.section_title, f) for a in analysis.domain_analyses for f in a.findings]
    pairs: list[dict] = []
    for alert_no, alert in enumerate(summary.alerts, start=1):
        alert_words = _words(alert.text)
        rows = [
            {
                "alert_no": alert_no,
                "alert_rating": alert.rating,
                "alert_text": alert.text,
                "finding_id": finding.id,
                "section_title": section_title,
                "severity": finding.severity,
                "finding_title": finding.title,
                "evidence": finding.evidence,
                "jaccard": _alert_score(alert_words, finding),
            }
            for section_title, finding in findings
        ]
        order = sorted(range(len(rows)), key=lambda i: (-rows[i]["jaccard"], i))
        for rank, i in enumerate(order, start=1):
            rows[i]["jaccard_rank"] = rank
        pairs.extend(rows)
    return pairs


def pair_state(pair: dict) -> dict:
    return decision_state(
        {"rating": pair["alert_rating"], "text": pair["alert_text"]},
        {"id": pair["finding_id"], "severity": pair["severity"],
         "title": pair["finding_title"], "evidence": pair["evidence"]},
        pair["section_title"],
    )


def request_chars(pairs: list[dict]) -> int:
    """Rough size of what is sent: question + criteria + state text for every pair."""
    fixed = len(QUESTION) + sum(len(v) for v in CRITERIA.values())
    total = 0
    for pair in pairs:
        state = pair_state(pair)
        total += fixed + sum(len(str(v)) for part in state.values() for v in part.values())
    return total


def score_pairs(pairs: list[dict], ask: Ask, workers: int = 4) -> dict[tuple[int, str], float | None]:
    """Ask Decision-1 about every pair. An empty answer ({}) becomes None (an error)."""
    def one(pair: dict) -> float | None:
        answer = ask(QUESTION, CRITERIA, pair_state(pair))
        p = answer.get("true") if answer else None
        return float(p) if p is not None else None

    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        values = list(pool.map(one, pairs))
    return {(p["alert_no"], p["finding_id"]): v for p, v in zip(pairs, values)}


def _by_alert(pairs: list[dict]) -> dict[int, list[dict]]:
    grouped: dict[int, list[dict]] = {}
    for pair in pairs:
        grouped.setdefault(pair["alert_no"], []).append(pair)
    return grouped


def pick_word_overlap(pairs: list[dict]) -> dict[int, dict | None]:
    """Today's rule: best Jaccard per alert, kept only if it reaches the threshold."""
    picks: dict[int, dict | None] = {}
    for alert_no, group in _by_alert(pairs).items():
        best = min(group, key=lambda p: p["jaccard_rank"])
        picks[alert_no] = (
            {"finding_id": best["finding_id"], "score": best["jaccard"]}
            if best["jaccard"] > 0 and best["jaccard"] >= ALERT_MATCH_THRESHOLD else None
        )
    return picks


def pick_decision(pairs: list[dict], scores: dict, keep: float = 0.8, possible: float = 0.5):
    """Decision-1 picks. Returns (by_alert, by_pair).

    by_alert[alert_no] = {"pick": id|None, "p": float|None, "extra": [ids], "possibles": [ids]}
    by_pair[(alert_no, finding_id)] = {"p", "rank", "verdict"} with verdict
    match / possible / none / error.
    """
    by_alert: dict[int, dict] = {}
    by_pair: dict[tuple[int, str], dict] = {}
    for alert_no, group in _by_alert(pairs).items():
        scored = [(p, scores.get((alert_no, p["finding_id"]))) for p in group]
        ranked = sorted(
            (item for item in scored if item[1] is not None),
            key=lambda item: (-item[1], item[0]["jaccard_rank"]),
        )
        rank_of = {item[0]["finding_id"]: r for r, item in enumerate(ranked, start=1)}
        for pair, p in scored:
            if p is None:
                verdict = "error"
            elif p >= keep:
                verdict = "match"
            elif p >= possible:
                verdict = "possible"
            else:
                verdict = "none"
            by_pair[(alert_no, pair["finding_id"])] = {
                "p": p, "rank": rank_of.get(pair["finding_id"]), "verdict": verdict,
            }
        matches = [item for item in ranked if item[1] >= keep]
        by_alert[alert_no] = {
            "pick": matches[0][0]["finding_id"] if matches else None,
            "p": matches[0][1] if matches else None,
            "extra": [item[0]["finding_id"] for item in matches[1:]],
            "possibles": [item[0]["finding_id"] for item in ranked if possible <= item[1] < keep],
        }
    return by_alert, by_pair


def _fmt_p(value: float | None) -> str:
    return "" if value is None else f"{value:.3f}"


def write_pairs_csv(path: Path, pairs: list[dict], by_pair: dict) -> None:
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=PAIR_COLUMNS)
        writer.writeheader()
        for pair in pairs:
            info = by_pair[(pair["alert_no"], pair["finding_id"])]
            row = {c: pair.get(c, "") for c in PAIR_COLUMNS}
            row["jaccard"] = f"{pair['jaccard']:.3f}"
            row["d1_p"] = _fmt_p(info["p"])
            row["d1_rank"] = "" if info["rank"] is None else info["rank"]
            row["d1_verdict"] = info["verdict"]
            writer.writerow(row)


def _top_candidates(group: list[dict], scores: dict) -> str:
    by_j = sorted(group, key=lambda p: p["jaccard_rank"])[:3]
    scored = [p for p in group if scores.get((p["alert_no"], p["finding_id"])) is not None]
    by_p = sorted(scored, key=lambda p: (-scores[(p["alert_no"], p["finding_id"])], p["jaccard_rank"]))[:3]
    chosen: list[dict] = []
    for p in by_p + by_j:
        if p not in chosen:
            chosen.append(p)
    parts = []
    for p in chosen:
        value = scores.get((p["alert_no"], p["finding_id"]))
        p_text = "n/a" if value is None else f"{value:.2f}"
        parts.append(f"{p['finding_id']}: {p['finding_title']} (p={p_text}, J={p['jaccard']:.2f})")
    return " | ".join(parts)


def write_summary_csv(path: Path, pairs: list[dict], wo_picks: dict, d1_by_alert: dict,
                      scores: dict) -> None:
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=SUMMARY_COLUMNS)
        writer.writeheader()
        for alert_no, group in _by_alert(pairs).items():
            wo, d1 = wo_picks.get(alert_no), d1_by_alert[alert_no]
            writer.writerow({
                "alert_no": alert_no,
                "alert_rating": group[0]["alert_rating"],
                "alert_text": group[0]["alert_text"],
                "wo_pick": wo["finding_id"] if wo else "",
                "wo_score": f"{wo['score']:.3f}" if wo else "",
                "d1_pick": d1["pick"] or "",
                "d1_p": _fmt_p(d1["p"]),
                "d1_extra_matches": "; ".join(d1["extra"]),
                "d1_possibles": "; ".join(d1["possibles"]),
                "top_candidates": _top_candidates(group, scores),
                "proposed_correct_ids": "",
                "correct_finding_ids": "",
            })


def summary_has_labels(path: Path) -> bool:
    """True if the file already holds any hand-filled label (so it must not be lost)."""
    if not Path(path).exists():
        return False
    with open(path, newline="", encoding="utf-8-sig") as f:
        return any(
            (row.get("correct_finding_ids") or "").strip() or (row.get("proposed_correct_ids") or "").strip()
            for row in csv.DictReader(f)
        )


def read_labels(summary_csv: Path) -> dict[int, set[str]]:
    """{alert_no: set of correct finding ids}. The word 'none' gives an empty set. Blank rows are skipped."""
    labels: dict[int, set[str]] = {}
    with open(summary_csv, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            raw = (row.get("correct_finding_ids") or "").strip()
            if not raw:
                continue
            if raw.lower() == "none":
                labels[int(row["alert_no"])] = set()
            else:
                labels[int(row["alert_no"])] = {part.strip() for part in raw.split(";") if part.strip()}
    return labels


def scoreboard(labels: dict[int, set[str]], wo_picks: dict, d1_by_alert: dict) -> dict:
    """Count Right / Wrong / Missed / Correct-none per method, for labelled alerts only."""
    def empty() -> dict:
        return {"right": 0, "wrong": 0, "missed": 0, "correct_none": 0}

    board = {"alerts": 0, "word_overlap": empty(), "decision": {**empty(), "wrong_extras": 0}}

    def tally(counts: dict, pick: str | None, correct: set[str]) -> None:
        if pick is None:
            counts["correct_none" if not correct else "missed"] += 1
        else:
            counts["right" if pick in correct else "wrong"] += 1

    for alert_no, correct in labels.items():
        if alert_no not in d1_by_alert:
            continue
        board["alerts"] += 1
        wo = wo_picks.get(alert_no)
        tally(board["word_overlap"], wo["finding_id"] if wo else None, correct)
        d1 = d1_by_alert[alert_no]
        tally(board["decision"], d1["pick"], correct)
        board["decision"]["wrong_extras"] += sum(1 for fid in d1["extra"] if fid not in correct)
    return board


def format_scoreboard(board: dict) -> str:
    lines = [f"Scoreboard ({board['alerts']} labelled alerts)",
             f"{'Method':<14}{'Right':>7}{'Wrong':>7}{'Missed':>8}{'Correct-none':>14}"]
    for name, key in (("Word overlap", "word_overlap"), ("Decision-1", "decision")):
        c = board[key]
        lines.append(f"{name:<14}{c['right']:>7}{c['wrong']:>7}{c['missed']:>8}{c['correct_none']:>14}")
    lines.append(f"Decision-1 wrong extra matches: {board['decision']['wrong_extras']}")
    return "\n".join(lines)


def replay_board(result: dict, tree: dict, saved: dict, labels: dict[int, set[str]],
                 keep: float, possible: float) -> dict:
    """Re-run the live matching rules on saved Decision-1 scores, with and without the heading and same-statement checks.

    Makes no AI calls. `saved` is the _d1_scores.json content: {"<alert no>|<finding id>": p}.
    Alert numbers start at 1. Returns {"before", "after", "changed"} where before/after count
    right / wrong / missed / correct_none for labelled alerts, and changed lists
    (alert_no, old finding id, new finding id) for every alert those checks moved.
    """
    analysis = AnalysisResult.model_validate(result)
    summary = SapServiceSummary.model_validate(result.get("sap_summary") or {})
    alert_scores: dict[int, dict[str, float]] = {}
    for key, p in saved.items():
        alert_no, _, finding_id = key.partition("|")
        if p is not None and alert_no.isdigit():
            alert_scores.setdefault(int(alert_no) - 1, {})[finding_id] = float(p)

    def first_ids(checks: bool) -> dict[int, str | None]:
        rows = reconcile(
            analysis, summary, tree, analysis.system_profile, alert_scores=alert_scores,
            keep=keep, possible=possible, heading_check=checks, statement_check=checks,
        )
        alert_rows = [r for r in rows if r.source == "Alert"]
        return {i: (r.finding_ids[0] if r.finding_ids else None) for i, r in enumerate(alert_rows, start=1)}

    def tally(picks: dict[int, str | None]) -> dict:
        counts = {"right": 0, "wrong": 0, "missed": 0, "correct_none": 0}
        for alert_no, correct in labels.items():
            if alert_no not in picks:
                continue
            pick = picks[alert_no]
            if pick is None:
                counts["correct_none" if not correct else "missed"] += 1
            else:
                counts["right" if pick in correct else "wrong"] += 1
        return counts

    before, after = first_ids(False), first_ids(True)
    return {
        "before": tally(before),
        "after": tally(after),
        "changed": [(n, before[n], after[n]) for n in sorted(before) if before[n] != after[n]],
    }


def format_replay(board: dict) -> str:
    lines = [f"{'':<8}{'Right':>7}{'Wrong':>7}{'Missed':>8}{'Correct-none':>14}"]
    for name in ("before", "after"):
        c = board[name]
        lines.append(f"{name:<8}{c['right']:>7}{c['wrong']:>7}{c['missed']:>8}{c['correct_none']:>14}")
    if board["changed"]:
        lines.append("Changed alerts (alert no: old -> new):")
        lines += [f"  {n}: {old} -> {new}" for n, old, new in board["changed"]]
    else:
        lines.append("Changed alerts: none")
    return "\n".join(lines)
