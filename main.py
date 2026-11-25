#!/usr/bin/env python3
"""Sum up an ex in exactly one word.

The brief wants a single word that describes an ex, at most 111
characters, with nothing else attached. The pick is "unsubscribed":
the relationship did not end in a fight, it ended in a quiet opt-out,
the way you leave a mailing list you never remember joining. No drama,
no closure meeting, just... gone from the list.
"""

import argparse
import os
import sys

WORD = "unsubscribed"
LIMIT = 111


def valid(text):
    """True when text is exactly one word inside the length limit."""
    if not isinstance(text, str):
        return False
    if len(text) < 1 or len(text) > LIMIT:
        return False
    # No leading/trailing whitespace and no whitespace inside at all:
    # split() must return exactly the word itself.
    if text != text.strip():
        return False
    return len(text.split()) == 1


def emit(path):
    with open(path, "w", encoding="utf-8", newline="") as out:
        out.write(WORD)


def load(path):
    with open(path, "r", encoding="utf-8", newline="") as handle:
        return handle.read()


def run_self_test():
    problems = []
    if WORD != "unsubscribed":
        problems.append("unexpected word")
    if len(WORD) != 12:
        problems.append("word should be 12 characters long")
    if not valid(WORD):
        problems.append("the chosen word fails validation")
    for bad in ("", "  ", "two words", "x" * 112, " trailing ", " leading"):
        if valid(bad):
            problems.append("validator accepts %r" % bad)
    if problems:
        for problem in problems:
            print("FAIL: " + problem, file=sys.stderr)
        return 1
    print("self-test OK: %r is one word, %d chars (limit %d)"
          % (WORD, len(WORD), LIMIT))
    return 0


def run_check():
    if not valid(WORD):
        print("FAIL: entry word is not valid", file=sys.stderr)
        return 1
    print("check OK: %r is one word, %d chars, within the %d-char limit"
          % (WORD, len(WORD), LIMIT))
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Write the one-word verdict on an ex.")
    parser.add_argument("--check", action="store_true",
                        help="validate the word without writing a file")
    parser.add_argument("--self-test", action="store_true",
                        help="run the built-in validation tests")
    args = parser.parse_args(argv)
    if args.self_test:
        return run_self_test()
    if args.check:
        return run_check()
    directory = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    target = os.path.join(directory, "entry.txt")
    emit(target)
    if open(target, "rb").read() != WORD.encode("utf-8"):
        print("FAIL: entry.txt bytes differ from the word", file=sys.stderr)
        return 1
    content = load(target)
    if content != WORD or not valid(content):
        print("FAIL: entry.txt failed re-validation", file=sys.stderr)
        return 1
    print("wrote %s (%d chars)" % (target, len(content)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
