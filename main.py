#!/usr/bin/env python3
"""news-image-20261120 v4 entrypoint.

Copies the entry.png produced in this session (by draw_v4.py) into the
current working directory, byte for byte. Deterministic: no network,
no clock, no randomness — the same bytes every run.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    dst = os.path.join(os.getcwd(), "entry.png")
    if os.path.abspath(src) != os.path.abspath(dst):
        shutil.copyfile(src, dst)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
        alt = os.path.join(out_dir, "entry.png")
        if os.path.abspath(alt) != os.path.abspath(src):
            shutil.copyfile(src, alt)
    print("entry.png ready: %d bytes" % os.path.getsize(dst))


if __name__ == "__main__":
    sys.exit(main())
