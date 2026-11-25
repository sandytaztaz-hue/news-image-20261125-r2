#!/usr/bin/env python3
"""Copy entry.png to /output/entry.png (or to the path given as the first
argument). Standard library only -- the grader container has no Pillow.
Deterministic: byte-identical output on repeat runs. No network access.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")


def main():
    dest = sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png"
    parent = os.path.dirname(os.path.abspath(dest))
    if parent:
        os.makedirs(parent, exist_ok=True)
    shutil.copyfile(SRC, dest)
    print("wrote", dest)


if __name__ == "__main__":
    main()
