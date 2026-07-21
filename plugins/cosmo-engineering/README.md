# Cosmo Engineering — Plugin kỹ thuật cơ khí

Bộ 3 skill dùng nội bộ cho Cosmo Engineering / DHP. Song ngữ VI/EN, khớp ngôn ngữ theo yêu cầu đến.

## Các skill

- **machining-quotation** — Chào giá gia công từ email/RFQ: tách hạng mục, chốt vật liệu, định tuyến quy trình (tiện tay / phay / Haas VF-4 / wire EDM / thuê ngoài), đơn giá + thành tiền + thời gian giao, kèm khối NỘI BỘ (giá vốn → biên lãi → giá bán) 2 tầng JPT/khách trực tiếp.
  - Điền số thật vào `skills/machining-quotation/references/rate-card.md` để chạy ra giá đầy đủ.
- **coupling-dhp-advisory** — Tư vấn khớp nối (gear, Cardan/các đăng, B-Flex, HTD belt, rigid) và kỹ thuật xưởng DHP (WPS/hàn, chọn vật liệu, tấm cách nhiệt, sửa chữa drivetrain, NDT).
- **mechanical-project-concept** — Đề xuất design-concept dự án cơ khí: phân tích yêu cầu → phương án → BOM sơ bộ → kế hoạch theo giai đoạn → timeline → dự toán, gửi khách trước khi thiết kế chi tiết.

## Dùng thế nào

Đã cài thì Claude tự nhận khi yêu cầu khớp, hoặc gọi tay bằng `/` rồi chọn skill.

Lưu ý: skill cần bật **Code execution and file creation** trong Settings mới chạy được.
