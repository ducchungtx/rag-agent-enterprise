# Chính sách nội bộ — Phòng Pháp chế (quy trình đất đai)

Áp dụng cho workspace **Phòng Pháp chế** — Công ty Demo Land.

## Phạm vi

- Thẩm định hồ sơ chuyển mục đích sử dụng đất trước khi nộp ra ngoài.
- Lưu trữ bản scan + metadata trong Knowledge Base `Luật Đất đai + Policy`.
- Chỉ **Contributor** trở lên được upload; **Viewer** chỉ hỏi đáp và xem tài liệu được share.

## Hồ sơ chuyển mục đích (nội bộ)

Bộ hồ sơ tối thiểu phòng Pháp chế yêu cầu:

1. Đơn đề nghị (mẫu NB-01).
2. Bản sao Giấy chứng nhận quyền sử dụng đất.
3. Bản vẽ vị trí thửa đất tỷ lệ 1:500 (hoặc bản đồ số được phê duyệt).
4. Báo cáo môi trường rút gọn (nếu diện tích trên **5.000 m²**).

SLA nội bộ: Trưởng phòng Pháp chế ký thẩm định trong **07 ngày làm việc** kể từ ngày nhận đủ hồ sơ.

## Phê duyệt và audit

- Mọi upload tài liệu mật ghi audit: `document.upload`, kèm `tenant_id` và `user_id`.
- Đổi role thành viên chỉ **Owner** hoặc **Admin**; bắt buộc ghi audit `member.role`.
- API Key tạo cho tích hợp RPA: scope tối đa `retrieve` + `qa`; không cấp `ingest` trừ khi có ticket IT-SEC.

## Câu hỏi thường gặp (FAQ nội bộ)

**Viewer có được tải lên quyết định thu hồi không?**  
Không. Viewer chỉ chat và search; upload thuộc Contributor.

**Team khác có thấy KB Pháp chế không?**  
Không — isolation theo tenant; tenant khác nhận 404 khi truy cập `kb_id` không thuộc workspace.

## Từ khóa tra cứu

`ho so`, `07 ngay`, `truong phong phap che`, `viewer`, `upload`, `contributor`, `audit`
