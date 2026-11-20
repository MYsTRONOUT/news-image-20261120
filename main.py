"""news-image-20261120 entry program (Python 3.13, standard library only).

The entry image ships next to this file. Running the program copies it
byte-for-byte to $MAKEFUN_OUTPUT_DIR/entry.png (default /output), then
checks the copy against the original with SHA-256. No network, no clock,
no randomness: two runs produce identical bytes.

Local check: mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
IMAGE = HERE / "entry.png"


def source_image():
    if not IMAGE.is_file():
        print("error: entry.png missing next to main.py", file=sys.stderr)
        raise SystemExit(1)
    return IMAGE


def checksum(path):
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def publish():
    # Straight copy plus a hash check: the output must match the source
    # exactly, so a second run can never drift from the first.
    src = source_image()
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(src, dest)
    if checksum(dest) != checksum(src):
        print("error: copied bytes differ from entry.png", file=sys.stderr)
        raise SystemExit(1)
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")


def main():
    publish()


if __name__ == "__main__":
    main()
