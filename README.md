# Phổ điểm các năm

Kho dữ liệu và script phân tích điểm thi tại Việt Nam, tập trung vào dữ liệu thí sinh kỳ thi THPT quốc gia/tốt nghiệp THPT qua các năm, kèm dữ liệu legacy tuyển sinh ĐH-CĐ 2013-2014.

Repo này được chuẩn hóa để:

- giữ nguồn raw rõ ràng, có provenance;
- tạo các bảng phân tích nhỏ, dễ dùng;
- tránh đếm trùng file aggregate;
- ghi rõ phần nào có/không có trường định danh như họ tên, ngày sinh;
- hỗ trợ kiểm chứng lại bằng script.

## Web tĩnh

Web báo cáo 101 câu hỏi được dựng trong thư mục `site/` và deploy bằng GitHub Pages:

- Trang web: https://nhanaz.github.io/pho-diem-cac-nam/
- Bản Markdown đầy đủ: [101 câu hỏi và câu trả lời](docs/101_CAU_HOI_VA_TRA_LOI_PHAN_TICH_DIEM_THPT.md)
- Bản chỉ câu hỏi: [101 câu hỏi phân tích](docs/101_CAU_HOI_PHAN_TICH_DIEM_THPT.md)

## Trạng thái dữ liệu

- Legacy tuyển sinh ĐH-CĐ 2013-2014: **2,412,155** dòng.
- THPT/THPT quốc gia/tốt nghiệp THPT canonical 2016-2026: **10,865,001** dòng.
- Tổng canonical cả legacy và THPT: **13,277,156** dòng.
- Năm 2026 đã đối chiếu với nguồn độc lập `anhdung98/diem_thi_2026`: cùng SBD và không lệch điểm ở các cột đã map.
- Năm 2025 đã tải bản XLSX từ Báo Chính phủ/Cổng TTĐT Chính phủ để đối chiếu số dòng CT2018/CT2006.

## Cấu trúc repo

```text
.
├── data/
│   ├── analysis/   # bảng phân tích sinh ra từ raw data
│   └── summary/    # phổ điểm và thống kê gọn theo môn/năm
├── docs/           # tài liệu tiếng Việt
├── metadata/       # manifest, registry nguồn, gap report, mã tỉnh/môn
├── scripts/        # script build/validate
└── sources/
    ├── du-lieu-diem-thi/   # raw data chính, dạng git submodule
    └── crosscheck/         # nguồn tải về để đối chiếu
```

`sources/du-lieu-diem-thi` là submodule trỏ tới `https://github.com/sdgedfegw/du-lieu-diem-thi` tại commit `1178a012c8af3f07f7d40c614dc61fb342687e46`.

## Clone lại repo

```powershell
git clone --recurse-submodules <repo-url>
cd pho-diem-cac-nam
git lfs pull
```

Nếu đã clone mà thiếu submodule:

```powershell
git submodule update --init --recursive
git lfs pull
```

## Cài phụ thuộc

```powershell
python -m pip install -r requirements.txt
```

## Build lại bảng phân tích

```powershell
python scripts\build_subject_summaries.py
python scripts\build_legacy_features.py
python scripts\build_qa_site_data.py
python scripts\validate_repo.py
```

Kết quả chính:

- `data/summary/subject_score_distribution.csv`: phổ điểm theo `year, subject, score, count`.
- `data/summary/year_subject_stats.csv`: thống kê count/mean/std/percentile theo môn/năm.
- `data/analysis/legacy_2013_2014_features.csv`: biến phân tích từ legacy 2013-2014, gồm tháng sinh, họ, tên chính, mã trường/khối và điểm.
- `data/analysis/legacy_name_score_stats.csv`: thống kê điểm theo họ/tên chính, chỉ giữ nhóm có ít nhất 30 bản ghi.
- `data/analysis/legacy_birth_month_score_stats.csv`: thống kê điểm theo tháng sinh.
- `data/analysis/qa_report_data.json`: dữ liệu đã đóng gói cho báo cáo 101 câu.
- `site/`: web tĩnh để deploy GitHub Pages.

## Tài liệu

- [Nguồn dữ liệu](docs/NGUON_DU_LIEU.md)
- [Từ điển dữ liệu](docs/TU_DIEN_DU_LIEU.md)
- [Quyền riêng tư và giới hạn phân tích](docs/QUYEN_RIENG_TU.md)
- [101 câu hỏi và câu trả lời phân tích điểm THPT](docs/101_CAU_HOI_VA_TRA_LOI_PHAN_TICH_DIEM_THPT.md)
- [Gap report](metadata/gap_report.md)

## Lưu ý quan trọng

- File `du_lieu_diem_thi_2016-2025.csv` trong nguồn raw là file aggregate tiện ích, không dùng khi tạo summary để tránh đếm trùng.
- Dữ liệu 2013-2014 có `HovaTen` và `NgaySinh`; raw data giữ nguyên trong submodule, còn output phân tích không chứa full name/ngày sinh đầy đủ.
- Một phần tên legacy bị lỗi font TCVN3; `scripts/build_legacy_features.py` chuẩn hóa tên/tokens sang Unicode trong bảng feature và đánh dấu bằng cột `name_font_fixed`.
- Dữ liệu bulk 2016-2026 đã rà hiện không có họ tên/ngày sinh. Không nên suy đoán tháng sinh/tên từ SBD.
- Các phân tích tên/tháng sinh chỉ nên xem là tương quan, không đủ để kết luận nhân quả nếu chưa có thiết kế kiểm soát nhiễu.
