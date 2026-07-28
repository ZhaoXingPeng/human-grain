#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
fail(){ echo "FAIL: $1" >&2; exit 1; }
pass(){ echo "PASS: $1"; }

echo "Human Grain strict audit"

grep -q '三次内部检查' "$root/SKILL.md" || fail 'internal review workflow missing'
for mode in draft rewrite repair variant notes-to-doc; do
  grep -q "\`$mode\`" "$root/SKILL.md" || fail "mode missing: $mode"
done
grep -q '不改事实' "$root/SKILL.md" || fail 'semantic guard missing'
grep -q '粗糙度' "$root/SKILL.md" || fail 'roughness guidance missing'
grep -q '默认输出正文，不加模式行' "$root/SKILL.md" || fail 'anti-ledger output rule missing'
grep -q '反引号和波浪号代码围栏' "$root/SKILL.md" || fail 'variable fence guard missing'
grep -q '参考链接' "$root/SKILL.md" || fail 'reference link guard missing'
grep -q 'pre-2019-corpus' "$root/SKILL.md" || fail 'corpus reference missing'
pass 'contract, corpus and protection rules'

test "$(wc -l < "$root/references/pre-2019-corpus.md")" -ge 50 || fail 'corpus audit too short'
test "$(rg -c '^\| [0-9]+ \|' "$root/references/pre-2019-corpus.md")" -eq 20 || fail 'corpus does not list 20 samples'
pass '20-source pre-2019 corpus record'

for n in 01-draft 02-rewrite 03-repair 04-variant 05-notes-to-doc 06-protected 07-safe 08-extreme; do
  test -s "$root/tests/cases/$n-input.md" || fail "$n input missing"
  test -s "$root/tests/cases/$n-output.md" || fail "$n output missing"
done
for phrase in '模式：' '处理记录：' '噪声台账：' '格式台账：' '先说背景' '先说清楚' '先记一下' '先弄个' '这里故意' '闭环以后再说' '这份稿子不漂亮'; do
  if rg -n "$phrase" "$root/tests/cases" "$root/examples"; then
    fail "fixed format recipe remains: $phrase"
  fi
done
pass 'fixtures reject format theatre and fixed phrases'

python3 "$root/scripts/validate_markdown.py" || fail 'markdown fixture validation'
pass 'Markdown protection regression, including tilde and variable fences'

audit_tmp="$(mktemp -d "${TMPDIR:-/tmp}/human-grain-audit.XXXXXX")"
trap 'rm -rf "$audit_tmp"' EXIT
for n in 01-draft 02-rewrite 03-repair 04-variant 05-notes-to-doc 06-protected 07-safe 08-extreme; do
  python3 "$root/scripts/ai_tell_report.py" "$root/tests/cases/$n-input.md" > "$audit_tmp/before-$n.json"
  python3 "$root/scripts/ai_tell_report.py" "$root/tests/cases/$n-output.md" > "$audit_tmp/after-$n.json"
done
python3 - "$audit_tmp" <<'PY' || fail 'AI-tell score did not improve or hold'
import json
import pathlib
import sys

root = pathlib.Path(sys.argv[1])
for before in root.glob('before-*.json'):
    after = root / before.name.replace('before-', 'after-')
    b = json.loads(before.read_text())['total']
    a = json.loads(after.read_text())['total']
    if a > b:
        raise SystemExit(f'{before.stem}: before={b}, after={a}')
PY
pass 'AI-tell scores hold or improve for eight fixtures'

echo "RESULT: corpus, structure, protection and anti-template checks passed"
