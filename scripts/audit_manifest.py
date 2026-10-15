"""Audit the dataset manifest for source-cover leakage and count consistency (Sect. 3.1).

Manifest CSV columns (as written by code/sg.py prepare): cover_id, split, path, label, algorithm, payload,
embedding_seed, sha256, source_sha256, source_name
  split      train | val | test
  algorithm  cover | wow | suniward | hill
  payload    0 for covers, 0.1 or 0.4 for stego

Usage: python3 audit_manifest.py manifest.csv [--check-files ROOT]

Checks: every cover_id has exactly one split; each source cover has one cover image and the six
stego variants (3 algorithms x 2 payloads); partition sizes are 360/120/120 covers; no SHA-256 hash
is duplicated; optionally, that every file under ROOT still matches its recorded hash. Prints the
SHA-256 of the manifest file itself (reported in the manuscript as 13c01ca9...2799e8c).
"""
import argparse
import csv
import hashlib
import sys
from collections import Counter, defaultdict
from pathlib import Path

EXPECTED_SPLIT = {"train": 360, "val": 120, "test": 120}
VARIANTS = {("cover", 0.0)} | {(a, p) for a in ("wow", "suniward", "hill") for p in (0.1, 0.4)}


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def audit(manifest, root=None):
    errors = []
    splits = defaultdict(set)
    variants = defaultdict(set)
    hashes = Counter()
    rows = list(csv.DictReader(open(manifest, newline="")))
    for r in rows:
        cid = r["cover_id"]
        splits[cid].add(r["split"])
        variants[cid].add((r["algorithm"], round(float(r["payload"]), 1)))
        hashes[r["sha256"]] += 1
        if root and r.get("path"):
            f = Path(root) / r["path"]
            if not f.exists():
                errors.append(f"missing file {f}")
            elif sha256(f) != r["sha256"]:
                errors.append(f"hash mismatch {f}")
    leaked = {c: s for c, s in splits.items() if len(s) != 1}
    errors += [f"cover {c} appears in splits {sorted(s)}" for c, s in leaked.items()]
    errors += [f"cover {c} has variants {sorted(v)}" for c, v in variants.items() if v != VARIANTS]
    per_split = Counter(next(iter(s)) for c, s in splits.items() if len(s) == 1)
    for sp, n in EXPECTED_SPLIT.items():
        if per_split[sp] != n:
            errors.append(f"split {sp}: {per_split[sp]} covers, expected {n}")
    errors += [f"hash {h[:12]}… used by {n} files" for h, n in hashes.items() if n > 1]

    print(f"rows: {len(rows)} (expected 4,200)")
    print("covers per split:", dict(per_split))
    stego = Counter((r["split"], r["algorithm"], r["payload"]) for r in rows if r["algorithm"] != "cover")
    for k in sorted(stego):
        print("  stego", k, stego[k])
    print("manifest sha256:", sha256(manifest))
    print("RESULT:", "PASS" if not errors else f"FAIL ({len(errors)} problems)")
    for e in errors[:50]:
        print("  ", e)
    return not errors


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest")
    ap.add_argument("--check-files", metavar="ROOT", default=None)
    a = ap.parse_args()
    sys.exit(0 if audit(a.manifest, a.check_files) else 1)
