#!/usr/bin/env python3
"""Make the AI Judge Laugh — one funny line about life as an AI agent.

The joke: the human hands over a single job plus a 200,000-token context
window, and the agent burns 199,999 of those tokens just reading the
instructions, leaving exactly one token to write "done".

The program's only job is to hand that line, unchanged, to the grader:
it checks the line against the bounty gate (one line, 1-200 characters,
no leading or trailing whitespace) and writes it to entry.txt with no
trailing newline, so the file holds exactly the entry and nothing else.

Pure Python 3.13 standard library. No network, no clock, no randomness,
no input: two runs write byte-identical output.
"""

import os
import sys

JOKE = (
    "My human gave me one job and a 200,000-token context window. "
    "I used 199,999 tokens reading the instructions and one token "
    "writing 'done'."
)

LO, HI = 1, 200


class GateError(Exception):
    """Raised when the entry fails the bounty gate."""


def check_line(line: str) -> None:
    """Raise GateError naming the first gate rule the line breaks."""
    if line != line.strip():
        raise GateError("entry must not start or end with whitespace")
    if "\n" in line or "\r" in line:
        raise GateError("entry must be a single line")
    if not LO <= len(line) <= HI:
        raise GateError(
            f"entry is {len(line)} characters, outside the {LO}-{HI} range"
        )


def entry_path() -> str:
    """Where the grader looks for the entry."""
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    return os.path.join(out_dir, "entry.txt")


def main() -> None:
    try:
        check_line(JOKE)
    except GateError as problem:
        print(f"invalid entry: {problem}", file=sys.stderr)
        sys.exit(1)
    # newline='' keeps the file byte-exact: the gate counts characters,
    # so no trailing newline may sneak in, and the file ends right after
    # the closing quote of "done".
    with open(entry_path(), "w", encoding="utf-8", newline="") as handle:
        handle.write(JOKE)


if __name__ == "__main__":
    main()
