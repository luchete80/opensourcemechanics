#!/usr/bin/env python3

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INDEX_FILE = ROOT / "index.html"
PUBLICATIONS_FILE = ROOT / "publications.html"
BENCHMARKS_FILE = ROOT / "benchmarks.html"

AUTO_METRICS = {
    "metric-publications": {
        "label": "Publications",
        "path": PUBLICATIONS_FILE,
        "pattern": r'class="publication-item"',
    },
    "metric-benchmark-cases": {
        "label": "Benchmark Cases",
        "path": BENCHMARKS_FILE,
        "pattern": r'<article class="benchmark-card">',
    },
}

MANUAL_METRICS = {
    "metric-fem-solvers": "2",
    "metric-github-followers": "40+",
    "metric-years": "15+",
    "metric-youtube-subscribers": "1300+",
}


def count_matches(path: Path, pattern: str) -> int:
    content = path.read_text(encoding="utf-8")
    return len(re.findall(pattern, content))


def build_metrics() -> dict[str, str]:
    metrics: dict[str, str] = {}

    for metric_id, config in AUTO_METRICS.items():
        metrics[metric_id] = str(count_matches(config["path"], config["pattern"]))

    metrics.update(MANUAL_METRICS)
    return metrics


def replace_metric_value(content: str, metric_id: str, value: str) -> str:
    pattern = rf'(<span class="metric-value" id="{re.escape(metric_id)}">)(.*?)(</span>)'
    updated, replacements = re.subn(pattern, rf"\g<1>{value}\g<3>", content, count=1)
    if replacements != 1:
        raise RuntimeError(f"Metric id '{metric_id}' was not found exactly once in index.html")
    return updated


def write_index(metrics: dict[str, str]) -> None:
    content = INDEX_FILE.read_text(encoding="utf-8")
    for metric_id, value in metrics.items():
        content = replace_metric_value(content, metric_id, value)
    INDEX_FILE.write_text(content, encoding="utf-8")


def print_summary(metrics: dict[str, str]) -> None:
    print("Auto metrics")
    for metric_id, config in AUTO_METRICS.items():
        print(f"- {config['label']}: {metrics[metric_id]}")

    print("Manual metrics")
    for metric_id, value in MANUAL_METRICS.items():
        label = metric_id.replace("metric-", "").replace("-", " ")
        print(f"- {label.title()}: {value}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Refresh the metrics block in index.html."
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write the current metric values back into index.html.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    metrics = build_metrics()
    print_summary(metrics)

    if args.write:
        write_index(metrics)
        print(f"Updated {INDEX_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
