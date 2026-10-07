#!/usr/bin/env bash
set -euo pipefail
BASE="${BASE_URL:-http://127.0.0.1:8000}"

echo "== health =="
curl -sf "$BASE/health" | tee /tmp/rae_health.json

echo "== register alice =="
TOKEN=$(curl -sf -X POST "$BASE/auth/register" \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"alice_rag_$(date +%s)@example.com\",\"password\":\"Secret123\",\"username\":\"alice\"}" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["access_token"])')

ME=$(curl -sf "$BASE/auth/me" -H "Authorization: Bearer $TOKEN")
TENANT=$(echo "$ME" | python3 -c 'import sys,json; print(json.load(sys.stdin)["memberships"][0]["tenant_id"])')
echo "tenant=$TENANT"

echo "== create KB =="
KB=$(curl -sf -X POST "$BASE/kb" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Tenant-Id: $TENANT" \
  -H 'Content-Type: application/json' \
  -d '{"name":"Policy","description":"sample"}' \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')
echo "kb=$KB"

echo "== upload sample =="
DOC=$(curl -sf -X POST "$BASE/kb/$KB/documents" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Tenant-Id: $TENANT" \
  -F "file=@testdata/sample-policy.md" \
  -F "title=sample-policy" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')
echo "doc=$DOC"

sleep 1
STATUS=$(curl -sf "$BASE/documents/$DOC" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Tenant-Id: $TENANT" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["parse_status"])')
echo "parse_status=$STATUS"
test "$STATUS" = "completed"

echo "== search =="
curl -sf -X POST "$BASE/search" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Tenant-Id: $TENANT" \
  -H 'Content-Type: application/json' \
  -d "{\"kb_id\":\"$KB\",\"query\":\"bao hanh bao lau\",\"top_k\":3}" | tee /tmp/rae_search.json

echo "== chat =="
curl -sf -X POST "$BASE/chat" \
  -H "Authorization: Bearer $TOKEN" \
  -H "X-Tenant-Id: $TENANT" \
  -H 'Content-Type: application/json' \
  -d "{\"kb_id\":\"$KB\",\"question\":\"Sản phẩm được bảo hành bao nhiêu tháng?\"}" | tee /tmp/rae_chat.json

echo "OK smoke_rag"
