"""news-23 b53 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only. Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import hashlib
import os
import struct
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        print("error: MAKEFUN_OUTPUT_DIR is empty", file=sys.stderr)
        return 1
    out_dir = os.path.abspath(out_dir)
    if out_dir == os.path.abspath(here) or out_dir.startswith(os.path.abspath(here) + os.sep):
        print("error: MAKEFUN_OUTPUT_DIR must be outside the repo", file=sys.stderr)
        return 1
    with open(src, "rb") as f:
        data = f.read()
    if len(data) > 1024 * 1024:
        print("error: entry.png over 1 MiB", file=sys.stderr)
        return 1
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        print("error: bad PNG signature", file=sys.stderr)
        return 1
    w, h, depth, ctype = struct.unpack(">IIBB", data[16:26])
    if (w, h) != (1024, 1024):
        print("error: expected 1024x1024, got %dx%d" % (w, h), file=sys.stderr)
        return 1
    if depth != 8 or ctype not in (2, 6):
        print("error: unexpected bit depth %d / colour type %d" % (depth, ctype), file=sys.stderr)
        return 1
    if data[-12:] != struct.pack(">I", 0) + b"IEND" + struct.pack(">I", 0xAE426082):
        print("error: malformed IEND trailer", file=sys.stderr)
        return 1
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        back = f.read()
    if back != data:
        print("error: output not byte-identical to source", file=sys.stderr)
        return 1
    print("ok: wrote %s (%d bytes, %dx%d, sha256 %s)"
          % (dst, len(data), w, h, hashlib.sha256(data).hexdigest()))
    print("source: %s (%d bytes)" % (src, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
