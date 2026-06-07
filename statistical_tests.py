# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║  STATISTICAL TESTS PANEL: Gaussian OU Process vs Actual IEX DAM Prices    ║
# ╚══════════════════════════════════════════════════════════════════════════════╝
#
# Paste this cell into main.ipynb AFTER cell 11 (the failure-analysis figure).
# It relies on variables already defined in earlier cells:
#   • mcp_values   — numpy array of actual MCP prices  (shape: 2976,)
#   • X_sim        — numpy array of simulated OU paths  (shape: 2976, 200)
# ──────────────────────────────────────────────────────────────────────────────

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats

# ---------------------------------------------------------------------------
# 0.  Prepare data
# ---------------------------------------------------------------------------
actual = mcp_values.copy()
sim_mean = np.mean(X_sim, axis=1)          # representative simulated path

# ---------------------------------------------------------------------------
# 1.  Run all three tests and print results to console
# ---------------------------------------------------------------------------

# ── Jarque-Bera ──────────────────────────────────────────────────────────────
jb_actual_stat, jb_actual_p = stats.jarque_bera(actual)
jb_sim_stat, jb_sim_p       = stats.jarque_bera(sim_mean)

skew_actual   = stats.skew(actual)
kurt_actual   = stats.kurtosis(actual)          # excess kurtosis
skew_sim      = stats.skew(sim_mean)
kurt_sim      = stats.kurtosis(sim_mean)

print("=" * 72)
print("  JARQUE-BERA NORMALITY TEST")
print("=" * 72)
print(f"  Actual MCP  →  JB = {jb_actual_stat:>12.2f},  p = {jb_actual_p:.4e}"
      f"  {'REJECT H₀' if jb_actual_p < 0.05 else 'FAIL TO REJECT H₀'} (α=0.05)")
print(f"                 Skewness = {skew_actual:+.4f},  Excess Kurtosis = {kurt_actual:+.4f}")
print(f"  Simulated   →  JB = {jb_sim_stat:>12.2f},  p = {jb_sim_p:.4e}"
      f"  {'REJECT H₀' if jb_sim_p < 0.05 else 'FAIL TO REJECT H₀'} (α=0.05)")
print(f"                 Skewness = {skew_sim:+.4f},  Excess Kurtosis = {kurt_sim:+.4f}")
print()

# ── Kolmogorov-Smirnov ───────────────────────────────────────────────────────
ks2_stat, ks2_p = stats.ks_2samp(actual, sim_mean)
ks1_stat, ks1_p = stats.kstest(
    actual, 'norm', args=(np.mean(actual), np.std(actual, ddof=1))
)

print("=" * 72)
print("  KOLMOGOROV-SMIRNOV TESTS")
print("=" * 72)
print(f"  Two-sample (Actual vs Sim mean)")
print(f"    D = {ks2_stat:.6f},  p = {ks2_p:.4e}"
      f"  {'REJECT H₀' if ks2_p < 0.05 else 'FAIL TO REJECT H₀'} (α=0.05)")
print(f"  One-sample (Actual vs fitted Normal)")
print(f"    D = {ks1_stat:.6f},  p = {ks1_p:.4e}"
      f"  {'REJECT H₀' if ks1_p < 0.05 else 'FAIL TO REJECT H₀'} (α=0.05)")
print()

# ── Anderson-Darling ─────────────────────────────────────────────────────────
ad_actual = stats.anderson(actual, dist='norm')
ad_sim    = stats.anderson(sim_mean, dist='norm')

print("=" * 72)
print("  ANDERSON-DARLING NORMALITY TEST")
print("=" * 72)
print(f"  Actual MCP  →  A² = {ad_actual.statistic:.4f}")
for sl, cv in zip(ad_actual.significance_level, ad_actual.critical_values):
    exceeded = "***EXCEEDED***" if ad_actual.statistic > cv else ""
    print(f"    {sl:5.1f}% significance:  critical value = {cv:.4f}  {exceeded}")
print(f"  Simulated   →  A² = {ad_sim.statistic:.4f}")
for sl, cv in zip(ad_sim.significance_level, ad_sim.critical_values):
    exceeded = "***EXCEEDED***" if ad_sim.statistic > cv else ""
    print(f"    {sl:5.1f}% significance:  critical value = {cv:.4f}  {exceeded}")
print("=" * 72)
print()

# ---------------------------------------------------------------------------
# 2.  Build the figure  (22 × 8)
#     Top row  = 3 subplots (charts only, no annotation clutter)
#     Bottom   = annotation text boxes placed via fig.text() below each axis
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(22, 8))

# Use GridSpec: top 55% for plots, bottom 45% reserved for text boxes
gs = gridspec.GridSpec(
    2, 3,
    height_ratios=[1.0, 0.75],
    hspace=0.05,          # minimal gap — text boxes sit right below axes
    wspace=0.30
)

# Create the three plot axes (top row only)
ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[0, 1])
ax3 = fig.add_subplot(gs[0, 2])

# Create invisible axes for text boxes (bottom row)
ax_txt1 = fig.add_subplot(gs[1, 0])
ax_txt2 = fig.add_subplot(gs[1, 1])
ax_txt3 = fig.add_subplot(gs[1, 2])
for a in [ax_txt1, ax_txt2, ax_txt3]:
    a.axis('off')

fig.suptitle(
    "Statistical Tests: Gaussian OU vs Actual IEX DAM Prices",
    fontsize=15, fontweight='bold', y=0.98
)

# Colour palette — red for actual, gray for simulated
CLR_ACT  = '#D32F2F'   # Material Red 700
CLR_SIM  = '#757575'   # Material Grey 600
CLR_PASS = '#2E7D32'   # green
CLR_FAIL = '#C62828'   # deep-red

props = dict(boxstyle='round,pad=0.6', facecolor='#FFF9C4', alpha=0.92,
             edgecolor='#BDBDBD')

# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SUBPLOT 1 — Jarque-Bera Test                                          ║
# ╚══════════════════════════════════════════════════════════════════════════╝
ax = ax1
ax.set_title("Jarque-Bera Normality Test", fontweight='bold', fontsize=12, pad=10)

# Standardise both series so they can share the same x-axis
z_actual = (actual - np.mean(actual)) / np.std(actual)
z_sim    = (sim_mean - np.mean(sim_mean)) / np.std(sim_mean)

# Common bin edges
bins = np.linspace(-5, 5, 61)

# Histograms
ax.hist(z_actual, bins=bins, density=True, alpha=0.55, color=CLR_ACT,
        edgecolor='white', linewidth=0.4, label='Actual MCP')
ax.hist(z_sim, bins=bins, density=True, alpha=0.45, color=CLR_SIM,
        edgecolor='white', linewidth=0.4, label='Simulated (mean path)')

# Fitted normal curve
x_norm = np.linspace(-5, 5, 300)
ax.plot(x_norm, stats.norm.pdf(x_norm), 'k--', linewidth=1.5,
        label='Standard Normal')

ax.set_xlabel("Standardised Value", fontsize=10)
ax.set_ylabel("Density", fontsize=10)
ax.legend(fontsize=8, loc='upper left',
          framealpha=0.9, edgecolor='#BDBDBD')

# ── Text box BELOW subplot 1 ──
jb_act_verdict = "FAIL" if jb_actual_p < 0.05 else "PASS"
jb_sim_verdict = "FAIL" if jb_sim_p < 0.05 else "PASS"

jb_text = (
    f"── Actual ──\n"
    f"JB = {jb_actual_stat:.1f},  p = {jb_actual_p:.2e}\n"
    f"Skew = {skew_actual:+.3f},  Excess Kurt = {kurt_actual:+.3f}\n"
    f"Normality @ 5%: {jb_act_verdict}\n"
    f"\n"
    f"── Simulated ──\n"
    f"JB = {jb_sim_stat:.1f},  p = {jb_sim_p:.2e}\n"
    f"Skew = {skew_sim:+.3f},  Excess Kurt = {kurt_sim:+.3f}\n"
    f"Normality @ 5%: {jb_sim_verdict}\n"
    f"\n"
    f"⚡ {'Non-normal prices → heavy tails/spikes' if jb_actual_p < 0.05 else 'Prices appear Gaussian'}\n"
    f"{'   typical of electricity markets;' if jb_actual_p < 0.05 else '   — Gaussian OU is reasonable.'}\n"
    f"{'   Gaussian OU cannot capture this.' if jb_actual_p < 0.05 else ''}"
)
ax_txt1.text(0.50, 0.95, jb_text, transform=ax_txt1.transAxes, fontsize=8,
             verticalalignment='top', horizontalalignment='center',
             bbox=props, family='monospace')


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SUBPLOT 2 — Kolmogorov-Smirnov Test                                   ║
# ╚══════════════════════════════════════════════════════════════════════════╝
ax = ax2
ax.set_title("Kolmogorov-Smirnov Test", fontweight='bold', fontsize=12, pad=10)

# Empirical CDFs
sorted_actual = np.sort(actual)
ecdf_actual   = np.arange(1, len(sorted_actual) + 1) / len(sorted_actual)

sorted_sim    = np.sort(sim_mean)
ecdf_sim      = np.arange(1, len(sorted_sim) + 1) / len(sorted_sim)

ax.step(sorted_actual, ecdf_actual, color=CLR_ACT, linewidth=1.5,
        label='Actual ECDF', where='post')
ax.step(sorted_sim, ecdf_sim, color=CLR_SIM, linewidth=1.5,
        label='Simulated ECDF', where='post')

# Find point of maximum deviation between the two ECDFs
combined = np.sort(np.concatenate([sorted_actual, sorted_sim]))
ecdf_actual_interp = np.searchsorted(sorted_actual, combined, side='right') / len(sorted_actual)
ecdf_sim_interp    = np.searchsorted(sorted_sim, combined, side='right') / len(sorted_sim)
abs_diff = np.abs(ecdf_actual_interp - ecdf_sim_interp)
max_idx  = np.argmax(abs_diff)
x_max_dev = combined[max_idx]
y_actual_at_max = ecdf_actual_interp[max_idx]
y_sim_at_max    = ecdf_sim_interp[max_idx]

# Vertical line at max deviation
ax.plot([x_max_dev, x_max_dev],
        [min(y_actual_at_max, y_sim_at_max), max(y_actual_at_max, y_sim_at_max)],
        color='#FF6F00', linewidth=2.5, linestyle='-',
        label=f'Max D = {ks2_stat:.4f}')
ax.plot(x_max_dev, y_actual_at_max, 'o', color=CLR_ACT, markersize=6, zorder=5)
ax.plot(x_max_dev, y_sim_at_max, 'o', color=CLR_SIM, markersize=6, zorder=5)

ax.set_xlabel("MCP (Rs/MWh)", fontsize=10)
ax.set_ylabel("Cumulative Probability", fontsize=10)
ax.legend(fontsize=8, loc='lower right',
          framealpha=0.9, edgecolor='#BDBDBD')

# ── Text box BELOW subplot 2 ──
ks2_verdict = "FAIL" if ks2_p < 0.05 else "PASS"
ks1_verdict = "FAIL" if ks1_p < 0.05 else "PASS"

ks_text = (
    f"── Two-sample KS ──\n"
    f"(Actual vs Simulated mean)\n"
    f"D = {ks2_stat:.4f},  p = {ks2_p:.2e}\n"
    f"Same distribution @ 5%: {ks2_verdict}\n"
    f"\n"
    f"── One-sample KS ──\n"
    f"(Actual vs fitted Normal)\n"
    f"D = {ks1_stat:.4f},  p = {ks1_p:.2e}\n"
    f"Normality @ 5%: {ks1_verdict}\n"
    f"\n"
    f"⚡ {'Distributional gap: Gaussian OU' if ks2_p < 0.05 else 'CDFs are similar — Gaussian OU'}\n"
    f"{'   fails to replicate heavy-tailed,' if ks2_p < 0.05 else '   replicates MCP distribution'}\n"
    f"{'   spike-prone MCP distribution.' if ks2_p < 0.05 else '   adequately.'}"
)
ax_txt2.text(0.50, 0.95, ks_text, transform=ax_txt2.transAxes, fontsize=8,
             verticalalignment='top', horizontalalignment='center',
             bbox=props, family='monospace')


# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  SUBPLOT 3 — Anderson-Darling Test                                     ║
# ╚══════════════════════════════════════════════════════════════════════════╝
ax = ax3
ax.set_title("Anderson-Darling Test", fontweight='bold', fontsize=12, pad=10)

sig_labels = [f"{sl:.1f}%" for sl in ad_actual.significance_level]

y_positions = np.arange(len(sig_labels))
bar_height  = 0.35

# Critical values as background bars
bars_cv = ax.barh(y_positions + bar_height / 2, ad_actual.critical_values,
                  height=bar_height, color='#E0E0E0', edgecolor='#9E9E9E',
                  label='Critical Values')

# Actual test statistic fill
for i, cv in enumerate(ad_actual.critical_values):
    colour = CLR_FAIL if ad_actual.statistic > cv else CLR_PASS
    ax.barh(y_positions[i] + bar_height / 2, min(ad_actual.statistic, cv),
            height=bar_height, color=colour, alpha=0.7, edgecolor='none')

# Overlay simulated test statistic bars (offset below)
bars_cv_sim = ax.barh(y_positions - bar_height / 2, ad_sim.critical_values,
                      height=bar_height, color='#E0E0E0', edgecolor='#9E9E9E')
for i, cv in enumerate(ad_sim.critical_values):
    colour_s = CLR_FAIL if ad_sim.statistic > cv else CLR_PASS
    ax.barh(y_positions[i] - bar_height / 2, min(ad_sim.statistic, cv),
            height=bar_height, color=colour_s, alpha=0.4, edgecolor='none')

# Draw vertical lines for test statistics
ax.axvline(ad_actual.statistic, color=CLR_ACT, linewidth=2.5, linestyle='--',
           label=f'Actual A² = {ad_actual.statistic:.2f}')
ax.axvline(ad_sim.statistic, color=CLR_SIM, linewidth=2.5, linestyle=':',
           label=f'Simulated A² = {ad_sim.statistic:.2f}')

ax.set_yticks(y_positions)
ax.set_yticklabels(sig_labels, fontsize=9)
ax.set_ylabel("Significance Level", fontsize=10)
ax.set_xlabel("Statistic / Critical Value", fontsize=10)
ax.legend(fontsize=8, loc='lower right',
          framealpha=0.9, edgecolor='#BDBDBD')

# Mark exceeded levels with ✗ / ✓
for i, (sl, cv) in enumerate(zip(ad_actual.significance_level,
                                  ad_actual.critical_values)):
    marker = "✗" if ad_actual.statistic > cv else "✓"
    clr    = CLR_FAIL if ad_actual.statistic > cv else CLR_PASS
    ax.text(cv + 0.15, y_positions[i] + bar_height / 2, marker,
            color=clr, fontsize=12, fontweight='bold',
            verticalalignment='center')

for i, (sl, cv) in enumerate(zip(ad_sim.significance_level,
                                  ad_sim.critical_values)):
    marker = "✗" if ad_sim.statistic > cv else "✓"
    clr    = CLR_FAIL if ad_sim.statistic > cv else CLR_PASS
    ax.text(cv + 0.15, y_positions[i] - bar_height / 2, marker,
            color=clr, fontsize=10, fontweight='bold',
            verticalalignment='center', alpha=0.7)

# ── Text box BELOW subplot 3 ──
ad_act_verdict = "FAIL" if ad_actual.statistic > ad_actual.critical_values[2] else "PASS"
ad_sim_verdict = "FAIL" if ad_sim.statistic > ad_sim.critical_values[2] else "PASS"

ad_text = (
    f"── Actual ──\n"
    f"A² = {ad_actual.statistic:.2f}\n"
    f"Normal @ 5%: {ad_act_verdict}\n"
    f"\n"
    f"── Simulated ──\n"
    f"A² = {ad_sim.statistic:.2f}\n"
    f"Normal @ 5%: {ad_sim_verdict}\n"
    f"\n"
    f"⚡ {'Tail-weight mismatch: Gaussian OU' if ad_actual.statistic > ad_actual.critical_values[2] else 'Tails consistent with normality —'}\n"
    f"{'   underestimates extreme price events;' if ad_actual.statistic > ad_actual.critical_values[2] else '   Gaussian OU tail behaviour is'}\n"
    f"{'   consider jump-diffusion or' if ad_actual.statistic > ad_actual.critical_values[2] else '   adequate.'}\n"
    f"{'   regime-switching extensions.' if ad_actual.statistic > ad_actual.critical_values[2] else ''}"
)
ax_txt3.text(0.50, 0.95, ad_text, transform=ax_txt3.transAxes, fontsize=8,
             verticalalignment='top', horizontalalignment='center',
             bbox=props, family='monospace')

plt.tight_layout(pad=3.0)
plt.savefig("statistical_tests_panel.png", dpi=300, bbox_inches='tight')
plt.show()

print("\n✅ Figure saved → statistical_tests_panel.png")
