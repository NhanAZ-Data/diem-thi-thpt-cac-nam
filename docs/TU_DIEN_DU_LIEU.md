# Từ điển dữ liệu

## Nhóm THPT 2016-2026

Các cột phổ biến:

- `SBD`: số báo danh.
- `Nam`: năm thi dạng hai chữ số trong raw, ví dụ `24`, `25`, `26`.
- `Tinh`: mã hội đồng/tỉnh/thành theo từng giai đoạn.
- `Toan`, `NguVan`, `VatLy`, `HoaHoc`, `SinhHoc`, `LichSu`, `DiaLy`, `NgoaiNgu`: điểm môn.
- `GDCD`: giáo dục công dân, chủ yếu trong schema GDPT 2006.
- `KinhTePhapLuat`, `TinHoc`, `CongNgheCongNghiep`, `CongNgheNongNghiep`: các môn trong schema mới 2025-2026.
- `MaMonNgoaiNgu`: mã ngoại ngữ, ví dụ `N1` là tiếng Anh.
- `KhoiA`, `KhoiA1`, `KhoiB`, `KhoiC`, `KhoiD`, `KhoiA02`, `KhoiC01`, `KhoiD07`: tổ hợp điểm tính sẵn từ nguồn.
- `KHTN`, `KHXH`, `TongDiemKHTN`, `TongDiemKHXH`: các cột tổng/điểm trung bình theo bài tổ hợp ở giai đoạn phù hợp.

Danh sách mô tả ngắn nằm ở `metadata/subjects.csv`.

## Nhóm legacy 2013-2014

Raw source có:

- `Nam`: `13` hoặc `14`.
- `Tinh`: mã tỉnh/thành hoặc để trống tùy dòng.
- `KyThi`: `DH` hoặc `CD`.
- `DH`: mã trường.
- `Khoi`: mã khối thi.
- `SBD`: số báo danh.
- `HovaTen`: họ và tên thí sinh.
- `NgaySinh`: dạng `ddmmyy`, `000000` là trống.
- `Mon1`, `Mon2`, `Mon3`, `TongDiem`: điểm dạng số nguyên, ví dụ `775` tương ứng `7.75`.

Feature output tại `data/analysis/legacy_2013_2014_features.csv` tách ra:

- `family_name`: họ.
- `given_name`: tên chính.
- `middle_name_token_count`: số token tên đệm.
- `birth_day`, `birth_month`, `birth_year_yy`: ngày/tháng/năm sinh đã parse.
- `birth_date_valid`: ngày sinh có parse hợp lệ hay không.
- `name_font_fixed`: tên/tokens đã được chuyển font TCVN3 sang Unicode hay chưa.
- `score_mon1`, `score_mon2`, `score_mon3`, `score_total`: điểm đã chia về thang thông thường.
