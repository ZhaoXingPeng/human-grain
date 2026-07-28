#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
test -f "$root/SKILL.md"
test -f "$root/agents/openai.yaml"
test -f "$root/THREE-ROUNDS.md"
test -f "$root/examples/before.md"
test -f "$root/examples/after.md"
grep -q 'name: human-grain-writer' "$root/SKILL.md"
grep -q '三轮' "$root/SKILL.md"
grep -q 'repair' "$root/SKILL.md"
grep -q 'Markdown' "$root/SKILL.md"
echo "human-grain skill structure: ok"
