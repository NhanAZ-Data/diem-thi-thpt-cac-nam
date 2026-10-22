#!/usr/bin/env python
"""Validate key generated files and row-count assumptions."""

from __future__ import annotations

import csv
from pathlib import Path


EXPECTED_THPT_ROWS = 10_865_001
EXPECTED_LEGACY_ROWS = 2_412_155


def count_data_rows(path: Path) -> int:
    with path.open("rb") as handle:
        return max(sum(1 for _ in handle) - 1, 0)


def assert_exists(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(path)


def validate_summary() -> None:
    path = Path("data/summary/processed_file_inventory.csv")
    assert_exists(path)
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    total = sum(int(row["rows"]) for row in rows)
    if total != EXPECTED_THPT_ROWS:
        raise AssertionError(f"THPT row count mismatch: {total} != {EXPECTED_THPT_ROWS}")
    if len(rows) != 15:
        raise AssertionError(f"Expected 15 canonical THPT files, got {len(rows)}")
    print(f"OK summary inventory: {len(rows)} files, {total:,} rows")


def validate_legacy() -> None:
    feature_path = Path("data/analysis/legacy_2013_2014_features.csv")
    assert_exists(feature_path)
    rows = count_data_rows(feature_path)
    if rows != EXPECTED_LEGACY_ROWS:
        raise AssertionError(f"Legacy feature row count mismatch: {rows} != {EXPECTED_LEGACY_ROWS}")

    name_stats = Path("data/analysis/legacy_name_score_stats.csv")
    birth_stats = Path("data/analysis/legacy_birth_month_score_stats.csv")
    assert_exists(name_stats)
    assert_exists(birth_stats)
    text = name_stats.read_text(encoding="utf-8")
    bad_tokens = ["NguyÔn", "TrÇn", "Lª", "Ph¹m", "Hoµng", "§"]
    leftovers = [token for token in bad_tokens if token in text]
    if leftovers:
        raise AssertionError(f"Legacy name stats still contain likely TCVN3 tokens: {leftovers}")
    print(f"OK legacy features: {rows:,} rows")


def validate_crosscheck_2026() -> None:
    path = Path("metadata/crosscheck_2026_anhdung98.csv")
    assert_exists(path)
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    metrics = {row["metric"]: int(row["value"]) for row in rows}
    if metrics.get("left_rows") != 1_208_863 or metrics.get("right_rows") != 1_208_863:
        raise AssertionError("2026 crosscheck row counts are not as expected")
    nonzero_mismatches = {
        key: value
        for key, value in metrics.items()
        if key.startswith("mismatched_") and value != 0
    }
    if metrics.get("left_only_sbd") != 0 or metrics.get("right_only_sbd") != 0:
        raise AssertionError("2026 crosscheck has SBD set differences")
    if nonzero_mismatches:
        raise AssertionError(f"2026 crosscheck mismatches: {nonzero_mismatches}")
    print("OK 2026 crosscheck: SBD and mapped score fields match")


def main() -> None:
    validate_summary()
    validate_legacy()
    validate_crosscheck_2026()
    print("All validation checks passed.")


if __name__ == "__main__":
    main()
