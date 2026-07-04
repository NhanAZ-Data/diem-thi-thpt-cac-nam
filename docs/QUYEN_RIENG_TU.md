# Quyền riêng tư và giới hạn phân tích

## Trường định danh

Dữ liệu legacy 2013-2014 có họ tên và ngày sinh trong raw source. Repo này giữ raw data ở submodule nguồn, còn bảng phân tích mặc định chỉ xuất:

- họ;
- tên chính;
- tháng/ngày/năm sinh dạng tách trường;
- điểm và mã thi.

Không nên công bố lại row-level identity data nếu chưa có rà soát pháp lý/đạo đức riêng.

## Dữ liệu 2016-2026

Các nguồn bulk đã rà hiện chỉ có SBD, mã tỉnh/hội đồng, môn và điểm. Chưa thấy bulk data hợp lệ có họ tên/ngày sinh cho các năm này.

Không nên suy đoán tháng sinh, giới tính, vùng miền cá nhân hoặc danh tính từ SBD nếu không có nguồn công bố rõ ràng.

## Cảnh báo về nhân quả

Các bảng theo tên/tháng sinh dùng cho phân tích khám phá. Chúng không đủ để kết luận rằng tên hoặc tháng sinh gây ra điểm cao/thấp.

Muốn bàn về nhân quả cần tối thiểu kiểm soát:

- năm thi;
- tỉnh/hội đồng;
- khối thi/trường/ngành ở legacy;
- cấu trúc đề và môn thi;
- phân bố giới tính/xã hội/kinh tế nếu có dữ liệu;
- thay đổi hệ thống giáo dục và cách tính điểm qua năm.
