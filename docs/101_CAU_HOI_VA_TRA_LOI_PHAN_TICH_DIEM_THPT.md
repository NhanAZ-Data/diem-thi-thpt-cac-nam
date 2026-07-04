# 101 câu hỏi và câu trả lời phân tích điểm thi THPT

Bộ câu hỏi này được xây dựng lại từ file `cau_hoi_phan_tich_diem_thpt.md`, theo tiêu chí: nhiều người quan tâm, hữu ích, vui vừa đủ, và có thể kiểm chứng tương đối bằng dữ liệu hiện có.

## Cách đọc nhanh

- Phạm vi THPT chính: 2016-2026, 10.865.001 dòng canonical.
- Legacy có họ tên/ngày sinh: 2013-2014, 2.412.155 dòng.
- Các câu về tên, tháng sinh, cung hoàng đạo chỉ là kiểm chứng vui trên legacy, không phải nhân quả.
- Những câu thiếu biến quan trọng được đánh dấu `Không đủ dữ liệu` hoặc `Một phần` thay vì suy diễn.

## Kết luận nổi bật

- Năm có mặt bằng điểm thấp nhất theo lượt điểm môn là 2016; cao nhất là 2024.
- Môn tăng mạnh nhất theo mean đầu-cuối là Ngoại ngữ; giảm mạnh nhất là Kinh tế và pháp luật.
- Năm/môn có nhiều điểm 10 nhất là 2021 - GDCD.
- Tỉnh/thành dẫn đầu mặt bằng điểm 2026 là Ninh Bình.
- Tổ hợp có mean cao nhất 2026 là B00.

## Xu hướng điểm số

### 1. Năm nào có mặt bằng điểm chung thấp nhất và cao nhất trong chuỗi 2016-2026?

**Trạng thái:** Trả lời được

**Trả lời:** Theo trung bình có trọng số trên các lượt điểm môn, năm thấp nhất là 2016 với mean 4,70; năm cao nhất là 2024 với mean 6,73.

**Bằng chứng/cách tính:** Tính từ data/summary/subject_score_distribution.csv và year_subject_stats.csv; cần đọc cùng chú thích đổi cấu trúc 2025-2026.

### 2. Môn nào tăng điểm trung bình mạnh nhất qua toàn bộ quãng có dữ liệu?

**Trạng thái:** Trả lời được

**Trả lời:** Ngoại ngữ tăng mạnh nhất: từ 3,23 năm 2016 lên 5,09 năm 2026, chênh 1,87 điểm.

**Bằng chứng/cách tính:** So sánh năm đầu và năm cuối có mặt của từng môn.

### 3. Môn nào giảm điểm trung bình mạnh nhất qua toàn bộ quãng có dữ liệu?

**Trạng thái:** Trả lời được

**Trả lời:** Kinh tế và pháp luật giảm mạnh nhất: từ 7,69 năm 2025 xuống 5,02 năm 2026, chênh -2,67 điểm.

**Bằng chứng/cách tính:** So sánh năm đầu và năm cuối có mặt của từng môn.

### 4. Điểm trung bình môn Toán thay đổi thế nào qua các năm?

**Trạng thái:** Trả lời được

**Trả lời:** Toán đi từ 4,44 năm 2016 đến 5,65 năm 2026; riêng 2026 mean là 5,65, p90 là 8,25.

**Bằng chứng/cách tính:** Dựa trên thống kê theo môn/năm; không điều chỉnh khác biệt đề thi giữa các năm.

### 5. Điểm trung bình môn Ngữ văn thay đổi thế nào qua các năm?

**Trạng thái:** Trả lời được

**Trả lời:** Ngữ văn đi từ 4,92 năm 2016 đến 6,50 năm 2026; riêng 2026 mean là 6,50, p90 là 8,00.

**Bằng chứng/cách tính:** Dựa trên thống kê theo môn/năm; không điều chỉnh khác biệt đề thi giữa các năm.

### 6. Điểm trung bình môn Ngoại ngữ thay đổi thế nào qua các năm?

**Trạng thái:** Trả lời được

**Trả lời:** Ngoại ngữ đi từ 3,23 năm 2016 đến 5,09 năm 2026; riêng 2026 mean là 5,09, p90 là 7,50.

**Bằng chứng/cách tính:** Dựa trên thống kê theo môn/năm; không điều chỉnh khác biệt đề thi giữa các năm.

### 7. Điểm trung bình môn Lịch sử thay đổi thế nào qua các năm?

**Trạng thái:** Trả lời được

**Trả lời:** Lịch sử đi từ 4,50 năm 2016 đến 6,19 năm 2026; riêng 2026 mean là 6,19, p90 là 8,50.

**Bằng chứng/cách tính:** Dựa trên thống kê theo môn/năm; không điều chỉnh khác biệt đề thi giữa các năm.

### 8. GDCD/Kinh tế và pháp luật có còn là nhóm môn điểm cao không?

**Trạng thái:** Trả lời được

**Trả lời:** Có, trong giai đoạn GDPT 2006, GDCD thường nằm nhóm mean cao; ở 2026, Kinh tế và pháp luật đạt mean 5,02 và p90 6,75.

**Bằng chứng/cách tính:** GDCD có 9 năm dữ liệu; Kinh tế và pháp luật xuất hiện ở schema 2025-2026.

### 9. Tỷ lệ điểm 8+ năm gần nhất cao nhất ở môn nào?

**Trạng thái:** Trả lời được

**Trả lời:** Năm 2026, Công nghệ nông nghiệp có tỷ lệ 8+ cao nhất: 24,30%.

**Bằng chứng/cách tính:** Tỷ lệ = số lượt điểm >=8 / số lượt dự thi môn đó.

### 10. Tỷ lệ điểm liệt (<=1) cao nhất rơi vào môn/năm nào?

**Trạng thái:** Trả lời được

**Trả lời:** Cực trị toàn chuỗi là Lịch sử năm 2016: 1,79%.

**Bằng chứng/cách tính:** Tính trên từng môn/năm, ngưỡng <=1.

### 11. Môn/năm nào có tỷ lệ dưới trung bình (<5) cao nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Ngoại ngữ năm 2016 có tỷ lệ dưới 5 cao nhất: 88,27%.

**Bằng chứng/cách tính:** Tính trên từng môn/năm.

### 12. Năm nào và môn nào có nhiều điểm 10 nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Kỷ lục số lượng điểm 10 là GDCD năm 2021 với 18.789 điểm 10.

**Bằng chứng/cách tính:** Đếm tuyệt đối từ phổ điểm theo môn/năm.

### 13. Có môn nào giảm điểm trung bình liên tục nhiều năm liền không?

**Trạng thái:** Trả lời được

**Trả lời:** Có. Chuỗi giảm dài nhất là Toán với 3 bước giảm liên tiếp, kết thúc năm 2023.

**Bằng chứng/cách tính:** Dò chuỗi mean năm sau < năm trước theo từng môn.

### 14. So sánh Toán và Ngữ văn: môn nào ổn định hơn theo trung bình năm?

**Trạng thái:** Trả lời được

**Trả lời:** Ngữ văn ổn định hơn theo độ lệch chuẩn của mean qua năm: 0,76, so với Toán là 0,81.

**Bằng chứng/cách tính:** Dùng độ lệch chuẩn của điểm trung bình năm, không phải độ lệch chuẩn điểm cá nhân.

### 15. Năm gần nhất có dễ hơn năm trước không?

**Trạng thái:** Một phần

**Trả lời:** So với 2025, các môn chung năm 2026 biến động không đồng đều. Môn giảm mạnh nhất là Kinh tế và pháp luật (-2,67); môn tăng mạnh nhất là Toán (0,85).

**Bằng chứng/cách tính:** 2025 là năm chuyển tiếp CT2006/CT2018, nên kết luận 'dễ hơn' chỉ nên đọc theo từng môn.

## Tỉnh thành và vùng miền

### 16. Năm 2026, tỉnh/thành nào có mặt bằng điểm cao nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Ninh Bình đứng đầu theo trung bình mọi lượt điểm môn: 6,32.

**Bằng chứng/cách tính:** Xếp hạng theo mean có trọng số các lượt điểm môn trong năm 2026.

### 17. Năm 2026, tỉnh/thành nào có mặt bằng điểm thấp nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Sơn La thấp nhất theo cùng cách tính: 4,98.

**Bằng chứng/cách tính:** Xếp hạng theo mean có trọng số các lượt điểm môn trong năm 2026.

### 18. Top tỉnh/thành môn Toán năm 2026 là ai?

**Trạng thái:** Trả lời được

**Trả lời:** Top 3 là: Ninh Bình 6,26; TP. Hồ Chí Minh 6,19; Hà Nội 6,16.

**Bằng chứng/cách tính:** Chỉ xét tỉnh/thành có ít nhất 500 lượt điểm môn đó.

### 19. Top tỉnh/thành môn Ngữ văn năm 2026 là ai?

**Trạng thái:** Trả lời được

**Trả lời:** Top 3 là: Ninh Bình 7,26; Hải Phòng 7,25; Nghệ An 7,03.

**Bằng chứng/cách tính:** Chỉ xét tỉnh/thành có ít nhất 500 lượt điểm môn đó.

### 20. Top tỉnh/thành môn Ngoại ngữ năm 2026 là ai?

**Trạng thái:** Trả lời được

**Trả lời:** Top 3 là: Hà Nội 5,57; TP. Hồ Chí Minh 5,37; Tuyên Quang 5,37.

**Bằng chứng/cách tính:** Chỉ xét tỉnh/thành có ít nhất 500 lượt điểm môn đó.

### 21. Tỉnh nào có điểm Ngoại ngữ trung bình thấp nhất năm gần nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Tây Ninh thấp nhất trong bảng Ngoại ngữ 2026, mean 4,54.

**Bằng chứng/cách tính:** Không tự gán nguyên nhân nông thôn/miền núi nếu chưa có biến kinh tế-xã hội.

### 22. Hà Nội chênh so với phần còn lại bao nhiêu điểm?

**Trạng thái:** Trả lời được

**Trả lời:** Năm 2026, Hà Nội mean 6,18, cao hơn phần còn lại 0,38 điểm.

**Bằng chứng/cách tính:** So sánh theo trung bình mọi lượt điểm môn.

### 23. TP.HCM chênh so với phần còn lại bao nhiêu điểm?

**Trạng thái:** Trả lời được

**Trả lời:** Năm 2026, TP.HCM mean 6,04, chênh 0,23 điểm so với phần còn lại.

**Bằng chứng/cách tính:** So sánh theo trung bình mọi lượt điểm môn.

### 24. Hà Nội và TP.HCM: nơi nào nhỉnh hơn trong năm gần nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Hà Nội nhỉnh hơn TP.HCM 0,14 điểm theo mean tổng hợp lượt điểm môn.

**Bằng chứng/cách tính:** Nếu giá trị âm nghĩa là TP.HCM cao hơn; ở đây dùng dữ liệu 2026.

### 25. Tỉnh nào 'vượt trội bất ngờ' nếu bỏ Hà Nội và TP.HCM?

**Trạng thái:** Trả lời được

**Trả lời:** Ninh Bình là tỉnh/thành ngoài hai trung tâm lớn có mean tổng hợp cao nhất: 6,32.

**Bằng chứng/cách tính:** Đây là cách đặt câu hỏi vui; không kết luận chất lượng giáo dục chỉ từ điểm thi.

### 26. Tỉnh nào có tỷ lệ điểm 10 cao nhất so với số lượt dự thi?

**Trạng thái:** Trả lời được

**Trả lời:** Nghệ An có tỷ lệ điểm 10 cao nhất năm 2026: 0,37%.

**Bằng chứng/cách tính:** Tính trên mọi lượt điểm môn, không phải số thí sinh.

### 27. Miền nào học đều các môn hơn trong năm gần nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Miền Bắc có độ lệch chuẩn mean giữa các môn thấp nhất: 0,62.

**Bằng chứng/cách tính:** Region mapping là quy ước phân tích, nhất là sau sáp nhập 2026.

### 28. Tỉnh nào tăng trưởng mặt bằng điểm nhanh nhất giai đoạn mã tỉnh ổn định 2017-2024?

**Trạng thái:** Trả lời được

**Trả lời:** Bắc Ninh tăng mạnh nhất: 1,79 điểm từ 2017 đến 2024.

**Bằng chứng/cách tính:** Không dùng 2026 vì mã tỉnh đã đổi theo mô hình 34 tỉnh/thành.

### 29. Nếu đặt biệt danh theo môn mạnh, tỉnh nào xứng đáng là 'vương quốc Ngoại ngữ'?

**Trạng thái:** Trả lời được

**Trả lời:** Năm 2026, Hà Nội dẫn đầu Ngoại ngữ với mean 5,57; biệt danh vui: 'vương quốc Ngoại ngữ'.

**Bằng chứng/cách tính:** Biệt danh chỉ là cách kể chuyện dữ liệu, không phải xếp hạng chính thức.

### 30. Có nên xếp hạng trường/cụm thi từ bộ này không?

**Trạng thái:** Một phần

**Trả lời:** Chỉ làm được một phần: legacy 2013-2014 có mã trường dự thi, còn THPT 2016-2026 bulk hiện không có trường THPT. Vì vậy web không xếp hạng trường để tránh suy diễn thiếu dữ liệu.

**Bằng chứng/cách tính:** Gap report xác nhận thiếu trường học cho chuỗi THPT hiện đại.

## Môn học và tổ hợp

### 31. Trong nhóm tự nhiên năm gần nhất, môn nào có nhiều thí sinh nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Vật lí có nhiều lượt điểm nhất trong nhóm tự nhiên: 385.930.

**Bằng chứng/cách tính:** Đếm số lượt điểm hợp lệ theo môn năm 2026.

### 32. Trong nhóm xã hội năm gần nhất, môn nào có nhiều thí sinh nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Lịch sử có nhiều lượt điểm nhất trong nhóm xã hội: 565.056.

**Bằng chứng/cách tính:** Đếm số lượt điểm hợp lệ theo môn năm 2026.

### 33. Xu hướng chọn tự nhiên hay xã hội thay đổi ra sao?

**Trạng thái:** Một phần

**Trả lời:** Có thể theo dõi bằng số lượt dự thi từng môn, nhưng sau 2025 cấu trúc môn tự chọn đổi rõ nên cần tách giai đoạn 2017-2024 và 2025-2026 khi phân tích sâu.

**Bằng chứng/cách tính:** Dữ liệu có count theo môn/năm; diễn giải xu hướng phải tôn trọng thay đổi chương trình.

### 34. Tổ hợp nào có điểm trung bình cao nhất năm 2026?

**Trạng thái:** Trả lời được

**Trả lời:** B00 cao nhất, mean 19,69, p90 25,25.

**Bằng chứng/cách tính:** Dựa trên cột tổ hợp do nguồn tính sẵn, loại dòng không có điểm tổ hợp.

### 35. Điểm tổ hợp A00 thay đổi thế nào?

**Trạng thái:** Trả lời được

**Trả lời:** A00 đi từ mean 17,25 năm 2016 đến 19,41 năm 2026; năm 2026 tỷ lệ >=27 là 1,99%.

**Bằng chứng/cách tính:** Dùng các cột tổ hợp đã có trong raw data.

### 36. Điểm tổ hợp A01 thay đổi thế nào?

**Trạng thái:** Trả lời được

**Trả lời:** A01 đi từ mean 15,13 năm 2016 đến 18,41 năm 2026; năm 2026 tỷ lệ >=27 là 0,83%.

**Bằng chứng/cách tính:** Dùng các cột tổ hợp đã có trong raw data.

### 37. Điểm tổ hợp D01/D00 thay đổi thế nào?

**Trạng thái:** Trả lời được

**Trả lời:** D01/D00 đi từ mean 13,00 năm 2016 đến 19,02 năm 2026; năm 2026 tỷ lệ >=27 là 0,18%.

**Bằng chứng/cách tính:** Dùng các cột tổ hợp đã có trong raw data.

### 38. Điểm tổ hợp C00 thay đổi thế nào?

**Trạng thái:** Trả lời được

**Trả lời:** C00 đi từ mean 15,13 năm 2016 đến 17,23 năm 2026; năm 2026 tỷ lệ >=27 là 0,21%.

**Bằng chứng/cách tính:** Dùng các cột tổ hợp đã có trong raw data.

### 39. Điểm tổ hợp B00 thay đổi thế nào?

**Trạng thái:** Trả lời được

**Trả lời:** B00 đi từ mean 15,90 năm 2016 đến 19,69 năm 2026; năm 2026 tỷ lệ >=27 là 3,53%.

**Bằng chứng/cách tính:** Dùng các cột tổ hợp đã có trong raw data.

### 40. Tổ hợp nào có tỷ lệ từ 27 điểm trở lên cao nhất năm 2026?

**Trạng thái:** Trả lời được

**Trả lời:** B00 có tỷ lệ >=27 cao nhất: 3,53%.

**Bằng chứng/cách tính:** Đây là chỉ báo 'lạm phát điểm' theo tổ hợp, không phải xác suất đỗ.

### 41. Ngưỡng top 10% theo tổ hợp năm gần nhất là bao nhiêu?

**Trạng thái:** Trả lời được

**Trả lời:** Một vài ngưỡng p90 năm 2026: B00: 25,25; A00: 24,75; C01: 23,75; D01/D00: 23,25; D07: 23,50.

**Bằng chứng/cách tính:** p90 nghĩa là khoảng 10% lượt tổ hợp hợp lệ cao hơn hoặc bằng mốc này.

### 42. GDCD có phải 'môn cứu điểm' mọi năm không?

**Trạng thái:** Một phần

**Trả lời:** Trong các năm có GDCD, môn này thường ở nhóm mean cao, nhưng từ 2025-2026 schema mới thay bằng Kinh tế và pháp luật cho nhóm CT2018; vì vậy nên nói 'nhóm môn công dân/pháp luật thường dễ kéo điểm' hơn là khẳng định mọi năm.

**Bằng chứng/cách tính:** Dựa trên mean môn theo năm và thay đổi schema 2025.

### 43. Môn tự luận và trắc nghiệm khác nhau thế nào qua phổ điểm?

**Trạng thái:** Một phần

**Trả lời:** Năm 2026, Ngữ văn mean 6,50; Toán mean 5,65; Ngoại ngữ mean 5,09. Khác biệt có thật trên phổ điểm, nhưng không chỉ do hình thức thi.

**Bằng chứng/cách tính:** Cần kiểm soát năng lực nhóm thí sinh và cấu trúc đề nếu muốn kết luận nguyên nhân.

### 44. Môn nào dưới trung bình nhiều nhất ở năm gần nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Năm 2026, Ngoại ngữ có tỷ lệ <5 cao nhất: 49,95%.

**Bằng chứng/cách tính:** Tính theo lượt điểm hợp lệ từng môn.

### 45. Ngoại ngữ đang cải thiện hay vẫn là nỗi ám ảnh?

**Trạng thái:** Trả lời được

**Trả lời:** Năm 2026, Ngoại ngữ mean 5,09, p90 7,50, tỷ lệ <5 là 49,95%. Đây vẫn là môn phân hóa mạnh, không thể chỉ gọi là 'dễ'.

**Bằng chứng/cách tính:** Dựa trên mean, p90 và tỷ lệ dưới 5.

## Ứng dụng và ngưỡng điểm

### 46. Ngưỡng top 10% theo môn năm 2026 là gì?

**Trạng thái:** Trả lời được

**Trả lời:** Các mốc p90 cao nhất: Công nghệ công nghiệp: 8,75; Công nghệ nông nghiệp: 8,50; Lịch sử: 8,50; Hóa học: 8,25; Tin học: 8,25; Sinh học: 8,25.

**Bằng chứng/cách tính:** p90 tính từ phổ điểm theo từng môn.

### 47. Đạt 8 điểm Toán năm 2026 thuộc nhóm nào?

**Trạng thái:** Trả lời được

**Trả lời:** Khoảng 15,63% lượt điểm Toán đạt từ 8 trở lên; nói cách khác 8 điểm thuộc nhóm trên với độ hiếm như vậy.

**Bằng chứng/cách tính:** Tính trực tiếp từ share_ge_8.

### 48. Đạt 8 điểm Ngoại ngữ năm 2026 thuộc nhóm nào?

**Trạng thái:** Trả lời được

**Trả lời:** Khoảng 7,38% lượt điểm Ngoại ngữ đạt từ 8 trở lên; nói cách khác 8 điểm thuộc nhóm trên với độ hiếm như vậy.

**Bằng chứng/cách tính:** Tính trực tiếp từ share_ge_8.

### 49. Môn nào phân hóa mạnh nhất năm gần nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Toán có độ lệch chuẩn cao nhất năm 2026: 1,89.

**Bằng chứng/cách tính:** Độ lệch chuẩn cao thường cho thấy phổ điểm trải rộng hơn.

### 50. Môn nào ít phân hóa nhất năm gần nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Công nghệ nông nghiệp có độ lệch chuẩn thấp nhất năm 2026: 1,27.

**Bằng chứng/cách tính:** Độ lệch chuẩn thấp nghĩa là điểm tập trung hơn quanh trung bình.

### 51. Môn nào có mean và median lệch nhau đáng chú ý nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Năm 2026, Ngữ văn có độ lệch/skew nổi bật nhất trong nhóm mới: skew -0,75.

**Bằng chứng/cách tính:** Skew tính từ phân phối điểm rời rạc.

### 52. Nếu học mạnh Toán, nên nhìn tổ hợp nào trước?

**Trạng thái:** Một phần

**Trả lời:** Về mặt phổ điểm năm 2026, B00 có mean cao nhất, còn B00 có tỷ lệ >=27 cao nhất. Chọn ngành vẫn cần điểm chuẩn thật, sở thích và môn mạnh cá nhân.

**Bằng chứng/cách tính:** Đây là gợi ý đọc phổ điểm, không phải tư vấn tuyển sinh cá nhân.

### 53. Nếu mục tiêu 27+ thì tổ hợp nào 'dễ thở' hơn theo dữ liệu?

**Trạng thái:** Trả lời được

**Trả lời:** B00 có tỷ lệ >=27 cao nhất năm 2026: 3,53%.

**Bằng chứng/cách tính:** Chỉ so trong nhóm thí sinh có đủ điểm tổ hợp.

### 54. Nếu ở tỉnh có mặt bằng cao, mức cạnh tranh tham khảo là bao nhiêu?

**Trạng thái:** Một phần

**Trả lời:** Ở tỉnh/thành đứng đầu 2026 là Ninh Bình, mean tổng hợp đạt 6,32. Khi làm bản tương tác, nên cho người dùng chọn tỉnh X để xem p50/p90 theo môn.

**Bằng chứng/cách tính:** Hiện web cung cấp bảng top và có thể mở rộng selector tỉnh.

### 55. Năm gần nhất có bao nhiêu lượt điểm môn được dùng để phân tích?

**Trạng thái:** Trả lời được

**Trả lời:** Năm 2026 có 4.787.559 lượt điểm môn hợp lệ trên 12 môn.

**Bằng chứng/cách tính:** Một thí sinh có nhiều lượt điểm môn, nên đây không phải số thí sinh.

### 56. Môn nào cần cảnh báo rủi ro điểm liệt nhất năm gần nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Năm 2026, môn có tỷ lệ <=1 cao nhất là Địa lí.

**Bằng chứng/cách tính:** Dựa trên ngưỡng <=1 điểm.

## Tương quan và thống kê sâu

### 57. Toán và Vật lí tương quan thế nào năm 2026?

**Trạng thái:** Trả lời được

**Trả lời:** Hệ số Pearson là 0,732 trên 385.903 thí sinh có đủ cả hai điểm.

**Bằng chứng/cách tính:** Pearson đo tương quan tuyến tính, không phải quan hệ nhân quả.

### 58. Toán và Hóa học tương quan thế nào năm 2026?

**Trạng thái:** Trả lời được

**Trả lời:** Hệ số Pearson là 0,711 trên 250.784 thí sinh có đủ cả hai điểm.

**Bằng chứng/cách tính:** Pearson đo tương quan tuyến tính, không phải quan hệ nhân quả.

### 59. Ngữ văn và Lịch sử tương quan thế nào năm 2026?

**Trạng thái:** Trả lời được

**Trả lời:** Hệ số Pearson là 0,529 trên 564.666 thí sinh có đủ cả hai điểm.

**Bằng chứng/cách tính:** Pearson đo tương quan tuyến tính, không phải quan hệ nhân quả.

### 60. Ngữ văn và Địa lí tương quan thế nào năm 2026?

**Trạng thái:** Trả lời được

**Trả lời:** Hệ số Pearson là 0,548 trên 443.639 thí sinh có đủ cả hai điểm.

**Bằng chứng/cách tính:** Pearson đo tương quan tuyến tính, không phải quan hệ nhân quả.

### 61. Ngoại ngữ tương quan với khối tự nhiên hay xã hội hơn?

**Trạng thái:** Trả lời được

**Trả lời:** Năm 2026, tương quan trung bình của Ngoại ngữ với khối tự nhiên cao hơn: tự nhiên 0,503, xã hội 0,293.

**Bằng chứng/cách tính:** So trung bình các Pearson theo cặp môn.

### 62. Thí sinh điểm 10 một môn có học đều không?

**Trạng thái:** Trả lời được

**Trả lời:** Nhóm đạt 10 ở Hóa học có mean các lượt điểm môn khác cao nhất trong bảng perfect-10: 8,52.

**Bằng chứng/cách tính:** Tính mean các môn khác trong năm 2026 cho từng nhóm đạt 10.

### 63. Có hiện tượng giỏi lệch một môn ở nhóm điểm 10 không?

**Trạng thái:** Một phần

**Trả lời:** Có thể có. Nhóm đạt 10 ở Công nghệ nông nghiệp có mean môn khác thấp nhất trong nhóm điểm 10: 6,40.

**Bằng chứng/cách tính:** Cần xem thêm tổ hợp môn thí sinh chọn để kết luận sâu hơn.

### 64. Có cặp môn nào biến động ngược chiều giữa các năm không?

**Trạng thái:** Trả lời được

**Trả lời:** Giai đoạn 2017-2024, cặp có tương quan mean năm thấp nhất là Địa lí - Sinh học: r=0,586.

**Bằng chứng/cách tính:** Tính tương quan giữa chuỗi mean theo năm, không phải tương quan cá nhân.

### 65. Phổ điểm nào gần hình chuông nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Gần chuẩn nhất theo thước đo skew+kurtosis là Địa lí năm 2016.

**Bằng chứng/cách tính:** Thước đo đơn giản: |skew| + |excess kurtosis|.

### 66. Phổ điểm nào lệch khỏi hình chuông nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Lệch nhiều nhất theo cùng thước đo là Ngoại ngữ năm 2016.

**Bằng chứng/cách tính:** Không coi đây là kiểm định phân phối chuẩn chính thức.

### 67. Môn nào có nhiều điểm thấp nhất trong lịch sử chuỗi?

**Trạng thái:** Trả lời được

**Trả lời:** Theo tỷ lệ <5, cực trị là Ngoại ngữ năm 2016: 88,27%.

**Bằng chứng/cách tính:** Dùng tỷ lệ dưới trung bình như proxy cho 'lệch về điểm thấp'.

### 68. Môn nào có đuôi điểm cao dày nhất năm gần nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Năm 2026, Công nghệ công nghiệp có tỷ lệ >=9 cao nhất.

**Bằng chứng/cách tính:** Tỷ lệ >=9 đo đuôi phải của phổ điểm.

### 69. Đề thi có đang phân hóa mạnh hơn không?

**Trạng thái:** Một phần

**Trả lời:** Nhìn từng môn thì không đồng loạt. Năm 2026, môn phân hóa mạnh nhất là Toán (std 1,89); cần đọc theo từng môn thay vì một kết luận chung.

**Bằng chứng/cách tính:** Dựa trên độ lệch chuẩn theo môn/năm.

## Thời sự, cải cách và chất lượng dữ liệu

### 70. Bước chuyển 2019 sang 2020 có làm mặt bằng điểm thay đổi không?

**Trạng thái:** Trả lời được

**Trả lời:** Có dấu hiệu tăng rõ: mean có trọng số toàn chuỗi tăng 0,87 điểm từ 2019 sang 2020.

**Bằng chứng/cách tính:** Đây là mô tả dữ liệu, không tự chứng minh nguyên nhân do cấu trúc đề.

### 71. Cú đổi chương trình 2025-2026 ảnh hưởng thế nào?

**Trạng thái:** Trả lời được

**Trả lời:** Ảnh hưởng lớn nhất nằm ở schema môn: xuất hiện Kinh tế và pháp luật, Tin học, Công nghệ; một số môn cũ như GDCD không còn trực tiếp tương đương cho toàn bộ thí sinh CT2018.

**Bằng chứng/cách tính:** Dựa trên metadata/subjects.csv và raw schema 2025-2026.

### 72. Các môn mới 2025-2026 có đủ dữ liệu để phân tích không?

**Trạng thái:** Một phần

**Trả lời:** Có cho phân tích mô tả. Năm 2026, Tin học có 18.264 lượt điểm; Kinh tế và pháp luật có 282.519 lượt điểm.

**Bằng chứng/cách tính:** Dữ liệu mới chỉ có hai năm nên phân tích xu hướng dài hạn còn yếu.

### 73. Năm 2025 CT2018 và CT2006 có cần tách riêng không?

**Trạng thái:** Trả lời được

**Trả lời:** Có. CT2018 chiếm phần lớn còn CT2006 là nhóm nhỏ hơn nhiều; gộp chung được cho tổng quan nhưng phân tích cải cách nên tách hai segment.

**Bằng chứng/cách tính:** processed_file_inventory.csv ghi CT2018 1.131.136 dòng và CT2006 22.090 dòng.

### 74. Đợt 2 năm 2020 có làm méo thống kê không?

**Trạng thái:** Trả lời được

**Trả lời:** Đợt 2 Đà Nẵng có 10.857 dòng, nhỏ so với đợt chính 870.517 dòng; nên giữ lại để đủ dữ liệu nhưng có thể tách segment khi cần.

**Bằng chứng/cách tính:** Dựa trên processed_file_inventory.csv.

### 75. Đợt 2 năm 2021 có làm méo thống kê không?

**Trạng thái:** Trả lời được

**Trả lời:** Đợt 2 năm 2021 có 12.086 dòng, nhỏ so với đợt chính 987.704 dòng; ảnh hưởng tổng thể hạn chế nhưng vẫn nên ghi provenance.

**Bằng chứng/cách tính:** Dựa trên processed_file_inventory.csv.

### 76. Cụm đại học và cụm địa phương năm 2016 khác nhau thế nào?

**Trạng thái:** Trả lời được

**Trả lời:** Năm 2016, cụm đại học mean tổng hợp khoảng 4,88, cụm địa phương khoảng 4,19.

**Bằng chứng/cách tính:** 2016 có Tinh là mã cụm, không hoàn toàn tương đương mã tỉnh.

### 77. Có dữ liệu năm 2015 không?

**Trạng thái:** Không đủ dữ liệu

**Trả lời:** Chưa có trong nguồn canonical hiện tại, nên mọi biểu đồ thời gian phải ghi rõ khoảng trống 2015.

**Bằng chứng/cách tính:** metadata/gap_report.md xác nhận thiếu file raw 2015.

### 78. Dữ liệu 2026 đã được đối chiếu độc lập chưa?

**Trạng thái:** Trả lời được

**Trả lời:** Có. Repo lưu crosscheck với nguồn anhdung98: cùng 1.208.863 SBD và không có mismatch ở các cột điểm đã map.

**Bằng chứng/cách tính:** metadata/crosscheck_2026_anhdung98.csv.

### 79. Dữ liệu có phải sau phúc khảo không?

**Trạng thái:** Không đủ dữ liệu

**Trả lời:** Chưa thể khẳng định nhất quán cho toàn chuỗi; đa số nguồn công khai là snapshot công bố điểm, không có trường phúc khảo chuẩn hóa.

**Bằng chứng/cách tính:** Gap report ghi đây là vùng yếu cần bổ sung nguồn nếu phân tích pháp lí/chính sách.

## Vui, bói toán có kiểm chứng

### 80. Nếu hỏi vui 'tên nào thông minh nhất' theo điểm legacy thì tên nào đứng đầu?

**Trạng thái:** Trả lời được

**Trả lời:** Trong legacy 2013-2014, với ngưỡng tối thiểu 1.000 người, tên chính 'Bách' có mean tổng điểm cao nhất: 14,49. Đây chỉ là tương quan vui, tuyệt đối không phải nhân quả.

**Bằng chứng/cách tính:** Dựa trên data/analysis/legacy_2013_2014_features.csv; không dùng cho THPT 2016-2026 vì thiếu tên.

### 81. Top 5 tên chính có tỷ lệ vào nhóm điểm cao tốt nhất là gì?

**Trạng thái:** Trả lời được

**Trả lời:** Top 5 theo tỷ lệ lọt nhóm top 5% legacy là: Bách, Đan, Kiên, Minh, Anh.

**Bằng chứng/cách tính:** Chỉ tính tên có ít nhất 1.000 bản ghi để tránh nhiễu mẫu nhỏ.

### 82. Bạn tên Anh có giỏi Ngoại ngữ hơn không?

**Trạng thái:** Trả lời được

**Trả lời:** Trong khối D legacy, thí sinh tên chính Anh có mean môn Ngoại ngữ 4,68, nhóm tên khác 4,34; chênh 0,34 điểm.

**Bằng chứng/cách tính:** Đùa chữ nhưng có kiểm chứng trên khối D 2013-2014.

### 83. Họ Nguyễn có điểm trung bình khác các họ khác không?

**Trạng thái:** Trả lời được

**Trả lời:** Họ Nguyễn mean tổng điểm 13,50; nhóm họ khác 13,30; chênh 0,20.

**Bằng chứng/cách tính:** Chênh lệch nhỏ không nói lên nguyên nhân.

### 84. Tháng sinh nào có mean tổng điểm cao nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Trong legacy, tháng 11 cao nhất với mean 13,54.

**Bằng chứng/cách tính:** Chỉ dùng bản ghi có ngày sinh parse hợp lệ.

### 85. Tháng sinh có tạo khác biệt lớn không?

**Trạng thái:** Trả lời được

**Trả lời:** Khoảng cách giữa tháng cao nhất (11) và thấp nhất (6) là 0,27 điểm tổng 3 môn; khá nhỏ so với biến thiên cá nhân.

**Bằng chứng/cách tính:** Không đủ cơ sở để nói tháng sinh quyết định điểm.

### 86. Cung hoàng đạo nào có mean cao nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Bọ Cạp cao nhất trong legacy, mean 13,55. Nhắc lại: đây là trò vui thống kê, không phải khoa học chiêm tinh.

**Bằng chứng/cách tính:** Suy ra từ ngày/tháng sinh parse hợp lệ 2013-2014.

### 87. Cung hoàng đạo có khác biệt đáng kể không?

**Trạng thái:** Trả lời được

**Trả lời:** Khoảng cách mean giữa cung cao nhất và thấp nhất là 0,26 điểm tổng 3 môn; không đủ để tin vào 'cung học giỏi'.

**Bằng chứng/cách tính:** Không kiểm soát tỉnh, trường, khối thi, năm sinh.

### 88. Tên đệm dài hơn có điểm cao hơn không?

**Trạng thái:** Trả lời được

**Trả lời:** Nhóm có 2 token tên đệm có mean cao nhất (13,55), nhưng đây dễ là nhiễu văn hóa đặt tên hơn là tác động thật.

**Bằng chứng/cách tính:** Feature chỉ lưu số token tên đệm, không xuất bản tên đầy đủ.

### 89. Số báo danh có chữ số 'đẹp' thì điểm cao hơn không?

**Trạng thái:** Trả lời được

**Trả lời:** Hầu như không. Tương quan giữa tổng chữ số SBD và mean điểm cá nhân năm 2026 là -0,0313.

**Bằng chứng/cách tính:** SBD là mã hành chính/kỹ thuật, không nên gán ý nghĩa phong thủy.

### 90. SBD chứa 68/86 có 'lộc phát' điểm số không?

**Trạng thái:** Trả lời được

**Trả lời:** Nhóm SBD chứa 68/86 có mean 5,67; toàn bộ thí sinh có mean 5,84. Chênh lệch này không đáng để mê tín.

**Bằng chứng/cách tính:** Tính mean điểm cá nhân 2026 theo các môn có điểm.

### 91. Năm nào xứng biệt danh 'mưa điểm 10'?

**Trạng thái:** Trả lời được

**Trả lời:** Năm/môn xứng danh nhất là 2021 - GDCD, với 18.789 điểm 10.

**Bằng chứng/cách tính:** Đặt biệt danh theo số lượng tuyệt đối điểm 10.

### 92. Tỉnh nào xứng danh 'thủ phủ Toán học' năm gần nhất?

**Trạng thái:** Trả lời được

**Trả lời:** Ninh Bình dẫn đầu Toán 2026, mean 6,26.

**Bằng chứng/cách tính:** Biệt danh vui dựa trên mean Toán cấp tỉnh.

### 93. Có tên nào 'nên tránh' khi đặt tên con không?

**Trạng thái:** Một phần

**Trả lời:** Không. Bộ dữ liệu chỉ cho tương quan thô theo tên trong legacy 2013-2014; dùng để kể chuyện vui thì được, dùng để chọn/né tên thì không nghiêm túc.

**Bằng chứng/cách tính:** Thiếu thiết kế nhân quả và thiếu trường nền tảng gia đình/xã hội.

### 94. Nếu dự đoán vui năm sau, môn nào có khả năng tăng mean nhất?

**Trạng thái:** Một phần

**Trả lời:** Theo trend tuyến tính thô vài năm gần đây, Lịch sử có slope dương cao nhất (0,044 điểm/năm). Đây chỉ là dự báo vui.

**Bằng chứng/cách tính:** Không dùng để dự báo chính sách hoặc điểm chuẩn.

## Phạm vi, đạo đức và sản phẩm

### 95. Dữ liệu THPT 2016-2026 có họ tên và ngày sinh không?

**Trạng thái:** Không đủ dữ liệu

**Trả lời:** Không trong các bulk file đã rà. Họ tên/ngày sinh chỉ có ở legacy tuyển sinh ĐH-CĐ 2013-2014.

**Bằng chứng/cách tính:** metadata/gap_report.md và schema raw 2016-2026.

### 96. Có thể kết luận tên hoặc tháng sinh gây ra học giỏi không?

**Trạng thái:** Không đủ dữ liệu

**Trả lời:** Không. Các mục tên/tháng sinh chỉ là tương quan vui; muốn nói nhân quả cần kiểm soát tỉnh, trường, khối thi, nền tảng gia đình, cohort và nhiều biến nhiễu khác.

**Bằng chứng/cách tính:** Đây là cảnh báo phương pháp bắt buộc khi công bố phân tích định danh.

### 97. Những câu hỏi nào hiện chưa trả lời được tốt?

**Trạng thái:** Không đủ dữ liệu

**Trả lời:** Các câu về giới tính, thí sinh tự do, trường THPT, tỷ lệ tốt nghiệp, điểm chuẩn đại học/ngành cụ thể và phúc khảo chưa trả lời chắc bằng dữ liệu hiện có.

**Bằng chứng/cách tính:** Các trường đó không có hoặc không chuẩn hóa trong bộ bulk hiện tại.

### 98. Bộ dữ liệu hiện bao phủ bao nhiêu dòng?

**Trạng thái:** Trả lời được

**Trả lời:** Repo có 10.865.001 dòng THPT canonical 2016-2026 và 2.412.155 dòng legacy 2013-2014, tổng 13.277.156 dòng canonical.

**Bằng chứng/cách tính:** metadata/dataset_manifest.csv và validation script.

### 99. Mã tỉnh 2026 có so sánh trực tiếp với các năm cũ được không?

**Trạng thái:** Một phần

**Trả lời:** Không nên so trực tiếp nếu chưa map lại theo sáp nhập. Web tách phân tích 2026 và dùng 2017-2024 cho trend tỉnh ổn định.

**Bằng chứng/cách tính:** 2026 dùng danh sách 34 tỉnh/thành; 2002-2025 dùng mã cũ.

### 100. 101 câu hỏi có quá nhiều không?

**Trạng thái:** Trả lời được

**Trả lời:** Không quá nhiều nếu xem là ngân hàng câu hỏi. Nhưng cho một bài viết/web chính, nên highlight khoảng 20 insight đầu và để 101 câu ở phần tra cứu/tải về.

**Bằng chứng/cách tính:** Thiết kế site dùng bộ lọc nhóm và trạng thái để tránh quá tải.

### 101. Nếu chỉ chọn 20 câu nổi bật để truyền thông, nên chọn nhóm nào?

**Trạng thái:** Trả lời được

**Trả lời:** Nên ưu tiên: xu hướng mean, năm khó/dễ, điểm 10, 8+, dưới 5, top tỉnh Toán/Văn/Ngoại ngữ, HN/HCM vs rest, tổ hợp 27+, p90 theo môn, tương quan Toán-Lý/Hóa, Ngoại ngữ, và 3-4 câu vui về tên/tháng sinh/SBD có cảnh báo nhân quả.

**Bằng chứng/cách tính:** Cân bằng nghiêm túc, hữu ích và vui; tránh biến câu vui thành kết luận định kiến.
