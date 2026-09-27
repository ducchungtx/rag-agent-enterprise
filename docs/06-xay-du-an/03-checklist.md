# 03 — Checklist trước demo / thử nghiệm nội bộ

## Chức năng

- [ ] Đăng ký / đăng nhập / refresh  
- [ ] Tạo workspace, mời user, đổi role  
- [ ] CRUD KB đúng quyền  
- [ ] Upload → completed → search hit  
- [ ] Chat có citation  
- [ ] Agent gọi tool, không vượt max_steps  
- [ ] API Key theo capability  

## Bảo mật

- [ ] Cross-tenant IDOR tests xanh  
- [ ] Viewer bị chặn ingest  
- [ ] Không log secret  
- [ ] Rate limit login  

## Vận hành

- [ ] `docker compose up` documented  
- [ ] Backup Postgres thử restore 1 lần  
- [ ] Healthcheck + migrate  

## Quan sát

- [ ] Có `request_id` trên response/error  
- [ ] Job fail nhìn thấy được (status/UI/log)  

## Tài liệu giao cho đồng nghiệp

- [ ] README chạy local  
- [ ] Ma trận role 1 trang  
- [ ] 5 câu hỏi mẫu + tài liệu nguồn  

---

Khi checklist đủ: bạn đã có **nền** để mở rộng theo hướng WeKnora (Wiki, MCP, sandbox…) một cách có chủ đích — không copy mù.
