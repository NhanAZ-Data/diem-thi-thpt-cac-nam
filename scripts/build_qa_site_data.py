#!/usr/bin/env python
"""Build the 101-question analysis report and static-site data.

The report intentionally separates what the local dataset can prove from what
it cannot prove. Name and birth-month sections use only the legacy 2013-2014
entrance dataset because the THPT 2016-2026 bulk files do not expose those
fields.
"""

from __future__ import annotations

import csv
import json
import math
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "sources" / "du-lieu-diem-thi"
SUMMARY_DIR = ROOT / "data" / "summary"
ANALYSIS_DIR = ROOT / "data" / "analysis"
DOCS_DIR = ROOT / "docs"
SITE_DIR = ROOT / "site"

SUBJECTS = [
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

SUBJECT_LABELS = {
    "Toan": "Toán",
    "NguVan": "Ngữ văn",
    "VatLy": "Vật lí",
    "HoaHoc": "Hóa học",
    "SinhHoc": "Sinh học",
    "LichSu": "Lịch sử",
    "DiaLy": "Địa lí",
    "GDCD": "GDCD",
    "KinhTePhapLuat": "Kinh tế và pháp luật",
    "TinHoc": "Tin học",
    "CongNgheCongNghiep": "Công nghệ công nghiệp",
    "CongNgheNongNghiep": "Công nghệ nông nghiệp",
    "NgoaiNgu": "Ngoại ngữ",
}

COMBOS = [
    "KhoiA",
    "KhoiA1",
    "KhoiB",
    "KhoiC",
    "KhoiD",
    "KhoiA02",
    "KhoiC01",
    "KhoiD07",
]

COMBO_LABELS = {
    "KhoiA": "A00",
    "KhoiA1": "A01",
    "KhoiB": "B00",
    "KhoiC": "C00",
    "KhoiD": "D01/D00",
    "KhoiA02": "A02",
    "KhoiC01": "C01",
    "KhoiD07": "D07",
}

SUSPICIOUS_GIVEN_NAMES = {
    # Legacy 2014 has font/noise artifacts. This token behaves like a broken
    # name in sampled rows and should not be promoted in playful name rankings.
    "Tó",
}

CANONICAL_FILES = [
    ("du-lieu-diem-thi-2016-dh.csv", 2016, "university_cluster"),
    ("du-lieu-diem-thi-2016-dp.csv", 2016, "local_cluster"),
    ("du_lieu_diem_thi_2017.csv", 2017, "main"),
    ("du_lieu_diem_thi_2018.csv", 2018, "main"),
    ("du_lieu_diem_thi_2019.csv", 2019, "main"),
    ("du_lieu_diem_thi_2020.csv", 2020, "main"),
    ("du_lieu_diem_thi_2020_dot_2_da_nang.csv", 2020, "round_2_da_nang"),
    ("du_lieu_diem_thi_2021.csv", 2021, "main"),
    ("du_lieu_diem_thi_2021_dot_2.csv", 2021, "round_2"),
    ("du_lieu_diem_thi_2022.csv", 2022, "main"),
    ("du_lieu_diem_thi_2023.csv", 2023, "main"),
    ("du_lieu_diem_thi_2024.csv", 2024, "main"),
    ("du-lieu-diem-thi-2025-ct2006.csv", 2025, "gdpt_2006"),
    ("du-lieu-diem-thi-2025-ct2018.csv", 2025, "gdpt_2018"),
    ("du_lieu_diem_thi_2026.csv", 2026, "main"),
]

OLD_PROVINCES = {
    "1": "Hà Nội",
    "2": "TP. Hồ Chí Minh",
    "3": "Hải Phòng",
    "4": "Đà Nẵng",
    "5": "Hà Giang",
    "6": "Cao Bằng",
    "7": "Lai Châu",
    "8": "Lào Cai",
    "9": "Tuyên Quang",
    "10": "Lạng Sơn",
    "11": "Bắc Kạn",
    "12": "Thái Nguyên",
    "13": "Yên Bái",
    "14": "Sơn La",
    "15": "Phú Thọ",
    "16": "Vĩnh Phúc",
    "17": "Quảng Ninh",
    "18": "Bắc Giang",
    "19": "Bắc Ninh",
    "21": "Hải Dương",
    "22": "Hưng Yên",
    "23": "Hòa Bình",
    "24": "Hà Nam",
    "25": "Nam Định",
    "26": "Thái Bình",
    "27": "Ninh Bình",
    "28": "Thanh Hóa",
    "29": "Nghệ An",
    "30": "Hà Tĩnh",
    "31": "Quảng Bình",
    "32": "Quảng Trị",
    "33": "Thừa Thiên Huế",
    "34": "Quảng Nam",
    "35": "Quảng Ngãi",
    "36": "Kon Tum",
    "37": "Bình Định",
    "38": "Gia Lai",
    "39": "Phú Yên",
    "40": "Đắk Lắk",
    "41": "Khánh Hòa",
    "42": "Lâm Đồng",
    "43": "Bình Phước",
    "44": "Bình Dương",
    "45": "Ninh Thuận",
    "46": "Tây Ninh",
    "47": "Bình Thuận",
    "48": "Đồng Nai",
    "49": "Long An",
    "50": "Đồng Tháp",
    "51": "An Giang",
    "52": "Bà Rịa - Vũng Tàu",
    "53": "Tiền Giang",
    "54": "Kiên Giang",
    "55": "Cần Thơ",
    "56": "Bến Tre",
    "57": "Vĩnh Long",
    "58": "Trà Vinh",
    "59": "Sóc Trăng",
    "60": "Bạc Liêu",
    "61": "Cà Mau",
    "62": "Điện Biên",
    "63": "Đắk Nông",
    "64": "Hậu Giang",
}

NEW_PROVINCES = {
    "01": "Hà Nội",
    "04": "Cao Bằng",
    "08": "Tuyên Quang",
    "11": "Điện Biên",
    "12": "Lai Châu",
    "14": "Sơn La",
    "15": "Lào Cai",
    "19": "Thái Nguyên",
    "20": "Lạng Sơn",
    "22": "Quảng Ninh",
    "24": "Bắc Ninh",
    "25": "Phú Thọ",
    "31": "Hải Phòng",
    "33": "Hưng Yên",
    "37": "Ninh Bình",
    "38": "Thanh Hóa",
    "40": "Nghệ An",
    "42": "Hà Tĩnh",
    "44": "Quảng Trị",
    "46": "Huế",
    "48": "Đà Nẵng",
    "51": "Quảng Ngãi",
    "52": "Gia Lai",
    "56": "Khánh Hòa",
    "66": "Đắk Lắk",
    "68": "Lâm Đồng",
    "75": "Đồng Nai",
    "79": "TP. Hồ Chí Minh",
    "80": "Tây Ninh",
    "82": "Đồng Tháp",
    "86": "Vĩnh Long",
    "91": "An Giang",
    "92": "Cần Thơ",
    "96": "Cà Mau",
}

NORTH = {
    "Hà Nội",
    "Hải Phòng",
    "Hà Giang",
    "Cao Bằng",
    "Lai Châu",
    "Lào Cai",
    "Tuyên Quang",
    "Lạng Sơn",
    "Bắc Kạn",
    "Thái Nguyên",
    "Yên Bái",
    "Sơn La",
    "Phú Thọ",
    "Vĩnh Phúc",
    "Quảng Ninh",
    "Bắc Giang",
    "Bắc Ninh",
    "Hải Dương",
    "Hưng Yên",
    "Hòa Bình",
    "Hà Nam",
    "Nam Định",
    "Thái Bình",
    "Ninh Bình",
    "Điện Biên",
}

CENTRAL = {
    "Thanh Hóa",
    "Nghệ An",
    "Hà Tĩnh",
    "Quảng Bình",
    "Quảng Trị",
    "Thừa Thiên Huế",
    "Huế",
    "Đà Nẵng",
    "Quảng Nam",
    "Quảng Ngãi",
    "Kon Tum",
    "Bình Định",
    "Gia Lai",
    "Phú Yên",
    "Đắk Lắk",
    "Khánh Hòa",
    "Lâm Đồng",
    "Ninh Thuận",
    "Bình Thuận",
    "Đắk Nông",
}


def fmt_num(value: float | int | None, digits: int = 2) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "không có"
    if isinstance(value, int):
        return f"{value:,}".replace(",", ".")
    return f"{value:,.{digits}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_score(value: float | None, digits: int = 2) -> str:
    if value is None or math.isnan(float(value)):
        return "không có"
    return fmt_num(float(value), digits)


def fmt_pct(value: float | None, digits: int = 2) -> str:
    if value is None or math.isnan(float(value)):
        return "không có"
    return f"{float(value) * 100:.{digits}f}%".replace(".", ",")


def clean_float(value: Any) -> float | None:
    try:
        if pd.isna(value):
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def weighted_quantile(score_counts: list[tuple[float, int]], q: float) -> float:
    if not score_counts:
        return math.nan
    total = sum(count for _, count in score_counts)
    threshold = q * (total - 1) + 1
    running = 0
    for score, count in sorted(score_counts):
        running += count
        if running >= threshold:
            return float(score)
    return float(score_counts[-1][0])


def pearson_from_sums(n: int, sx: float, sy: float, sx2: float, sy2: float, sxy: float) -> float:
    denom_x = n * sx2 - sx * sx
    denom_y = n * sy2 - sy * sy
    denom = math.sqrt(max(denom_x, 0.0) * max(denom_y, 0.0))
    if n < 2 or denom == 0:
        return math.nan
    return (n * sxy - sx * sy) / denom


def province_name(year: int, code: str) -> str:
    if year >= 2026:
        return NEW_PROVINCES.get(code.zfill(2), f"Mã {code}")
    return OLD_PROVINCES.get(str(int(code)) if code.isdigit() else code, f"Mã {code}")


def province_region(name: str) -> str:
    if name in NORTH:
        return "Miền Bắc"
    if name in CENTRAL:
        return "Miền Trung"
    return "Miền Nam"


def normalize_province_code(series: pd.Series, year: int) -> pd.Series:
    as_text = series.astype("string").fillna("").str.strip()
    as_text = as_text.str.replace(r"\.0$", "", regex=True)
    if year >= 2026:
        return as_text.str.zfill(2)
    return as_text.str.replace(r"^0+", "", regex=True).replace("", pd.NA)


def header_columns(path: Path) -> list[str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return next(csv.reader(handle))


def subject_label(subject: str) -> str:
    return SUBJECT_LABELS.get(subject, subject)


def combo_label(combo: str) -> str:
    return COMBO_LABELS.get(combo, combo)


def build_subject_metrics() -> tuple[pd.DataFrame, dict[tuple[int, str], dict[str, Any]]]:
    dist = pd.read_csv(SUMMARY_DIR / "subject_score_distribution.csv")
    stats = pd.read_csv(SUMMARY_DIR / "year_subject_stats.csv")
    rows: list[dict[str, Any]] = []
    metric_map: dict[tuple[int, str], dict[str, Any]] = {}

    for (year, subject), group in dist.groupby(["year", "subject"], sort=True):
        score_counts = [(float(score), int(count)) for score, count in group[["score", "count"]].itertuples(index=False, name=None)]
        count = sum(count for _, count in score_counts)
        score_sum = sum(score * count for score, count in score_counts)
        mean = score_sum / count
        sumsq = sum(score * score * count for score, count in score_counts)
        variance = max(sumsq / count - mean * mean, 0.0)
        std = math.sqrt(variance)
        if std > 0:
            third = sum(((score - mean) ** 3) * count for score, count in score_counts) / count
            fourth = sum(((score - mean) ** 4) * count for score, count in score_counts) / count
            skew = third / (std**3)
            excess_kurtosis = fourth / (std**4) - 3
        else:
            skew = math.nan
            excess_kurtosis = math.nan
        row = {
            "year": int(year),
            "subject": subject,
            "subject_label": subject_label(subject),
            "count": int(count),
            "mean": round(mean, 4),
            "std": round(std, 4),
            "p90": weighted_quantile(score_counts, 0.90),
            "p95": weighted_quantile(score_counts, 0.95),
            "share_ge_8": sum(c for s, c in score_counts if s >= 8) / count,
            "share_ge_9": sum(c for s, c in score_counts if s >= 9) / count,
            "share_ge_10": sum(c for s, c in score_counts if s == 10) / count,
            "count_10": int(sum(c for s, c in score_counts if s == 10)),
            "share_lt_5": sum(c for s, c in score_counts if s < 5) / count,
            "share_le_1": sum(c for s, c in score_counts if s <= 1) / count,
            "skew": round(skew, 4) if not math.isnan(skew) else None,
            "excess_kurtosis": round(excess_kurtosis, 4) if not math.isnan(excess_kurtosis) else None,
            "normality_distance": abs(skew) + abs(excess_kurtosis) if not math.isnan(skew) else None,
        }
        rows.append(row)
        metric_map[(int(year), subject)] = row

    out = pd.DataFrame(rows)
    merged = stats.merge(
        out[
            [
                "year",
                "subject",
                "p90",
                "share_ge_8",
                "share_ge_9",
                "share_ge_10",
                "count_10",
                "share_lt_5",
                "share_le_1",
                "skew",
                "excess_kurtosis",
                "normality_distance",
            ]
        ],
        on=["year", "subject"],
        how="left",
    )
    merged.insert(2, "subject_label", merged["subject"].map(subject_label))
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    merged.to_csv(ANALYSIS_DIR / "subject_year_metrics.csv", index=False)
    return merged, metric_map


def build_segment_metrics() -> pd.DataFrame:
    dist = pd.read_csv(SUMMARY_DIR / "subject_score_distribution_by_segment.csv")
    rows: list[dict[str, Any]] = []
    for (year, segment, subject), group in dist.groupby(["year", "segment", "subject"], sort=True):
        score_counts = [(float(score), int(count)) for score, count in group[["score", "count"]].itertuples(index=False, name=None)]
        count = sum(count for _, count in score_counts)
        if count == 0:
            continue
        mean = sum(score * count for score, count in score_counts) / count
        rows.append(
            {
                "year": int(year),
                "segment": segment,
                "subject": subject,
                "subject_label": subject_label(subject),
                "count": int(count),
                "mean": round(mean, 4),
                "share_ge_8": sum(c for s, c in score_counts if s >= 8) / count,
                "share_le_1": sum(c for s, c in score_counts if s <= 1) / count,
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(ANALYSIS_DIR / "segment_subject_metrics.csv", index=False)
    return out


def build_province_metrics(chunksize: int = 160_000) -> pd.DataFrame:
    acc: dict[tuple[int, str, str], dict[str, float]] = defaultdict(
        lambda: {"count": 0, "sum": 0.0, "sumsq": 0.0, "count_10": 0, "count_ge_8": 0, "count_lt_5": 0}
    )

    for filename, year, _segment in CANONICAL_FILES:
        if year == 2016:
            continue
        path = RAW_DIR / filename
        columns = header_columns(path)
        subjects = [subject for subject in SUBJECTS if subject in columns]
        usecols = ["Tinh", *subjects]
        for chunk in pd.read_csv(path, usecols=usecols, dtype={"Tinh": "string"}, chunksize=chunksize):
            chunk["province_code"] = normalize_province_code(chunk["Tinh"], year)
            chunk = chunk.dropna(subset=["province_code"])
            for subject in subjects:
                values = pd.to_numeric(chunk[subject], errors="coerce")
                valid = values.notna()
                if not valid.any():
                    continue
                frame = pd.DataFrame({"province_code": chunk.loc[valid, "province_code"], "score": values.loc[valid]})
                grouped = frame.groupby("province_code")["score"]
                for code, scores in grouped:
                    key = (year, str(code), subject)
                    data = acc[key]
                    count = int(scores.count())
                    data["count"] += count
                    data["sum"] += float(scores.sum())
                    data["sumsq"] += float((scores * scores).sum())
                    data["count_10"] += int((scores == 10).sum())
                    data["count_ge_8"] += int((scores >= 8).sum())
                    data["count_lt_5"] += int((scores < 5).sum())

    rows: list[dict[str, Any]] = []
    for (year, code, subject), data in sorted(acc.items()):
        count = int(data["count"])
        if count == 0:
            continue
        mean = data["sum"] / count
        variance = max(data["sumsq"] / count - mean * mean, 0.0)
        name = province_name(year, code)
        rows.append(
            {
                "year": year,
                "province_code": code,
                "province_name": name,
                "region": province_region(name),
                "subject": subject,
                "subject_label": subject_label(subject),
                "count": count,
                "mean": round(mean, 4),
                "std": round(math.sqrt(variance), 4),
                "share_ge_8": data["count_ge_8"] / count,
                "share_ge_10": data["count_10"] / count,
                "share_lt_5": data["count_lt_5"] / count,
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(ANALYSIS_DIR / "province_subject_metrics.csv", index=False)
    return out


def build_combo_metrics(chunksize: int = 180_000) -> pd.DataFrame:
    dist: Counter[tuple[int, str, float]] = Counter()
    for filename, year, _segment in CANONICAL_FILES:
        path = RAW_DIR / filename
        columns = header_columns(path)
        combos = [combo for combo in COMBOS if combo in columns]
        if not combos:
            continue
        for chunk in pd.read_csv(path, usecols=combos, chunksize=chunksize):
            for combo in combos:
                values = pd.to_numeric(chunk[combo], errors="coerce").dropna()
                values = values[values > 0]
                if values.empty:
                    continue
                counts = values.round(2).value_counts()
                for score, count in counts.items():
                    dist[(year, combo, float(score))] += int(count)

    rows: list[dict[str, Any]] = []
    grouped: dict[tuple[int, str], list[tuple[float, int]]] = defaultdict(list)
    for (year, combo, score), count in dist.items():
        grouped[(year, combo)].append((score, count))
    for (year, combo), score_counts in sorted(grouped.items()):
        total = sum(count for _, count in score_counts)
        mean = sum(score * count for score, count in score_counts) / total
        rows.append(
            {
                "year": year,
                "combo": combo,
                "combo_label": combo_label(combo),
                "count": int(total),
                "mean": round(mean, 4),
                "p90": weighted_quantile(score_counts, 0.90),
                "p95": weighted_quantile(score_counts, 0.95),
                "share_ge_24": sum(c for s, c in score_counts if s >= 24) / total,
                "share_ge_27": sum(c for s, c in score_counts if s >= 27) / total,
                "share_ge_29": sum(c for s, c in score_counts if s >= 29) / total,
            }
        )
    out = pd.DataFrame(rows)
    out.to_csv(ANALYSIS_DIR / "combo_year_metrics.csv", index=False)
    return out


def build_correlations_2026(chunksize: int = 180_000) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    path = RAW_DIR / "du_lieu_diem_thi_2026.csv"
    available_subjects = [subject for subject in SUBJECTS if subject in header_columns(path)]
    pairs = [
        ("Toan", "VatLy"),
        ("Toan", "HoaHoc"),
        ("Toan", "SinhHoc"),
        ("VatLy", "HoaHoc"),
        ("NguVan", "LichSu"),
        ("NguVan", "DiaLy"),
        ("LichSu", "DiaLy"),
        ("NgoaiNgu", "Toan"),
        ("NgoaiNgu", "VatLy"),
        ("NgoaiNgu", "HoaHoc"),
        ("NgoaiNgu", "SinhHoc"),
        ("NgoaiNgu", "NguVan"),
        ("NgoaiNgu", "LichSu"),
        ("NgoaiNgu", "DiaLy"),
        ("NgoaiNgu", "KinhTePhapLuat"),
    ]
    pairs = [(left, right) for left, right in pairs if left in available_subjects and right in available_subjects]
    pair_acc = {pair: [0, 0.0, 0.0, 0.0, 0.0, 0.0] for pair in pairs}
    ten_acc: dict[str, dict[str, float]] = defaultdict(lambda: {"count": 0, "other_sum": 0.0, "other_count": 0})
    digit_acc = {"n": 0, "sx": 0.0, "sy": 0.0, "sx2": 0.0, "sy2": 0.0, "sxy": 0.0}
    lucky_acc: dict[str, dict[str, float]] = defaultdict(lambda: {"count": 0, "sum": 0.0})

    usecols = ["SBD", *available_subjects]
    for chunk in pd.read_csv(path, usecols=usecols, dtype={"SBD": "string"}, chunksize=chunksize):
        scores = chunk[available_subjects].apply(pd.to_numeric, errors="coerce")
        for left, right in pairs:
            frame = scores[[left, right]].dropna()
            if frame.empty:
                continue
            x = frame[left]
            y = frame[right]
            acc = pair_acc[(left, right)]
            acc[0] += int(len(frame))
            acc[1] += float(x.sum())
            acc[2] += float(y.sum())
            acc[3] += float((x * x).sum())
            acc[4] += float((y * y).sum())
            acc[5] += float((x * y).sum())

        for subject in available_subjects:
            if subject not in scores.columns:
                continue
            mask = scores[subject] == 10
            if not mask.any():
                continue
            other = scores.loc[mask, [col for col in available_subjects if col != subject]]
            data = ten_acc[subject]
            data["count"] += int(mask.sum())
            data["other_sum"] += float(other.sum(skipna=True).sum())
            data["other_count"] += int(other.count().sum())

        avg_score = scores.mean(axis=1, skipna=True)
        valid = avg_score.notna()
        sbd = chunk.loc[valid, "SBD"].astype("string").fillna("")
        avg = avg_score.loc[valid]
        digit_sum = sbd.str.replace(r"\D", "", regex=True).map(lambda x: sum(int(ch) for ch in x) if x else math.nan)
        valid_digit = digit_sum.notna()
        x = digit_sum.loc[valid_digit].astype(float)
        y = avg.loc[valid_digit].astype(float)
        digit_acc["n"] += int(len(x))
        digit_acc["sx"] += float(x.sum())
        digit_acc["sy"] += float(y.sum())
        digit_acc["sx2"] += float((x * x).sum())
        digit_acc["sy2"] += float((y * y).sum())
        digit_acc["sxy"] += float((x * y).sum())

        lucky_masks = {
            "contains_68_or_86": sbd.str.contains("68|86", regex=True, na=False),
            "ends_88": sbd.str.endswith("88", na=False),
            "repeated_four": sbd.map(lambda value: any(value.count(str(digit)) >= 4 for digit in range(10))),
            "all_candidates": pd.Series(True, index=sbd.index),
        }
        for label, mask in lucky_masks.items():
            selected = avg.loc[mask.reindex(avg.index, fill_value=False)]
            lucky_acc[label]["count"] += int(selected.count())
            lucky_acc[label]["sum"] += float(selected.sum())

    corr_rows = []
    for (left, right), (n, sx, sy, sx2, sy2, sxy) in pair_acc.items():
        corr_rows.append(
            {
                "year": 2026,
                "left": left,
                "left_label": subject_label(left),
                "right": right,
                "right_label": subject_label(right),
                "n": int(n),
                "pearson": round(pearson_from_sums(int(n), sx, sy, sx2, sy2, sxy), 4),
            }
        )
    corr = pd.DataFrame(corr_rows)
    corr.to_csv(ANALYSIS_DIR / "correlation_2026.csv", index=False)

    ten_rows = []
    for subject, data in sorted(ten_acc.items()):
        ten_rows.append(
            {
                "year": 2026,
                "subject": subject,
                "subject_label": subject_label(subject),
                "count_10": int(data["count"]),
                "mean_other_scores": round(data["other_sum"] / data["other_count"], 4)
                if data["other_count"]
                else math.nan,
                "other_score_attempts": int(data["other_count"]),
            }
        )
    ten = pd.DataFrame(ten_rows)
    ten.to_csv(ANALYSIS_DIR / "perfect_10_peer_scores_2026.csv", index=False)

    sbd = {
        "digit_sum_corr": round(
            pearson_from_sums(
                int(digit_acc["n"]),
                digit_acc["sx"],
                digit_acc["sy"],
                digit_acc["sx2"],
                digit_acc["sy2"],
                digit_acc["sxy"],
            ),
            6,
        ),
        "groups": {
            key: {
                "count": int(value["count"]),
                "mean_candidate_score": round(value["sum"] / value["count"], 4) if value["count"] else math.nan,
            }
            for key, value in lucky_acc.items()
        },
    }
    return corr, ten, sbd


def zodiac(day: float | int | None, month: float | int | None) -> str | None:
    if day is None or month is None or math.isnan(float(day)) or math.isnan(float(month)):
        return None
    d = int(day)
    m = int(month)
    if not (1 <= d <= 31 and 1 <= m <= 12):
        return None
    signs = [
        ("Ma Kết", (1, 19)),
        ("Bảo Bình", (2, 18)),
        ("Song Ngư", (3, 20)),
        ("Bạch Dương", (4, 19)),
        ("Kim Ngưu", (5, 20)),
        ("Song Tử", (6, 21)),
        ("Cự Giải", (7, 22)),
        ("Sư Tử", (8, 22)),
        ("Xử Nữ", (9, 22)),
        ("Thiên Bình", (10, 23)),
        ("Bọ Cạp", (11, 22)),
        ("Nhân Mã", (12, 21)),
        ("Ma Kết", (12, 31)),
    ]
    for sign, (end_month, end_day) in signs:
        if (m, d) <= (end_month, end_day):
            return sign
    return "Ma Kết"


def normalize_name(value: Any) -> str:
    if pd.isna(value):
        return ""
    text = str(value).strip()
    if not text:
        return ""
    return text.title()


def build_legacy_fun_metrics(chunksize: int = 180_000) -> dict[str, Any]:
    path = ANALYSIS_DIR / "legacy_2013_2014_features.csv"
    score_series = pd.read_csv(path, usecols=["score_total"])["score_total"].dropna()
    score_series = score_series[(score_series >= 0) & (score_series <= 30)]
    p90 = float(score_series.quantile(0.90))
    p95 = float(score_series.quantile(0.95))
    valedictorian_cutoff = 29.0

    given: dict[str, dict[str, float]] = defaultdict(
        lambda: {"count": 0, "sum": 0.0, "high": 0, "near_valedictorian": 0, "perfect_30": 0}
    )
    family: dict[str, dict[str, float]] = defaultdict(lambda: {"count": 0, "sum": 0.0, "high": 0})
    month: dict[int, dict[str, float]] = defaultdict(lambda: {"count": 0, "sum": 0.0, "high": 0})
    sign_acc: dict[str, dict[str, float]] = defaultdict(lambda: {"count": 0, "sum": 0.0, "high": 0})
    middle: dict[int, dict[str, float]] = defaultdict(lambda: {"count": 0, "sum": 0.0})
    anh_foreign = {"anh_count": 0, "anh_sum": 0.0, "other_count": 0, "other_sum": 0.0}
    nguyen = {"nguyen_count": 0, "nguyen_sum": 0.0, "other_count": 0, "other_sum": 0.0}

    usecols = [
        "family_name",
        "given_name",
        "birth_day",
        "birth_month",
        "birth_date_valid",
        "middle_name_token_count",
        "block_code",
        "score_mon2",
        "score_total",
    ]
    for chunk in pd.read_csv(path, usecols=usecols, chunksize=chunksize):
        scores = pd.to_numeric(chunk["score_total"], errors="coerce")
        valid_score = scores.notna() & scores.between(0, 30)
        high = scores >= p95
        for name, score, is_high in zip(chunk.loc[valid_score, "given_name"], scores.loc[valid_score], high.loc[valid_score]):
            key = normalize_name(name)
            if len(key) < 2 or key in SUSPICIOUS_GIVEN_NAMES:
                continue
            given[key]["count"] += 1
            given[key]["sum"] += float(score)
            given[key]["high"] += int(bool(is_high))
            given[key]["near_valedictorian"] += int(float(score) >= valedictorian_cutoff)
            given[key]["perfect_30"] += int(float(score) == 30.0)
        for name, score, is_high in zip(chunk.loc[valid_score, "family_name"], scores.loc[valid_score], high.loc[valid_score]):
            key = normalize_name(name)
            if len(key) < 2:
                continue
            family[key]["count"] += 1
            family[key]["sum"] += float(score)
            family[key]["high"] += int(bool(is_high))
            if key == "Nguyễn":
                nguyen["nguyen_count"] += 1
                nguyen["nguyen_sum"] += float(score)
            else:
                nguyen["other_count"] += 1
                nguyen["other_sum"] += float(score)

        months = pd.to_numeric(chunk["birth_month"], errors="coerce")
        days = pd.to_numeric(chunk["birth_day"], errors="coerce")
        birth_valid = chunk["birth_date_valid"].astype(str).str.lower().eq("true")
        for day, mon, score, is_high in zip(days[birth_valid & valid_score], months[birth_valid & valid_score], scores[birth_valid & valid_score], high[birth_valid & valid_score]):
            if pd.isna(mon):
                continue
            mon_int = int(mon)
            if not (1 <= mon_int <= 12):
                continue
            month[mon_int]["count"] += 1
            month[mon_int]["sum"] += float(score)
            month[mon_int]["high"] += int(bool(is_high))
            sign = zodiac(day, mon)
            if sign:
                sign_acc[sign]["count"] += 1
                sign_acc[sign]["sum"] += float(score)
                sign_acc[sign]["high"] += int(bool(is_high))

        middle_counts = pd.to_numeric(chunk["middle_name_token_count"], errors="coerce")
        for count_value, score in zip(middle_counts[valid_score], scores[valid_score]):
            if pd.isna(count_value):
                continue
            key = int(count_value)
            middle[key]["count"] += 1
            middle[key]["sum"] += float(score)

        block = chunk["block_code"].astype("string").fillna("")
        mon2 = pd.to_numeric(chunk["score_mon2"], errors="coerce")
        block_d = block.str.upper().str.startswith("D") & mon2.notna()
        given_name = chunk["given_name"].map(normalize_name)
        anh_mask = block_d & given_name.eq("Anh")
        other_mask = block_d & ~given_name.eq("Anh")
        anh_foreign["anh_count"] += int(anh_mask.sum())
        anh_foreign["anh_sum"] += float(mon2[anh_mask].sum())
        anh_foreign["other_count"] += int(other_mask.sum())
        anh_foreign["other_sum"] += float(mon2[other_mask].sum())

    def top_by_mean(bucket: dict[str, dict[str, float]], min_count: int, limit: int = 10) -> list[dict[str, Any]]:
        rows = [
            {
                "name": key,
                "count": int(value["count"]),
                "mean_total_score": value["sum"] / value["count"],
                "high_share": value["high"] / value["count"],
                "high_count": int(value["high"]),
                "near_valedictorian_count": int(value.get("near_valedictorian", 0)),
                "near_valedictorian_share": value.get("near_valedictorian", 0) / value["count"],
                "perfect_30_count": int(value.get("perfect_30", 0)),
            }
            for key, value in bucket.items()
            if value["count"] >= min_count
        ]
        return sorted(rows, key=lambda item: (-item["mean_total_score"], -item["count"]))[:limit]

    def top_high(bucket: dict[str, dict[str, float]], min_count: int, limit: int = 10) -> list[dict[str, Any]]:
        rows = [
            {
                "name": key,
                "count": int(value["count"]),
                "mean_total_score": value["sum"] / value["count"],
                "high_share": value["high"] / value["count"],
                "high_count": int(value["high"]),
                "near_valedictorian_count": int(value.get("near_valedictorian", 0)),
                "near_valedictorian_share": value.get("near_valedictorian", 0) / value["count"],
                "perfect_30_count": int(value.get("perfect_30", 0)),
            }
            for key, value in bucket.items()
            if value["count"] >= min_count
        ]
        return sorted(rows, key=lambda item: (-item["high_share"], -item["high_count"]))[:limit]

    def top_valedictorian_count(min_count: int, limit: int = 10) -> list[dict[str, Any]]:
        rows = [
            {
                "name": key,
                "count": int(value["count"]),
                "mean_total_score": value["sum"] / value["count"],
                "near_valedictorian_count": int(value.get("near_valedictorian", 0)),
                "near_valedictorian_share": value.get("near_valedictorian", 0) / value["count"],
                "perfect_30_count": int(value.get("perfect_30", 0)),
            }
            for key, value in given.items()
            if value["count"] >= min_count and value.get("near_valedictorian", 0) > 0
        ]
        return sorted(rows, key=lambda item: (-item["near_valedictorian_count"], -item["count"]))[:limit]

    def top_valedictorian_share(min_count: int, limit: int = 10) -> list[dict[str, Any]]:
        rows = [
            {
                "name": key,
                "count": int(value["count"]),
                "mean_total_score": value["sum"] / value["count"],
                "near_valedictorian_count": int(value.get("near_valedictorian", 0)),
                "near_valedictorian_share": value.get("near_valedictorian", 0) / value["count"],
                "perfect_30_count": int(value.get("perfect_30", 0)),
            }
            for key, value in given.items()
            if value["count"] >= min_count and value.get("near_valedictorian", 0) > 0
        ]
        return sorted(
            rows,
            key=lambda item: (-item["near_valedictorian_share"], -item["near_valedictorian_count"], -item["count"]),
        )[:limit]

    def bucket_rows(bucket: dict[int | str, dict[str, float]], key_name: str) -> list[dict[str, Any]]:
        rows = []
        for key, value in bucket.items():
            count = int(value["count"])
            rows.append(
                {
                    key_name: key,
                    "count": count,
                    "mean_total_score": round(value["sum"] / count, 4),
                    "high_share": round(value.get("high", 0) / count, 6) if count else None,
                }
            )
        return sorted(rows, key=lambda item: item[key_name])

    given_mean = top_by_mean(given, 1_000)
    given_high = top_high(given, 1_000)
    given_valedictorian_count = top_valedictorian_count(1_000)
    given_valedictorian_share = top_valedictorian_share(1_000)
    family_mean = top_by_mean(family, 2_000)
    month_rows = bucket_rows(month, "birth_month")
    zodiac_rows = bucket_rows(sign_acc, "zodiac")
    middle_rows = bucket_rows(middle, "middle_name_token_count")

    return {
        "p90_total_score": round(p90, 4),
        "p95_total_score": round(p95, 4),
        "valedictorian_cutoff": valedictorian_cutoff,
        "top_given_by_mean": given_mean,
        "top_given_by_high_share": given_high,
        "top_given_by_valedictorian_count": given_valedictorian_count,
        "top_given_by_valedictorian_share": given_valedictorian_share,
        "top_family_by_mean": family_mean,
        "birth_month": month_rows,
        "zodiac": zodiac_rows,
        "middle_name_token_count": middle_rows,
        "anh_foreign_language": {
            "anh_count": anh_foreign["anh_count"],
            "anh_mean_score_mon2": round(anh_foreign["anh_sum"] / anh_foreign["anh_count"], 4)
            if anh_foreign["anh_count"]
            else None,
            "other_count": anh_foreign["other_count"],
            "other_mean_score_mon2": round(anh_foreign["other_sum"] / anh_foreign["other_count"], 4)
            if anh_foreign["other_count"]
            else None,
        },
        "nguyen_vs_other": {
            "nguyen_count": nguyen["nguyen_count"],
            "nguyen_mean_total_score": round(nguyen["nguyen_sum"] / nguyen["nguyen_count"], 4),
            "other_count": nguyen["other_count"],
            "other_mean_total_score": round(nguyen["other_sum"] / nguyen["other_count"], 4),
        },
    }


def top_records(df: pd.DataFrame, sort_col: str, limit: int = 5, ascending: bool = False) -> list[dict[str, Any]]:
    if df.empty:
        return []
    return df.sort_values(sort_col, ascending=ascending).head(limit).to_dict("records")


def row_by(df: pd.DataFrame, **conditions: Any) -> dict[str, Any] | None:
    mask = pd.Series(True, index=df.index)
    for key, value in conditions.items():
        mask &= df[key] == value
    if not mask.any():
        return None
    return df.loc[mask].iloc[0].to_dict()


def compute_story(
    subject_metrics: pd.DataFrame,
    segment_metrics: pd.DataFrame,
    province_metrics: pd.DataFrame,
    combo_metrics: pd.DataFrame,
    correlations: pd.DataFrame,
    perfect10: pd.DataFrame,
    sbd_metrics: dict[str, Any],
    legacy: dict[str, Any],
) -> dict[str, Any]:
    latest_year = int(subject_metrics["year"].max())
    latest_subjects = subject_metrics[subject_metrics["year"] == latest_year].copy()
    years = sorted(subject_metrics["year"].unique().tolist())

    annual = (
        subject_metrics.groupby("year")
        .apply(lambda g: pd.Series({"weighted_mean": (g["mean"] * g["count"]).sum() / g["count"].sum(), "subject_count": len(g)}))
        .reset_index()
    )
    hardest = annual.sort_values("weighted_mean").iloc[0].to_dict()
    easiest = annual.sort_values("weighted_mean", ascending=False).iloc[0].to_dict()

    subject_changes = []
    for subject, group in subject_metrics.groupby("subject"):
        group = group.sort_values("year")
        first = group.iloc[0]
        last = group.iloc[-1]
        subject_changes.append(
            {
                "subject": subject,
                "subject_label": subject_label(subject),
                "first_year": int(first["year"]),
                "last_year": int(last["year"]),
                "first_mean": float(first["mean"]),
                "last_mean": float(last["mean"]),
                "change": float(last["mean"] - first["mean"]),
            }
        )
    biggest_gain = max(subject_changes, key=lambda item: item["change"])
    biggest_drop = min(subject_changes, key=lambda item: item["change"])

    streaks = []
    for subject, group in subject_metrics.groupby("subject"):
        group = group.sort_values("year")
        current = 0
        best = 0
        best_end = None
        last_mean = None
        for _, row in group.iterrows():
            mean = float(row["mean"])
            if last_mean is not None and mean < last_mean:
                current += 1
            else:
                current = 0
            if current > best:
                best = current
                best_end = int(row["year"])
            last_mean = mean
        if best:
            streaks.append({"subject": subject, "subject_label": subject_label(subject), "decline_steps": best, "end_year": best_end})
    longest_decline = max(streaks, key=lambda item: item["decline_steps"])

    mean_variation = (
        subject_metrics[subject_metrics["subject"].isin(["Toan", "NguVan"])]
        .groupby("subject")["mean"]
        .std()
        .to_dict()
    )
    stable_subject = "Toan" if mean_variation.get("Toan", 0) < mean_variation.get("NguVan", 0) else "NguVan"

    top10_row = subject_metrics.sort_values("count_10", ascending=False).iloc[0].to_dict()
    highest_liet = subject_metrics.sort_values("share_le_1", ascending=False).iloc[0].to_dict()
    highest_below5 = subject_metrics.sort_values("share_lt_5", ascending=False).iloc[0].to_dict()
    highest_8_latest = latest_subjects.sort_values("share_ge_8", ascending=False).iloc[0].to_dict()
    highest_std_latest = latest_subjects.sort_values("std", ascending=False).iloc[0].to_dict()
    lowest_std_latest = latest_subjects.sort_values("std").iloc[0].to_dict()
    low_heavy_latest = latest_subjects.sort_values("share_lt_5", ascending=False).iloc[0].to_dict()
    normal_closest = subject_metrics.dropna(subset=["normality_distance"]).sort_values("normality_distance").iloc[0].to_dict()
    normal_farthest = subject_metrics.dropna(subset=["normality_distance"]).sort_values("normality_distance", ascending=False).iloc[0].to_dict()

    latest_province = province_metrics[province_metrics["year"] == latest_year].copy()
    province_overall = (
        latest_province.groupby(["province_code", "province_name", "region"])
        .apply(lambda g: pd.Series({"mean": (g["mean"] * g["count"]).sum() / g["count"].sum(), "attempts": int(g["count"].sum())}))
        .reset_index()
    )
    province_best = province_overall.sort_values("mean", ascending=False).iloc[0].to_dict()
    province_worst = province_overall.sort_values("mean").iloc[0].to_dict()
    province_non_center = province_overall[~province_overall["province_name"].isin(["Hà Nội", "TP. Hồ Chí Minh"])]
    province_surprise = province_non_center.sort_values("mean", ascending=False).iloc[0].to_dict()

    province_10 = (
        latest_province.groupby(["province_code", "province_name"])
        .apply(lambda g: pd.Series({"score_attempts": int(g["count"].sum()), "share_10": (g["share_ge_10"] * g["count"]).sum() / g["count"].sum()}))
        .reset_index()
        .sort_values("share_10", ascending=False)
    )
    province_10_best = province_10.iloc[0].to_dict()

    def top_provinces_for(subject: str, limit: int = 10, ascending: bool = False) -> list[dict[str, Any]]:
        sub = latest_province[(latest_province["subject"] == subject) & (latest_province["count"] >= 500)]
        return sub.sort_values("mean", ascending=ascending).head(limit).to_dict("records")

    province_top_subjects = {
        "Toan": top_provinces_for("Toan"),
        "NguVan": top_provinces_for("NguVan"),
        "NgoaiNgu": top_provinces_for("NgoaiNgu"),
    }
    province_english_lowest = top_provinces_for("NgoaiNgu", limit=1, ascending=True)[0]

    centers = {}
    for name in ["Hà Nội", "TP. Hồ Chí Minh"]:
        item = province_overall[province_overall["province_name"] == name].iloc[0].to_dict()
        rest = province_overall[province_overall["province_name"] != name]
        centers[name] = {
            "mean": float(item["mean"]),
            "rest_mean": float((rest["mean"] * rest["attempts"]).sum() / rest["attempts"].sum()),
        }
        centers[name]["gap_vs_rest"] = centers[name]["mean"] - centers[name]["rest_mean"]
    centers["HaNoi_vs_HCM"] = centers["Hà Nội"]["mean"] - centers["TP. Hồ Chí Minh"]["mean"]

    region_balance = (
        latest_province.groupby(["region", "subject"])
        .apply(lambda g: pd.Series({"mean": (g["mean"] * g["count"]).sum() / g["count"].sum(), "count": int(g["count"].sum())}))
        .reset_index()
    )
    region_spread = region_balance.groupby("region")["mean"].std().reset_index(name="subject_mean_std").sort_values("subject_mean_std")
    region_most_balanced = region_spread.iloc[0].to_dict()

    stable_years = province_metrics[(province_metrics["year"].isin([2017, 2024])) & (province_metrics["count"] >= 100)]
    growth_base = (
        stable_years.groupby(["year", "province_code", "province_name"])
        .apply(lambda g: pd.Series({"mean": (g["mean"] * g["count"]).sum() / g["count"].sum(), "attempts": int(g["count"].sum())}))
        .reset_index()
    )
    pivot_growth = growth_base.pivot_table(index=["province_code", "province_name"], columns="year", values="mean")
    pivot_growth = pivot_growth.dropna()
    pivot_growth["change"] = pivot_growth[2024] - pivot_growth[2017]
    province_fastest_growth = pivot_growth.sort_values("change", ascending=False).reset_index().iloc[0].to_dict()

    latest_combo = combo_metrics[combo_metrics["year"] == latest_year].copy()
    best_combo = latest_combo.sort_values("mean", ascending=False).iloc[0].to_dict()
    best_combo_27 = latest_combo.sort_values("share_ge_27", ascending=False).iloc[0].to_dict()

    corr_lookup = {(row.left, row.right): row for row in correlations.itertuples(index=False)}
    natural_corrs = [
        float(corr_lookup[("NgoaiNgu", subject)].pearson)
        for subject in ["Toan", "VatLy", "HoaHoc", "SinhHoc"]
        if ("NgoaiNgu", subject) in corr_lookup and not pd.isna(corr_lookup[("NgoaiNgu", subject)].pearson)
    ]
    social_corrs = [
        float(corr_lookup[("NgoaiNgu", subject)].pearson)
        for subject in ["NguVan", "LichSu", "DiaLy", "KinhTePhapLuat"]
        if ("NgoaiNgu", subject) in corr_lookup and not pd.isna(corr_lookup[("NgoaiNgu", subject)].pearson)
    ]
    english_corr_side = {
        "natural": sum(natural_corrs) / len(natural_corrs),
        "social": sum(social_corrs) / len(social_corrs),
    }

    common_subjects = ["Toan", "NguVan", "VatLy", "HoaHoc", "SinhHoc", "LichSu", "DiaLy", "NgoaiNgu"]
    annual_wide = subject_metrics[subject_metrics["year"].between(2017, 2024) & subject_metrics["subject"].isin(common_subjects)]
    annual_wide = annual_wide.pivot(index="year", columns="subject", values="mean")
    annual_corr = annual_wide.corr()
    inverse_pair = None
    for left in common_subjects:
        for right in common_subjects:
            if left >= right:
                continue
            value = float(annual_corr.loc[left, right])
            if inverse_pair is None or value < inverse_pair["corr"]:
                inverse_pair = {"left": left, "right": right, "corr": value}

    latest_2025_common = subject_metrics[subject_metrics["year"] == 2025]
    common_25_26 = sorted(set(latest_2025_common["subject"]) & set(latest_subjects["subject"]))
    diff_25_26 = []
    for subject in common_25_26:
        row25 = row_by(subject_metrics, year=2025, subject=subject)
        row26 = row_by(subject_metrics, year=2026, subject=subject)
        if row25 and row26:
            diff_25_26.append({"subject": subject, "change": float(row26["mean"] - row25["mean"])})
    diff_25_26_sorted = sorted(diff_25_26, key=lambda item: item["change"])

    macro_2019 = float(annual[annual["year"] == 2019]["weighted_mean"].iloc[0])
    macro_2020 = float(annual[annual["year"] == 2020]["weighted_mean"].iloc[0])

    segment_2016 = segment_metrics[segment_metrics["year"] == 2016]
    segment_2016_macro = (
        segment_2016.groupby("segment")
        .apply(lambda g: pd.Series({"mean": (g["mean"] * g["count"]).sum() / g["count"].sum(), "count": int(g["count"].sum())}))
        .reset_index()
        .to_dict("records")
    )

    forecast_subjects = subject_metrics[subject_metrics["subject"].isin(common_subjects)]
    forecast_rows = []
    for subject, group in forecast_subjects.groupby("subject"):
        recent = group.sort_values("year").tail(4)
        if len(recent) < 3:
            continue
        xs = recent["year"].astype(float)
        ys = recent["mean"].astype(float)
        xbar = xs.mean()
        ybar = ys.mean()
        slope = float(((xs - xbar) * (ys - ybar)).sum() / ((xs - xbar) ** 2).sum())
        forecast_rows.append({"subject": subject, "subject_label": subject_label(subject), "slope": slope})
    forecast_rise = max(forecast_rows, key=lambda item: item["slope"])

    return {
        "latest_year": latest_year,
        "years": years,
        "annual": annual.to_dict("records"),
        "hardest": hardest,
        "easiest": easiest,
        "biggest_gain": biggest_gain,
        "biggest_drop": biggest_drop,
        "longest_decline": longest_decline,
        "mean_variation": mean_variation,
        "stable_subject": stable_subject,
        "top10_row": top10_row,
        "highest_liet": highest_liet,
        "highest_below5": highest_below5,
        "highest_8_latest": highest_8_latest,
        "highest_std_latest": highest_std_latest,
        "lowest_std_latest": lowest_std_latest,
        "low_heavy_latest": low_heavy_latest,
        "normal_closest": normal_closest,
        "normal_farthest": normal_farthest,
        "latest_subjects": latest_subjects.sort_values("mean", ascending=False).to_dict("records"),
        "province_overall_latest": province_overall.sort_values("mean", ascending=False).to_dict("records"),
        "province_best": province_best,
        "province_worst": province_worst,
        "province_surprise": province_surprise,
        "province_10_best": province_10_best,
        "province_top_subjects": province_top_subjects,
        "province_english_lowest": province_english_lowest,
        "centers": centers,
        "region_most_balanced": region_most_balanced,
        "province_fastest_growth": province_fastest_growth,
        "latest_combo": latest_combo.sort_values("mean", ascending=False).to_dict("records"),
        "best_combo": best_combo,
        "best_combo_27": best_combo_27,
        "combo_metrics": combo_metrics.to_dict("records"),
        "correlations": correlations.to_dict("records"),
        "perfect10": perfect10.sort_values("mean_other_scores", ascending=False).to_dict("records"),
        "english_corr_side": english_corr_side,
        "inverse_pair": inverse_pair,
        "diff_25_26": diff_25_26_sorted,
        "macro_2019_2020_change": macro_2020 - macro_2019,
        "segment_2016_macro": segment_2016_macro,
        "sbd_metrics": sbd_metrics,
        "legacy": legacy,
        "forecast_rise": forecast_rise,
    }


def build_questions(story: dict[str, Any]) -> list[dict[str, Any]]:
    questions: list[dict[str, Any]] = []

    def add(group: str, question: str, answer: str, evidence: str, status: str = "Trả lời được", tags: list[str] | None = None) -> None:
        questions.append(
            {
                "id": len(questions) + 1,
                "group": group,
                "question": question,
                "answer": answer,
                "evidence": evidence,
                "status": status,
                "tags": tags or [],
            }
        )

    latest_year = story["latest_year"]
    hardest = story["hardest"]
    easiest = story["easiest"]
    gain = story["biggest_gain"]
    drop = story["biggest_drop"]
    ten = story["top10_row"]
    liet = story["highest_liet"]
    below5 = story["highest_below5"]
    latest_subjects = {row["subject"]: row for row in story["latest_subjects"]}
    combos_latest = {row["combo"]: row for row in story["latest_combo"]}
    corr = {(row["left"], row["right"]): row for row in story["correlations"]}
    legacy = story["legacy"]

    add(
        "Xu hướng điểm số",
        "Năm nào có mặt bằng điểm chung thấp nhất và cao nhất trong chuỗi 2016-2026?",
        f"Theo trung bình có trọng số trên các lượt điểm môn, năm thấp nhất là {int(hardest['year'])} với mean {fmt_score(hardest['weighted_mean'])}; năm cao nhất là {int(easiest['year'])} với mean {fmt_score(easiest['weighted_mean'])}.",
        "Tính từ data/summary/subject_score_distribution.csv và year_subject_stats.csv; cần đọc cùng chú thích đổi cấu trúc 2025-2026.",
    )
    add(
        "Xu hướng điểm số",
        "Môn nào tăng điểm trung bình mạnh nhất qua toàn bộ quãng có dữ liệu?",
        f"{gain['subject_label']} tăng mạnh nhất: từ {fmt_score(gain['first_mean'])} năm {gain['first_year']} lên {fmt_score(gain['last_mean'])} năm {gain['last_year']}, chênh {fmt_score(gain['change'])} điểm.",
        "So sánh năm đầu và năm cuối có mặt của từng môn.",
    )
    add(
        "Xu hướng điểm số",
        "Môn nào giảm điểm trung bình mạnh nhất qua toàn bộ quãng có dữ liệu?",
        f"{drop['subject_label']} giảm mạnh nhất: từ {fmt_score(drop['first_mean'])} năm {drop['first_year']} xuống {fmt_score(drop['last_mean'])} năm {drop['last_year']}, chênh {fmt_score(drop['change'])} điểm.",
        "So sánh năm đầu và năm cuối có mặt của từng môn.",
    )

    for subject in ["Toan", "NguVan", "NgoaiNgu", "LichSu"]:
        rows = [row for row in story["latest_subjects"] if row["subject"] == subject]
        latest = rows[0] if rows else latest_subjects.get(subject)
        first = None
        for item in sorted([r for r in story["annual"]], key=lambda x: x["year"]):
            del item
        # Pull first/last directly from subject metrics stored in chart rows later.
        subject_rows = [r for r in story["subject_chart"] if r["subject"] == subject]
        subject_rows = sorted(subject_rows, key=lambda r: r["year"])
        first = subject_rows[0]
        last = subject_rows[-1]
        add(
            "Xu hướng điểm số",
            f"Điểm trung bình môn {subject_label(subject)} thay đổi thế nào qua các năm?",
            f"{subject_label(subject)} đi từ {fmt_score(first['mean'])} năm {first['year']} đến {fmt_score(last['mean'])} năm {last['year']}; riêng {latest_year} mean là {fmt_score(latest['mean'])}, p90 là {fmt_score(latest['p90'])}.",
            "Dựa trên thống kê theo môn/năm; không điều chỉnh khác biệt đề thi giữa các năm.",
        )

    gdcd_rows = sorted([r for r in story["subject_chart"] if r["subject"] == "GDCD"], key=lambda r: r["year"])
    ktpl = latest_subjects.get("KinhTePhapLuat")
    add(
        "Xu hướng điểm số",
        "GDCD/Kinh tế và pháp luật có còn là nhóm môn điểm cao không?",
        f"Có, trong giai đoạn GDPT 2006, GDCD thường nằm nhóm mean cao; ở {latest_year}, Kinh tế và pháp luật đạt mean {fmt_score(ktpl['mean'])} và p90 {fmt_score(ktpl['p90'])}." if ktpl else "Không đủ dữ liệu năm mới cho Kinh tế và pháp luật.",
        f"GDCD có {len(gdcd_rows)} năm dữ liệu; Kinh tế và pháp luật xuất hiện ở schema 2025-2026.",
    )
    add(
        "Xu hướng điểm số",
        "Tỷ lệ điểm 8+ năm gần nhất cao nhất ở môn nào?",
        f"Năm {latest_year}, {story['highest_8_latest']['subject_label']} có tỷ lệ 8+ cao nhất: {fmt_pct(story['highest_8_latest']['share_ge_8'])}.",
        "Tỷ lệ = số lượt điểm >=8 / số lượt dự thi môn đó.",
    )
    add(
        "Xu hướng điểm số",
        "Tỷ lệ điểm liệt (<=1) cao nhất rơi vào môn/năm nào?",
        f"Cực trị toàn chuỗi là {liet['subject_label']} năm {int(liet['year'])}: {fmt_pct(liet['share_le_1'])}.",
        "Tính trên từng môn/năm, ngưỡng <=1.",
    )
    add(
        "Xu hướng điểm số",
        "Môn/năm nào có tỷ lệ dưới trung bình (<5) cao nhất?",
        f"{below5['subject_label']} năm {int(below5['year'])} có tỷ lệ dưới 5 cao nhất: {fmt_pct(below5['share_lt_5'])}.",
        "Tính trên từng môn/năm.",
    )
    add(
        "Xu hướng điểm số",
        "Năm nào và môn nào có nhiều điểm 10 nhất?",
        f"Kỷ lục số lượng điểm 10 là {ten['subject_label']} năm {int(ten['year'])} với {fmt_num(int(ten['count_10']))} điểm 10.",
        "Đếm tuyệt đối từ phổ điểm theo môn/năm.",
    )
    add(
        "Xu hướng điểm số",
        "Có môn nào giảm điểm trung bình liên tục nhiều năm liền không?",
        f"Có. Chuỗi giảm dài nhất là {story['longest_decline']['subject_label']} với {story['longest_decline']['decline_steps']} bước giảm liên tiếp, kết thúc năm {story['longest_decline']['end_year']}.",
        "Dò chuỗi mean năm sau < năm trước theo từng môn.",
    )
    stable = story["stable_subject"]
    other = "NguVan" if stable == "Toan" else "Toan"
    add(
        "Xu hướng điểm số",
        "So sánh Toán và Ngữ văn: môn nào ổn định hơn theo trung bình năm?",
        f"{subject_label(stable)} ổn định hơn theo độ lệch chuẩn của mean qua năm: {fmt_score(story['mean_variation'][stable])}, so với {subject_label(other)} là {fmt_score(story['mean_variation'][other])}.",
        "Dùng độ lệch chuẩn của điểm trung bình năm, không phải độ lệch chuẩn điểm cá nhân.",
    )
    add(
        "Xu hướng điểm số",
        "Năm gần nhất có dễ hơn năm trước không?",
        f"So với 2025, các môn chung năm 2026 biến động không đồng đều. Môn giảm mạnh nhất là {subject_label(story['diff_25_26'][0]['subject'])} ({fmt_score(story['diff_25_26'][0]['change'])}); môn tăng mạnh nhất là {subject_label(story['diff_25_26'][-1]['subject'])} ({fmt_score(story['diff_25_26'][-1]['change'])}).",
        "2025 là năm chuyển tiếp CT2006/CT2018, nên kết luận 'dễ hơn' chỉ nên đọc theo từng môn.",
        "Một phần",
    )

    # Province and region
    add(
        "Tỉnh thành và vùng miền",
        f"Năm {latest_year}, tỉnh/thành nào có mặt bằng điểm cao nhất?",
        f"{story['province_best']['province_name']} đứng đầu theo trung bình mọi lượt điểm môn: {fmt_score(story['province_best']['mean'])}.",
        "Xếp hạng theo mean có trọng số các lượt điểm môn trong năm 2026.",
    )
    add(
        "Tỉnh thành và vùng miền",
        f"Năm {latest_year}, tỉnh/thành nào có mặt bằng điểm thấp nhất?",
        f"{story['province_worst']['province_name']} thấp nhất theo cùng cách tính: {fmt_score(story['province_worst']['mean'])}.",
        "Xếp hạng theo mean có trọng số các lượt điểm môn trong năm 2026.",
    )
    for subject in ["Toan", "NguVan", "NgoaiNgu"]:
        top = story["province_top_subjects"][subject][:3]
        answer = "; ".join(f"{row['province_name']} {fmt_score(row['mean'])}" for row in top)
        add(
            "Tỉnh thành và vùng miền",
            f"Top tỉnh/thành môn {subject_label(subject)} năm {latest_year} là ai?",
            f"Top 3 là: {answer}.",
            "Chỉ xét tỉnh/thành có ít nhất 500 lượt điểm môn đó.",
        )
    add(
        "Tỉnh thành và vùng miền",
        "Tỉnh nào có điểm Ngoại ngữ trung bình thấp nhất năm gần nhất?",
        f"{story['province_english_lowest']['province_name']} thấp nhất trong bảng Ngoại ngữ 2026, mean {fmt_score(story['province_english_lowest']['mean'])}.",
        "Không tự gán nguyên nhân nông thôn/miền núi nếu chưa có biến kinh tế-xã hội.",
    )
    add(
        "Tỉnh thành và vùng miền",
        "Hà Nội chênh so với phần còn lại bao nhiêu điểm?",
        f"Năm {latest_year}, Hà Nội mean {fmt_score(story['centers']['Hà Nội']['mean'])}, cao hơn phần còn lại {fmt_score(story['centers']['Hà Nội']['gap_vs_rest'])} điểm.",
        "So sánh theo trung bình mọi lượt điểm môn.",
    )
    add(
        "Tỉnh thành và vùng miền",
        "TP.HCM chênh so với phần còn lại bao nhiêu điểm?",
        f"Năm {latest_year}, TP.HCM mean {fmt_score(story['centers']['TP. Hồ Chí Minh']['mean'])}, chênh {fmt_score(story['centers']['TP. Hồ Chí Minh']['gap_vs_rest'])} điểm so với phần còn lại.",
        "So sánh theo trung bình mọi lượt điểm môn.",
    )
    add(
        "Tỉnh thành và vùng miền",
        "Hà Nội và TP.HCM: nơi nào nhỉnh hơn trong năm gần nhất?",
        f"Hà Nội nhỉnh hơn TP.HCM {fmt_score(story['centers']['HaNoi_vs_HCM'])} điểm theo mean tổng hợp lượt điểm môn.",
        "Nếu giá trị âm nghĩa là TP.HCM cao hơn; ở đây dùng dữ liệu 2026.",
    )
    add(
        "Tỉnh thành và vùng miền",
        "Tỉnh nào 'vượt trội bất ngờ' nếu bỏ Hà Nội và TP.HCM?",
        f"{story['province_surprise']['province_name']} là tỉnh/thành ngoài hai trung tâm lớn có mean tổng hợp cao nhất: {fmt_score(story['province_surprise']['mean'])}.",
        "Đây là cách đặt câu hỏi vui; không kết luận chất lượng giáo dục chỉ từ điểm thi.",
    )
    add(
        "Tỉnh thành và vùng miền",
        "Tỉnh nào có tỷ lệ điểm 10 cao nhất so với số lượt dự thi?",
        f"{story['province_10_best']['province_name']} có tỷ lệ điểm 10 cao nhất năm {latest_year}: {fmt_pct(story['province_10_best']['share_10'])}.",
        "Tính trên mọi lượt điểm môn, không phải số thí sinh.",
    )
    add(
        "Tỉnh thành và vùng miền",
        "Miền nào học đều các môn hơn trong năm gần nhất?",
        f"{story['region_most_balanced']['region']} có độ lệch chuẩn mean giữa các môn thấp nhất: {fmt_score(story['region_most_balanced']['subject_mean_std'])}.",
        "Region mapping là quy ước phân tích, nhất là sau sáp nhập 2026.",
    )
    add(
        "Tỉnh thành và vùng miền",
        "Tỉnh nào tăng trưởng mặt bằng điểm nhanh nhất giai đoạn mã tỉnh ổn định 2017-2024?",
        f"{story['province_fastest_growth']['province_name']} tăng mạnh nhất: {fmt_score(story['province_fastest_growth']['change'])} điểm từ 2017 đến 2024.",
        "Không dùng 2026 vì mã tỉnh đã đổi theo mô hình 34 tỉnh/thành.",
    )
    nick = story["province_top_subjects"]["NgoaiNgu"][0]
    add(
        "Tỉnh thành và vùng miền",
        "Nếu đặt biệt danh theo môn mạnh, tỉnh nào xứng đáng là 'vương quốc Ngoại ngữ'?",
        f"Năm {latest_year}, {nick['province_name']} dẫn đầu Ngoại ngữ với mean {fmt_score(nick['mean'])}; biệt danh vui: 'vương quốc Ngoại ngữ'.",
        "Biệt danh chỉ là cách kể chuyện dữ liệu, không phải xếp hạng chính thức.",
    )
    add(
        "Tỉnh thành và vùng miền",
        "Có nên xếp hạng trường/cụm thi từ bộ này không?",
        "Chỉ làm được một phần: legacy 2013-2014 có mã trường dự thi, còn THPT 2016-2026 bulk hiện không có trường THPT. Vì vậy web không xếp hạng trường để tránh suy diễn thiếu dữ liệu.",
        "Gap report xác nhận thiếu trường học cho chuỗi THPT hiện đại.",
        "Một phần",
    )

    # Subjects and combos
    nat_counts = {s: latest_subjects[s]["count"] for s in ["VatLy", "HoaHoc", "SinhHoc"] if s in latest_subjects}
    soc_candidates = [s for s in ["LichSu", "DiaLy", "KinhTePhapLuat", "GDCD"] if s in latest_subjects]
    soc_counts = {s: latest_subjects[s]["count"] for s in soc_candidates}
    nat_top = max(nat_counts.items(), key=lambda x: x[1])
    soc_top = max(soc_counts.items(), key=lambda x: x[1])
    add(
        "Môn học và tổ hợp",
        "Trong nhóm tự nhiên năm gần nhất, môn nào có nhiều thí sinh nhất?",
        f"{subject_label(nat_top[0])} có nhiều lượt điểm nhất trong nhóm tự nhiên: {fmt_num(int(nat_top[1]))}.",
        "Đếm số lượt điểm hợp lệ theo môn năm 2026.",
    )
    add(
        "Môn học và tổ hợp",
        "Trong nhóm xã hội năm gần nhất, môn nào có nhiều thí sinh nhất?",
        f"{subject_label(soc_top[0])} có nhiều lượt điểm nhất trong nhóm xã hội: {fmt_num(int(soc_top[1]))}.",
        "Đếm số lượt điểm hợp lệ theo môn năm 2026.",
    )
    add(
        "Môn học và tổ hợp",
        "Xu hướng chọn tự nhiên hay xã hội thay đổi ra sao?",
        "Có thể theo dõi bằng số lượt dự thi từng môn, nhưng sau 2025 cấu trúc môn tự chọn đổi rõ nên cần tách giai đoạn 2017-2024 và 2025-2026 khi phân tích sâu.",
        "Dữ liệu có count theo môn/năm; diễn giải xu hướng phải tôn trọng thay đổi chương trình.",
        "Một phần",
    )
    add(
        "Môn học và tổ hợp",
        f"Tổ hợp nào có điểm trung bình cao nhất năm {latest_year}?",
        f"{combo_label(story['best_combo']['combo'])} cao nhất, mean {fmt_score(story['best_combo']['mean'])}, p90 {fmt_score(story['best_combo']['p90'])}.",
        "Dựa trên cột tổ hợp do nguồn tính sẵn, loại dòng không có điểm tổ hợp.",
    )
    for combo in ["KhoiA", "KhoiA1", "KhoiD", "KhoiC", "KhoiB"]:
        rows = sorted([r for r in story["combo_metrics"] if r["combo"] == combo], key=lambda r: r["year"])
        first = rows[0]
        last = rows[-1]
        add(
            "Môn học và tổ hợp",
            f"Điểm tổ hợp {combo_label(combo)} thay đổi thế nào?",
            f"{combo_label(combo)} đi từ mean {fmt_score(first['mean'])} năm {first['year']} đến {fmt_score(last['mean'])} năm {last['year']}; năm {latest_year} tỷ lệ >=27 là {fmt_pct(last['share_ge_27'])}.",
            "Dùng các cột tổ hợp đã có trong raw data.",
        )
    add(
        "Môn học và tổ hợp",
        f"Tổ hợp nào có tỷ lệ từ 27 điểm trở lên cao nhất năm {latest_year}?",
        f"{combo_label(story['best_combo_27']['combo'])} có tỷ lệ >=27 cao nhất: {fmt_pct(story['best_combo_27']['share_ge_27'])}.",
        "Đây là chỉ báo 'lạm phát điểm' theo tổ hợp, không phải xác suất đỗ.",
    )
    combo_threshold = "; ".join(f"{combo_label(row['combo'])}: {fmt_score(row['p90'])}" for row in story["latest_combo"][:5])
    add(
        "Môn học và tổ hợp",
        "Ngưỡng top 10% theo tổ hợp năm gần nhất là bao nhiêu?",
        f"Một vài ngưỡng p90 năm {latest_year}: {combo_threshold}.",
        "p90 nghĩa là khoảng 10% lượt tổ hợp hợp lệ cao hơn hoặc bằng mốc này.",
    )
    add(
        "Môn học và tổ hợp",
        "GDCD có phải 'môn cứu điểm' mọi năm không?",
        "Trong các năm có GDCD, môn này thường ở nhóm mean cao, nhưng từ 2025-2026 schema mới thay bằng Kinh tế và pháp luật cho nhóm CT2018; vì vậy nên nói 'nhóm môn công dân/pháp luật thường dễ kéo điểm' hơn là khẳng định mọi năm.",
        "Dựa trên mean môn theo năm và thay đổi schema 2025.",
        "Một phần",
    )
    add(
        "Môn học và tổ hợp",
        "Môn tự luận và trắc nghiệm khác nhau thế nào qua phổ điểm?",
        f"Năm {latest_year}, Ngữ văn mean {fmt_score(latest_subjects['NguVan']['mean'])}; Toán mean {fmt_score(latest_subjects['Toan']['mean'])}; Ngoại ngữ mean {fmt_score(latest_subjects['NgoaiNgu']['mean'])}. Khác biệt có thật trên phổ điểm, nhưng không chỉ do hình thức thi.",
        "Cần kiểm soát năng lực nhóm thí sinh và cấu trúc đề nếu muốn kết luận nguyên nhân.",
        "Một phần",
    )
    add(
        "Môn học và tổ hợp",
        "Môn nào dưới trung bình nhiều nhất ở năm gần nhất?",
        f"Năm {latest_year}, {story['low_heavy_latest']['subject_label']} có tỷ lệ <5 cao nhất: {fmt_pct(story['low_heavy_latest']['share_lt_5'])}.",
        "Tính theo lượt điểm hợp lệ từng môn.",
    )
    add(
        "Môn học và tổ hợp",
        "Ngoại ngữ đang cải thiện hay vẫn là nỗi ám ảnh?",
        f"Năm {latest_year}, Ngoại ngữ mean {fmt_score(latest_subjects['NgoaiNgu']['mean'])}, p90 {fmt_score(latest_subjects['NgoaiNgu']['p90'])}, tỷ lệ <5 là {fmt_pct(latest_subjects['NgoaiNgu']['share_lt_5'])}. Đây vẫn là môn phân hóa mạnh, không thể chỉ gọi là 'dễ'.",
        "Dựa trên mean, p90 và tỷ lệ dưới 5.",
    )

    # Applications
    thresholds = "; ".join(
        f"{row['subject_label']}: {fmt_score(row['p90'])}" for row in sorted(story["latest_subjects"], key=lambda r: r["p90"], reverse=True)[:6]
    )
    add(
        "Ứng dụng và ngưỡng điểm",
        f"Ngưỡng top 10% theo môn năm {latest_year} là gì?",
        f"Các mốc p90 cao nhất: {thresholds}.",
        "p90 tính từ phổ điểm theo từng môn.",
    )
    for subject in ["Toan", "NgoaiNgu"]:
        row = latest_subjects[subject]
        add(
            "Ứng dụng và ngưỡng điểm",
            f"Đạt 8 điểm {subject_label(subject)} năm {latest_year} thuộc nhóm nào?",
            f"Khoảng {fmt_pct(row['share_ge_8'])} lượt điểm {subject_label(subject)} đạt từ 8 trở lên; nói cách khác 8 điểm thuộc nhóm trên với độ hiếm như vậy.",
            "Tính trực tiếp từ share_ge_8.",
        )
    add(
        "Ứng dụng và ngưỡng điểm",
        "Môn nào phân hóa mạnh nhất năm gần nhất?",
        f"{story['highest_std_latest']['subject_label']} có độ lệch chuẩn cao nhất năm {latest_year}: {fmt_score(story['highest_std_latest']['std'])}.",
        "Độ lệch chuẩn cao thường cho thấy phổ điểm trải rộng hơn.",
    )
    add(
        "Ứng dụng và ngưỡng điểm",
        "Môn nào ít phân hóa nhất năm gần nhất?",
        f"{story['lowest_std_latest']['subject_label']} có độ lệch chuẩn thấp nhất năm {latest_year}: {fmt_score(story['lowest_std_latest']['std'])}.",
        "Độ lệch chuẩn thấp nghĩa là điểm tập trung hơn quanh trung bình.",
    )
    skewed = max(story["latest_subjects"], key=lambda r: abs(r["skew"] or 0))
    add(
        "Ứng dụng và ngưỡng điểm",
        "Môn nào có mean và median lệch nhau đáng chú ý nhất?",
        f"Năm {latest_year}, {skewed['subject_label']} có độ lệch/skew nổi bật nhất trong nhóm mới: skew {fmt_score(skewed['skew'])}.",
        "Skew tính từ phân phối điểm rời rạc.",
    )
    add(
        "Ứng dụng và ngưỡng điểm",
        "Nếu học mạnh Toán, nên nhìn tổ hợp nào trước?",
        f"Về mặt phổ điểm năm {latest_year}, {combo_label(story['best_combo']['combo'])} có mean cao nhất, còn {combo_label(story['best_combo_27']['combo'])} có tỷ lệ >=27 cao nhất. Chọn ngành vẫn cần điểm chuẩn thật, sở thích và môn mạnh cá nhân.",
        "Đây là gợi ý đọc phổ điểm, không phải tư vấn tuyển sinh cá nhân.",
        "Một phần",
    )
    add(
        "Ứng dụng và ngưỡng điểm",
        "Nếu mục tiêu 27+ thì tổ hợp nào 'dễ thở' hơn theo dữ liệu?",
        f"{combo_label(story['best_combo_27']['combo'])} có tỷ lệ >=27 cao nhất năm {latest_year}: {fmt_pct(story['best_combo_27']['share_ge_27'])}.",
        "Chỉ so trong nhóm thí sinh có đủ điểm tổ hợp.",
    )
    add(
        "Ứng dụng và ngưỡng điểm",
        "Nếu ở tỉnh có mặt bằng cao, mức cạnh tranh tham khảo là bao nhiêu?",
        f"Ở tỉnh/thành đứng đầu {latest_year} là {story['province_best']['province_name']}, mean tổng hợp đạt {fmt_score(story['province_best']['mean'])}. Khi làm bản tương tác, nên cho người dùng chọn tỉnh X để xem p50/p90 theo môn.",
        "Hiện web cung cấp bảng top và có thể mở rộng selector tỉnh.",
        "Một phần",
    )
    add(
        "Ứng dụng và ngưỡng điểm",
        "Năm gần nhất có bao nhiêu lượt điểm môn được dùng để phân tích?",
        f"Năm {latest_year} có {fmt_num(sum(int(row['count']) for row in story['latest_subjects']))} lượt điểm môn hợp lệ trên {len(story['latest_subjects'])} môn.",
        "Một thí sinh có nhiều lượt điểm môn, nên đây không phải số thí sinh.",
    )
    add(
        "Ứng dụng và ngưỡng điểm",
        "Môn nào cần cảnh báo rủi ro điểm liệt nhất năm gần nhất?",
        f"Năm {latest_year}, môn có tỷ lệ <=1 cao nhất là {max(story['latest_subjects'], key=lambda r: r['share_le_1'])['subject_label']}.",
        "Dựa trên ngưỡng <=1 điểm.",
    )
    # Correlations
    for left, right in [("Toan", "VatLy"), ("Toan", "HoaHoc"), ("NguVan", "LichSu"), ("NguVan", "DiaLy")]:
        row = corr[(left, right)]
        add(
            "Tương quan và thống kê sâu",
            f"{subject_label(left)} và {subject_label(right)} tương quan thế nào năm {latest_year}?",
            f"Hệ số Pearson là {fmt_score(row['pearson'], 3)} trên {fmt_num(int(row['n']))} thí sinh có đủ cả hai điểm.",
            "Pearson đo tương quan tuyến tính, không phải quan hệ nhân quả.",
        )
    side = "khối tự nhiên" if story["english_corr_side"]["natural"] > story["english_corr_side"]["social"] else "khối xã hội"
    add(
        "Tương quan và thống kê sâu",
        "Ngoại ngữ tương quan với khối tự nhiên hay xã hội hơn?",
        f"Năm {latest_year}, tương quan trung bình của Ngoại ngữ với {side} cao hơn: tự nhiên {fmt_score(story['english_corr_side']['natural'], 3)}, xã hội {fmt_score(story['english_corr_side']['social'], 3)}.",
        "So trung bình các Pearson theo cặp môn.",
    )
    top_ten_peer = story["perfect10"][0]
    add(
        "Tương quan và thống kê sâu",
        "Thí sinh điểm 10 một môn có học đều không?",
        f"Nhóm đạt 10 ở {top_ten_peer['subject_label']} có mean các lượt điểm môn khác cao nhất trong bảng perfect-10: {fmt_score(top_ten_peer['mean_other_scores'])}.",
        "Tính mean các môn khác trong năm 2026 cho từng nhóm đạt 10.",
    )
    low_ten_peer = story["perfect10"][-1]
    add(
        "Tương quan và thống kê sâu",
        "Có hiện tượng giỏi lệch một môn ở nhóm điểm 10 không?",
        f"Có thể có. Nhóm đạt 10 ở {low_ten_peer['subject_label']} có mean môn khác thấp nhất trong nhóm điểm 10: {fmt_score(low_ten_peer['mean_other_scores'])}.",
        "Cần xem thêm tổ hợp môn thí sinh chọn để kết luận sâu hơn.",
        "Một phần",
    )
    inverse = story["inverse_pair"]
    add(
        "Tương quan và thống kê sâu",
        "Có cặp môn nào biến động ngược chiều giữa các năm không?",
        f"Giai đoạn 2017-2024, cặp có tương quan mean năm thấp nhất là {subject_label(inverse['left'])} - {subject_label(inverse['right'])}: r={fmt_score(inverse['corr'], 3)}.",
        "Tính tương quan giữa chuỗi mean theo năm, không phải tương quan cá nhân.",
    )
    add(
        "Tương quan và thống kê sâu",
        "Phổ điểm nào gần hình chuông nhất?",
        f"Gần chuẩn nhất theo thước đo skew+kurtosis là {story['normal_closest']['subject_label']} năm {int(story['normal_closest']['year'])}.",
        "Thước đo đơn giản: |skew| + |excess kurtosis|.",
    )
    add(
        "Tương quan và thống kê sâu",
        "Phổ điểm nào lệch khỏi hình chuông nhất?",
        f"Lệch nhiều nhất theo cùng thước đo là {story['normal_farthest']['subject_label']} năm {int(story['normal_farthest']['year'])}.",
        "Không coi đây là kiểm định phân phối chuẩn chính thức.",
    )
    add(
        "Tương quan và thống kê sâu",
        "Môn nào có nhiều điểm thấp nhất trong lịch sử chuỗi?",
        f"Theo tỷ lệ <5, cực trị là {below5['subject_label']} năm {int(below5['year'])}: {fmt_pct(below5['share_lt_5'])}.",
        "Dùng tỷ lệ dưới trung bình như proxy cho 'lệch về điểm thấp'.",
    )
    add(
        "Tương quan và thống kê sâu",
        "Môn nào có đuôi điểm cao dày nhất năm gần nhất?",
        f"Năm {latest_year}, {max(story['latest_subjects'], key=lambda r: r['share_ge_9'])['subject_label']} có tỷ lệ >=9 cao nhất.",
        "Tỷ lệ >=9 đo đuôi phải của phổ điểm.",
    )
    add(
        "Tương quan và thống kê sâu",
        "Đề thi có đang phân hóa mạnh hơn không?",
        f"Nhìn từng môn thì không đồng loạt. Năm {latest_year}, môn phân hóa mạnh nhất là {story['highest_std_latest']['subject_label']} (std {fmt_score(story['highest_std_latest']['std'])}); cần đọc theo từng môn thay vì một kết luận chung.",
        "Dựa trên độ lệch chuẩn theo môn/năm.",
        "Một phần",
    )

    # Reform and data issues
    add(
        "Thời sự, cải cách và chất lượng dữ liệu",
        "Bước chuyển 2019 sang 2020 có làm mặt bằng điểm thay đổi không?",
        f"Có dấu hiệu tăng rõ: mean có trọng số toàn chuỗi tăng {fmt_score(story['macro_2019_2020_change'])} điểm từ 2019 sang 2020.",
        "Đây là mô tả dữ liệu, không tự chứng minh nguyên nhân do cấu trúc đề.",
    )
    add(
        "Thời sự, cải cách và chất lượng dữ liệu",
        "Cú đổi chương trình 2025-2026 ảnh hưởng thế nào?",
        f"Ảnh hưởng lớn nhất nằm ở schema môn: xuất hiện Kinh tế và pháp luật, Tin học, Công nghệ; một số môn cũ như GDCD không còn trực tiếp tương đương cho toàn bộ thí sinh CT2018.",
        "Dựa trên metadata/subjects.csv và raw schema 2025-2026.",
    )
    add(
        "Thời sự, cải cách và chất lượng dữ liệu",
        "Các môn mới 2025-2026 có đủ dữ liệu để phân tích không?",
        f"Có cho phân tích mô tả. Năm {latest_year}, Tin học có {fmt_num(int(latest_subjects['TinHoc']['count']))} lượt điểm; Kinh tế và pháp luật có {fmt_num(int(latest_subjects['KinhTePhapLuat']['count']))} lượt điểm.",
        "Dữ liệu mới chỉ có hai năm nên phân tích xu hướng dài hạn còn yếu.",
        "Một phần",
    )
    add(
        "Thời sự, cải cách và chất lượng dữ liệu",
        "Năm 2025 CT2018 và CT2006 có cần tách riêng không?",
        "Có. CT2018 chiếm phần lớn còn CT2006 là nhóm nhỏ hơn nhiều; gộp chung được cho tổng quan nhưng phân tích cải cách nên tách hai segment.",
        "processed_file_inventory.csv ghi CT2018 1.131.136 dòng và CT2006 22.090 dòng.",
    )
    add(
        "Thời sự, cải cách và chất lượng dữ liệu",
        "Đợt 2 năm 2020 có làm méo thống kê không?",
        "Đợt 2 Đà Nẵng có 10.857 dòng, nhỏ so với đợt chính 870.517 dòng; nên giữ lại để đủ dữ liệu nhưng có thể tách segment khi cần.",
        "Dựa trên processed_file_inventory.csv.",
    )
    add(
        "Thời sự, cải cách và chất lượng dữ liệu",
        "Đợt 2 năm 2021 có làm méo thống kê không?",
        "Đợt 2 năm 2021 có 12.086 dòng, nhỏ so với đợt chính 987.704 dòng; ảnh hưởng tổng thể hạn chế nhưng vẫn nên ghi provenance.",
        "Dựa trên processed_file_inventory.csv.",
    )
    seg = {row["segment"]: row for row in story["segment_2016_macro"]}
    add(
        "Thời sự, cải cách và chất lượng dữ liệu",
        "Cụm đại học và cụm địa phương năm 2016 khác nhau thế nào?",
        f"Năm 2016, cụm đại học mean tổng hợp khoảng {fmt_score(seg['university_cluster']['mean'])}, cụm địa phương khoảng {fmt_score(seg['local_cluster']['mean'])}.",
        "2016 có Tinh là mã cụm, không hoàn toàn tương đương mã tỉnh.",
    )
    add(
        "Thời sự, cải cách và chất lượng dữ liệu",
        "Có dữ liệu năm 2015 không?",
        "Chưa có trong nguồn canonical hiện tại, nên mọi biểu đồ thời gian phải ghi rõ khoảng trống 2015.",
        "metadata/gap_report.md xác nhận thiếu file raw 2015.",
        "Không đủ dữ liệu",
    )
    add(
        "Thời sự, cải cách và chất lượng dữ liệu",
        "Dữ liệu 2026 đã được đối chiếu độc lập chưa?",
        "Có. Repo lưu crosscheck với nguồn anhdung98: cùng 1.208.863 SBD và không có mismatch ở các cột điểm đã map.",
        "metadata/crosscheck_2026_anhdung98.csv.",
    )
    add(
        "Thời sự, cải cách và chất lượng dữ liệu",
        "Dữ liệu có phải sau phúc khảo không?",
        "Chưa thể khẳng định nhất quán cho toàn chuỗi; đa số nguồn công khai là snapshot công bố điểm, không có trường phúc khảo chuẩn hóa.",
        "Gap report ghi đây là vùng yếu cần bổ sung nguồn nếu phân tích pháp lí/chính sách.",
        "Không đủ dữ liệu",
    )

    # Fun and playful checks
    top_name = legacy["top_given_by_mean"][0]
    add(
        "Vui, bói toán có kiểm chứng",
        "Nếu hỏi vui 'tên nào thông minh nhất' theo điểm legacy thì tên nào đứng đầu?",
        f"Trong legacy 2013-2014, với ngưỡng tối thiểu 1.000 người, tên chính '{top_name['name']}' có mean tổng điểm cao nhất: {fmt_score(top_name['mean_total_score'])}. Đây chỉ là tương quan vui, tuyệt đối không phải nhân quả.",
        "Dựa trên data/analysis/legacy_2013_2014_features.csv; không dùng cho THPT 2016-2026 vì thiếu tên.",
    )
    top_valedictorian_names = ", ".join(
        f"{row['name']} ({int(row['near_valedictorian_count'])})"
        for row in legacy["top_given_by_valedictorian_count"][:5]
    )
    top_valedictorian_rate_names = ", ".join(
        f"{row['name']} ({fmt_pct(row['near_valedictorian_share'], 3)})"
        for row in legacy["top_given_by_valedictorian_share"][:5]
    )
    add(
        "Vui, bói toán có kiểm chứng",
        "Top 5 tên chính xuất hiện nhiều nhất trong nhóm thủ khoa/sát thủ khoa là gì?",
        f"Với ngưỡng >=29/30 điểm, top theo số lượng là: {top_valedictorian_names}. Nếu xếp theo tỷ lệ trong từng tên, top là: {top_valedictorian_rate_names}.",
        "Chỉ tính tên có ít nhất 1.000 bản ghi; ngưỡng >=29/30 có 245 thí sinh trong legacy sau khi lọc điểm hợp lệ.",
    )
    anh = legacy["anh_foreign_language"]
    diff_anh = anh["anh_mean_score_mon2"] - anh["other_mean_score_mon2"]
    add(
        "Vui, bói toán có kiểm chứng",
        "Bạn tên Anh có giỏi Ngoại ngữ hơn không?",
        f"Trong khối D legacy, thí sinh tên chính Anh có mean môn Ngoại ngữ {fmt_score(anh['anh_mean_score_mon2'])}, nhóm tên khác {fmt_score(anh['other_mean_score_mon2'])}; chênh {fmt_score(diff_anh)} điểm.",
        "Đùa chữ nhưng có kiểm chứng trên khối D 2013-2014.",
    )
    nguyen = legacy["nguyen_vs_other"]
    add(
        "Vui, bói toán có kiểm chứng",
        "Họ Nguyễn có điểm trung bình khác các họ khác không?",
        f"Họ Nguyễn mean tổng điểm {fmt_score(nguyen['nguyen_mean_total_score'])}; nhóm họ khác {fmt_score(nguyen['other_mean_total_score'])}; chênh {fmt_score(nguyen['nguyen_mean_total_score'] - nguyen['other_mean_total_score'])}.",
        "Chênh lệch nhỏ không nói lên nguyên nhân.",
    )
    best_month = max(legacy["birth_month"], key=lambda row: row["mean_total_score"])
    worst_month = min(legacy["birth_month"], key=lambda row: row["mean_total_score"])
    add(
        "Vui, bói toán có kiểm chứng",
        "Tháng sinh nào có mean tổng điểm cao nhất?",
        f"Trong legacy, tháng {int(best_month['birth_month'])} cao nhất với mean {fmt_score(best_month['mean_total_score'])}.",
        "Chỉ dùng bản ghi có ngày sinh parse hợp lệ.",
    )
    add(
        "Vui, bói toán có kiểm chứng",
        "Tháng sinh có tạo khác biệt lớn không?",
        f"Khoảng cách giữa tháng cao nhất ({int(best_month['birth_month'])}) và thấp nhất ({int(worst_month['birth_month'])}) là {fmt_score(best_month['mean_total_score'] - worst_month['mean_total_score'])} điểm tổng 3 môn; khá nhỏ so với biến thiên cá nhân.",
        "Không đủ cơ sở để nói tháng sinh quyết định điểm.",
    )
    best_zodiac = max(legacy["zodiac"], key=lambda row: row["mean_total_score"])
    worst_zodiac = min(legacy["zodiac"], key=lambda row: row["mean_total_score"])
    add(
        "Vui, bói toán có kiểm chứng",
        "Cung hoàng đạo nào có mean cao nhất?",
        f"{best_zodiac['zodiac']} cao nhất trong legacy, mean {fmt_score(best_zodiac['mean_total_score'])}. Nhắc lại: đây là trò vui thống kê, không phải khoa học chiêm tinh.",
        "Suy ra từ ngày/tháng sinh parse hợp lệ 2013-2014.",
    )
    add(
        "Vui, bói toán có kiểm chứng",
        "Cung hoàng đạo có khác biệt đáng kể không?",
        f"Khoảng cách mean giữa cung cao nhất và thấp nhất là {fmt_score(best_zodiac['mean_total_score'] - worst_zodiac['mean_total_score'])} điểm tổng 3 môn; không đủ để tin vào 'cung học giỏi'.",
        "Không kiểm soát tỉnh, trường, khối thi, năm sinh.",
    )
    best_middle = max(legacy["middle_name_token_count"], key=lambda row: row["mean_total_score"])
    add(
        "Vui, bói toán có kiểm chứng",
        "Tên đệm dài hơn có điểm cao hơn không?",
        f"Nhóm có {int(best_middle['middle_name_token_count'])} token tên đệm có mean cao nhất ({fmt_score(best_middle['mean_total_score'])}), nhưng đây dễ là nhiễu văn hóa đặt tên hơn là tác động thật.",
        "Feature chỉ lưu số token tên đệm, không xuất bản tên đầy đủ.",
    )
    add(
        "Vui, bói toán có kiểm chứng",
        "Số báo danh có chữ số 'đẹp' thì điểm cao hơn không?",
        f"Hầu như không. Tương quan giữa tổng chữ số SBD và mean điểm cá nhân năm {latest_year} là {fmt_score(story['sbd_metrics']['digit_sum_corr'], 4)}.",
        "SBD là mã hành chính/kỹ thuật, không nên gán ý nghĩa phong thủy.",
    )
    lucky = story["sbd_metrics"]["groups"]
    add(
        "Vui, bói toán có kiểm chứng",
        "SBD chứa 68/86 có 'lộc phát' điểm số không?",
        f"Nhóm SBD chứa 68/86 có mean {fmt_score(lucky['contains_68_or_86']['mean_candidate_score'])}; toàn bộ thí sinh có mean {fmt_score(lucky['all_candidates']['mean_candidate_score'])}. Chênh lệch này không đáng để mê tín.",
        "Tính mean điểm cá nhân 2026 theo các môn có điểm.",
    )
    add(
        "Vui, bói toán có kiểm chứng",
        "Năm nào xứng biệt danh 'mưa điểm 10'?",
        f"Năm/môn xứng danh nhất là {int(ten['year'])} - {ten['subject_label']}, với {fmt_num(int(ten['count_10']))} điểm 10.",
        "Đặt biệt danh theo số lượng tuyệt đối điểm 10.",
    )
    add(
        "Vui, bói toán có kiểm chứng",
        "Tỉnh nào xứng danh 'thủ phủ Toán học' năm gần nhất?",
        f"{story['province_top_subjects']['Toan'][0]['province_name']} dẫn đầu Toán {latest_year}, mean {fmt_score(story['province_top_subjects']['Toan'][0]['mean'])}.",
        "Biệt danh vui dựa trên mean Toán cấp tỉnh.",
    )
    add(
        "Vui, bói toán có kiểm chứng",
        "Có tên nào 'nên tránh' khi đặt tên con không?",
        "Không. Bộ dữ liệu chỉ cho tương quan thô theo tên trong legacy 2013-2014; dùng để kể chuyện vui thì được, dùng để chọn/né tên thì không nghiêm túc.",
        "Thiếu thiết kế nhân quả và thiếu trường nền tảng gia đình/xã hội.",
        "Một phần",
    )
    add(
        "Vui, bói toán có kiểm chứng",
        "Nếu dự đoán vui năm sau, môn nào có khả năng tăng mean nhất?",
        f"Theo trend tuyến tính thô vài năm gần đây, {story['forecast_rise']['subject_label']} có slope dương cao nhất ({fmt_score(story['forecast_rise']['slope'], 3)} điểm/năm). Đây chỉ là dự báo vui.",
        "Không dùng để dự báo chính sách hoặc điểm chuẩn.",
        "Một phần",
    )
    # Ethics, scope, and product guidance
    add(
        "Phạm vi, đạo đức và sản phẩm",
        "Dữ liệu THPT 2016-2026 có họ tên và ngày sinh không?",
        "Không trong các bulk file đã rà. Họ tên/ngày sinh chỉ có ở legacy tuyển sinh ĐH-CĐ 2013-2014.",
        "metadata/gap_report.md và schema raw 2016-2026.",
        "Không đủ dữ liệu",
    )
    add(
        "Phạm vi, đạo đức và sản phẩm",
        "Có thể kết luận tên hoặc tháng sinh gây ra học giỏi không?",
        "Không. Các mục tên/tháng sinh chỉ là tương quan vui; muốn nói nhân quả cần kiểm soát tỉnh, trường, khối thi, nền tảng gia đình, cohort và nhiều biến nhiễu khác.",
        "Đây là cảnh báo phương pháp bắt buộc khi công bố phân tích định danh.",
        "Không đủ dữ liệu",
    )
    add(
        "Phạm vi, đạo đức và sản phẩm",
        "Những câu hỏi nào hiện chưa trả lời được tốt?",
        "Các câu về giới tính, thí sinh tự do, trường THPT, tỷ lệ tốt nghiệp, điểm chuẩn đại học/ngành cụ thể và phúc khảo chưa trả lời chắc bằng dữ liệu hiện có.",
        "Các trường đó không có hoặc không chuẩn hóa trong bộ bulk hiện tại.",
        "Không đủ dữ liệu",
    )
    add(
        "Phạm vi, đạo đức và sản phẩm",
        "Bộ dữ liệu hiện bao phủ bao nhiêu dòng?",
        "Repo có 10.865.001 dòng THPT canonical 2016-2026 và 2.412.155 dòng legacy 2013-2014, tổng 13.277.156 dòng canonical.",
        "metadata/dataset_manifest.csv và validation script.",
    )
    add(
        "Phạm vi, đạo đức và sản phẩm",
        "Mã tỉnh 2026 có so sánh trực tiếp với các năm cũ được không?",
        "Không nên so trực tiếp nếu chưa map lại theo sáp nhập. Web tách phân tích 2026 và dùng 2017-2024 cho trend tỉnh ổn định.",
        "2026 dùng danh sách 34 tỉnh/thành; 2002-2025 dùng mã cũ.",
        "Một phần",
    )
    add(
        "Phạm vi, đạo đức và sản phẩm",
        "101 câu hỏi có quá nhiều không?",
        "Không quá nhiều nếu xem là ngân hàng câu hỏi. Nhưng cho một bài viết/web chính, nên highlight khoảng 20 insight đầu và để 101 câu ở phần tra cứu/tải về.",
        "Thiết kế site dùng bộ lọc nhóm và trạng thái để tránh quá tải.",
    )
    add(
        "Phạm vi, đạo đức và sản phẩm",
        "Nếu chỉ chọn 20 câu nổi bật để truyền thông, nên chọn nhóm nào?",
        "Nên ưu tiên: xu hướng mean, năm khó/dễ, điểm 10, 8+, dưới 5, top tỉnh Toán/Văn/Ngoại ngữ, HN/HCM vs rest, tổ hợp 27+, p90 theo môn, tương quan Toán-Lý/Hóa, Ngoại ngữ, và 3-4 câu vui về tên/tháng sinh/SBD có cảnh báo nhân quả.",
        "Cân bằng nghiêm túc, hữu ích và vui; tránh biến câu vui thành kết luận định kiến.",
    )

    if len(questions) != 101:
        raise AssertionError(f"Expected 101 questions, built {len(questions)}")
    return questions


def write_markdown(questions: list[dict[str, Any]], story: dict[str, Any]) -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    lines.append("# 101 câu hỏi và câu trả lời phân tích điểm thi THPT")
    lines.append("")
    lines.append("Bộ câu hỏi này được xây dựng lại từ file `cau_hoi_phan_tich_diem_thpt.md`, theo tiêu chí: nhiều người quan tâm, hữu ích, vui vừa đủ, và có thể kiểm chứng tương đối bằng dữ liệu hiện có.")
    lines.append("")
    lines.append("## Cách đọc nhanh")
    lines.append("")
    lines.append(f"- Phạm vi THPT chính: 2016-2026, {fmt_num(10865001)} dòng canonical.")
    lines.append(f"- Legacy có họ tên/ngày sinh: 2013-2014, {fmt_num(2412155)} dòng.")
    lines.append("- Các câu về tên, tháng sinh, cung hoàng đạo chỉ là kiểm chứng vui trên legacy, không phải nhân quả.")
    lines.append("- Những câu thiếu biến quan trọng được đánh dấu `Không đủ dữ liệu` hoặc `Một phần` thay vì suy diễn.")
    lines.append("")
    lines.append("## Kết luận nổi bật")
    lines.append("")
    highlights = [
        f"Năm có mặt bằng điểm thấp nhất theo lượt điểm môn là {int(story['hardest']['year'])}; cao nhất là {int(story['easiest']['year'])}.",
        f"Môn tăng mạnh nhất theo mean đầu-cuối là {story['biggest_gain']['subject_label']}; giảm mạnh nhất là {story['biggest_drop']['subject_label']}.",
        f"Năm/môn có nhiều điểm 10 nhất là {int(story['top10_row']['year'])} - {story['top10_row']['subject_label']}.",
        f"Tỉnh/thành dẫn đầu mặt bằng điểm {story['latest_year']} là {story['province_best']['province_name']}.",
        f"Tổ hợp có mean cao nhất {story['latest_year']} là {combo_label(story['best_combo']['combo'])}.",
    ]
    for item in highlights:
        lines.append(f"- {item}")
    lines.append("")
    current_group = None
    for item in questions:
        if item["group"] != current_group:
            current_group = item["group"]
            lines.append(f"## {current_group}")
            lines.append("")
        lines.append(f"### {item['id']}. {item['question']}")
        lines.append("")
        lines.append(f"**Trạng thái:** {item['status']}")
        lines.append("")
        lines.append(f"**Trả lời:** {item['answer']}")
        lines.append("")
        lines.append(f"**Bằng chứng/cách tính:** {item['evidence']}")
        lines.append("")

    while lines and lines[-1] == "":
        lines.pop()
    report_path = DOCS_DIR / "101_CAU_HOI_VA_TRA_LOI_PHAN_TICH_DIEM_THPT.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    q_lines = ["# 101 câu hỏi phân tích điểm thi THPT", ""]
    for item in questions:
        q_lines.append(f"{item['id']}. {item['question']}")
    (DOCS_DIR / "101_CAU_HOI_PHAN_TICH_DIEM_THPT.md").write_text("\n".join(q_lines) + "\n", encoding="utf-8")


def write_site(report: dict[str, Any]) -> None:
    SITE_DIR.mkdir(parents=True, exist_ok=True)
    (SITE_DIR / "assets").mkdir(exist_ok=True)
    (SITE_DIR / "data").mkdir(exist_ok=True)
    (SITE_DIR / "downloads").mkdir(exist_ok=True)

    (SITE_DIR / "data" / "answers.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False),
        encoding="utf-8",
    )
    shutil.copyfile(
        DOCS_DIR / "101_CAU_HOI_VA_TRA_LOI_PHAN_TICH_DIEM_THPT.md",
        SITE_DIR / "downloads" / "101-cau-hoi-va-tra-loi-phan-tich-diem-thpt.md",
    )
    shutil.copyfile(
        DOCS_DIR / "101_CAU_HOI_PHAN_TICH_DIEM_THPT.md",
        SITE_DIR / "downloads" / "101-cau-hoi-phan-tich-diem-thpt.md",
    )

    html = """<!doctype html>
<html lang="vi">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>101 câu hỏi điểm thi THPT</title>
  <meta name="description" content="Báo cáo tĩnh: 101 câu hỏi và câu trả lời phân tích điểm thi THPT qua các năm.">
  <link rel="stylesheet" href="assets/styles.css?v=20260705">
</head>
<body>
  <header class="topbar">
    <div>
      <p class="eyebrow">Phổ điểm THPT 2016-2026 + legacy 2013-2014</p>
      <h1>101 câu hỏi phân tích điểm thi THPT</h1>
      <p class="lede">Một báo cáo tối giản: có câu nghiêm túc, câu hữu ích, câu vui kiểu bói toán, nhưng câu nào cũng ghi rõ dữ liệu có chứng minh được đến đâu.</p>
    </div>
    <nav class="downloads" aria-label="Tải xuống">
      <a href="downloads/101-cau-hoi-va-tra-loi-phan-tich-diem-thpt.md" download>Tải Markdown đầy đủ</a>
      <a href="downloads/101-cau-hoi-phan-tich-diem-thpt.md" download>Chỉ câu hỏi</a>
      <a href="data/answers.json">JSON</a>
    </nav>
  </header>

  <main>
    <section class="kpis" id="kpis" aria-label="Tóm tắt số liệu"></section>

    <section class="chart-grid" aria-label="Biểu đồ chính">
      <article class="panel">
        <div class="panel-head">
          <h2>Mean theo năm</h2>
          <p>Trung bình có trọng số trên lượt điểm môn.</p>
        </div>
        <div id="annualChart" class="chart"></div>
      </article>
      <article class="panel">
        <div class="panel-head">
          <h2>Môn năm gần nhất</h2>
          <p>Mean và tỷ lệ 8+ theo môn.</p>
        </div>
        <div id="subjectChart" class="chart"></div>
      </article>
    </section>

    <section class="toolbar" aria-label="Bộ lọc câu hỏi">
      <label>
        <span>Tìm kiếm</span>
        <input id="searchBox" type="search" placeholder="Ví dụ: Ngoại ngữ, tên, Hà Nội, 27+">
      </label>
      <label>
        <span>Nhóm</span>
        <select id="groupFilter">
          <option value="">Tất cả nhóm</option>
        </select>
      </label>
      <label>
        <span>Trạng thái</span>
        <select id="statusFilter">
          <option value="">Tất cả trạng thái</option>
        </select>
      </label>
    </section>

    <section class="content-layout">
      <aside class="insights">
        <h2>Điểm nhấn</h2>
        <ul id="highlights"></ul>
      </aside>
      <section>
        <div class="section-title">
          <h2>Toàn bộ 101 câu</h2>
          <p id="resultCount"></p>
        </div>
        <div id="questionList" class="question-list"></div>
      </section>
    </section>
  </main>

  <footer>
    <p>Dữ liệu định danh chỉ dùng ở dạng tổng hợp. Các câu vui về tên, tháng sinh, cung hoàng đạo không phải kết luận nhân quả.</p>
  </footer>
  <script src="assets/app.js?v=20260705"></script>
</body>
</html>
"""
    (SITE_DIR / "index.html").write_text(html, encoding="utf-8")

    css = """:root {
  color-scheme: light;
  --bg: #f7f8fa;
  --paper: #ffffff;
  --ink: #17202a;
  --muted: #5b6573;
  --line: #d9dee7;
  --accent: #0e7c86;
  --accent-2: #bc5b33;
  --good: #1f7a4d;
  --warn: #a46500;
  --bad: #9b2d2d;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  background: var(--bg);
  color: var(--ink);
  line-height: 1.55;
}

a { color: inherit; }

.topbar {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 24px;
  align-items: end;
  padding: 32px clamp(18px, 4vw, 56px) 24px;
  border-bottom: 1px solid var(--line);
  background: var(--paper);
}

.eyebrow {
  margin: 0 0 8px;
  color: var(--accent);
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
}

h1, h2, h3, p { margin-top: 0; }

h1 {
  margin-bottom: 10px;
  font-size: clamp(28px, 4vw, 48px);
  line-height: 1.05;
  letter-spacing: 0;
}

h2 { font-size: 20px; line-height: 1.2; }
h3 { font-size: 16px; line-height: 1.35; }

.lede {
  max-width: 850px;
  margin-bottom: 0;
  color: var(--muted);
  font-size: 17px;
}

.downloads {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: flex-end;
}

.downloads a,
.toolbar select,
.toolbar input {
  min-height: 38px;
  border: 1px solid var(--line);
  border-radius: 6px;
  background: var(--paper);
  color: var(--ink);
}

.downloads a {
  display: inline-flex;
  align-items: center;
  padding: 8px 12px;
  text-decoration: none;
  font-weight: 650;
}

main {
  width: min(1280px, 100%);
  margin: 0 auto;
  padding: 22px clamp(14px, 3vw, 32px) 36px;
}

.kpis {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 16px;
}

.kpi, .panel, .insights, .question-card {
  background: var(--paper);
  border: 1px solid var(--line);
  border-radius: 8px;
}

.kpi {
  padding: 16px;
  min-height: 112px;
}

.kpi strong {
  display: block;
  font-size: 24px;
  line-height: 1.1;
}

.kpi span {
  display: block;
  margin-top: 8px;
  color: var(--muted);
  font-size: 13px;
}

.chart-grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 16px;
}

.panel {
  padding: 16px;
}

.panel-head {
  display: flex;
  justify-content: space-between;
  gap: 16px;
  align-items: start;
}

.panel-head p {
  max-width: 320px;
  margin-bottom: 0;
  color: var(--muted);
  font-size: 13px;
}

.chart {
  min-height: 280px;
  overflow-x: auto;
}

.chart svg {
  display: block;
  width: 100%;
  min-width: 420px;
  height: 280px;
}

.toolbar {
  display: grid;
  grid-template-columns: minmax(240px, 1fr) 220px 180px;
  gap: 12px;
  margin: 16px 0;
  padding: 12px;
  background: #eef2f5;
  border: 1px solid var(--line);
  border-radius: 8px;
}

.toolbar label {
  display: grid;
  gap: 6px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 700;
}

.toolbar input,
.toolbar select {
  width: 100%;
  padding: 8px 10px;
  font: inherit;
}

.content-layout {
  display: grid;
  grid-template-columns: 290px minmax(0, 1fr);
  gap: 16px;
  align-items: start;
}

.insights {
  position: sticky;
  top: 12px;
  padding: 16px;
}

.insights ul {
  padding-left: 18px;
  margin-bottom: 0;
}

.insights li {
  margin-bottom: 10px;
  color: var(--muted);
}

.section-title {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 12px;
}

.section-title p {
  color: var(--muted);
}

.question-list {
  display: grid;
  gap: 10px;
}

.question-card {
  padding: 16px;
}

.question-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
  color: var(--muted);
  font-size: 12px;
  font-weight: 700;
}

.pill {
  display: inline-flex;
  align-items: center;
  min-height: 24px;
  padding: 3px 8px;
  border-radius: 999px;
  background: #eef2f5;
}

.pill.ok { color: var(--good); background: #e9f5ee; }
.pill.partial { color: var(--warn); background: #fff3d8; }
.pill.missing { color: var(--bad); background: #fdecec; }

.question-card h3 {
  margin-bottom: 10px;
}

.answer {
  margin-bottom: 10px;
}

.evidence {
  margin-bottom: 0;
  color: var(--muted);
  font-size: 13px;
}

footer {
  padding: 18px clamp(18px, 4vw, 56px) 30px;
  border-top: 1px solid var(--line);
  color: var(--muted);
  background: var(--paper);
}

footer p { margin-bottom: 0; }

@media (max-width: 900px) {
  .topbar,
  .chart-grid,
  .content-layout,
  .toolbar,
  .kpis {
    grid-template-columns: 1fr;
  }

  .downloads { justify-content: flex-start; }
  .insights { position: static; }
  .section-title { display: block; }
  .chart svg { min-width: 0 !important; }
  .downloads a { max-width: 100%; }
}
"""
    (SITE_DIR / "assets" / "styles.css").write_text(css, encoding="utf-8")

    js = """const state = {
  data: null,
  group: "",
  status: "",
  search: ""
};

const fmt = new Intl.NumberFormat("vi-VN", { maximumFractionDigits: 2 });

function statusClass(status) {
  if (status === "Trả lời được") return "ok";
  if (status === "Một phần") return "partial";
  return "missing";
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function renderKpis(data) {
  const items = [
    ["10,865,001", "Dòng THPT canonical 2016-2026"],
    ["2,412,155", "Dòng legacy có tên/ngày sinh 2013-2014"],
    [String(data.questions.length), "Câu hỏi đã trả lời và gắn trạng thái"],
    [String(data.story.latest_year), "Năm mới nhất trong bộ phân tích"]
  ];
  document.querySelector("#kpis").innerHTML = items.map(([value, label]) => `
    <article class="kpi"><strong>${value}</strong><span>${label}</span></article>
  `).join("");
}

function lineChart(el, rows) {
  const width = 640, height = 280, pad = 34;
  const xs = rows.map(d => d.year);
  const ys = rows.map(d => d.weighted_mean);
  const minX = Math.min(...xs), maxX = Math.max(...xs);
  const minY = Math.min(...ys) - 0.15, maxY = Math.max(...ys) + 0.15;
  const x = year => pad + ((year - minX) / Math.max(maxX - minX, 1)) * (width - pad * 2);
  const y = value => height - pad - ((value - minY) / Math.max(maxY - minY, 1)) * (height - pad * 2);
  const points = rows.map(d => `${x(d.year)},${y(d.weighted_mean)}`).join(" ");
  const labels = rows.map(d => `<text x="${x(d.year)}" y="${height - 10}" text-anchor="middle" font-size="10" fill="#5b6573">${d.year}</text>`).join("");
  const dots = rows.map(d => `<circle cx="${x(d.year)}" cy="${y(d.weighted_mean)}" r="3.5"><title>${d.year}: ${fmt.format(d.weighted_mean)}</title></circle>`).join("");
  el.innerHTML = `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Mean theo năm">
    <line x1="${pad}" y1="${height-pad}" x2="${width-pad}" y2="${height-pad}" stroke="#d9dee7"/>
    <line x1="${pad}" y1="${pad}" x2="${pad}" y2="${height-pad}" stroke="#d9dee7"/>
    <polyline points="${points}" fill="none" stroke="#0e7c86" stroke-width="3"/>
    <g fill="#0e7c86">${dots}</g>
    ${labels}
  </svg>`;
}

function barChart(el, rows) {
  const data = rows.slice().sort((a, b) => b.mean - a.mean);
  const width = 640, height = 280, pad = 34;
  const max = Math.max(...data.map(d => d.mean));
  const barW = (width - pad * 2) / data.length - 5;
  const bars = data.map((d, i) => {
    const x = pad + i * ((width - pad * 2) / data.length);
    const h = (d.mean / max) * (height - pad * 2);
    const y = height - pad - h;
    const label = d.subject_label.length > 11 ? d.subject_label.slice(0, 10) + "." : d.subject_label;
    return `<g>
      <rect x="${x}" y="${y}" width="${barW}" height="${h}" rx="3" fill="#bc5b33"><title>${escapeHtml(d.subject_label)}: ${fmt.format(d.mean)}</title></rect>
      <text transform="translate(${x + barW / 2},${height - 8}) rotate(-35)" text-anchor="end" font-size="10" fill="#5b6573">${escapeHtml(label)}</text>
    </g>`;
  }).join("");
  el.innerHTML = `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="Mean theo môn năm gần nhất">
    <line x1="${pad}" y1="${height-pad}" x2="${width-pad}" y2="${height-pad}" stroke="#d9dee7"/>
    ${bars}
  </svg>`;
}

function renderFilters(data) {
  const groups = [...new Set(data.questions.map(q => q.group))];
  const statuses = [...new Set(data.questions.map(q => q.status))];
  document.querySelector("#groupFilter").innerHTML += groups.map(g => `<option value="${escapeHtml(g)}">${escapeHtml(g)}</option>`).join("");
  document.querySelector("#statusFilter").innerHTML += statuses.map(s => `<option value="${escapeHtml(s)}">${escapeHtml(s)}</option>`).join("");
}

function renderHighlights(data) {
  document.querySelector("#highlights").innerHTML = data.highlights.map(item => `<li>${escapeHtml(item)}</li>`).join("");
}

function renderQuestions() {
  const query = state.search.trim().toLowerCase();
  const rows = state.data.questions.filter(q => {
    const matchesGroup = !state.group || q.group === state.group;
    const matchesStatus = !state.status || q.status === state.status;
    const haystack = `${q.question} ${q.answer} ${q.evidence} ${q.group}`.toLowerCase();
    const matchesSearch = !query || haystack.includes(query);
    return matchesGroup && matchesStatus && matchesSearch;
  });
  document.querySelector("#resultCount").textContent = `${rows.length} câu đang hiển thị`;
  document.querySelector("#questionList").innerHTML = rows.map(q => `
    <article class="question-card">
      <div class="question-meta">
        <span class="pill">#${q.id}</span>
        <span class="pill">${escapeHtml(q.group)}</span>
        <span class="pill ${statusClass(q.status)}">${escapeHtml(q.status)}</span>
      </div>
      <h3>${escapeHtml(q.question)}</h3>
      <p class="answer">${escapeHtml(q.answer)}</p>
      <p class="evidence">${escapeHtml(q.evidence)}</p>
    </article>
  `).join("");
}

fetch("data/answers.json")
  .then(response => response.json())
  .then(data => {
    state.data = data;
    renderKpis(data);
    renderFilters(data);
    renderHighlights(data);
    lineChart(document.querySelector("#annualChart"), data.charts.annual);
    barChart(document.querySelector("#subjectChart"), data.charts.latest_subjects);
    renderQuestions();
  });

document.querySelector("#searchBox").addEventListener("input", event => {
  state.search = event.target.value;
  renderQuestions();
});
document.querySelector("#groupFilter").addEventListener("change", event => {
  state.group = event.target.value;
  renderQuestions();
});
document.querySelector("#statusFilter").addEventListener("change", event => {
  state.status = event.target.value;
  renderQuestions();
});
"""
    (SITE_DIR / "assets" / "app.js").write_text(js, encoding="utf-8")


def json_ready(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): json_ready(item) for key, item in value.items()}
    if isinstance(value, list):
        return [json_ready(item) for item in value]
    if isinstance(value, tuple):
        return [json_ready(item) for item in value]
    if hasattr(value, "item"):
        try:
            return json_ready(value.item())
        except (TypeError, ValueError):
            pass
    if isinstance(value, float) and math.isnan(value):
        return None
    return value


def build_report() -> dict[str, Any]:
    subject_metrics, _metric_map = build_subject_metrics()
    segment_metrics = build_segment_metrics()
    province_metrics = build_province_metrics()
    combo_metrics = build_combo_metrics()
    correlations, perfect10, sbd_metrics = build_correlations_2026()
    legacy = build_legacy_fun_metrics()
    story = compute_story(subject_metrics, segment_metrics, province_metrics, combo_metrics, correlations, perfect10, sbd_metrics, legacy)
    story["subject_chart"] = subject_metrics.to_dict("records")
    questions = build_questions(story)

    highlights = [
        f"{int(story['hardest']['year'])} là năm có mặt bằng điểm thấp nhất trong chuỗi; {int(story['easiest']['year'])} là năm cao nhất theo mean có trọng số.",
        f"{story['top10_row']['subject_label']} năm {int(story['top10_row']['year'])} là kỷ lục điểm 10: {fmt_num(int(story['top10_row']['count_10']))} lượt.",
        f"{story['province_best']['province_name']} dẫn đầu mặt bằng điểm {story['latest_year']}; {story['province_surprise']['province_name']} là cái tên nổi bật nếu bỏ Hà Nội/TP.HCM.",
        f"Tổ hợp {combo_label(story['best_combo']['combo'])} có mean cao nhất năm {story['latest_year']}; {combo_label(story['best_combo_27']['combo'])} dẫn tỷ lệ >=27.",
        "Tên, tháng sinh, cung hoàng đạo và SBD chỉ nên đọc như trò vui có kiểm chứng, không phải nguyên nhân học giỏi.",
    ]

    compact_story = {
        "latest_year": story["latest_year"],
        "hardest": story["hardest"],
        "easiest": story["easiest"],
        "province_best": story["province_best"],
        "province_worst": story["province_worst"],
        "best_combo": story["best_combo"],
    }
    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "source_scope": {
            "thpt_years": "2016-2026",
            "legacy_years": "2013-2014",
            "thpt_rows": 10865001,
            "legacy_rows": 2412155,
        },
        "highlights": highlights,
        "story": compact_story,
        "charts": {
            "annual": story["annual"],
            "latest_subjects": story["latest_subjects"],
            "latest_combo": story["latest_combo"],
            "province_overall_latest": story["province_overall_latest"][:20],
            "correlations": story["correlations"],
            "birth_month": legacy["birth_month"],
        },
        "questions": questions,
    }
    report = json_ready(report)
    (ANALYSIS_DIR / "qa_report_data.json").write_text(json.dumps(report, ensure_ascii=False, indent=2, allow_nan=False), encoding="utf-8")
    write_markdown(questions, story)
    write_site(report)
    return report


def main() -> None:
    report = build_report()
    print(f"Built {len(report['questions'])} questions")
    print("Wrote docs/101_CAU_HOI_VA_TRA_LOI_PHAN_TICH_DIEM_THPT.md")
    print("Wrote site/index.html")


if __name__ == "__main__":
    main()
