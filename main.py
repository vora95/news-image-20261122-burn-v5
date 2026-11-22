#!/usr/bin/env python3
"""THE SUNDAY ATLAS — entrypoint.

Copies the sealed front page (entry.png, rendered deterministically from
the 22 November 2026 wires) into $MAKEFUN_OUTPUT_DIR and verifies the copy
byte-for-byte against the sealed SHA-256.
Standard library only.
"""
import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
EXPECTED_SHA256 = "93bdd9e85f069078eddbfd3419d0fb9e13a54483c61f8939ff1e5861e85c771c"


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        print("MAKEFUN_OUTPUT_DIR is not set", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    got = sha256_of(dst)
    if got != EXPECTED_SHA256:
        print(f"SHA-256 mismatch: got {got}, expected {EXPECTED_SHA256}",
              file=sys.stderr)
        return 1
    print(f"entry.png -> {dst} ({os.path.getsize(dst)} bytes, sha256 OK)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
