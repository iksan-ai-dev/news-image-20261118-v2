#!/usr/bin/env python3
"""Entry point for news-image-20261118-v2.

Copies the pre-rendered entry.png next to this file into the harness
output directory. Standard library only.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    size = os.path.getsize(dst)
    if size > 1024 * 1024:
        raise SystemExit(f"entry.png too large: {size} bytes")
    print(f"wrote {dst} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
