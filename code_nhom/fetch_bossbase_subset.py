"""Reproducibly fetch individual PGM members from the official BOSSbase ZIP.

The university archive supports HTTP byte ranges, so a documented pilot can
retrieve dispersed source images without downloading the entire 1.56-GiB ZIP.
Only publicly distributed cover images are fetched; ZIP CRC and PNG provenance
are checked and preserved in a manifest.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import json
import random
import struct
import time
import urllib.request
import zlib
from pathlib import Path

URL = "https://dde.binghamton.edu/download/ImageDB/BOSSbase_1.01.zip"
SIZE = 1671626159
ETAG = '"4aabc4fc20ffd11:0"'


def byte_range(start: int, end: int, tries: int = 4) -> bytes:
    if start < 0 or end < start or end >= SIZE:
        raise ValueError(f"Invalid byte range: {start}-{end}")
    for attempt in range(tries):
        try:
            req = urllib.request.Request(
                URL, headers={"Range": f"bytes={start}-{end}", "User-Agent": "StegaGuard-Research/1.0"}
            )
            with urllib.request.urlopen(req, timeout=50) as response:
                data = response.read()
                if response.status != 206 or len(data) != end - start + 1:
                    raise IOError(f"Expected 206 and {end-start+1} bytes; got {response.status} / {len(data)}")
                if response.headers.get("ETag") != ETAG:
                    raise IOError("ZIP ETag changed: refuse to mix different archive versions")
                return data
        except Exception:
            if attempt == tries - 1:
                raise
            time.sleep(min(2**attempt, 8))
    raise AssertionError("unreachable")


def central_directory():
    tail_start = SIZE - 1_500_000
    tail = byte_range(tail_start, SIZE - 1)
    eocd = tail.rfind(b"PK\x05\x06")
    if eocd < 0:
        raise ValueError("End-of-central-directory not found")
    signature, disk, cd_disk, on_disk, n, cd_len, cd_at, comment_len = struct.unpack_from(
        "<IHHHHIIH", tail, eocd
    )
    if disk or cd_disk or n != on_disk or n < 10000:
        raise ValueError("Unexpected archive structure")
    directory = tail[cd_at-tail_start:cd_at-tail_start+cd_len]
    if len(directory) != cd_len:
        directory = byte_range(cd_at, cd_at+cd_len-1)
    items = []
    cursor = 0
    for _ in range(n):
        values = struct.unpack_from("<4s6H3I5H2I", directory, cursor)
        if values[0] != b"PK\x01\x02":
            raise ValueError(f"Bad central-directory entry at {cursor}")
        _, made, needed, flags, method, mtime, mdate, crc, compressed, size, flen, xlen, clen, diskno, iattr, eattr, offset = values
        filename = directory[cursor+46:cursor+46+flen].decode("utf-8" if flags & 2048 else "cp437")
        items.append(dict(name=filename, flags=flags, method=method, crc32=crc,
                          compressed=compressed, uncompressed=size, local_offset=offset))
        cursor += 46 + flen + xlen + clen
    return items


def extract(item, target_dir: Path):
    name = item["name"]
    if not name.lower().endswith(".pgm") or "/" in name.rstrip("/").split("/")[-1]:
        raise ValueError(f"Not a PGM image: {name}")
    # Fetch the local header and entire compressed content in one HTTP request.
    start = item["local_offset"]
    blob = byte_range(start, start + 30 + len(name.encode("utf-8")) + 65535 + item["compressed"] - 1)
    header = struct.unpack_from("<4s5H3I2H", blob, 0)
    if header[0] != b"PK\x03\x04":
        raise ValueError(f"Unexpected local header: {name}")
    filename_len, extra_len = header[-2:]
    raw = blob[30+filename_len+extra_len:30+filename_len+extra_len+item["compressed"]]
    if len(raw) != item["compressed"]:
        raise ValueError(f"Truncated member: {name}")
    if item["method"] == 8:
        payload = zlib.decompress(raw, -15)
    elif item["method"] == 0:
        payload = raw
    else:
        raise ValueError(f"Unsupported ZIP compression: {item['method']}")
    if len(payload) != item["uncompressed"] or zlib.crc32(payload) != item["crc32"]:
        raise ValueError(f"CRC/size mismatch: {name}")
    output = target_dir / Path(name).name
    if output.exists():
        if output.read_bytes() != payload:
            raise ValueError(f"Existing image differs: {output}")
    else:
        output.write_bytes(payload)
    return dict(source_member=name, filename=output.name, sha256=hashlib.sha256(payload).hexdigest(),
                uncompressed_bytes=len(payload), zip_crc32=f"{item['crc32']:08x}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=180)
    parser.add_argument("--seed", type=int, default=20260918)
    parser.add_argument("--workers", type=int, default=6)
    parser.add_argument("--inspect", action="store_true")
    parser.add_argument("--out", default="bossbase_original/pilot_covers")
    args = parser.parse_args()
    archive = central_directory()
    images = sorted((entry for entry in archive if entry["name"].lower().endswith(".pgm")), key=lambda x:x["name"])
    print(json.dumps(dict(archive_entries=len(archive), pgm_members=len(images),
                          first=images[:1], last=images[-1:]), ensure_ascii=False), flush=True)
    if args.inspect:
        return
    if not 10 <= args.count <= len(images):
        raise ValueError("Invalid pilot sample count")
    selected = sorted(random.Random(args.seed).sample(images, args.count), key=lambda x:x["local_offset"])
    output = Path(args.out)
    output.mkdir(parents=True, exist_ok=True)
    rows=[]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(extract, entry, output):entry for entry in selected}
        for completed in concurrent.futures.as_completed(futures):
            row = completed.result()
            rows.append(row)
            if len(rows)%20==0 or len(rows)==args.count:
                print(f"Verified {len(rows)}/{args.count} original BOSSbase covers", flush=True)
    metadata = dict(source_url=URL, archive_bytes=SIZE, archive_etag=ETAG,
                    total_pgm_members=len(images), sample_count=args.count,
                    random_seed=args.seed, selection="uniform random without replacement among PGM members",
                    file_checks="ZIP CRC32, uncompressed size, SHA-256", files=sorted(rows,key=lambda x:x["source_member"]))
    (output.parent/'source_provenance.json').write_text(json.dumps(metadata,indent=2,ensure_ascii=False),encoding="utf-8")
    print(f"Saved {len(rows)} original source images and provenance to {output.parent}",flush=True)


if __name__ == "__main__":
    main()
