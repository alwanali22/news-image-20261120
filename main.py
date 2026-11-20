#!/usr/bin/env python3
"""main.py — news-image-20261120 v3 entrypoint.
Copies the pre-rendered entry.png to the output directory.
Deterministic: the same bytes every run.
"""
import os
import shutil


def publish():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    outdir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    dst = os.path.join(outdir, "entry.png")
    shutil.copyfile(src, dst)
    with open(src, "rb") as fh:
        size = len(fh.read())
    print(f"entry.png ({size} bytes) -> {dst}")


if __name__ == "__main__":
    publish()
