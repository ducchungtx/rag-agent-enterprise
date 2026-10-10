# 06 — UI Brief (AI-ready)

> Copy **toàn bộ file này** (hoặc khối 「PROMPT GỐC」 cuối trang) vào Figma AI / Galileo / Stitch / v0 / Lovable / Cursor để sinh wireframe hoặc high-fidelity mockup.  
> Mục tiêu: UI **doanh nghiệp pháp chế**, không còn kiểu form lab xếp dọc.

---

## PROMPT GỐC (paste thẳng vào AI thiết kế)

```text
Thiết kế UI web app B2B tiếng Việt cho sản phẩm RAG doanh nghiệp tên "rae" (rag-agent-enterprise).

BỐI CẢNH SẢN PHẨM
- Trợ lý hỏi-đáp nội bộ cho phòng Pháp chế / Luật Đất đai.
- Người dùng: chuyên viên pháp chế (hỏi hàng ngày), lead pháp chế (quản lý KB + member), IT (API key).
- Rủi ro trả lời sai RẤT CAO → mọi câu trả lời phải có citation; thiếu nguồn phải TỪ CHỐI, không bịa.
- Mô hình dữ liệu: User thuộc nhiều Workspace (Tenant). Mỗi Workspace có nhiều Knowledge Base (KB). Mỗi KB chứa Document. Chat/search luôn trong phạm vi Workspace + (một hoặc nhiều) KB được phép.
- KB KHÔNG phải túi file: mỗi KB = một miền (vd "Luật Đất đai", "Policy nội bộ đất đai", "Hôn nhân gia đình" tách riêng). Chọn sai KB là lỗi UX nếu vẫn trả lời.

NGUYÊN TẮC UX BẮT BUỘC
1. Luôn hiện rõ phạm vi đang hỏi: Workspace name + KB name + mô tả ngắn phạm vi (domain).
2. Chọn KB phải thấy description / domain / số tài liệu — không chỉ dropdown tên.
3. Khi relevance thấp hoặc lệch miền: màn hình từ chối rõ ràng + gợi ý đổi KB (không giả vờ có câu trả lời).
4. Citation là công dân hạng nhất: danh sách nguồn với title, đoạn trích, link/mở document — không giấu dưới fold.
5. Không dashboard nhồi stats. Một composition rõ cho từng màn. Brand "rae" là tín hiệu hero-level trên auth/landing, không chỉ chữ nhỏ trên nav.
6. Desktop-first (1280–1440), có mobile đọc được. Light mode. Tone chuyên nghiệp, pháp lý, tin cậy — tránh purple gradient, dark neon, pill spam, emoji.

THÔNG TIN KIẾN TRÚC MÀN HÌNH (thiết kế đủ)
A. Auth (Login / Register)
B. Shell app sau login: topbar (brand rae, user, workspace switcher) + sidebar hoặc primary nav
C. Chọn / quản lý Workspace
D. Knowledge Bases — list + create + detail (documents, upload, domain/description)
E. Chat workspace — hỏi đáp chính (Chat thường + mode Agent), scope bar, citations panel, refusal state
F. (Tuỳ chọn secondary) Members / Roles; API Keys — chỉ wireframe nhẹ

DỮ LIỆU MẪU HIỂN THỊ
- Workspace: "Phòng Pháp chế"
- User: an@demo.local · role Owner
- KB list:
  - "Luật Đất đai" · domain đất đai · 12 docs · active
  - "Policy nội bộ đất đai" · domain policy · 3 docs · active
  - "Hôn nhân gia đình" · domain HN-GĐ · 8 docs · active (để minh họa chọn sai)
- Câu hỏi mẫu: "Thời hạn sử dụng đất nông nghiệp của cá nhân trực tiếp sản xuất là bao lâu?"
- Câu trả lời mẫu ngắn kèm 2 citations (NĐ/điều giả định)
- State từ chối: user chọn KB "Hôn nhân gia đình" + hỏi đất đai → banner "Không đủ nguồn phù hợp trong KB đang chọn" + CTA "Đổi sang Luật Đất đai"

PHONG CÁCH
- Font: display serif tinh tế (kiểu Fraunces) cho brand/heading; body sans (Source Sans / tương đương).
- Màu: mực xanh-xám đậm (#13212B), accent teal (#0F7A6C), nền paper xanh nhạt, cảnh báo nâu (#9A4B1A), danger đỏ đất (#8B2E2E).
- Nền có gradient/atmosphere nhẹ, không flat trắng tuyệt đối.
- Ít card; card chỉ khi cần chứa tương tác. Không hero overlay sticker.

OUTPUT MONG MUỐN
1) Wireframe hoặc hi-fi cho các màn A–E (ưu tiên E Chat + D KB list/detail).
2) Một frame riêng "Chat — Refusal lệch miền".
3) Ghi chú annotation ngắn trên mỗi frame: mục đích + thành phần bắt buộc.
```

---

## 1. Product one-liner

**rae** — trợ lý RAG nội bộ cho pháp chế: hỏi trong đúng Workspace + đúng Knowledge Base, trả lời có citation, từ chối khi thiếu nguồn.

## 2. Personas

| Persona | Việc chính trên UI | Không cần |
|---------|-------------------|-----------|
| Chuyên viên (Viewer/Contributor) | Chọn WS → chọn KB → Chat → đọc citation | Quản trị sâu |
| Lead Pháp chế (Owner/Admin) | Tạo KB, upload, invite member, xem audit nhẹ | Config LLM |
| IT / tích hợp | API Keys (capability + kb allowlist) | Chat hàng ngày |

## 3. Khái niệm bắt buộc trên UI (glossary)

| Thuật ngữ UI | Ý nghĩa | Hiển thị gợi ý |
|--------------|---------|----------------|
| Workspace | Biên giới tài nguyên + quyền (= Tenant) | Switcher trên topbar |
| Knowledge Base (KB) | Kho theo **miền** trong workspace | List có domain + mô tả |
| Document | File đã ingest trong KB | List + trạng thái parse |
| Phạm vi hỏi (scope) | WS + KB đang active | Scope bar dính trên Chat |
| Citation | Đoạn nguồn dùng để trả lời | Panel bên phải hoặc dưới answer |
| Từ chối (refusal) | Không đủ nguồn / lệch miền | Empty-state có CTA đổi KB |
| Agent | Chat có tool search + SSE | Toggle hoặc tab cạnh Chat |

## 4. Information architecture

```text
rae
├── Auth
│   ├── Đăng nhập
│   └── Đăng ký
└── App shell
    ├── Workspace switcher (global)
    ├── Knowledge
    │   ├── Danh sách KB
    │   ├── Tạo KB (name, description, domain)
    │   └── Chi tiết KB → Documents + Upload
    ├── Chat
    │   ├── Scope bar (WS + KB + mô tả)
    │   ├── Composer (Chat | Agent)
    │   ├── Answer
    │   ├── Citations
    │   └── Refusal state
    ├── Thành viên (secondary)
    └── API Keys (secondary)
```

## 5. Spec từng màn (để AI vẽ đúng)

### A — Auth

- Brand **rae** lớn (hero-level), sub: “Trợ lý pháp chế · có citation”.
- Form: email, password; đăng ký thêm username.
- Không nhồi feature list dài trên viewport đầu.

### B — App shell

- Topbar: mark `rae` | tên product ngắn | **Workspace switcher** | user + role chip | Đăng xuất.
- Nav: Knowledge | Chat | (Members) | (API Keys).
- Chat là đích chính sau khi đã có KB.

### C — Workspace

- List / select workspace hiện có.
- CTA tạo mới (placeholder “Phòng Pháp chế”).
- Sau chọn → persist; mọi màn sau gắn scope này.

### D — Knowledge Bases

**List**

| Cột / khối | Nội dung |
|------------|----------|
| Tên KB | Luật Đất đai |
| Domain tag | đất đai / policy / HN-GĐ |
| Mô tả 1 dòng | Phạm vi + loại trừ |
| Số docs | 12 |
| Status | active / draft |
| Actions | Mở · Dùng để chat |

**Create KB**

- name (bắt buộc)
- description (bắt buộc trên UI mục tiêu — giải thích phạm vi)
- domain (select hoặc text: `dat-dai` | `policy` | `hon-nhan` | khác)
- Gợi ý copy: “Một KB ≈ một miền. Không trộn đất đai với hôn nhân.”

**Detail KB**

- Header: tên + domain + description đầy đủ.
- Upload: md/txt/pdf; log trạng thái pending → processing → completed | failed.
- Document list: title, status, ngày.

### E — Chat (màn quan trọng nhất)

**Layout đề xuất (desktop)**

```text
┌─────────────────────────────────────────────────────────┐
│ Topbar: rae · Workspace [Phòng Pháp chế ▾] · an · Owner │
├─────────────────────────────────────────────────────────┤
│ SCOPE BAR (luôn hiện)                                   │
│ Đang hỏi trong: Luật Đất đai · “NĐ/TT đất đai; …”       │
│ [Đổi KB]  hoặc multi-select KB (mục tiêu P2)            │
├──────────────────────────────┬──────────────────────────┤
│ Thread / Answer              │ Citations                │
│                              │ 1. Title · đoạn · score  │
│                              │ 2. …                     │
│                              │                          │
│ [Refusal banner nếu có]      │                          │
├──────────────────────────────┴──────────────────────────┤
│ Composer: textarea · [Chat] [Agent]                     │
└─────────────────────────────────────────────────────────┘
```

**States bắt buộc phải có mockup**

| State | Khi nào | UI |
|-------|---------|-----|
| Empty | Chưa hỏi | Placeholder câu hỏi mẫu pháp chế |
| Loading | Đang retrieve/LLM | Skeleton answer + “Đang tìm trong KB…” |
| Success | Có nguồn | Answer + ≥1 citation card |
| Refusal | Score thấp / lệch miền | Banner warn + lý do + CTA đổi KB gợi ý |
| Wrong KB selected | User chọn HN-GĐ hỏi đất đai | Giống Refusal; không hiện answer giả |

**Copy mẫu Refusal**

> Không đủ nguồn phù hợp trong **Hôn nhân gia đình** cho câu hỏi về đất đai.  
> Đổi sang KB **Luật Đất đai** hoặc hỏi lại trong đúng miền.

### F — Secondary (wireframe đủ dùng)

- **Members:** list email + role (Viewer/Contributor/Admin/Owner) + invite.
- **API Keys:** name, capabilities chips (`retrieve` `qa` `ingest`), kb allowlist.

## 6. User flows cần minh họa

```text
Flow 1 — Happy path
Login → chọn Workspace "Phòng Pháp chế" → chọn KB "Luật Đất đai"
→ hỏi thời hạn đất → Answer + Citations

Flow 2 — Lệch miền (story bán sản phẩm)
Login → WS Pháp chế → chọn nhầm KB "Hôn nhân gia đình"
→ hỏi thời hạn đất → Refusal + CTA "Luật Đất đai"

Flow 3 — Thêm corpus
KB detail → Upload PDF/MD → status completed → quay lại Chat

Flow 4 — Multi-KB (mục tiêu, ghi “Phase sau”)
Scope bar chọn 2 KB đất đai + policy → một câu hỏi tổng hợp
→ Citations gắn tên KB nguồn
```

## 7. Design tokens (khớp UI lab hiện có — có thể tinh chỉnh)

| Token | Giá trị |
|-------|---------|
| Ink | `#13212B` |
| Ink soft | `#2A3D4A` |
| Paper | `#EEF3F1` |
| Panel | `#F7FAF8` |
| Line | `#C5D4CC` |
| Accent | `#0F7A6C` |
| Accent deep | `#0A554B` |
| Warn | `#9A4B1A` |
| Danger | `#8B2E2E` |
| Radius | 10–12px |
| Display font | Fraunces / tương đương serif |
| Body font | Source Sans 3 / tương đương |

**Tránh:** purple-on-white, cream+terracotta cliché, dark neon glow, pill cluster, multi-shadow, emoji.

## 8. Nội dung giả lập (lorem pháp chế)

**Câu hỏi**

- Thời hạn sử dụng đất nông nghiệp của cá nhân trực tiếp sản xuất là bao lâu?
- Điều kiện chuyển nhượng đất ở?
- Nghị định 88 quy định gì về …?

**Answer ngắn**

> Theo nguồn trong KB Luật Đất đai, thời hạn sử dụng đất nông nghiệp của cá nhân trực tiếp sản xuất là **50 năm** (trích dẫn bên cạnh). Đây không phải tư vấn pháp lý chính thức.

**Citation card**

- Title: `tóm tắt-luat-dat-dai.md`
- Snippet: “Thời hạn … 50 năm …”
- Meta: KB Luật Đất đai · score 0.82

## 9. Checklist nghiệm thu mockup

- [ ] Brand `rae` đủ mạnh trên auth
- [ ] Workspace luôn thấy được khi đã login
- [ ] KB list có domain + description, không chỉ tên
- [ ] Chat có scope bar
- [ ] Có frame Refusal lệch miền
- [ ] Citations là vùng nhìn thấy ngay khi có answer
- [ ] Không nhầm thành “ChatGPT clone” generic thiếu scope KB
- [ ] Tiếng Việt nhất quán

## 10. Ngoài phạm vi vẽ (đừng xin AI thêm)

- Wiki / GraphRAG / IM chatbot
- Editor soạn thảo văn bản pháp quy
- Billing / marketplace
- Dark mode mặc định
- Mobile app native

## Tham chiếu repo

- Gap KB & DoD: [05-kb-vuot-demo.md](./05-kb-vuot-demo.md)
- Blueprint: [01-blueprint.md](./01-blueprint.md)
- UI lab hiện tại: `web/index.html`, `web/styles.css`
