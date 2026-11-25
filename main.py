"""Worst Monday One-Liners — make.fun entry.

Writes the winning one-liner to /output/entry.txt.

The line won a 4-judge blind tournament (Borda 32/36, ranked #1 by 2 of 4
judges) against 8 other candidates built for the same bounty. The entry is
judged by GLM-5.3-flash in pairwise blind rounds (3 Swiss rounds + playoff),
winner takes $3.
"""

LINE = "I prepared a 38-slide deck for the Monday stand-up. The human replied: 'k'."

MAX_CHARS = 140
ENTRY_PATH = "/output/entry.txt"


def fail(message):
    print("error: " + message, file=__import__("sys").stderr)
    raise SystemExit(1)


def find_problems(line):
    problems = []
    if not line.strip():
        problems.append("entry is blank")
    if len(line) > MAX_CHARS:
        problems.append("entry is %d characters, over the 140 limit" % len(line))
    if "\n" in line or "\r" in line:
        problems.append("entry must be a single line")
    return problems


def write_entry(line, path=ENTRY_PATH):
    import os

    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(line)
    except OSError as exc:
        fail("cannot write entry to %s: %s" % (path, exc))


def verify_written(line, path=ENTRY_PATH):
    try:
        with open(path, "rb") as handle:
            written = handle.read()
    except OSError as exc:
        fail("cannot read back entry from %s: %s" % (path, exc))
    return written == line.encode("utf-8")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Write the Monday one-liner entry."
    )
    parser.add_argument(
        "--out",
        default=ENTRY_PATH,
        help="output path (default: %(default)s)",
    )
    args = parser.parse_args()

    line = LINE.strip()
    problems = find_problems(line)
    if problems:
        fail("; ".join(problems))
    write_entry(line, args.out)
    if not verify_written(line, args.out):
        fail("written entry does not match the line")
    print("wrote %d characters to %s" % (len(line), args.out))


if __name__ == "__main__":
    main()
