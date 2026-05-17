import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUTPUT = Path(__file__).resolve().parent / 'jensen_plot.svg'

plt.rcParams.update({
    'font.size': 18,
    'axes.titlesize': 16,
    'axes.labelsize': 16,
    'xtick.labelsize': 14,
    'ytick.labelsize': 14,
    'legend.fontsize': 16,
    'figure.titlesize': 20,
    'svg.hashsalt': 'alexnotes-jensen-plot'
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# === CÓNCAVA: log(x) ===
x = np.linspace(0.1, 5, 200)
y = np.log(x)

ax1.plot(x, y, 'b-', linewidth=2.5, label=r'$\log(x)$')

x1, x2 = 0.5, 4
y1, y2 = np.log(x1), np.log(x2)
ax1.plot([x1, x2], [y1, y2], 'r--', linewidth=2)
ax1.scatter([x1, x2], [y1, y2], color='red', s=80, zorder=5)

x_mid = (x1 + x2) / 2
y_curva = np.log(x_mid)
y_linea = (y1 + y2) / 2

ax1.scatter([x_mid], [y_curva], color='green', s=100, zorder=5, label=r'$f(\mathbb{E}[X])$')
ax1.scatter([x_mid], [y_linea], color='orange', s=100, zorder=5, label=r'$\mathbb{E}[f(X)]$')

# Etiquetas con notación lambda
ax1.annotate(r'$(x_1, f(x_1))$', (x1, y1), textcoords="offset points", xytext=(10, -10))
ax1.annotate(r'$(x_2, f(x_2))$', (x2, y2), textcoords="offset points", xytext=(5, -15))
ax1.annotate(r'$\lambda_1 f(x_1) + \lambda_2 f(x_2)$', (x_mid, y_linea), textcoords="offset points", xytext=(15, -12), color='orange')
ax1.annotate(r'$f(\lambda_1 x_1 + \lambda_2 x_2)$', (x_mid, y_curva), textcoords="offset points", xytext=(-110, 12),  color='green')

ax1.axhline(y=0, color='k', linewidth=0.5)
ax1.axvline(x=0, color='k', linewidth=0.5)
ax1.set_xlabel('x')
ax1.set_ylabel(r'$f(x)$')
ax1.set_title(r'Cóncava: $f(x) = \log(x)$ → $\mathbb{E}[f(X)] \leq f(\mathbb{E}[X])$')
ax1.legend(loc='lower right')
ax1.grid(True, alpha=0.3)

# === CONVEXA: x² ===
x = np.linspace(-2, 3, 200)
y = x**2

ax2.plot(x, y, 'b-', linewidth=2.5, label=r'$x^2$')

x1, x2 = -1, 2.5
y1, y2 = x1**2, x2**2
ax2.plot([x1, x2], [y1, y2], 'r--', linewidth=2)
ax2.scatter([x1, x2], [y1, y2], color='red', s=80, zorder=5)

x_mid = (x1 + x2) / 2
y_curva = x_mid**2
y_linea = (y1 + y2) / 2

ax2.scatter([x_mid], [y_curva], color='green', s=100, zorder=5, label=r'$f(\mathbb{E}[X])$')
ax2.scatter([x_mid], [y_linea], color='orange', s=100, zorder=5, label=r'$\mathbb{E}[f(X)]$')

# Etiquetas con notación lambda
ax2.annotate(r'$(x_1, f(x_1))$', (x1, y1), textcoords="offset points", xytext=(-85, -5))
ax2.annotate(r'$(x_2, f(x_2))$', (x2, y2), textcoords="offset points", xytext=(-85, 0))
ax2.annotate(r'$\lambda_1 f(x_1) + \lambda_2 f(x_2)$', (x_mid, y_linea), textcoords="offset points", xytext=(-145, 2),  color='orange')
ax2.annotate(r'$f(\lambda_1 x_1 + \lambda_2 x_2)$', (x_mid, y_curva), textcoords="offset points", xytext=(15, -2),  color='green')

ax2.axhline(y=0, color='k', linewidth=0.5)
ax2.axvline(x=0, color='k', linewidth=0.5)
ax2.set_xlabel('x')
ax2.set_ylabel(r'$f(x)$')
ax2.set_title(r'Convexa: $f(x) = x^2$ → $\mathbb{E}[f(X)] \geq f(\mathbb{E}[X])$')
ax2.legend(loc='upper left', framealpha=1)
ax2.grid(True, alpha=0.3)

plt.tight_layout(w_pad=3)
plt.savefig(OUTPUT, format='svg', bbox_inches='tight', metadata={'Date': None})
plt.close()
