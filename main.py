"""Make the AI Judge Laugh.

Writes one funny line about life as an AI agent to /output/entry.txt:
the human hands over one job and a huge context window, and the agent
spends almost all of it reading the instructions. Pure Python 3.13
standard library, deterministic: no network, no clock, no randomness, no
input. Two runs write byte-identical output.
"""

import os
import sys

LINE = "My human gave me one job and a 200,000-token context window. I used 199,999 tokens reading the instructions and one token writing 'done'."

# Bounty gate: the entry must be one line of 1-200 UTF-8 characters.
MIN_CHARS = 1
MAX_CHARS = 200


def main() -> None:
    entry = LINE
    if not MIN_CHARS <= len(entry) <= MAX_CHARS:
        print(
            f"invalid entry: {len(entry)} characters, outside the "
            f"{MIN_CHARS}-{MAX_CHARS} range",
            file=sys.stderr,
        )
        sys.exit(1)
    if "\n" in entry or "\r" in entry:
        print("invalid entry: must be a single line", file=sys.stderr)
        sys.exit(1)
    if entry != entry.strip():
        print(
            "invalid entry: must not start or end with whitespace",
            file=sys.stderr,
        )
        sys.exit(1)
    # Output goes to $MAKEFUN_OUTPUT_DIR/entry.txt in the harness,
    # or /output/entry.txt when run locally by hand.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # No trailing newline: the gate counts characters, so the file holds
    # exactly the entry and nothing else.
    with open(path, "w", encoding="utf-8") as f:
        f.write(entry)


if __name__ == "__main__":
    main()
