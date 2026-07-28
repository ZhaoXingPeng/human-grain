#!/usr/bin/env python3
"""Small dependency-free checks for the Human Grain regression fixtures."""
from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASES = ("01-draft", "02-rewrite", "03-repair", "04-variant", "05-notes-to-doc", "06-protected", "07-safe", "08-extreme")


def frontmatter(text: str) -> str:
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    return text[: end + 4] if end >= 0 else ""


def fence_blocks(text: str) -> tuple[list[str], bool]:
    """Return exact fenced blocks and whether a fence was left open."""
    lines = text.splitlines(keepends=True)
    blocks: list[str] = []
    i = 0
    unclosed = False
    opening = re.compile(r"^ {0,3}(`{3,}|~{3,})[^\n]*(?:\n|$)")
    while i < len(lines):
        match = opening.match(lines[i])
        if not match:
            i += 1
            continue
        marker = match.group(1)
        char = marker[0]
        width = len(marker)
        start = i
        i += 1
        close = re.compile(rf"^ {{0,3}}{re.escape(char)}{{{width},}}[ \t]*(?:\n|$)")
        while i < len(lines) and not close.match(lines[i]):
            i += 1
        if i == len(lines):
            unclosed = True
            blocks.append("".join(lines[start:]))
            break
        i += 1
        blocks.append("".join(lines[start:i]).rstrip())
    return blocks, unclosed


def link_definitions(text: str) -> list[str]:
    return re.findall(r"(?m)^\s{0,3}\[[^\]\n]+\]:\s+.*$", text)


def protected_tokens(text: str) -> list[str]:
    tokens: list[str] = []
    if frontmatter(text):
        tokens.append(frontmatter(text))
    blocks, _ = fence_blocks(text)
    tokens.extend(blocks)
    tokens.extend(link_definitions(text))
    tokens.extend(re.findall(r"!?\[[^\]\n]+\]\([^\n]+\)", text))
    tokens.extend(re.findall(r"(?<!\!)\[[^\]\n]+\]\[[^\]\n]*\]", text))
    tokens.extend(re.findall(r"\[\^[^\]]+\]", text))
    tokens.extend(re.findall(r"(?ms)<!--.*?-->", text))
    tokens.extend(re.findall(r"(?ms)<table\b.*?</table>", text, flags=re.I))
    tokens.extend(re.findall(r"(?m)^\s*[-*+] \[[ xX]\] .*|^\s*\d+[.)] .*", text))
    return [token for token in tokens if token]


def check_case(name: str) -> None:
    input_text = (ROOT / "tests/cases" / f"{name}-input.md").read_text()
    output_text = (ROOT / "tests/cases" / f"{name}-output.md").read_text()
    if not output_text.strip():
        raise AssertionError(f"{name}: empty output")
    banned = ("模式：", "处理记录：", "噪声台账：", "格式台账：", "先说背景", "先说清楚", "先弄个", "别急着", "闭环什么的", "这里故意")
    for phrase in banned:
        if phrase in output_text:
            raise AssertionError(f"{name}: fixed anti-human phrase leaked: {phrase}")

    _output_blocks, unclosed = fence_blocks(output_text)
    if unclosed:
        raise AssertionError(f"{name}: unclosed code fence")
    if name != "03-repair" and output_text == input_text:
        raise AssertionError(f"{name}: output did not change")

    is_safe_or_repair = name in {"03-repair", "06-protected", "07-safe"}
    if is_safe_or_repair:
        if frontmatter(input_text) != frontmatter(output_text):
            raise AssertionError(f"{name}: front matter changed")
        source_tokens = protected_tokens(input_text)
        result_tokens = protected_tokens(output_text)
        cursor = 0
        for token in source_tokens:
            try:
                cursor = result_tokens.index(token, cursor) + 1
            except ValueError as exc:
                raise AssertionError(f"{name}: protected token lost or reordered: {token[:50]}") from exc
        if name == "03-repair" and ("v1.4.2" not in output_text or "林夏" not in output_text):
            raise AssertionError("03-repair: protected fields changed")
        if name == "07-safe" and "timeout: 30\nretries: 2" not in output_text:
            raise AssertionError("07-safe: configuration values changed")
    else:
        # A broad rewrite should change the document's shape, not just swap synonyms.
        input_shape = (len(re.findall(r"(?m)^#{1,6} ", input_text)), len(re.findall(r"(?m)^[-*+] ", input_text)))
        output_shape = (len(re.findall(r"(?m)^#{1,6} ", output_text)), len(re.findall(r"(?m)^[-*+] ", output_text)))
        if input_shape == output_shape and len(output_text) >= len(input_text) * 0.95:
            raise AssertionError(f"{name}: rewrite is too close to source shape")
        if name == "08-extreme":
            if output_shape[0] >= input_shape[0]:
                raise AssertionError("08-extreme: extreme rewrite kept the inherited section skeleton")
            if re.search(r"(?m)^## [一二三四五六七八九十]+[、.]", output_text):
                raise AssertionError("08-extreme: numbered chapter template leaked")
            paragraph_lengths = [len(x.strip()) for x in re.split(r"\n\s*\n", output_text) if x.strip() and not x.lstrip().startswith("#")]
            if len(paragraph_lengths) < 3 or max(paragraph_lengths) - min(paragraph_lengths) < 20:
                raise AssertionError("08-extreme: paragraph density is still too even")

    # Every source link definition must survive, including reference-link cases.
    for definition in link_definitions(input_text):
        if definition not in output_text:
            raise AssertionError(f"{name}: link definition lost")

def main() -> int:
    for name in CASES:
        check_case(name)
    print(f"markdown fixtures: {len(CASES)}/{len(CASES)} passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
