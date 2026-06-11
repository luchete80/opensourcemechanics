#!/usr/bin/env python3

import argparse
import csv
import html
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute relative error from a CSV and generate PNG, Markdown, and HTML outputs."
    )
    parser.add_argument("csv_file", help="Input CSV file.")
    parser.add_argument(
        "--x-col",
        help="Column name for the x-axis. Defaults to the first CSV column.",
    )
    parser.add_argument(
        "--value-col",
        help="Column name for the computed/simulated values. Defaults to the second CSV column.",
    )
    parser.add_argument(
        "--reference-col",
        help="Column name for the reference values. Defaults to the third CSV column.",
    )
    parser.add_argument(
        "--output-dir",
        help="Directory for generated files. Defaults to the CSV directory.",
    )
    parser.add_argument(
        "--prefix",
        help="Prefix for generated files. Defaults to the CSV stem.",
    )
    return parser.parse_args()


def clean_headers(fieldnames: list[str]) -> list[str]:
    return [name.strip() for name in fieldnames]


def read_csv(csv_path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, skipinitialspace=True)
        if reader.fieldnames is None:
            raise ValueError(f"{csv_path} does not contain a header row.")

        headers = clean_headers(reader.fieldnames)
        rows = []
        for raw_row in reader:
            row = {}
            for original, cleaned in zip(reader.fieldnames, headers):
                row[cleaned] = (raw_row.get(original) or "").strip()
            if any(value for value in row.values()):
                rows.append(row)

    if not rows:
        raise ValueError(f"{csv_path} does not contain data rows.")

    return headers, rows


def resolve_columns(
    headers: list[str], x_col: str | None, value_col: str | None, reference_col: str | None
) -> tuple[str, str, str]:
    if len(headers) < 3:
        raise ValueError("The CSV must contain at least three columns.")

    selected_x = x_col or headers[0]
    selected_value = value_col or headers[1]
    selected_reference = reference_col or headers[2]

    for column in (selected_x, selected_value, selected_reference):
        if column not in headers:
            raise ValueError(f"Column not found: {column}")

    return selected_x, selected_value, selected_reference


def compute_results(
    rows: list[dict[str, str]], x_col: str, value_col: str, reference_col: str
) -> list[dict[str, float | str]]:
    results = []
    for row in rows:
        x_raw = row[x_col]
        value_raw = row[value_col]
        reference_raw = row[reference_col]

        x_value = float(x_raw)
        value = float(value_raw)
        reference = float(reference_raw)

        if reference == 0:
            relative_error = float("inf")
        else:
            relative_error = abs(value - reference) / abs(reference)

        results.append(
            {
                "x": x_value,
                "x_raw": x_raw,
                "value": value,
                "reference": reference,
                "relative_error": relative_error,
            }
        )

    return results


def write_results_csv(
    output_path: Path, results: list[dict[str, float | str]], x_col: str, value_col: str, reference_col: str
) -> None:
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow([x_col, value_col, reference_col, "relative_error", "relative_error_percent"])
        for result in results:
            error = result["relative_error"]
            writer.writerow(
                [
                    result["x_raw"],
                    f"{result['value']:.10g}",
                    f"{result['reference']:.10g}",
                    f"{error:.10g}",
                    f"{error * 100:.6f}",
                ]
            )


def write_html_table(
    output_path: Path, results: list[dict[str, float | str]], x_col: str, value_col: str, reference_col: str
) -> None:
    rows = []
    for result in results:
        rows.append(
            "<tr>"
            f"<td>{html.escape(str(result['x_raw']))}</td>"
            f"<td>{result['value']:.6f}</td>"
            f"<td>{result['reference']:.6f}</td>"
            f"<td>{result['relative_error']:.6f}</td>"
            f"<td>{result['relative_error'] * 100:.3f}%</td>"
            "</tr>"
        )

    table_html = "\n".join(
        [
            "<table>",
            "  <thead>",
            "    <tr>",
            f"      <th>{html.escape(x_col)}</th>",
            f"      <th>{html.escape(value_col)}</th>",
            f"      <th>{html.escape(reference_col)}</th>",
            "      <th>relative_error</th>",
            "      <th>relative_error_percent</th>",
            "    </tr>",
            "  </thead>",
            "  <tbody>",
            *[f"    {row}" for row in rows],
            "  </tbody>",
            "</table>",
            "",
        ]
    )
    output_path.write_text(table_html, encoding="utf-8")


def write_markdown(
    output_path: Path,
    image_name: str,
    html_table_name: str,
    results: list[dict[str, float | str]],
    x_col: str,
    value_col: str,
    reference_col: str,
) -> None:
    avg_error = sum(result["relative_error"] for result in results) / len(results)
    max_result = max(results, key=lambda item: item["relative_error"])

    lines = [
        "# Relative Error Report",
        "",
        f"- X column: `{x_col}`",
        f"- Value column: `{value_col}`",
        f"- Reference column: `{reference_col}`",
        f"- Mean relative error: `{avg_error:.6f}`",
        f"- Max relative error: `{max_result['relative_error']:.6f}` at `{x_col} = {max_result['x_raw']}`",
        "",
        "## Plot",
        "",
        f"![Relative error plot]({image_name})",
        "",
        "## HTML Table",
        "",
        f"- Table file: `{html_table_name}`",
        "",
    ]
    output_path.write_text("\n".join(lines), encoding="utf-8")


def generate_plot(
    output_path: Path, results: list[dict[str, float | str]], x_col: str, value_col: str, reference_col: str
) -> None:
    import matplotlib.pyplot as plt

    x_values = [result["x"] for result in results]
    values = [result["value"] for result in results]
    references = [result["reference"] for result in results]
    relative_error_percent = [result["relative_error"] * 100 for result in results]

    fig, axes = plt.subplots(2, 1, figsize=(8, 8), constrained_layout=True)

    axes[0].plot(x_values, values, marker="o", label=value_col)
    axes[0].plot(x_values, references, marker="s", label=reference_col)
    axes[0].set_title("Value vs Reference")
    axes[0].set_xlabel(x_col)
    axes[0].set_ylabel("Value")
    axes[0].grid(True, alpha=0.3)
    axes[0].legend()

    axes[1].bar(x_values, relative_error_percent, width=0.04 if len(x_values) > 1 else 0.2)
    axes[1].set_title("Relative Error")
    axes[1].set_xlabel(x_col)
    axes[1].set_ylabel("Error (%)")
    axes[1].grid(True, axis="y", alpha=0.3)

    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def main() -> int:
    args = parse_args()
    csv_path = Path(args.csv_file)
    if not csv_path.is_file():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    headers, rows = read_csv(csv_path)
    x_col, value_col, reference_col = resolve_columns(
        headers, args.x_col, args.value_col, args.reference_col
    )
    results = compute_results(rows, x_col, value_col, reference_col)

    output_dir = Path(args.output_dir) if args.output_dir else csv_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    prefix = args.prefix or csv_path.stem

    plot_path = output_dir / f"{prefix}_relative_error.png"
    markdown_path = output_dir / f"{prefix}_relative_error.md"
    html_path = output_dir / f"{prefix}_relative_error_table.html"
    results_csv_path = output_dir / f"{prefix}_relative_error.csv"

    generate_plot(plot_path, results, x_col, value_col, reference_col)
    write_results_csv(results_csv_path, results, x_col, value_col, reference_col)
    write_html_table(html_path, results, x_col, value_col, reference_col)
    write_markdown(
        markdown_path,
        plot_path.name,
        html_path.name,
        results,
        x_col,
        value_col,
        reference_col,
    )

    print(f"Generated: {plot_path}")
    print(f"Generated: {markdown_path}")
    print(f"Generated: {html_path}")
    print(f"Generated: {results_csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
