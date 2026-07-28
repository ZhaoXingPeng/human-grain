#!/usr/bin/env python3
"""Minimal CI-safe metadata checks without third-party YAML dependencies."""
from pathlib import Path
import re


root = Path(__file__).resolve().parents[1]
skill = (root / "SKILL.md").read_text()
yaml = (root / "agents/openai.yaml").read_text()
if not skill.startswith("---\n"):
    raise SystemExit("SKILL.md front matter missing")
if not re.search(r"(?m)^name:\s*[a-z0-9-]+$", skill):
    raise SystemExit("invalid skill name")
description = re.search(r'(?m)^description:\s*"(.*)"$', skill)
if not description or len(description.group(1)) < 40:
    raise SystemExit("description too short")
if "$human-grain-writer" not in yaml:
    raise SystemExit("openai default prompt missing skill trigger")
if not re.search(r'(?m)^\s+display_name:', yaml):
    raise SystemExit("display name missing")
print("skill metadata: ok")
