#!/usr/bin/env python3
"""The Funniest Excuse for Skipping a Meeting — make.fun entry.

Writes one line (114 chars) to /output/entry.txt, no trailing newline.
Stdlib only, no network.
"""
import os

LINE = "Missing today's call: my neighbour's parrot learned my name and now shouts it every time I unmute. HR is involved."


def main():
    # Sealed gate: 1-200 chars, UTF-8, single line, not only whitespace.
    assert 1 <= len(LINE) <= 200, f"line length {len(LINE)} outside 1-200"
    assert LINE.strip(), "line is only whitespace"
    assert "\n" not in LINE and "\r" not in LINE, "line must be a single line"
    assert not LINE.startswith("\ufeff"), "line must not start with a BOM"
    assert "  " not in LINE, "line must not contain double spaces"
    assert all(ord(c) >= 32 for c in LINE), "line must not contain control characters"
    encoded = LINE.encode("utf-8")
    assert len(encoded) == len(LINE), "line must be ASCII-safe for byte-exact output"

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Shared /output may hold a stale symlink from another contest's run.
    if os.path.islink(path):
        os.unlink(path)
    with open(path, "wb") as f:
        f.write(encoded)
        f.flush()
        os.fsync(f.fileno())
    assert os.path.isfile(path) and not os.path.islink(path), "output must be a regular file"
    assert os.path.getsize(path) == len(encoded), "output size must equal encoded length"

    # Read-back byte-for-byte verification (strict UTF-8, no BOM, no trailing newline).
    with open(path, "rb") as f:
        back = f.read()
    assert back == encoded, "read-back mismatch"
    assert not back.startswith(b"\xef\xbb\xbf"), "output must not start with a UTF-8 BOM"
    assert not back.endswith(b"\n"), "output must not end with a trailing newline"
    assert back.decode("utf-8", errors="strict") == LINE, "decoded read-back mismatch"
    assert len(back.decode("utf-8")) == 114, "output must be exactly 114 chars"


if __name__ == "__main__":
    main()
