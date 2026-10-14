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
W, H = 4.8, 2.5   # inches; data coordinates are inches


def rect(ax, x, y, w, h, text, ls="-", size=7.2, style="normal"):
    ax.add_patch(Rectangle((x, y), w, h, fill=False, ec="black", lw=LW, ls=ls))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=size, style=style,
                linespacing=1.15)


def arrow(ax, p, q):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=5.5, lw=LW, color="black",
                                 shrinkA=0, shrinkB=0))


def line(ax, xs, ys):
    ax.plot(xs, ys, color="black", lw=LW, solid_capstyle="butt")


def figure1():
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    # data preparation: left column, top to bottom
    cw, ch = 1.15, 0.46
    ys = [1.98, 1.40, 0.82]
    rect(ax, 0.005, ys[0], cw, ch, "BOSSbase 1.01\n600 covers\n256 × 256")
    rect(ax, 0.005, ys[1], cw, ch, "Source-cover split\n360 / 120 / 120\n(before embedding)")
    rect(ax, 0.005, ys[2], cw, ch, "Stego generation\nWOW, S-UNIWARD,\nHILL; 0.1, 0.4 bpp")
    for a, b in zip(ys[:-1], ys[1:]):
        arrow(ax, (0.005 + cw / 2, a), (0.005 + cw / 2, b + ch))

    # feature extraction and detector training: two parallel detectors
    fx, fw, tx, tw, lh = 1.42, 0.86, 2.47, 0.86, 0.38
    lane_y = [1.62, 0.98]
    ax.text(fx + fw / 2, 2.36, "Feature extraction", ha="center", va="center", fontsize=7.5)
    ax.text(tx + tw / 2, 2.36, "Detector training", ha="center", va="center", fontsize=7.5)
    lanes = [("Residual-LR", "76 residual\nstatistics", "Logistic\nregression"),
             ("SRM+Ensemble", "SRM features\n(34,671-D)", "FLD ensemble\n$L$ = 50, $d_{\\mathrm{sub}}$ = 500")]
    ax.add_patch(Rectangle((1.33, 0.82), 2.09, 1.42, fill=False, ec="black", lw=LW, ls=(0, (3, 2))))
    for (name, feat, clf), y in zip(lanes, lane_y):
        ax.text(fx, y + lh + 0.07, name, ha="left", va="center", fontsize=7.2, style="italic")
        rect(ax, fx, y, fw, lh, feat)
        rect(ax, tx, y, tw, lh, clf)
        arrow(ax, (fx + fw, y + lh / 2), (tx, y + lh / 2))
    ax.text(3.37, 0.88, "P1–P3, 3 seeds, 360 pairs per run", ha="right", va="center", fontsize=6.6,
            style="italic")
    # stego images feed both detectors
    mid = 1.25
    y3 = ys[2] + ch / 2
    line(ax, [0.005 + cw, mid], [y3, y3])
    line(ax, [mid, mid], [y3, lane_y[0] + lh / 2])
    for y in lane_y:
        arrow(ax, (mid, y + lh / 2), (fx, y + lh / 2))

    # evaluation of every trained model on the shared test covers
    ex, ew, ey, eh = 3.60, 1.195, 0.98, 1.02
    rect(ax, ex, ey, ew, eh, "P1/P2/P3 evaluation\n\n120 test covers\n6 test conditions\n(3 algorithms × 2 payloads)",
         size=7)
    for y in lane_y:
        arrow(ax, (tx + tw + 0.09, y + lh / 2), (ex, y + lh / 2))

    # evaluation branches
    bw, bh, by = 1.13, 0.24, 0.43
    gap = (W - 0.01 - 4 * bw) / 3
    bxs = [0.005 + i * (bw + gap) for i in range(4)]
    labels = ["RQ1: algorithm shift", "RQ2: mixed training", "RQ3: payload shift", "Low-FPR operating point"]
    for x, t in zip(bxs, labels):
        rect(ax, x, by, bw, bh, t, size=7)
    bus = 0.75
    line(ax, [ex + ew / 2, ex + ew / 2], [ey, bus])
    line(ax, [bxs[0] + bw / 2, ex + ew / 2], [bus, bus])
    for x in bxs:
        arrow(ax, (x + bw / 2, bus), (x + bw / 2, by + bh))

    # metrics
    rect(ax, 0.005, 0.005, W - 0.01, 0.30,
         "Robustness and security metrics: ROC-AUC, F1, BER; paired ΔAUC with bootstrap 95% CI;\n"
         "recall and observed test FPR at " + TAU_LOW, size=7)
    for x in bxs:
        arrow(ax, (x + bw / 2, by), (x + bw / 2, 0.305))
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
