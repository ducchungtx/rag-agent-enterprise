#!/usr/bin/env bash
# Phase 6 — Demo blueprint Pháp chế / Luật Đất đai (API-only).
set -euo pipefail
BASE="${BASE_URL:-http://127.0.0.1:8000}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TS=$(date +%s)

reg() {
  local email=$1 user=$2
  curl -sf -X POST "$BASE/auth/register" \
    -H 'Content-Type: application/json' \
    -d "{\"email\":\"$email\",\"password\":\"Secret123\",\"username\":\"$user\"}" \
    | python3 -c 'import sys,json; print(json.load(sys.stdin)["access_token"])'
}

echo "== health =="
curl -sf "$BASE/health" >/dev/null

echo "== Lead tạo workspace Phòng Pháp chế =="
LEAD_TOKEN=$(reg "lead_$TS@example.com" "lead_phap_che")
TENANT=$(curl -sf -X POST "$BASE/tenants" \
  -H "Authorization: Bearer $LEAD_TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"name":"Phòng Pháp chế"}' \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')
echo "tenant=$TENANT"

echo "== KB Luật Đất đai + Policy =="
KB=$(curl -sf -X POST "$BASE/kb" \
  -H "Authorization: Bearer $LEAD_TOKEN" \
  -H "X-Tenant-Id: $TENANT" \
  -H 'Content-Type: application/json' \
  -d '{"name":"Luật Đất đai + Policy","description":"Corpus lab Pháp chế"}' \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')
echo "kb=$KB"

upload_doc() {
  local path=$1 title=$2
  curl -sf -X POST "$BASE/kb/$KB/documents" \
    -H "Authorization: Bearer $LEAD_TOKEN" \
    -H "X-Tenant-Id: $TENANT" \
    -F "file=@$path" \
    -F "title=$title" \
    | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])'
}

echo "== Ingest corpus: data/docs/*.md + converted/*.txt =="
DOC_IDS=()
while IFS= read -r -d '' f; do
  base=$(basename "$f")
  base="${base%.*}"
  id=$(upload_doc "$f" "$base")
  DOC_IDS+=("$id")
  echo "  uploaded $base -> $id"
done < <({
  find "$ROOT/data/docs" -maxdepth 1 -type f -name '*.md' ! -name 'README.md' -print0
  find "$ROOT/data/docs/converted" -maxdepth 1 -type f -name '*.txt' -print0 2>/dev/null || true
} | sort -z)

test "${#DOC_IDS[@]}" -ge 4
echo "total_docs=${#DOC_IDS[@]}"
sleep 2

for id in "${DOC_IDS[@]}"; do
  st=$(curl -sf "$BASE/documents/$id" \
    -H "Authorization: Bearer $LEAD_TOKEN" \
    -H "X-Tenant-Id: $TENANT" \
    | python3 -c 'import sys,json; print(json.load(sys.stdin)["parse_status"])')
  test "$st" = "completed"
done

echo "== Search (thời hạn đất nông nghiệp 50 năm) =="
curl -sf -X POST "$BASE/search" \
  -H "Authorization: Bearer $LEAD_TOKEN" \
  -H "X-Tenant-Id: $TENANT" \
  -H 'Content-Type: application/json' \
  -d "{\"kb_id\":\"$KB\",\"query\":\"thoi han dat nong nghiep 50 nam\",\"top_k\":3}" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert d["results"], "no search hits"'

echo "== Search (đất ở ổn định lâu dài) =="
curl -sf -X POST "$BASE/search" \
  -H "Authorization: Bearer $LEAD_TOKEN" \
  -H "X-Tenant-Id: $TENANT" \
  -H 'Content-Type: application/json' \
  -d "{\"kb_id\":\"$KB\",\"query\":\"dat o on dinh lau dai dieu 171\",\"top_k\":3}" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert d["results"], "no search hits for dieu 171"'

echo "== Chat citation (SLA nội bộ 07 ngày) =="
curl -sf -X POST "$BASE/chat" \
  -H "Authorization: Bearer $LEAD_TOKEN" \
  -H "X-Tenant-Id: $TENANT" \
  -H 'Content-Type: application/json' \
  -d "{\"kb_id\":\"$KB\",\"question\":\"Trưởng phòng Pháp chế phải ký thẩm định trong bao nhiêu ngày làm việc?\"}" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert d["citations"], "expected citations"'

echo "== Chat citation (NĐ 88 bồi thường) =="
curl -sf -X POST "$BASE/chat" \
  -H "Authorization: Bearer $LEAD_TOKEN" \
  -H "X-Tenant-Id: $TENANT" \
  -H 'Content-Type: application/json' \
  -d "{\"kb_id\":\"$KB\",\"question\":\"Nghị định nào quy định bồi thường hỗ trợ tái định cư khi Nhà nước thu hồi đất?\"}" \
  | python3 -c 'import sys,json; d=json.load(sys.stdin); assert d["citations"], "expected citations for ND 88"'

echo "== Mời nhân viên Viewer =="
VIEWER_TOKEN=$(reg "viewer_$TS@example.com" "nhan_vien")
curl -sf -X POST "$BASE/tenants/$TENANT/members/invite" \
  -H "Authorization: Bearer $LEAD_TOKEN" \
  -H "X-Tenant-Id: $TENANT" \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"viewer_$TS@example.com\",\"role\":\"viewer\"}" >/dev/null

curl -sf -X POST "$BASE/chat" \
  -H "Authorization: Bearer $VIEWER_TOKEN" \
  -H "X-Tenant-Id: $TENANT" \
  -H 'Content-Type: application/json' \
  -d "{\"kb_id\":\"$KB\",\"question\":\"Viewer có được upload không?\"}" >/dev/null

CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/kb/$KB/documents" \
  -H "Authorization: Bearer $VIEWER_TOKEN" \
  -H "X-Tenant-Id: $TENANT" \
  -F "file=@$ROOT/data/docs/chinh-sach-noi-bo-dat-dai.md")
test "$CODE" = "403"

echo "== Tenant khác không thấy KB =="
OTHER=$(reg "other_$TS@example.com" "team_khac")
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/chat" \
  -H "Authorization: Bearer $OTHER" \
  -H 'Content-Type: application/json' \
  -d "{\"kb_id\":\"$KB\",\"question\":\"test isolation\"}")
test "$CODE" = "404"

echo "OK demo_phap_che — blueprint Pháp chế / Luật Đất đai"
