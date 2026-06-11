#!/usr/bin/env python3

import argparse
import csv
import html
from pathlib import Path


START_MARKER = "<!-- AUTO-GENERATED: SHEAR TABLE START -->"
END_MARKER = "<!-- AUTO-GENERATED: SHEAR TABLE END -->"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render a CSV file into the benchmark_hot_upsetting_shear.html page."
    )
    parser.add_argument("csv_file", help="Path to the CSV file to render.")
    parser.add_argument(
        "--html",
        default="benchmark_hot_upsetting_shear.html",
        help="HTML file to update. Defaults to benchmark_hot_upsetting_shear.html.",
    )
    return parser.parse_args()


def read_csv_rows(csv_path: Path) -> tuple[list[str], list[list[str]]]:
    with csv_path.open(newline="", encoding="utf-8") as handle:
        sample = handle.read(2048)
        handle.seek(0)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t")
        except csv.Error:
            dialect = csv.excel

        reader = csv.reader(handle, dialect)
        rows = [[cell.strip() for cell in row] for row in reader if any(cell.strip() for cell in row)]

    if not rows:
        raise ValueError(f"{csv_path} is empty.")

    headers = rows[0]
    body = rows[1:]
    return headers, body


def build_table(headers: list[str], rows: list[list[str]], source_name: str) -> str:
    escaped_headers = [html.escape(header) for header in headers]
    body_lines = []

    for row in rows:
        padded = row + [""] * max(0, len(headers) - len(row))
        cells = "".join(f"<td>{html.escape(value)}</td>" for value in padded[: len(headers)])
        body_lines.append(f"      <tr>{cells}</tr>")

    if not body_lines:
        colspan = max(1, len(headers))
        body_lines.append(f'      <tr><td colspan="{colspan}">No data rows found.</td></tr>')

    head = "".join(f"<th>{header}</th>" for header in escaped_headers)

    return "\n".join(
        [
            START_MARKER,
            f'  <div class="table-source"><p>Source: <code>{html.escape(source_name)}</code></p></div>',
            '  <div class="table-wrapper">',
            '    <table class="benchmark-table">',
            f"      <thead><tr>{head}</tr></thead>",
            "      <tbody>",
            *body_lines,
            "      </tbody>",
            "    </table>",
            "  </div>",
            f"  {END_MARKER}",
        ]
    )


def replace_between_markers(document: str, replacement: str) -> str:
    start = document.find(START_MARKER)
    end = document.find(END_MARKER)

    if start == -1 or end == -1 or end < start:
        raise ValueError("Could not find table markers in the HTML file.")

    end += len(END_MARKER)
    return document[:start] + replacement + document[end:]


def main() -> int:
    args = parse_args()
    csv_path = Path(args.csv_file)
    html_path = Path(args.html)

    if not csv_path.is_file():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    if not html_path.is_file():
        raise FileNotFoundError(f"HTML file not found: {html_path}")

    headers, rows = read_csv_rows(csv_path)
    table_html = build_table(headers, rows, str(csv_path))

    html_text = html_path.read_text(encoding="utf-8")
    updated = replace_between_markers(html_text, table_html)
    html_path.write_text(updated, encoding="utf-8")

    print(f"Updated {html_path} with table data from {csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
