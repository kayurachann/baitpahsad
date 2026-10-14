"""Regenerate Figures 1-2 of the manuscript at print size (LNCS text width 12.2 cm).

Plain journal style: serif font matching the Times body text, black lines on white,
square-cornered boxes, no colour (PNG stored as single-channel grayscale).

Usage: python3 make_figures.py [output_dir]
"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch

from results_data import RQ3, PROTOCOLS, ALGORITHMS

OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "figures"
OUT.mkdir(parents=True, exist_ok=True)

LW = 0.6
plt.rcParams.update({
    "font.family": "serif",
    "font.serif": ["Times New Roman", "Liberation Serif", "DejaVu Serif"],
    "mathtext.fontset": "stix",
    "font.size": 7.5,
    "axes.labelsize": 7.5,
    "xtick.labelsize": 7,
    "ytick.labelsize": 7,
    "axes.linewidth": LW,
    "xtick.major.width": LW,
    "ytick.major.width": LW,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "savefig.dpi": 600,
})
TAU_LOW = r"$\tau_{\mathrm{low}}$"


def to_gray(png):
    """Store the PNG as single-channel grayscale so no colour can remain in the published figure."""
    from PIL import Image
    Image.open(png).convert("L").save(png, dpi=(600, 600))


# --------------------------------------------------------------------------- Fig. 1
W, H = 4.8, 1.6   # inches; data coordinates are inches
Y0 = 0.19         # lowest drawn element; the figure is cropped below it


def rect(ax, x, y, w, h, text, size=7):
    ax.add_patch(Rectangle((x, y), w, h, fill=False, ec="black", lw=LW))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, linespacing=1.15)


def arrow(ax, p, q):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=5, lw=LW, color="black",
                                 shrinkA=0, shrinkB=0))


def line(ax, xs, ys):
    ax.plot(xs, ys, color="black", lw=LW, solid_capstyle="butt")


def figure1():
    fig = plt.figure(figsize=(W, H - Y0))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(Y0, H)
    ax.axis("off")

    # data preparation (left column)
    dx, dw, dh = 0.005, 0.95, 0.36
    dys = [1.17, 0.69, 0.21]
    for y, t in zip(dys, ["BOSSbase 1.01\n600 covers", "Source-cover split\n360 / 120 / 120",
                          "Stego generation\n3,600 images"]):
        rect(ax, dx, y, dw, dh, t)
    for a, b in zip(dys[:-1], dys[1:]):
        arrow(ax, (dx + dw / 2, a), (dx + dw / 2, b + dh))

    # two detectors in parallel: feature extraction -> training
    fx, tx, cw, lh = 1.12, 2.09, 0.80, 0.34
    lanes = [(0.95, "Residual-LR", "76 residual\nfeatures", "Logistic\nregression"),
             (0.33, "SRM+Ensemble", "SRM features\n(34,671-D)", "FLD\nensemble")]
    for y, name, feat, clf in lanes:
        ax.text(fx, y + lh + 0.07, name, ha="left", va="center", fontsize=6.8, style="italic")
        rect(ax, fx, y, cw, lh, feat)
        rect(ax, tx, y, cw, lh, clf)
        arrow(ax, (fx + cw, y + lh / 2), (tx, y + lh / 2))
    ys_in = dys[2] + dh / 2
    line(ax, [dx + dw, 1.04], [ys_in, ys_in])
    line(ax, [1.04, 1.04], [ys_in, lanes[0][0] + lh / 2])
    for y, *_ in lanes:
        arrow(ax, (1.04, y + lh / 2), (fx, y + lh / 2))

    # evaluation of P1/P2/P3 models on the same test covers
    ex, ew, ey, eh = 3.06, 0.64, 0.33, 0.96
    rect(ax, ex, ey, ew, eh, "P1/P2/P3\nevaluation")
    for y, *_ in lanes:
        arrow(ax, (tx + cw, y + lh / 2), (ex, y + lh / 2))

    # robustness and security metrics (evaluation branches)
    mx, mw, bh, gap = 3.85, 0.945, 0.22, 0.07
    labels = ["RQ1: algorithm shift", "RQ2: mixed training", "RQ3: payload shift", "Low-FPR operation"]
    bys = [0.20 + k * (bh + gap) for k in range(4)][::-1]
    ax.text(mx + mw / 2, 1.46, "Robustness and\nsecurity metrics", ha="center", va="center", fontsize=7,
            linespacing=1.1)
    for y, t in zip(bys, labels):
        rect(ax, mx, y, mw, bh, t, size=6.8)
    bus = 3.78
    line(ax, [ex + ew, bus], [ey + eh / 2, ey + eh / 2])
    line(ax, [bus, bus], [bys[-1] + bh / 2, bys[0] + bh / 2])
    for y in bys:
        arrow(ax, (bus, y + bh / 2), (mx, y + bh / 2))
    fig.savefig(OUT / "fig1_pipeline.png", dpi=600)
    fig.savefig(OUT / "fig1_pipeline.pdf")
    plt.close(fig)
    to_gray(OUT / "fig1_pipeline.png")


# --------------------------------------------------------------------------- Fig. 2
def figure2():
    fig, axes = plt.subplots(1, 2, figsize=(4.7, 1.9), sharey=True, gridspec_kw={"wspace": 0.1})
    pairs = [(p, a) for p in PROTOCOLS for a in ALGORITHMS]
    ys = list(range(len(pairs)))[::-1]
    style = {"Residual-LR": dict(fmt="o", mfc="black"), "SRM+Ensemble": dict(fmt="s", mfc="white")}
    for ax, d, tag in zip(axes, ["Residual-LR", "SRM+Ensemble"], ["(a)", "(b)"]):
        for y, (p, a) in zip(ys, pairs):
            delta, lo, hi = RQ3[(d, p, a)]
            ax.errorbar([delta], [y], xerr=[[delta - lo], [hi - delta]], color="black", ms=3.2, mec="black",
                        elinewidth=0.7, capsize=1.8, capthick=0.7, **style[d])
        ax.axvline(0, color="black", lw=0.5, ls=(0, (3, 2)))
        for yy in (2.5, 5.5):
            ax.axhline(yy, color="0.75", lw=0.4, ls=(0, (1, 1.5)))
        ax.set_xlim(-0.225, 0.04)
        ax.set_xticks([-0.20, -0.15, -0.10, -0.05, 0.0], ["−0.20", "−0.15", "−0.10", "−0.05", "0"])
        ax.set_title(f"{tag} {d}", fontsize=7.5, loc="center", pad=3)
        ax.tick_params(length=2)
        for s in ("top", "right"):
            ax.spines[s].set_visible(False)
    axes[1].spines["left"].set_visible(False)
    axes[1].tick_params(axis="y", left=False)
    axes[0].set_yticks(ys, [f"{p} {a}" for p, a in pairs])
    axes[0].set_ylim(-0.6, len(pairs) - 0.4)
    fig.subplots_adjust(bottom=0.2, top=0.9)
    fig.supxlabel("ΔAUC = AUC(0.1 bpp) − AUC(0.4 bpp)", fontsize=7.5, y=0.01)
    for ext in ("png", "pdf"):
        fig.savefig(OUT / f"fig2_payload_shift.{ext}", bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)
    to_gray(OUT / "fig2_payload_shift.png")


if __name__ == "__main__":
    figure1()
    figure2()
    print("figures written to", OUT)
