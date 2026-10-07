# Bản convert `.txt` (để ingest RAG)

Nguồn: `../Van-ban-huong-dan-Luat-Dat-dai/` (file `.doc` gốc). Convert bằng `textutil` trên macOS.

| File | Nội dung gần đúng |
|------|-------------------|
| `88_2024_ND-CP_*.txt` | Bồi thường, hỗ trợ, tái định cư |
| `102_2024_ND-CP_*.txt` | Hướng dẫn chi tiết Luật Đất đai |
| `101_2024_ND-CP_*.txt` | Nghị định liên quan đất đai (cùng đợt) |
| `103_2024_ND-CP_*.txt` | Nghị định liên quan đất đai (cùng đợt) |
| `71_2024_ND-CP_*.txt` | Nghị định liên quan |
| `112_2024_ND-CP_*.txt` | Nghị định liên quan |
| `08–11_2024_TT-BTNMT_*.txt` | Thông tư BTNMT hướng dẫn |

Convert lại (nếu thêm `.doc` mới):

```bash
textutil -convert txt -output data/docs/converted/ten.txt path/toi/file.doc
```
