"""Entrypoint: publish the built front page as the entry image.

Copies the pre-rendered entry.png next to this file into the output
directory the harness gives us (MAKEFUN_OUTPUT_DIR, default /output),
then checks the copy landed with the same byte count. No rendering
happens here; draw_v2.py is the generator.
"""

import os
import shutil


def _paths():
    here = os.path.dirname(os.path.abspath(__file__))
    origin = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    target = os.path.join(out_dir, "entry.png")
    return origin, target


def publish():
    origin, target = _paths()
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copyfile(origin, target)
    if os.path.getsize(origin) != os.path.getsize(target):
        raise RuntimeError("published entry.png is a different size "
                           "than the shipped one")


if __name__ == "__main__":
    publish()
