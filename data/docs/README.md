# Corpus học tập — Pháp chế / Luật Đất đai

Ba lớp tài liệu:

| Lớp | Đường dẫn | Dùng khi |
|-----|-----------|----------|
| Tóm tắt + FAQ (`.md`) | thư mục này | Demo nhanh, câu hỏi điển hình |
| Văn bản convert (`.txt`) | [`converted/`](./converted/) | RAG đầy đủ hơn (đã convert từ `.doc`) |
| Gốc `.doc` | [`Van-ban-huong-dan-Luat-Dat-dai/`](./Van-ban-huong-dan-Luat-Dat-dai/) | Lưu trữ / convert lại |

**Không** dùng corpus lab thay văn bản chính thống khi tư vấn thật.

## Tóm tắt lab (`.md`)

| File | Mục đích |
|------|----------|
| `luat-dat-dai-2024-thoi-han.md` | Điều 171–172: ổn định lâu dài vs 50/70/99 năm |
| `luat-dat-dai-2024-chuyen-muc-dich.md` | Điều 173–174: chuyển mục đích / nhận chuyển quyền |
| `nd-88-2024-boi-thuong-tai-dinh-cu.md` | NĐ 88/2024 — tóm tắt bồi thường / TĐC |
| `nd-102-2024-huong-dan.md` | NĐ 102/2024 — khung hướng dẫn |
| `faq-tra-cuu-dat-dai.md` | Câu hỏi–đáp mẫu |
| `tom-tat-quy-dinh-su-dung-dat-lab.md` | Bản rút gọn (tương thích demo cũ) |
| `chinh-sach-noi-bo-dat-dai.md` | Quy trình nội bộ phòng Pháp chế |

## Nguồn tham chiếu công khai

- Luật 31/2024/QH15 — [VBPL](https://vbpl.moj.gov.vn/), [Wikisource Ch. XIII](https://vi.wikisource.org/wiki/Lu%E1%BA%ADt_%C4%90%E1%BA%A5t_%C4%91ai_n%C6%B0%E1%BB%9Bc_C%E1%BB%99ng_h%C3%B2a_x%C3%A3_h%E1%BB%99i_ch%E1%BB%A7_ngh%C4%A9a_Vi%E1%BB%87t_Nam_2024/Ch%C6%B0%C6%A1ng_XIII)
- NĐ 88/2024 — [Công báo](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-88-2024-nd-cp-42343/51007.htm)
- NĐ 102/2024 — [Công báo](https://congbao.chinhphu.vn/van-ban/nghi-dinh-so-102-2024-nd-cp-42485.htm)

Demo: `make demo-phap-che` (ingest `.md` + `converted/*.txt`).
