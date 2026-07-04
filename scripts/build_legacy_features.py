#!/usr/bin/env python
"""Derive analysis features from the 2013-2014 legacy entrance-exam file.

The source file contains names and date-of-birth values. This script writes
feature and aggregate tables for analysis without duplicating the full raw name
or exact date-of-birth in the main row-level output.
"""

from __future__ import annotations

import argparse
import re
import unicodedata
from collections import defaultdict
from pathlib import Path

import pandas as pd


SCORE_COLUMNS = ["Mon1", "Mon2", "Mon3", "TongDiem"]

TCVN3_TABLE = "µ¸¶·¹¨»¾¼½Æ©ÇÊÈÉË®ÌÐÎÏÑªÒÕÓÔÖ×ÝØÜÞßãáâä«åèæçé¬êíëìîïóñòô\u00adõøö÷ùúýûüþ¡¢§£¤¥¦"
UNICODE_TABLE = "àáảãạăằắẳẵặâầấẩẫậđèéẻẽẹêềếểễệìíỉĩịòóỏõọôồốổỗộơờớởỡợùúủũụưừứửữựỳýỷỹỵĂÂĐÊÔƠƯ"
TCVN3_TO_UNICODE = str.maketrans(dict(zip(TCVN3_TABLE, UNICODE_TABLE)))
TCVN3_STRONG_MARKERS = set(
    "µ¸¶·¹¨»¾¼½Æ©ÇÈÉË®ÌÐÎÏÑªÒÕÓÖ×ØÜÞßä«åæ¬ëîïñ\u00adøö÷ûüþ¡¢§£¤¥¦"
)
INTERNAL_UPPERCASE_RE = re.compile(r"[a-zà-ỹ][A-ZÀÁẢÃẠĂẰẮẲẴẶÂẦẤẨẪẬĐÈÉẺẼẸÊỀẾỂỄỆÌÍỈĨỊÒÓỎÕỌÔỒỐỔỖỘƠỜỚỞỠỢÙÚỦŨỤƯỪỨỬỮỰỲÝỶỸỴÇÐÑÞÆ]")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw-file",
        type=Path,
        default=Path("sources") / "du-lieu-diem-thi" / "du-lieu-diem-thi-2013-2014.csv",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("data") / "analysis",
    )
    parser.add_argument("--chunksize", type=int, default=200_000)
    parser.add_argument(
        "--min-group-size",
        type=int,
        default=30,
        help="Minimum records for name aggregate rows.",
    )
    return parser.parse_args()


def clean_name(value: object) -> str:
    if pd.isna(value):
        return ""
    text = unicodedata.normalize("NFC", str(value))
    return re.sub(r"\s+", " ", text).strip()


def tcvn3_to_unicode(value: object) -> str:
    return clean_name(value).translate(TCVN3_TO_UNICODE)


def looks_like_tcvn3(value: str) -> bool:
    return any(char in TCVN3_STRONG_MARKERS for char in value)


def looks_like_tcvn3_token(value: str) -> bool:
    if looks_like_tcvn3(value):
        return True
    return bool(INTERNAL_UPPERCASE_RE.search(value))


def fix_name_token(value: str) -> str:
    return tcvn3_to_unicode(value) if looks_like_tcvn3_token(value) else value


def split_name(value: object) -> tuple[str, str, int]:
    name = clean_name(value)
    if not name:
        return "", "", 0
    parts = name.split(" ")
    family_name = parts[0]
    given_name = parts[-1]
    middle_count = max(len(parts) - 2, 0)
    return family_name, given_name, middle_count


def parse_birth(value: object) -> tuple[int | None, int | None, int | None, bool]:
    if pd.isna(value):
        return None, None, None, False
    raw = re.sub(r"\D", "", str(value))
    if not raw or raw == "000000":
        return None, None, None, False
    raw = raw.zfill(6)[-6:]
    day = int(raw[:2])
    month = int(raw[2:4])
    year_yy = int(raw[4:6])
    valid = 1 <= day <= 31 and 1 <= month <= 12
    return day if valid else None, month if valid else None, year_yy if valid else None, valid


def add_to_aggregate(bucket: dict[tuple[str, int, str, str], list[float]], chunk: pd.DataFrame) -> None:
    for _, row in chunk.iterrows():
        total = row["score_total"]
        if pd.isna(total):
            continue
        for kind, value in (
            ("family_name", row["family_name"]),
            ("given_name", row["given_name"]),
        ):
            if value:
                bucket[(kind, int(row["year"]), str(row["exam_type"]), value)].append(float(total))


def build_aggregate_rows(
    bucket: dict[tuple[str, int, str, str], list[float]],
    min_group_size: int,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for (kind, year, exam_type, value), scores in sorted(bucket.items()):
        if len(scores) < min_group_size:
            continue
        series = pd.Series(scores, dtype="float64")
        rows.append(
            {
                "name_part_type": kind,
                "year": year,
                "exam_type": exam_type,
                "name_part": value,
                "count": int(series.count()),
                "mean_total_score": round(float(series.mean()), 4),
                "median_total_score": round(float(series.median()), 4),
                "p25_total_score": round(float(series.quantile(0.25)), 4),
                "p75_total_score": round(float(series.quantile(0.75)), 4),
                "max_total_score": round(float(series.max()), 4),
            }
        )
    return rows


def main() -> None:
    args = parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    features_path = args.out_dir / "legacy_2013_2014_features.csv"
    name_stats_path = args.out_dir / "legacy_name_score_stats.csv"
    birth_stats_path = args.out_dir / "legacy_birth_month_score_stats.csv"

    if features_path.exists():
        features_path.unlink()

    aggregate_bucket: dict[tuple[str, int, str, str], list[float]] = defaultdict(list)
    feature_rows_written = 0
    first_write = True

    dtype = {
        "Nam": "string",
        "Tinh": "string",
        "KyThi": "string",
        "DH": "string",
        "Khoi": "string",
        "SBD": "string",
        "HovaTen": "string",
        "NgaySinh": "string",
    }

    for chunk in pd.read_csv(args.raw_file, dtype=dtype, chunksize=args.chunksize):
        chunk = chunk.copy()
        chunk["year"] = pd.to_numeric(chunk["Nam"], errors="coerce").astype("Int64") + 2000
        chunk["province_code"] = chunk["Tinh"].fillna("").str.zfill(2).replace({"00": ""})
        chunk["exam_type"] = chunk["KyThi"].fillna("")
        chunk["school_code"] = chunk["DH"].fillna("")
        chunk["block_code"] = chunk["Khoi"].fillna("")
        chunk["candidate_number"] = chunk["SBD"].fillna("").str.zfill(6)

        name_source = chunk["HovaTen"].map(clean_name)
        name_needs_fix = name_source.map(looks_like_tcvn3)
        name_source.loc[name_needs_fix] = name_source.loc[name_needs_fix].map(tcvn3_to_unicode)

        name_parts = name_source.map(split_name)
        chunk["family_name"] = [item[0] for item in name_parts]
        chunk["given_name"] = [item[1] for item in name_parts]
        chunk["middle_name_token_count"] = [item[2] for item in name_parts]
        family_needs_fix = chunk["family_name"].map(looks_like_tcvn3_token)
        given_needs_fix = chunk["given_name"].map(looks_like_tcvn3_token)
        chunk.loc[family_needs_fix, "family_name"] = chunk.loc[family_needs_fix, "family_name"].map(fix_name_token)
        chunk.loc[given_needs_fix, "given_name"] = chunk.loc[given_needs_fix, "given_name"].map(fix_name_token)
        chunk["name_font_fixed"] = name_needs_fix | family_needs_fix | given_needs_fix

        birth_parts = chunk["NgaySinh"].map(parse_birth)
        chunk["birth_day"] = [item[0] for item in birth_parts]
        chunk["birth_month"] = [item[1] for item in birth_parts]
        chunk["birth_year_yy"] = [item[2] for item in birth_parts]
        chunk["birth_date_valid"] = [item[3] for item in birth_parts]

        for column in SCORE_COLUMNS:
            chunk[f"score_{column}"] = pd.to_numeric(chunk[column], errors="coerce") / 100.0
        chunk = chunk.rename(
            columns={
                "score_Mon1": "score_mon1",
                "score_Mon2": "score_mon2",
                "score_Mon3": "score_mon3",
                "score_TongDiem": "score_total",
            }
        )

        out_cols = [
            "year",
            "province_code",
            "exam_type",
            "school_code",
            "block_code",
            "candidate_number",
            "name_font_fixed",
            "family_name",
            "given_name",
            "middle_name_token_count",
            "birth_day",
            "birth_month",
            "birth_year_yy",
            "birth_date_valid",
            "score_mon1",
            "score_mon2",
            "score_mon3",
            "score_total",
        ]
        feature_chunk = chunk[out_cols]
        feature_chunk.to_csv(features_path, mode="a", header=first_write, index=False)
        first_write = False
        feature_rows_written += len(feature_chunk)

        add_to_aggregate(aggregate_bucket, chunk)

    name_stats = pd.DataFrame(build_aggregate_rows(aggregate_bucket, args.min_group_size))
    name_stats.to_csv(name_stats_path, index=False)

    features = pd.read_csv(
        features_path,
        usecols=["year", "exam_type", "birth_month", "score_total", "birth_date_valid"],
    )
    birth_stats = (
        features[features["birth_date_valid"] == True]
        .groupby(["year", "exam_type", "birth_month"])["score_total"]
        .agg(["count", "mean", "median", "min", "max"])
        .reset_index()
        .rename(columns={"mean": "mean_total_score", "median": "median_total_score"})
    )
    birth_stats["mean_total_score"] = birth_stats["mean_total_score"].round(4)
    birth_stats["median_total_score"] = birth_stats["median_total_score"].round(4)
    birth_stats.to_csv(birth_stats_path, index=False)

    print(f"Wrote {features_path} ({feature_rows_written} rows)")
    print(f"Wrote {name_stats_path} ({len(name_stats)} rows)")
    print(f"Wrote {birth_stats_path} ({len(birth_stats)} rows)")


if __name__ == "__main__":
    main()
