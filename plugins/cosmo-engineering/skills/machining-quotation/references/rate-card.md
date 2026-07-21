# Rate Card — Cosmo Engineering (bảng giá nội bộ)

> ĐIỀN SỐ THẬT CỦA BẠN VÀO ĐÂY. Khi các placeholder `[___]` đã được thay bằng số,
> skill chào giá sẽ chạy ra giá thành đầy đủ mà không cần hỏi lại. Cập nhật khi giá
> vật tư / nhân công / điện thay đổi.

## 1. Đơn giá giờ máy (machine-hour rate) — đã gồm khấu hao + điện + nhân công vận hành

| Máy (Machine)              | VND/giờ | USD/giờ | Ghi chú |
|----------------------------|---------|---------|---------|
| Tiện tay (manual lathe)    | `[___]` | `[___]` | |
| Phay tay (manual mill)     | `[___]` | `[___]` | |
| CNC Haas VF-4              | `[___]` | `[___]` | rate cao hơn do máy đắt + độ chính xác |
| Wire EDM (molybdenum)      | `[___]` | `[___]` | cộng thêm chi phí dây/điện cực bên dưới |
| Lập trình CAM / setup CNC  | `[___]` | `[___]` | tính theo giờ hoặc phí cố định/job |

## 2. Giá vật liệu cơ sở (material price basis) — VND/kg (cập nhật theo thị trường)

| Nhóm vật liệu | Grade tiêu biểu | VND/kg | Ghi chú |
|---------------|-----------------|--------|---------|
| Thép kết cấu   | SS400 / S235 / S275JR | `[___]` | |
| Thép C trung bình | C45 / C50 | `[___]` | |
| Thép hợp kim   | SCM440 / 42CrMo4 / SCM420 | `[___]` | |
| Inox           | SUS304 | `[___]` | |
| Inox           | SUS201 | `[___]` | |
| Nhôm           | (grade) | `[___]` | |
| Đồng/hợp kim đồng | (grade) | `[___]` | |

- Hao hụt phôi / scrap allowance mặc định: **`[___]`%** (thường 10–25% tùy hình dạng, phôi tròn vs. tấm).
- Nếu mua phôi lẻ (không tồn kho): cộng phí mua lẻ + thời gian đặt hàng vào lead time.

## 3. Vật tư tiêu hao (consumables)

| Hạng mục | Đơn giá | Áp dụng khi |
|----------|---------|-------------|
| Dây molybdenum EDM | `[___]`/m hoặc /job | mọi job wire cut |
| Insert/dao đặc biệt | `[___]` | vật liệu cứng / job lớn |
| Đồ gá chuyên dùng (fixture) | `[___]` | phân bổ vào giá theo số lượng |

## 4. Thuê ngoài (outsourcing) — cộng markup xử lý

| Công đoạn | Giá cơ sở | Markup xử lý | Turnaround điển hình |
|-----------|-----------|--------------|----------------------|
| Nhiệt luyện (heat treat) | theo báo giá NCC | `[___]`% | 5–7 ngày |
| Mạ / phủ (plating/coating) | theo báo giá NCC | `[___]`% | 3–5 ngày |
| Mài (grinding) | theo báo giá NCC | `[___]`% | 2–4 ngày |
| Cắt laser/plasma/waterjet | theo báo giá NCC | `[___]`% | 1–3 ngày |
| Phôi đúc/rèn / cắt răng | theo báo giá NCC | `[___]`% | tùy |

## 5. Biên lợi nhuận (margin tiers) — giá bán = giá vốn × (1 + margin)

| Tầng khách | Margin | Khi nào dùng |
|------------|--------|--------------|
| **JPT / qua trung gian** | `[___]`% | đơn qua đối tác/nhà thầu chính, giá gốc thấp hơn |
| **Khách trực tiếp (direct)** | `[___]`% | khách cuối, gồm chi phí bán hàng + rủi ro |
| Đơn gấp / độ khó cao | `[___]`% | job rush, dung sai ngặt, rủi ro kỹ thuật |

## 6. Mặc định khác

- VAT: `[___]`% (thường 10% — ghi rõ đã gồm/chưa gồm trên báo giá).
- Hiệu lực báo giá: 30 ngày (chỉnh nếu cần).
- Điều khoản thanh toán mặc định: 50% cọc / 50% trước giao.
- Tỷ giá USD/VND tham chiếu khi quy đổi: `[___]` (ghi ngày cập nhật).
