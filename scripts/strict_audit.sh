#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
fail(){ echo "FAIL: $1" >&2; exit 1; }
pass(){ echo "PASS: $1"; }

echo "Human Grain strict audit"

# Loop 1: contract and routing checks.
grep -q '三轮处理' "$root/SKILL.md" || fail 'three-round contract missing'
for mode in draft rewrite repair variant notes-to-doc; do
  grep -q "\`$mode\`" "$root/SKILL.md" || fail "mode missing: $mode"
done
grep -q '不改变原文事实' "$root/SKILL.md" || fail 'semantic guard missing'
grep -q '粗糙度刻度' "$root/SKILL.md" || fail 'roughness scale missing'
pass 'loop 1 / contract and routing'

# Loop 2: safety and Markdown behavior checks.
grep -q '代码围栏、链接、表格分隔线' "$root/SKILL.md" || fail 'markdown guard missing'
grep -q '医疗、法律、财务、安全' "$root/SKILL.md" || fail 'sensitive-domain guard missing'
grep -q '不要使用：连续乱码' "$root/references/roughness.md" || fail 'anti-random-noise guard missing'
grep -q 'token snapshot' "$root/SKILL.md" || fail 'protected token snapshot missing'
grep -q '噪声台账' "$root/SKILL.md" || fail 'noise ledger contract missing'
pass 'loop 2 / safety and format'

# Loop 3: five scenario fixtures and output trace checks.
for n in 01-draft 02-rewrite 03-repair 04-variant 05-notes-to-doc; do
  in_file="$root/tests/cases/$n-input.md"
  out_file="$root/tests/cases/$n-output.md"
  test -s "$in_file" || fail "$n input missing"
  test -s "$out_file" || fail "$n output missing"
  grep -q '^模式：' "$out_file" || fail "$n mode trace missing"
  grep -q '处理记录：' "$out_file" || fail "$n processing trace missing"
  grep -q '第 1 轮' "$out_file" || fail "$n loop 1 trace missing"
  grep -q '第 2 轮' "$out_file" || fail "$n loop 2 trace missing"
  grep -q '第 3 轮' "$out_file" || fail "$n loop 3 trace missing"
done
grep -q 'v1.4.2' "$root/tests/cases/03-repair-output.md" || fail 'repair changed version'
grep -q '林夏' "$root/tests/cases/03-repair-output.md" || fail 'repair changed owner'
grep -q '目标读者：项目组成员' "$root/tests/cases/04-variant-input.md" || fail 'variant reader context missing'
grep -q 'profile：extreme' "$root/examples/extreme.md" || fail 'extreme profile example missing'
grep -q '噪声台账：' "$root/examples/extreme.md" || fail 'extreme noise ledger missing'
for trace_file in "$root/examples/rounds/01-input.md" "$root/examples/rounds/01-round-1-strip.md" "$root/examples/rounds/01-round-2-friction.md" "$root/examples/rounds/01-round-3-grain.md" "$root/examples/rounds/TRACE.md"; do
  test -s "$trace_file" || fail "canonical round trace missing: $trace_file"
done
grep -q '格式台账：轮次 3' "$root/examples/rounds/01-round-3-grain.md" || fail 'round 3 format ledger missing'
pass 'loop 3 / five core fixtures and two regressions'

python3 "$root/scripts/validate_markdown.py" || fail 'markdown fixture validation'

audit_tmp="$(mktemp -d "${TMPDIR:-/tmp}/human-grain-audit.XXXXXX")"
trap 'rm -rf "$audit_tmp"' EXIT
for n in 01-draft 02-rewrite 03-repair 04-variant 05-notes-to-doc 06-protected 07-safe; do
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
pass 'round 1 / AI-tell reports and score comparison for seven fixtures'

echo "RESULT: 3 audit loops, 5 core document cases, 2 protection regressions passed"
