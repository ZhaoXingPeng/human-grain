#!/usr/bin/env python3
"""Dependency-free, deliberately small round-1 AI-tell report."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


PATTERNS = {
    "filler": [
        r"在[^。\n]{0,18}背景下",
        r"旨在",
        r"全面提升",
        r"高效闭环",
        r"赋能",
        r"值得注意的是",
        r"综上所述",
        r"delve",
        r"leverage",
        r"furthermore",
        r"moreover",
        r"in conclusion",
    ],
    "hedging": [r"需要指出的是", r"it is important to note", r"one might argue"],
    "generic": [r"多维度", r"系统化", r"标准化流程", r"significantly improved"],
}


def score(text: str) -> dict[str, int]:
    body = text
    if body.startswith("---\n"):
        end = body.find("\n---", 4)
        if end >= 0:
            body = body[end + 4 :]
    body = re.sub(r"(?m)^(?:模式：|处理记录：|噪声台账：|格式台账：).*$", "", body)
    body = re.sub(r"(?ms)^```.*?^```", "", body)
    result = {key: sum(len(re.findall(pattern, body, flags=re.I)) for pattern in patterns) for key, patterns in PATTERNS.items()}
    result["hits"] = [
        {"category": key, "match": match.group(0), "start": match.start()}
        for key, patterns in PATTERNS.items()
        for pattern in patterns
        for match in re.finditer(pattern, body, flags=re.I)
    ]
    sentences = [x.strip() for x in re.split(r"[。！？!?\n]+", body) if x.strip()]
    lengths = [len(x) for x in sentences]
    result["uniform_rhythm"] = int(len(lengths) >= 4 and max(lengths) - min(lengths) <= 8)
    result["total"] = sum(result[key] for key in PATTERNS) + result["uniform_rhythm"]
    return result


if __name__ == "__main__":
    path = Path(sys.argv[1])
    print(json.dumps(score(path.read_text()), ensure_ascii=False, indent=2))
