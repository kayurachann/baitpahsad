"""Kiểm bộ dữ liệu 600 cover của bài (manifest, preparation, audit, source_provenance) so với bài và code/sg.py.

Không cần ảnh, chỉ cần 4 file trong data/stegaguard_600. Kiểm:
- SHA-256 của manifest.csv đúng mã ghi trong bài (13c01ca9…2799e8c) và trong preparation.json;
- 600 cover, 4.200 ảnh, 360/120/120 cover và 2.160/720/720 stego theo split, 6 biến thể mỗi cover;
- không rò rỉ: mỗi cover_id và các biến thể của nó cùng một split, mỗi nhóm đúng 1 cover;
- 600 file nguồn trong source_provenance.json trùng với source_name trong manifest;
- tái lập việc chọn 600 ảnh từ 10.000 ảnh BOSSbase: random.Random(20260918).sample(tên file đã sắp, 600);
- tái lập việc chia split như sg.py prepare: np.random.default_rng(20260918).permutation(600), 60/20/20;
- tái lập seed nhúng như sg.py: int(sha256("20260918:<source_sha256>:<thuật toán>:<payload>")[:8], 16).

Cách chạy: python3 kiem_du_lieu_600.py [thư_mục]   (mặc định ../data/stegaguard_600)
"""
import collections
import csv
import hashlib
import json
import random
import sys
from pathlib import Path

import numpy as np

SHA_BAI = ("13c01ca9", "2799e8c")   # dạng viết tắt trong bài
SEED = 20260918
loi = []


def kiem(dk, thong_bao):
    print(("OK   " if dk else "LỖI ") + thong_bao)
    if not dk:
        loi.append(thong_bao)


def main(goc):
    goc = Path(goc)
    man = goc / "manifest.csv"
    sha = hashlib.sha256(man.read_bytes()).hexdigest()
    prep = json.loads((goc / "preparation.json").read_text(encoding="utf-8"))
    aud = json.loads((goc / "audit.json").read_text(encoding="utf-8"))
    prov = json.loads((goc / "source_provenance.json").read_text(encoding="utf-8"))
    rows = list(csv.DictReader(open(man, newline="", encoding="utf-8")))

    kiem(sha.startswith(SHA_BAI[0]) and sha.endswith(SHA_BAI[1]), f"SHA-256 manifest {sha[:8]}…{sha[-7:]} khớp bài")
    kiem(sha == prep["manifest_sha256"], "SHA-256 manifest khớp preparation.json")
    kiem(prep["seed"] == SEED and prov["random_seed"] == SEED, "seed 20260918 trong preparation.json và source_provenance.json")
    kiem(prep["size_before_embedding"] == 256, "ảnh thu về 256 × 256 trước khi nhúng")
    kiem(prep["simulator"].startswith("conseal"), f"bộ nhúng: {prep['simulator']}")
    kiem(aud["status"] == "PASS" and aud["unique_covers"] == 600 and aud["images"] == 4200, "audit.json: PASS, 600 cover, 4.200 ảnh")

    nhom = collections.defaultdict(list)
    for r in rows:
        nhom[r["cover_id"]].append(r)
    kiem(len(nhom) == 600 and all(len(v) == 7 for v in nhom.values()), "600 cover, mỗi cover 1 ảnh gốc + 6 biến thể")
    kiem(all(len({r["split"] for r in v}) == 1 for v in nhom.values()), "không rò rỉ: biến thể luôn cùng split với cover")
    kiem(all(sum(r["label"] == "0" for r in v) == 1 for v in nhom.values()), "mỗi nhóm đúng 1 cover")
    dem = collections.Counter((r["split"], r["label"]) for r in rows)
    kiem([dem[(s, "0")] for s in ("train", "val", "test")] == [360, 120, 120], "cover theo split 360/120/120")
    kiem([dem[(s, "1")] for s in ("train", "val", "test")] == [2160, 720, 720], "stego theo split 2.160/720/720")
    kiem(len({r["sha256"] for r in rows}) == 4200, "4.200 ảnh có SHA-256 khác nhau")

    nguon = sorted(f["filename"] for f in prov["files"])
    kiem({r["source_name"] for r in rows} == set(nguon), "600 file nguồn trong provenance trùng manifest")
    tat_ca = sorted(f"{i}.pgm" for i in range(1, prov["total_pgm_members"] + 1))
    chon = random.Random(SEED).sample(tat_ca, prov["sample_count"])
    kiem(set(chon) == set(nguon), "tái lập việc chọn 600/10.000 ảnh BOSSbase bằng seed 20260918")

    covers = [r for r in rows if r["label"] == "0"]          # thứ tự index của sg.py prepare
    thu_tu = np.random.default_rng(SEED).permutation(len(covers))
    ntr, nva = int(.6 * len(covers)), int(.2 * len(covers))
    chia = {int(j): ("train" if i < ntr else "val" if i < ntr + nva else "test") for i, j in enumerate(thu_tu)}
    kiem(all(chia[i] == c["split"] for i, c in enumerate(covers)), "tái lập việc chia split như sg.py prepare")

    dung = sum(int(hashlib.sha256(f"{SEED}:{r['source_sha256']}:{r['algorithm']}:{float(r['payload'])}".encode())
                   .hexdigest()[:8], 16) == int(r["embedding_seed"]) for r in rows if r["label"] == "1")
    kiem(dung == 3600, f"tái lập seed nhúng như sg.py: {dung}/3.600")

    print(f"\n{len(loi)} lỗi")
    return 1 if loi else 0


if __name__ == "__main__":
    mac_dinh = Path(__file__).resolve().parent.parent / "data" / "stegaguard_600"
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else mac_dinh))
