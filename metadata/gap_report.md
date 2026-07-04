# Gap report

## What is currently complete enough for score analysis

- THPT/tốt nghiệp THPT score-level data is locally available for 2016-2026, with 10,865,001 canonical rows.
- 2026 was cross-checked against an independent `anhdung98/diem_thi_2026` release. The SBD set and compared score/language fields match exactly.
- 2025 official Government portal workbooks were downloaded for CT2018 and CT2006. Their row counts match the canonical 2025 CSV files: 1,131,136 CT2018 rows and 22,090 CT2006 rows.

## Where detailed identity fields exist

- The local 2013-2014 legacy university/college entrance dataset includes `HovaTen` and `NgaySinh`.
- The 2016-2026 THPT score datasets checked so far expose SBD, province/exam code, subjects, and scores, but do not expose names or dates of birth as reusable bulk fields.

## Important missing or weak areas

- No 2015 raw file is present in the current canonical source.
- For 2016-2026, birth month/date and name are not present in the bulk datasets reviewed. Inferring these from SBD or score pages would be speculative unless a source explicitly publishes them.
- Province codes are not perfectly stable across all years. 2026 uses the post-reorganization 34-province list, while earlier years use the older 63/64-code scheme.
- Post-phúc-khảo scores are not consistently available in the public raw data sources reviewed; most releases explicitly state they are pre- or non-phúc-khảo snapshots.
- Cổng tra cứu by SBD is useful for spot-checking, but it is not a clean bulk source and may include captcha/rate limits/terms restrictions.

## Causality warning

Name and birth-month analyses can show associations, not causal effects by themselves. To make causal claims, you would need a credible design: controls for province/year/school/exam block, cohort effects, family and socioeconomic confounding, and a defensible identification strategy. The feature tables here are built to support exploratory analysis and hypothesis generation first.

## Privacy handling

The raw source retains the original 2013-2014 identity fields. Derived outputs in `data/analysis` avoid full names and exact birth dates by default, using birth month/year and name parts or aggregate statistics instead. Do not publish row-level identity data without a separate legal/ethical review.

## Legacy name cleaning

Some 2013-2014 names are encoded with TCVN3-style legacy characters. `scripts/build_legacy_features.py` normalizes detected TCVN3 names/tokens to Unicode in the derived feature outputs while leaving the raw source unchanged. The output column `name_font_fixed` marks rows where a name or name token was converted.
