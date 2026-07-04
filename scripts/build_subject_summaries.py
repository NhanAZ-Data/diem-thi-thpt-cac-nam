#!/usr/bin/env python
"""Build compact analysis tables from the canonical THPT score CSV files.

The raw source files stay untouched in sources/du-lieu-diem-thi. This script
streams them in chunks and writes exact score distributions plus per-subject
statistics, avoiding the aggregate 2016-2025 file so counts are not duplicated.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
from collections import Counter
from pathlib import Path

import pandas as pd


SUBJECT_COLUMNS = [
    "Toan",
    "NguVan",
    "VatLy",
    "HoaHoc",
    "SinhHoc",
    "LichSu",
    "DiaLy",
    "GDCD",
    "KinhTePhapLuat",
    "TinHoc",
    "CongNgheCongNghiep",
    "CongNgheNongNghiep",
    "NgoaiNgu",
]

CANONICAL_FILES = [
    ("du-lieu-diem-thi-2016-dh.csv", "university_cluster"),
    ("du-lieu-diem-thi-2016-dp.csv", "local_cluster"),
    ("du_lieu_diem_thi_2017.csv", "main"),
    ("du_lieu_diem_thi_2018.csv", "main"),
    ("du_lieu_diem_thi_2019.csv", "main"),
    ("du_lieu_diem_thi_2020.csv", "main"),
    ("du_lieu_diem_thi_2020_dot_2_da_nang.csv", "round_2_da_nang"),
    ("du_lieu_diem_thi_2021.csv", "main"),
    ("du_lieu_diem_thi_2021_dot_2.csv", "round_2"),
    ("du_lieu_diem_thi_2022.csv", "main"),
    ("du_lieu_diem_thi_2023.csv", "main"),
    ("du_lieu_diem_thi_2024.csv", "main"),
    ("du-lieu-diem-thi-2025-ct2006.csv", "gdpt_2006"),
    ("du-lieu-diem-thi-2025-ct2018.csv", "gdpt_2018"),
    ("du_lieu_diem_thi_2026.csv", "main"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw-dir",
        type=Path,
        default=Path("sources") / "du-lieu-diem-thi",
        help="Directory containing raw CSV files cloned from the source repo.",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data") / "summary",
        help="Directory where summary CSV files will be written.",
    )
    parser.add_argument(
        "--chunksize",
        type=int,
        default=200_000,
        help="Rows per pandas chunk.",
    )
    return parser.parse_args()


def detect_subjects(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        header = next(csv.reader(handle))
    return [column for column in SUBJECT_COLUMNS if column in header]


def detect_year(path: Path) -> int:
    sample = pd.read_csv(path, usecols=["Nam"], nrows=1)
    raw_value = str(sample["Nam"].iloc[0])
    match = re.search(r"\d{2,4}", raw_value)
    if not match:
        raise ValueError(f"Cannot detect year from Nam={raw_value!r} in {path}")
    value = int(match.group(0))
    return 2000 + value if value < 100 else value


def weighted_quantile(sorted_counts: list[tuple[float, int]], q: float) -> float:
    if not sorted_counts:
        return math.nan
    total = sum(count for _, count in sorted_counts)
    threshold = q * (total - 1) + 1
    running = 0
    for score, count in sorted_counts:
        running += count
        if running >= threshold:
            return score
    return sorted_counts[-1][0]


def build_stats(distribution: Counter[tuple[int, str, float]]) -> list[dict[str, object]]:
    grouped: dict[tuple[int, str], list[tuple[float, int]]] = {}
    for (year, subject, score), count in distribution.items():
        grouped.setdefault((year, subject), []).append((score, count))

    rows: list[dict[str, object]] = []
    for (year, subject), score_counts in sorted(grouped.items()):
        score_counts.sort()
        count = sum(item_count for _, item_count in score_counts)
        total = sum(score * item_count for score, item_count in score_counts)
        mean = total / count
        sumsq = sum((score * score) * item_count for score, item_count in score_counts)
        variance = max((sumsq / count) - (mean * mean), 0.0)
        rows.append(
            {
                "year": year,
                "subject": subject,
                "count": count,
                "mean": round(mean, 4),
                "std": round(math.sqrt(variance), 4),
                "min": score_counts[0][0],
                "p05": weighted_quantile(score_counts, 0.05),
                "p25": weighted_quantile(score_counts, 0.25),
                "median": weighted_quantile(score_counts, 0.50),
                "p75": weighted_quantile(score_counts, 0.75),
                "p95": weighted_quantile(score_counts, 0.95),
                "max": score_counts[-1][0],
            }
        )
    return rows


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    distribution: Counter[tuple[int, str, float]] = Counter()
    segment_distribution: Counter[tuple[int, str, str, float]] = Counter()
    file_rows: list[dict[str, object]] = []

    for filename, segment in CANONICAL_FILES:
        path = args.raw_dir / filename
        if not path.exists():
            raise FileNotFoundError(path)

        year = detect_year(path)
        subjects = detect_subjects(path)
        usecols = ["Nam", *subjects]
        row_count = 0
        print(f"Processing {filename} ({year}, {segment})...")

        for chunk in pd.read_csv(path, usecols=usecols, chunksize=args.chunksize):
            row_count += len(chunk)
            for subject in subjects:
                values = pd.to_numeric(chunk[subject], errors="coerce").dropna()
                if values.empty:
                    continue
                counts = values.value_counts()
                for score, count in counts.items():
                    score_value = float(score)
                    count_value = int(count)
                    distribution[(year, subject, score_value)] += count_value
                    segment_distribution[(year, segment, subject, score_value)] += count_value

        file_rows.append(
            {
                "file": str(path),
                "year": year,
                "segment": segment,
                "rows": row_count,
                "subjects": "|".join(subjects),
            }
        )

    file_inventory_path = args.out_dir / "processed_file_inventory.csv"
    pd.DataFrame(file_rows).to_csv(file_inventory_path, index=False)

    distribution_rows = [
        {"year": year, "subject": subject, "score": score, "count": count}
        for (year, subject, score), count in sorted(distribution.items())
    ]
    distribution_path = args.out_dir / "subject_score_distribution.csv"
    pd.DataFrame(distribution_rows).to_csv(distribution_path, index=False)

    segment_rows = [
        {
            "year": year,
            "segment": segment,
            "subject": subject,
            "score": score,
            "count": count,
        }
        for (year, segment, subject, score), count in sorted(segment_distribution.items())
    ]
    segment_path = args.out_dir / "subject_score_distribution_by_segment.csv"
    pd.DataFrame(segment_rows).to_csv(segment_path, index=False)

    stats_path = args.out_dir / "year_subject_stats.csv"
    pd.DataFrame(build_stats(distribution)).to_csv(stats_path, index=False)

    print(f"Wrote {file_inventory_path}")
    print(f"Wrote {distribution_path}")
    print(f"Wrote {segment_path}")
    print(f"Wrote {stats_path}")


if __name__ == "__main__":
    main()
