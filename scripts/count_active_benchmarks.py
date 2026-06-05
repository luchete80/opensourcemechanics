#!/usr/bin/env python3

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BENCHMARKS_FILE = ROOT / "benchmarks.html"


def count_active_benchmarks(content: str) -> int:
    pattern = r'<h3><a href="benchmark_[^"]+">'
    return len(re.findall(pattern, content))


def main() -> None:
    content = BENCHMARKS_FILE.read_text(encoding="utf-8")
    count = count_active_benchmarks(content)
    print(count)


if __name__ == "__main__":
    main()
