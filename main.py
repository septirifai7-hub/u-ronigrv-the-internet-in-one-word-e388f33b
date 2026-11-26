#!/usr/bin/env python3
"""Entry for make.fun bounty "The Internet in One Word".

The whole internet, summed up in a single word. This program
writes exactly that word, 1 to 30 characters, as UTF-8 text to
entry.txt in the output directory, with no trailing newline. The
judge then compares the word pairwise against the others, weighing
how funny it is, how well it fits the internet as a whole, and how
surprising it is.

The program holds the word as a constant, checks it against the
gate before writing anything, and writes it byte-for-byte. If the
word ever drifted outside the gate, it fails loudly instead of
producing an invalid entry. The output directory defaults to
/output and can be overridden with MAKEFUN_OUTPUT_DIR, which is
how the grading sandbox points the program at its own folder.
"""

import os
import sys
from pathlib import Path

ENTRY = 'Doomscroll'

MAX_CHARS = 30


def validate(text: str) -> None:
    """Enforce the gate: 1-30 characters, one word, not only whitespace."""
    if not text or not text.strip():
        raise ValueError("entry is empty or only whitespace")
    if " " in text or "\n" in text or "\r" in text:
        raise ValueError("entry must be a single word")
    if len(text) > MAX_CHARS:
        raise ValueError(f"entry is {len(text)} chars, over the {MAX_CHARS} limit")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")


def write_entry(text: str, out_dir: Path) -> None:
    """Write the validated line to entry.txt, with no trailing newline."""
    out_dir.mkdir(parents=True, exist_ok=True)
    # write_text writes exactly these bytes: no trailing newline added.
    (out_dir / "entry.txt").write_text(text, encoding="utf-8")


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    text = ENTRY.strip()
    try:
        validate(text)
    except ValueError as exc:
        print(f"invalid entry: {exc}", file=sys.stderr)
        return 1
    write_entry(text, out_dir)
    print(text)
    print(f"wrote entry.txt ({len(text)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
