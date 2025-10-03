import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# データ生成（前の例と同じ）
rng = np.random.default_rng(42)
n = 10
days = np.arange(n)

od_A = 0.05 * np.exp(0.45 * days) + rng.normal(0, 0.03, n)
od_A = np.clip(od_A, a_min=0, a_max=None)
rna_A = 80 * od_A + rng.normal(0, 0.1, n)

od_B = 0.1 + 0.07 * days + rng.normal(0, 0.02, n)
rna_B = 6 * od_B + 0.5 * (days / days.max()) + rng.normal(0, 0.2, n)

growth = 0.08 * np.exp(0.5 * np.minimum(days, 6))
decay = np.where(days > 6, 0.15 * (days - 6), 0)
od_C = growth - decay + rng.normal(0, 0.02, n)
rna_C = 0.5 * (1 - (od_C / (od_C.max() + 1e-9))) * 8 + 0.2 * (days > 6) * (days - 6)
rna_C += rng.normal(0, 0.15, n)

df = pd.DataFrame({
    "system": (["A_log↑"] * n) + (["B_moderate"] * n) + (["C_death↑RNA"] * n),
    "day": np.concatenate([days, days, days]),
    "OD": np.concatenate([od_A, od_B, od_C]),
    "RNA_expr": np.concatenate([rna_A, rna_B, rna_C])
})

# プロット
fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(111, projection='3d')

lines = {}
for sys, group in df.groupby("system"):
    g = group.sort_values("day")
    line, = ax.plot(g["day"], g["OD"], g["RNA_expr"], marker='o', label=sys)
    lines[sys] = line

ax.set_xlabel("Day")
ax.set_ylabel("OD")
ax.set_zlabel("RNA expression (a.u.)")
ax.legend()

# 回転アニメーション関数
def rotate(angle):
    ax.view_init(elev=20, azim=angle)

ani = FuncAnimation(fig, rotate, frames=360, interval=50)
plt.show()
