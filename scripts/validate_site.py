#!/usr/bin/env python
"""Validate the generated static report without requiring raw/LFS data."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DOCS = ROOT / "docs"
ANALYSIS = ROOT / "data" / "analysis"


def assert_exists(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(path)


def main() -> None:
    required = [
        SITE / "index.html",
        SITE / "assets" / "styles.css",
        SITE / "assets" / "app.js",
        SITE / "data" / "answers.json",
        SITE / "downloads" / "101-cau-hoi-va-tra-loi-phan-tich-diem-thpt.md",
        SITE / "downloads" / "101-cau-hoi-phan-tich-diem-thpt.md",
        DOCS / "101_CAU_HOI_VA_TRA_LOI_PHAN_TICH_DIEM_THPT.md",
        DOCS / "101_CAU_HOI_PHAN_TICH_DIEM_THPT.md",
        ANALYSIS / "qa_report_data.json",
    ]
    for path in required:
        assert_exists(path)

    data = json.loads((SITE / "data" / "answers.json").read_text(encoding="utf-8"))
    questions = data.get("questions", [])
    if len(questions) != 101:
        raise AssertionError(f"Expected 101 questions, got {len(questions)}")

    ids = [item.get("id") for item in questions]
    if ids != list(range(1, 102)):
        raise AssertionError("Question ids are not contiguous from 1 to 101")

    statuses = {item.get("status") for item in questions}
    expected_statuses = {"Trả lời được", "Một phần", "Không đủ dữ liệu"}
    if not statuses.issubset(expected_statuses):
        raise AssertionError(f"Unexpected statuses: {statuses - expected_statuses}")
    if not expected_statuses.issubset(statuses):
        raise AssertionError(f"Missing expected status groups: {expected_statuses - statuses}")

    groups = {item.get("group") for item in questions}
    if len(groups) < 6:
        raise AssertionError("Question bank is missing expected thematic groups")

    for item in questions:
        for key in ["question", "answer", "evidence", "group", "status"]:
            if not str(item.get(key, "")).strip():
                raise AssertionError(f"Question {item.get('id')} has an empty {key}")

    report_text = (DOCS / "101_CAU_HOI_VA_TRA_LOI_PHAN_TICH_DIEM_THPT.md").read_text(encoding="utf-8")
    if report_text.count("\n### ") != 101:
        raise AssertionError("Markdown report does not contain 101 question headings")

    html = (SITE / "index.html").read_text(encoding="utf-8")
    for needle in ["assets/styles.css", "assets/app.js", "data/answers.json", "Tải Markdown đầy đủ"]:
        if needle not in html:
            raise AssertionError(f"Missing {needle} in site/index.html")

    print("OK site report: 101 questions, markdown downloads, JSON, and assets are present")


if __name__ == "__main__":
    main()
