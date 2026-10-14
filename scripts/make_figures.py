"""Regenerate Figures 1-2 of the manuscript at print size (LNCS text width 12.2 cm).

Usage: python3 make_figures.py [output_dir]
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

from results_data import RQ3, PROTOCOLS, ALGORITHMS

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

TEXT_WIDTH_IN = 12.2 / 2.54
INK = "#0b0b0b"
INK_2 = "#52514e"
GRID = "#d9d8d4"
COLOR = {"Residual-LR": "#2a78d6", "SRM+Ensemble": "#eb6834"}
MARKER = {"Residual-LR": "o", "SRM+Ensemble": "s"}

plt.rcParams.update({
    "font.family": "Liberation Sans",
    "font.size": 8,
    "axes.labelsize": 8,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "legend.fontsize": 7.5,
    "axes.edgecolor": INK_2,
    "axes.linewidth": 0.6,
    "xtick.color": INK_2,
    "ytick.color": INK_2,
    "text.color": INK,
    "axes.labelcolor": INK,
    "savefig.dpi": 600,
})


def save(fig, name):
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"{name}.{ext}", bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


# --------------------------------------------------------------------------- Fig. 1
FIG1_W, FIG1_H = 4.8, 2.8  # inches; data coordinates are inches


def box(ax, x, y, w, h, title, body="", fc="#f3f2ef", ec=INK_2, lw=0.7, tsize=7.2, bsize=6.9):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.04",
                                fc=fc, ec=ec, lw=lw))
    if body:
        ax.text(x + w / 2, y + h - 0.05, title, ha="center", va="top", fontsize=tsize, fontweight="bold")
        ax.text(x + w / 2, y + h - 0.18, body, ha="center", va="top", fontsize=bsize, color=INK_2,
                linespacing=1.15)
    else:
        ax.text(x + w / 2, y + h / 2, title, ha="center", va="center", fontsize=tsize, fontweight="bold")


def arrow(ax, p, q):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=6, lw=0.7, color=INK_2,
                                 shrinkA=0, shrinkB=0))


def line(ax, xs, ys):
    ax.plot(xs, ys, color=INK_2, lw=0.7, solid_capstyle="butt")


def figure1():
    fig = plt.figure(figsize=(FIG1_W, FIG1_H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, FIG1_W)
    ax.set_ylim(0, FIG1_H)
    ax.axis("off")

    # stages 1-3: data preparation (left column, top to bottom)
    cw, ch = 1.22, 0.5
    ys = [2.29, 1.67, 1.05]
    box(ax, 0.01, ys[0], cw, ch, "1  BOSSbase 1.01", "600 source covers\n512×512 → 256×256")
    box(ax, 0.01, ys[1], cw, ch, "2  Source-cover split", "360 / 120 / 120 covers\nbefore embedding")
    box(ax, 0.01, ys[2], cw, ch, "3  Stego generation", "WOW, S-UNIWARD, HILL\n0.1, 0.4 bpp: 3,600 stego")
    for a, b in zip(ys[:-1], ys[1:]):
        arrow(ax, (0.01 + cw / 2, a), (0.01 + cw / 2, b + ch))

    # stages 4-5: two parallel detector lanes
    fx, fw = 1.45, 0.92
    tx, tw = 2.5, 0.95
    lh = 0.4
    lane_y = [1.9, 1.12]
    ax.text(fx + fw / 2, 2.71, "4  Feature extraction", ha="center", va="center", fontsize=7.2,
            fontweight="bold")
    ax.text(tx + tw / 2, 2.71, "5  Detector training", ha="center", va="center", fontsize=7.2,
            fontweight="bold")
    lanes = [("Residual-LR", "76 residual\nstatistics", "logistic regression\n360 pairs per run"),
             ("SRM+Ensemble", "SRM features\n34,671-D", "FLD ensemble\nL = 50, d_sub = 500")]
    for (name, feat, clf), y in zip(lanes, lane_y):
        c = COLOR[name]
        ax.add_patch(FancyBboxPatch((fx - 0.06, y - 0.05), tx + tw - fx + 0.12, lh + 0.27,
                                    boxstyle="round,pad=0,rounding_size=0.05", fc="none", ec=c, lw=0.9,
                                    ls=(0, (3, 1.5))))
        ax.text(fx, y + lh + 0.11, name, ha="left", va="center", fontsize=7.2, fontweight="bold", color=c)
        ax.text(tx + tw, y + lh + 0.11, "P1–P3 × 3 seeds", ha="right", va="center", fontsize=6.4,
                color=INK_2)
        for x, w, txt in ((fx, fw, feat), (tx, tw, clf)):
            ax.add_patch(FancyBboxPatch((x, y), w, lh, boxstyle="round,pad=0,rounding_size=0.04",
                                        fc="white", ec=c, lw=0.8))
            ax.text(x + w / 2, y + lh / 2, txt, ha="center", va="center", fontsize=6.7, linespacing=1.1)
        arrow(ax, (fx + fw, y + lh / 2), (tx, y + lh / 2))
    # fan-out from stage 3 to both lanes
    mid = 1.33
    y3 = ys[2] + ch / 2
    line(ax, [0.01 + cw, mid], [y3, y3])
    line(ax, [mid, mid], [y3, lane_y[0] + lh / 2])
    for y in lane_y:
        arrow(ax, (mid, y + lh / 2), (fx, y + lh / 2))

    # stage 6: evaluation on shared test covers
    ex, ew = 3.62, 1.17
    ey, eh = 1.07, 1.6
    ax.add_patch(FancyBboxPatch((ex, ey), ew, eh, boxstyle="round,pad=0,rounding_size=0.04",
                                fc="#f3f2ef", ec=INK_2, lw=0.7))
    ax.text(ex + ew / 2, ey + eh - 0.07, "6  P1/P2/P3\nevaluation", ha="center", va="top", fontsize=7.2,
            fontweight="bold", linespacing=1.1)
    ax.text(ex + ew / 2, ey + eh - 0.45, "same 120 test\ncovers for all\nprotocols\n\n6 conditions:\n"
            "3 algorithms\n× 2 payloads", ha="center", va="top", fontsize=6.7, color=INK_2, linespacing=1.12)
    for y in lane_y:
        arrow(ax, (tx + tw + 0.06, y + lh / 2), (ex, y + lh / 2))

    # branches
    bw, bh, by = 1.13, 0.42, 0.43
    gap = (FIG1_W - 0.02 - 4 * bw) / 3
    bxs = [0.01 + i * (bw + gap) for i in range(4)]
    branches = [("RQ1  Algorithm", "P1: WOW 0.4 → HILL 0.4"),
                ("RQ2  Mixed training", "P3 vs P2 on HILL 0.4"),
                ("RQ3  Payload", "0.4 → 0.1 bpp, 18 pairs"),
                ("Operating point", "τ: val FPR ≤ 1% → test")]
    for (t, b), x in zip(branches, bxs):
        box(ax, x, by, bw, bh, t, b, fc="white", tsize=7.0, bsize=6.6)
    bus = 0.95
    line(ax, [ex + ew / 2, ex + ew / 2], [ey, bus])
    line(ax, [bxs[0] + bw / 2, ex + ew / 2], [bus, bus])
    for x in bxs:
        arrow(ax, (x + bw / 2, bus), (x + bw / 2, by + bh))

    # stage 7: metrics
    box(ax, 0.01, 0.01, FIG1_W - 0.02, 0.34, "7  Robustness and security metrics",
        "ROC-AUC, F1, BER  ·  paired ΔAUC + source-cover bootstrap 95% CI  ·  recall and test FPR at τ",
        tsize=7.0, bsize=6.6)
    for x in bxs:
        arrow(ax, (x + bw / 2, by), (x + bw / 2, 0.35))
    fig.savefig(OUT / "fig1_pipeline.png", dpi=600)
    fig.savefig(OUT / "fig1_pipeline.pdf")
    plt.close(fig)


# --------------------------------------------------------------------------- Fig. 2
def figure2():
    fig, axes = plt.subplots(1, 2, figsize=(4.7, 1.85), sharey=True, gridspec_kw={"wspace": 0.08})
    pairs = [(p, a) for p in PROTOCOLS for a in ALGORITHMS]
    labels = [f"{p} {a}" for p, a in pairs]
    ys = list(range(len(labels)))[::-1]
    for ax, d in zip(axes, ["Residual-LR", "SRM+Ensemble"]):
        for y, (p, a) in zip(ys, pairs):
            delta, lo, hi = RQ3[(d, p, a)]
            ax.plot([lo, hi], [y, y], color=COLOR[d], lw=1.3, solid_capstyle="butt")
            ax.scatter([delta], [y], s=14, marker=MARKER[d], color=COLOR[d], zorder=3, edgecolor="white",
                       lw=0.5)
        ax.axvline(0, color=INK_2, lw=0.8)
        for yy in (2.5, 5.5):
            ax.axhline(yy, color=GRID, lw=0.5)
        ax.set_xlim(-0.225, 0.015)
        ax.set_xticks([-0.20, -0.15, -0.10, -0.05, 0.0], ["−0.20", "−0.15", "−0.10", "−0.05", "0"])
        ax.grid(axis="x", color=GRID, lw=0.5)
        ax.set_axisbelow(True)
        ax.tick_params(length=2, labelsize=7)
        ax.set_title(d, fontsize=7.2, loc="left", pad=2, fontweight="bold", color=INK)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    axes[0].set_yticks(ys, labels)
    axes[0].set_ylim(-0.6, len(labels) - 0.4)
    fig.subplots_adjust(bottom=0.22, top=0.9)
    fig.supxlabel("ΔAUC = AUC(0.1 bpp) − AUC(0.4 bpp), point estimate and 95% paired bootstrap CI",
                  fontsize=7, y=0.01)
    save(fig, "fig2_payload_shift")


if __name__ == "__main__":
    figure1()
    figure2()
    print("figures written to", OUT)
