import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

# ── Journal style — no external LaTeX, clean sans-serif ───────────────────
matplotlib.rcParams.update({
    'text.usetex': False,
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans'],
    'mathtext.fontset': 'stixsans',
    'font.size': 9,
    'axes.labelsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'legend.handlelength': 1.4,
    'legend.handleheight': 0.9,
    'legend.columnspacing': 1.2,
    'axes.linewidth': 0.7,
    'xtick.major.width': 0.7,
    'ytick.major.width': 0.7,
    'xtick.minor.width': 0.5,
    'ytick.minor.width': 0.5,
    'xtick.direction': 'out',
    'ytick.direction': 'out',
    'xtick.major.size': 3.5,
    'ytick.major.size': 3.5,
    'xtick.minor.size': 2.0,
    'ytick.minor.size': 2.0,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'figure.facecolor': 'white',
})

# ── Dimensions (inches) ────────────────────────────────────────────────────
FW = 6.69  # full A4 text width  ≈ 170 mm
SW = 3.27  # single column width ≈  83 mm
FH = 2.60  # common figure height
BW = 0.38  # width of each individual bar

# ── Colour palettes ────────────────────────────────────────────────────────
c_blue   = np.array([38,  70,  83]) / 255
c_orange = np.array([42, 157, 143]) / 255
cols1 = [c_blue, c_orange]        # Ra, Rz

c_dk = np.array([ 58,  64,  90]) / 255
c_lt = np.array([174, 197, 235]) / 255
cols2 = [c_dk, c_lt]              # RON, STR, CYL

c_gry = np.array([141, 167, 190]) / 255
c_brn = np.array([ 85,  70,  64]) / 255
cols3 = [c_gry, c_brn]            # Fatigue N

LEG = [
    r'$v_c$ = 40 m/min;  $f$ = 0.05 mm/rev',
    r'$v_c$ = 80 m/min;  $f$ = 0.20 mm/rev',
]
LBL_L = ['Machining', 'Corrosion', 'AJM']
LBL_R = ['Machining', 'AJM',      'Corrosion']


# ── Helpers ────────────────────────────────────────────────────────────────
def _style_ax(ax):
    ax.yaxis.set_minor_locator(AutoMinorLocator())
    ax.grid(True, axis='y', which='major', lw=0.40, alpha=0.30, zorder=0)
    ax.grid(True, axis='y', which='minor', lw=0.30, alpha=0.18, zorder=0)


def grouped_bars(ax, M, E, labels, colors):
    """2-series grouped bar chart + symmetric errorbars. Returns [BarContainer×2]."""
    n = M.shape[0]
    x = np.arange(n)
    bcs = []
    for k, dx in enumerate((-BW / 2, BW / 2)):
        bc = ax.bar(x + dx, M[:, k], width=BW,
                    color=colors[k], edgecolor='none', zorder=3)
        ax.errorbar(x + dx, M[:, k], yerr=E[:, k],
                    fmt='none', ecolor='k', elinewidth=0.8, capsize=4, zorder=4)
        bcs.append(bc)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_xlim(-0.6, n - 0.4)
    _style_ax(ax)
    return bcs


def save_two_panel(Ml, El, lbl_l, Mr, Er, lbl_r,
                   ylabel, ylim_top, colors, fname):
    """Full-width two-panel figure with shared horizontal legend above."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(FW, FH))
    fig.subplots_adjust(left=0.09, right=0.98, bottom=0.19,
                        top=0.79, wspace=0.40)

    bcs = grouped_bars(ax1, Ml, El, lbl_l, colors)
    ax1.set_ylim(0, ylim_top)
    ax1.set_ylabel(ylabel)

    grouped_bars(ax2, Mr, Er, lbl_r, colors)
    ax2.set_ylim(0, ylim_top)
    ax2.set_ylabel(ylabel)

    fig.legend([bcs[0][0], bcs[1][0]], LEG,
               loc='upper center', ncol=2, frameon=False,
               bbox_to_anchor=(0.535, 1.01))

    fig.savefig(fname, dpi=800, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f'Saved  {fname}')


# ══════════════════════════════════════════════════════════════════════════
# Ra
# ══════════════════════════════════════════════════════════════════════════
Ra_l = np.array([[0.418, 1.584],
                 [1.430, 1.552],
                 [1.422, 1.875]])
Ra_r = np.array([[0.462, 1.621],
                 [1.782, 1.844],
                 [2.711, 2.801]])
save_two_panel(Ra_l, 0.10 * Ra_l, LBL_L,
               Ra_r, 0.10 * Ra_r, LBL_R,
               r'$R_a$ (μm)', 3.5, cols1, 'Figure_Ra.png')

# ══════════════════════════════════════════════════════════════════════════
# Rz
# ══════════════════════════════════════════════════════════════════════════
Rz_l = np.array([[ 2.914,  7.082],
                 [11.596, 10.109],
                 [10.317, 11.601]])
Rz_r = np.array([[ 3.138,  7.321],
                 [11.232, 11.923],
                 [18.391, 19.227]])
save_two_panel(Rz_l, 0.10 * Rz_l, LBL_L,
               Rz_r, 0.10 * Rz_r, LBL_R,
               r'$R_z$ (μm)', 25, cols1, 'Figure_Rz.png')

# ══════════════════════════════════════════════════════════════════════════
# RON
# ══════════════════════════════════════════════════════════════════════════
RON_l  = np.array([[6.78, 11.27],
                   [7.48,  8.96],
                   [6.07,  8.01]])
RON_r  = np.array([[6.57, 11.18],
                   [8.65, 11.06],
                   [7.92,  9.23]])
eRON_l = np.array([[4.58, 5.43],
                   [5.50, 4.14],
                   [1.91, 3.23]])
eRON_r = np.array([[2.75, 5.64],
                   [3.35, 4.98],
                   [2.66, 4.43]])
save_two_panel(RON_l, eRON_l, LBL_L,
               RON_r, eRON_r, LBL_R,
               'RON (μm)', 20, cols2, 'Figure_RON.png')

# ══════════════════════════════════════════════════════════════════════════
# STR
# ══════════════════════════════════════════════════════════════════════════
STR_l  = np.array([[ 6.67, 11.16],
                   [11.20,  9.99],
                   [ 6.52,  8.50]])
STR_r  = np.array([[ 7.35, 13.54],
                   [ 9.77, 13.69],
                   [ 7.00, 10.90]])
eSTR_l = np.array([[3.20, 5.42],
                   [6.20, 3.91],
                   [2.20, 2.08]])
eSTR_r = np.array([[3.66, 3.58],
                   [4.61, 3.41],
                   [2.80, 3.15]])
save_two_panel(STR_l, eSTR_l, LBL_L,
               STR_r, eSTR_r, LBL_R,
               'STR (μm)', 20, cols2, 'Figure_STR.png')

# ══════════════════════════════════════════════════════════════════════════
# CYL
# ══════════════════════════════════════════════════════════════════════════
CYL_l  = np.array([[ 57.61,  49.55],
                   [233.25, 215.03],
                   [143.63, 128.55]])
CYL_r  = np.array([[ 69.04,  76.26],
                   [211.10, 180.74],
                   [200.35, 146.74]])
eCYL_l = np.array([[24.52, 16.75],
                   [34.30, 89.92],
                   [34.86, 15.83]])
eCYL_r = np.array([[22.20, 51.00],
                   [67.14, 97.03],
                   [25.12, 82.05]])
save_two_panel(CYL_l, eCYL_l, LBL_L,
               CYL_r, eCYL_r, LBL_R,
               'CYL (μm)', 350, cols2, 'Figure_CYL.png')


# ══════════════════════════════════════════════════════════════════════════
# N (Fatigue) — single column, asymmetric error bars
# ══════════════════════════════════════════════════════════════════════════
N_data = np.array([[344061.667, 436997.333],
                   [240253.333, 185523.000]]) / 1e5   # scale to ×10⁵

Eneg = np.array([[138584.667, 163729.333],
                 [174863.333, 120841.000]]) / 1e5

Epos = np.array([[217986.333, 150300.667],
                 [339139.667, 178023.000]]) / 1e5

lbl_N = ['Corrosion-AJM', 'AJM-Corrosion']

fig, ax = plt.subplots(figsize=(SW, FH))
fig.subplots_adjust(left=0.22, right=0.97, bottom=0.19, top=0.79)

x = np.arange(2)
bcs_N = []
for k, dx in enumerate((-BW / 2, BW / 2)):
    bc = ax.bar(x + dx, N_data[:, k], width=BW,
                color=cols3[k], edgecolor='none', zorder=3)
    ax.errorbar(x + dx, N_data[:, k],
                yerr=[Eneg[:, k], Epos[:, k]],
                fmt='none', ecolor='k', elinewidth=0.8, capsize=4, zorder=4)
    bcs_N.append(bc)

ax.set_xticks(x)
ax.set_xticklabels(lbl_N)
ax.set_xlim(-0.6, 1.4)
ax.set_ylim(0, 7.2)
ax.set_ylabel(r'$N$ (×10$^5$ cycles)')
_style_ax(ax)

fig.legend([bcs_N[0][0], bcs_N[1][0]], LEG,
           loc='upper center', ncol=1, frameon=False,
           bbox_to_anchor=(0.60, 1.01))

fig.savefig('Figure_Fatigue_N.png', dpi=800, bbox_inches='tight', facecolor='white')
plt.close(fig)
print('Saved  Figure_Fatigue_N.png')
