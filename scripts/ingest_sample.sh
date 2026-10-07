#!/usr/bin/env bash
# Ingest testdata/sample-policy.md vào KB hiện có (hoặc tạo mới).
# Corpus Luật Đất đai (.doc) cần LibreOffice convert → .txt trước; lab dùng sample.md.
set -euo pipefail
BASE="${BASE_URL:-http://127.0.0.1:8000}"
FILE="${1:-testdata/sample-policy.md}"
TS=$(date +%s)
TOKEN=$(curl -sf -X POST "$BASE/auth/register" \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"ingest_$TS@example.com\",\"password\":\"Secret123\",\"username\":\"ingest\"}" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["access_token"])')
TENANT=$(curl -sf "$BASE/auth/me" -H "Authorization: Bearer $TOKEN" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["memberships"][0]["tenant_id"])')
KB=$(curl -sf -X POST "$BASE/kb" \
  -H "Authorization: Bearer $TOKEN" -H "X-Tenant-Id: $TENANT" \
  -H 'Content-Type: application/json' -d '{"name":"Corpus"}' \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')
DOC=$(curl -sf -X POST "$BASE/kb/$KB/documents" \
  -H "Authorization: Bearer $TOKEN" -H "X-Tenant-Id: $TENANT" \
  -F "file=@$FILE" | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')
echo "tenant=$TENANT kb=$KB doc=$DOC file=$FILE"
