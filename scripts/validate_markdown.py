#!/usr/bin/env python3
"""Small dependency-free checks for the repository's Markdown fixtures."""
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    return text[: end + 4] if end >= 0 else ""


def fenced_blocks(text: str) -> list[str]:
    return [block.rstrip() for block in re.findall(r"(?ms)^(```[^\n]*\n.*?^```\s*)", text)]


def link_definitions(text: str) -> list[str]:
    return re.findall(r"(?m)^\s{0,3}\[[^\]]+\]:\s+\S+.*$", text)


def protected_tokens(text: str) -> list[str]:
    tokens = []
    tokens.extend([frontmatter(text)])
    tokens.extend(fenced_blocks(text))
    tokens.extend(link_definitions(text))
    tokens.extend(re.findall(r"!?\[[^\]]+\]\([^\n)]+\)", text))
    tokens.extend(re.findall(r"(?m)^\s{0,3}\[\^[^\]]+\]:.*$", text))
    tokens.extend(re.findall(r"(?ms)<!--.*?-->", text))
    tokens.extend(re.findall(r"(?ms)^```(?:mermaid|math).*?^```", text))
    tokens.extend(re.findall(r"!\[[^\]]*\]\([^\n)]+\)", text))
    tokens.extend(re.findall(r"(?ms)<table\b.*?</table>", text, flags=re.I))
    tokens.extend(re.findall(r"(?m)^\s*[-*+] \[[ xX]\] .*|^\s*\d+[.)] .*", text))
    return [token for token in tokens if token]


def sentence_lengths(text: str) -> list[int]:
    body = re.sub(r"(?ms)^```.*?^```", "", text)
    chunks = re.split(r"[。！？!?\n]+", body)
    return [len(x.strip()) for x in chunks if x.strip()]


def check_noise_ledger(input_text: str, output_text: str, name: str) -> None:
    ledger = re.search(r"原词[“\"]([^”\"]+)[”\"]\s*→\s*[“\"]([^”\"]+)[”\"]", output_text)
    if not ledger:
        return
    original, variant = ledger.groups()
    body = output_text.split("处理记录：", 1)[0]
    if original not in input_text:
        raise AssertionError(f"{name}: ledger original is not in input")
    if variant not in body:
        raise AssertionError(f"{name}: ledger variant is not in output body")
    eligible = len(re.sub(r"(?ms)^```.*?^```", "", body))
    buckets = max(1, (eligible + 499) // 500)
    if len(re.findall(r"原词[“\"]", output_text)) > buckets * 5:
        raise AssertionError(f"{name}: typo ledger exceeds roughness budget")


def check_case(name: str) -> None:
    input_text = (ROOT / "tests/cases" / f"{name}-input.md").read_text()
    output_text = (ROOT / "tests/cases" / f"{name}-output.md").read_text()
    if not output_text.strip():
        raise AssertionError(f"{name}: empty output")
    if "处理记录：" not in output_text or "噪声台账：" not in output_text or "格式台账：" not in output_text:
        raise AssertionError(f"{name}: missing trace or noise ledger")
    check_noise_ledger(input_text, output_text, name)
    lengths = sentence_lengths(output_text)
    if len(lengths) < 2 or max(lengths) - min(lengths) < 4:
        raise AssertionError(f"{name}: no sentence/paragraph rhythm variation")
    is_safe_or_repair = name in {"03-repair", "06-protected", "07-safe"}
    if is_safe_or_repair:
        if frontmatter(input_text) != frontmatter(output_text):
            raise AssertionError(f"{name}: front matter changed")
        if name == "03-repair" and ("v1.4.2" not in output_text or "林夏" not in output_text):
            raise AssertionError("03-repair: protected fields changed")
        if name != "07-safe" and "保留了原 Markdown 结构" not in output_text:
            raise AssertionError(f"{name}: missing explicit no-op format record")
        if name == "07-safe" and "保持代码块原样" not in output_text:
            raise AssertionError("07-safe: missing safe record")
        for token in protected_tokens(input_text):
            if token not in output_text:
                raise AssertionError(f"{name}: protected token lost: {token[:40]}")
        source_tokens = protected_tokens(input_text)
        result_tokens = protected_tokens(output_text)
        cursor = 0
        for token in source_tokens:
            try:
                cursor = result_tokens.index(token, cursor) + 1
            except ValueError as exc:
                raise AssertionError(f"{name}: protected token order changed") from exc
    else:
        # New drafts/rewrites/variants must show at least two distinct,
        # intentional and parseable format moves. Repair is allowed to keep
        # structure when the requested range is content-only.
        body = output_text.split("处理记录：", 1)[0]
        moves = {
            "quote": bool(re.search(r"(?m)^> ", body)),
            "list": bool(re.search(r"(?m)^[-*] ", body)),
            "subheading": bool(re.search(r"(?m)^## ", body)),
            "aside": bool(re.search(r"(?:\([^\n()]{2,}\)|（[^\n（）]{2,}）)", body)),
            "todo": "TODO：" in body,
        }
        if sum(moves.values()) < 2:
            raise AssertionError(f"{name}: fewer than two visible format moves")
    # No unclosed fenced block or broken link definition.
    if output_text.count("```") % 2:
        raise AssertionError(f"{name}: unclosed code fence")
    if len(fenced_blocks(output_text)) * 2 != output_text.count("```"):
        raise AssertionError(f"{name}: malformed fenced block")
    for definition in link_definitions(input_text):
        if definition not in output_text:
            raise AssertionError(f"{name}: link definition lost")


def main() -> int:
    for name in ("01-draft", "02-rewrite", "03-repair", "04-variant", "05-notes-to-doc", "06-protected", "07-safe"):
        check_case(name)
    print("markdown fixtures: 7/7 passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
