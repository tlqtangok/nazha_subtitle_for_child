#!/usr/bin/env python3
"""
Generate gg_learning.txt by combining nazha_subtitle.txt and to_implement_template.txt.

For each line in the template (B file), extract the Chinese character being taught,
find a subtitle line from nazha_subtitle.txt (A file) that contains that character,
and produce a new line in gg_learning.txt (C file) using the subtitle as the example.

Template format: 一：我有一个气球的一字
Output format:   一:孕育了一颗混元珠的一字
"""

import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SUBTITLE_FILE = os.path.join(SCRIPT_DIR, "nazha_subtitle.txt")
TEMPLATE_FILE = os.path.join(SCRIPT_DIR, "to_implement_template.txt")
OUTPUT_FILE = os.path.join(SCRIPT_DIR, "gg_learning.txt")


def load_subtitles(filepath):
    """Load non-empty subtitle lines from the subtitle file."""
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [line.strip() for line in lines if line.strip()]


def clean_line(text):
    """Strip whitespace and zero-width spaces from a line."""
    return text.strip().rstrip("\u200b")


def strip_trailing_punctuation(text):
    """Strip trailing Chinese and common punctuation from text."""
    return text.rstrip("。，！？；：、…—""''（）《》【】")


def find_subtitle_for_char(char, subtitles, used_indices):
    """Find a subtitle line containing the given character.
    
    Tries to avoid reusing the same subtitle line by tracking used indices.
    Falls back to reusing if no unused match is found.
    """
    # First pass: find an unused subtitle containing the character
    for i, subtitle in enumerate(subtitles):
        if char in subtitle and i not in used_indices:
            used_indices.add(i)
            return strip_trailing_punctuation(subtitle)
    # Second pass: allow reuse if no unused match found
    for i, subtitle in enumerate(subtitles):
        if char in subtitle:
            return strip_trailing_punctuation(subtitle)
    return None


def parse_template_line(line):
    """Parse a template line and extract the character and any annotation suffix.
    
    Expected format: 一：我有一个气球的一字
    Also handles: 说：我大胆说话的说话  (typo in template)
                  季：四季都很美季字    (missing 的 in template)
    Returns (char, annotation) where annotation is text after 字 like （补充场景）,
    or None if line doesn't have a colon.
    """
    # Match: character + full/half-width colon + rest
    match = re.match(r"^(.)[：:](.+)$", line)
    if not match:
        return None
    char = match.group(1)
    rest = match.group(2)
    # Extract annotation suffix after 字 (e.g. （补充场景）)
    ann_match = re.search(r"字(（.+）)$", rest)
    annotation = ann_match.group(1) if ann_match else ""
    return char, annotation


def main():
    subtitles = load_subtitles(SUBTITLE_FILE)
    with open(TEMPLATE_FILE, "r", encoding="utf-8") as f:
        template_lines = f.readlines()

    used_indices = set()
    output_lines = []

    for raw_line in template_lines:
        line = clean_line(raw_line)
        if not line:
            continue

        parsed = parse_template_line(line)
        if parsed is None:
            output_lines.append(line)
            continue

        char, annotation = parsed
        subtitle = find_subtitle_for_char(char, subtitles, used_indices)
        if subtitle:
            new_line = f"{char}:{subtitle}的{char}字{annotation}"
        else:
            # No subtitle found containing this character, keep original
            new_line = line
        output_lines.append(new_line)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for line in output_lines:
            f.write(line + "\n")

    print(f"Generated {OUTPUT_FILE} with {len(output_lines)} lines.")


if __name__ == "__main__":
    main()
