#!/usr/bin/env python3
"""
Local quality check: convert a Word .doc/.docx to Markdown end-to-end.

Examples:
  py -3 backend/scripts/doc_to_markdown_cli.py path/to/report.doc
  py -3 backend/scripts/doc_to_markdown_cli.py report.doc -o samples/compare/from_doc.md
  py -3 backend/scripts/doc_to_markdown_cli.py report.doc --compare samples/compare/html_from_zip.md
  py -3 backend/scripts/doc_to_markdown_cli.py report.doc --keep-workdir
"""

from __future__ import annotations

import argparse
import json
import logging
import sys
from pathlib import Path

# Allow running from repo root without installing the package.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from converters.doc_html_converter import LibreOfficeNotFoundError  # noqa: E402
from converters.doc_markdown_converter import (  # noqa: E402
    compare_markdown,
    convert_doc_to_markdown,
)


def _default_output_path(doc_path: Path) -> Path:
    repo_root = BACKEND_ROOT.parent
    out_dir = repo_root / "samples" / "compare"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir / f"{doc_path.stem}_from_doc.md"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert .doc/.docx to Markdown via LibreOffice + html_markdown_converter.",
    )
    parser.add_argument("doc", type=Path, help="Path to .doc or .docx EWA report")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output .md path (default: samples/compare/<stem>_from_doc.md)",
    )
    parser.add_argument(
        "--compare",
        type=Path,
        metavar="REFERENCE.md",
        help="Reference markdown (e.g. from ZIP/HTML path) for metric comparison",
    )
    parser.add_argument(
        "--keep-workdir",
        action="store_true",
        help="Keep intermediate HTML and assets (prints work directory path)",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable debug logging",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(levelname)s: %(message)s",
    )

    doc_path = args.doc.resolve()
    if not doc_path.is_file():
        print(f"Error: file not found: {doc_path}", file=sys.stderr)
        return 1

    output_path = args.output.resolve() if args.output else _default_output_path(doc_path)

    try:
        result = convert_doc_to_markdown(
            doc_path,
            output_path,
            keep_intermediate=args.keep_workdir,
        )
    except LibreOfficeNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        print(
            "\nInstall LibreOffice, then retry. On Windows:\n"
            "  winget install TheDocumentFoundation.LibreOffice",
            file=sys.stderr,
        )
        return 1
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(f"Document kind:      {result.document_kind}")
    print(f"Markdown written: {result.markdown_path}")
    print(f"HTML intermediate:  {result.html_path}")
    print("Metrics:")
    for key, value in result.metrics.items():
        print(f"  {key}: {value}")

    if args.compare:
        reference_path = args.compare.resolve()
        if not reference_path.is_file():
            print(f"Error: reference file not found: {reference_path}", file=sys.stderr)
            return 1
        reference_md = reference_path.read_text(encoding="utf-8", errors="replace")
        comparison = compare_markdown(reference_md, result.markdown)
        print(f"\nComparison vs {reference_path.name}:")
        print(json.dumps(comparison, indent=2))

    if args.keep_workdir:
        print(f"Work directory kept: {result.work_dir}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
