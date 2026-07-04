# Nguồn dữ liệu

## Nguồn canonical

Nguồn raw chính là `sdgedfegw/du-lieu-diem-thi`:

```text
https://github.com/sdgedfegw/du-lieu-diem-thi
commit: 1178a012c8af3f07f7d40c614dc61fb342687e46
```

Nguồn này bao gồm:

- tuyển sinh ĐH-CĐ 2013-2014;
- THPT quốc gia 2016-2019;
- tốt nghiệp THPT 2020-2026.

Trong repo này, nguồn đó được giữ dưới dạng git submodule tại `sources/du-lieu-diem-thi`.

## Nguồn đối chiếu

Các nguồn đã rà/tải/đối chiếu được ghi trong `metadata/source_registry.csv`.

Nguồn đáng chú ý:

- `anhdung98/diem_thi_2026`: file CSV 2026 schema `dm1..dm13`, đã map và đối chiếu với canonical.
- Báo Chính phủ/Cổng TTĐT Chính phủ 2025: file XLSX CT2018 và CT2006, đã tải về `sources/crosscheck/baochinhphu/2025`.
- Cổng tra cứu Bộ GDĐT 2026: dùng để xác nhận kênh tra cứu và danh sách Sở, không dùng để crawl bulk.
- VnExpress 2026: hữu ích cho spot-check/ranking, không dùng làm nguồn canonical.

## Nguyên tắc chọn canonical

- Ưu tiên file bulk có cấu trúc rõ, có thể tái tạo phân tích.
- Nếu có file aggregate và file năm riêng, dùng file năm riêng để tránh đếm trùng.
- Nếu nguồn khác chỉ là crawler hoặc trang tra cứu từng SBD, chỉ ghi nhận để audit/spot-check.
