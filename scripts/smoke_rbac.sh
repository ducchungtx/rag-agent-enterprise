#!/usr/bin/env bash
set -euo pipefail
BASE="${BASE_URL:-http://127.0.0.1:8000}"
TS=$(date +%s)

reg() {
  local email=$1 user=$2
  curl -sf -X POST "$BASE/auth/register" \
    -H 'Content-Type: application/json' \
    -d "{\"email\":\"$email\",\"password\":\"Secret123\",\"username\":\"$user\"}" \
    | python3 -c 'import sys,json; print(json.load(sys.stdin)["access_token"])'
}

echo "== Alice owner =="
ALICE_TOKEN=$(reg "alice_$TS@example.com" "alice")
ALICE_TENANT=$(curl -sf "$BASE/auth/me" -H "Authorization: Bearer $ALICE_TOKEN" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["memberships"][0]["tenant_id"])')

echo "== Bob register then invite as viewer =="
BOB_TOKEN=$(reg "bob_$TS@example.com" "bob")
curl -sf -X POST "$BASE/tenants/$ALICE_TENANT/members/invite" \
  -H "Authorization: Bearer $ALICE_TOKEN" \
  -H "X-Tenant-Id: $ALICE_TENANT" \
  -H 'Content-Type: application/json' \
  -d "{\"email\":\"bob_$TS@example.com\",\"role\":\"viewer\"}" >/dev/null

KB=$(curl -sf -X POST "$BASE/kb" \
  -H "Authorization: Bearer $ALICE_TOKEN" \
  -H "X-Tenant-Id: $ALICE_TENANT" \
  -H 'Content-Type: application/json' \
  -d '{"name":"RBAC KB"}' \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')

curl -sf -X POST "$BASE/kb/$KB/documents" \
  -H "Authorization: Bearer $ALICE_TOKEN" \
  -H "X-Tenant-Id: $ALICE_TENANT" \
  -F "file=@testdata/sample-policy.md" >/dev/null
sleep 1

echo "== Bob viewer chat OK =="
curl -sf -X POST "$BASE/chat" \
  -H "Authorization: Bearer $BOB_TOKEN" \
  -H "X-Tenant-Id: $ALICE_TENANT" \
  -H 'Content-Type: application/json' \
  -d "{\"kb_id\":\"$KB\",\"question\":\"bao hanh?\"}" >/dev/null

echo "== Bob viewer upload 403 =="
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/kb/$KB/documents" \
  -H "Authorization: Bearer $BOB_TOKEN" \
  -H "X-Tenant-Id: $ALICE_TENANT" \
  -F "file=@testdata/sample-policy.md")
test "$CODE" = "403"

echo "== Promote Bob to contributor =="
BOB_ID=$(curl -sf "$BASE/auth/me" -H "Authorization: Bearer $BOB_TOKEN" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["id"])')
curl -sf -X PATCH "$BASE/tenants/$ALICE_TENANT/members/$BOB_ID" \
  -H "Authorization: Bearer $ALICE_TOKEN" \
  -H "X-Tenant-Id: $ALICE_TENANT" \
  -H 'Content-Type: application/json' \
  -d '{"role":"contributor"}' >/dev/null

CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/kb/$KB/documents" \
  -H "Authorization: Bearer $BOB_TOKEN" \
  -H "X-Tenant-Id: $ALICE_TENANT" \
  -F "file=@testdata/sample-policy.md")
test "$CODE" = "200"

echo "== Carol other tenant cannot see KB =="
CAROL_TOKEN=$(reg "carol_$TS@example.com" "carol")
CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/chat" \
  -H "Authorization: Bearer $CAROL_TOKEN" \
  -H 'Content-Type: application/json' \
  -d "{\"kb_id\":\"$KB\",\"question\":\"hi\"}")
test "$CODE" = "404"

echo "== API Key retrieve only =="
RAW=$(curl -sf -X POST "$BASE/api-keys" \
  -H "Authorization: Bearer $ALICE_TOKEN" \
  -H "X-Tenant-Id: $ALICE_TENANT" \
  -H 'Content-Type: application/json' \
  -d "{\"name\":\"retr\",\"capabilities\":[\"retrieve\"],\"kb_allowlist\":[\"$KB\"]}" \
  | python3 -c 'import sys,json; print(json.load(sys.stdin)["raw_key"])')

CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/search" \
  -H "X-API-Key: $RAW" \
  -H 'Content-Type: application/json' \
  -d "{\"kb_id\":\"$KB\",\"query\":\"bao hanh\"}")
test "$CODE" = "200"

CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "$BASE/chat" \
  -H "X-API-Key: $RAW" \
  -H 'Content-Type: application/json' \
  -d "{\"kb_id\":\"$KB\",\"question\":\"bao hanh?\"}")
test "$CODE" = "403"

echo "OK smoke_rbac"
