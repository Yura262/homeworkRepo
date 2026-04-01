import numpy as np
import matplotlib.pyplot as plt


N = 100000
i = 10

def calc_exp_scale(k, i_val=10):
    variance = (i_val + 8 - k) / (2 * i_val + 1)
    return np.sqrt(variance)

def calc_norm_params(k, i_val=10):
    mean = (i_val + k) / (2 * i_val + 1)
    variance = (i_val + 7 - k) / (2 * i_val + 3)
    return mean, np.sqrt(variance)


t2 = np.random.exponential(scale=calc_exp_scale(2), size=N)
t4 = np.random.exponential(scale=calc_exp_scale(4), size=N)
t6 = np.random.exponential(scale=calc_exp_scale(6), size=N)
t8 = np.random.exponential(scale=calc_exp_scale(8), size=N)

t1 = np.clip(np.random.normal(*calc_norm_params(1), size=N), 0, None)
t3 = np.clip(np.random.normal(*calc_norm_params(3), size=N), 0, None)
t5 = np.clip(np.random.normal(*calc_norm_params(5), size=N), 0, None)
t7 = np.clip(np.random.normal(*calc_norm_params(7), size=N), 0, None)


elements = [
    (t1, "t1 (Norm)"), (t2, "t2 (Exp)"),
    (t3, "t3 (Norm)"), (t4, "t4 (Exp)"),
    (t5, "t5 (Norm)"), (t6, "t6 (Exp)"),
    (t7, "t7 (Norm)"), (t8, "t8 (Exp)")
]


fig, axes = plt.subplots(4, 2, figsize=(12, 16))
fig.suptitle(f"Розподіл часу життя елементів (N={N}, i={i})", fontsize=16)

for idx, (data, name) in enumerate(elements):
    ax = axes[idx // 2, idx % 2]
    ax.hist(data, bins=100, color='skyblue', edgecolor='black', alpha=0.7)
    ax.axvline(np.mean(data), color='red', linestyle='dashed', linewidth=2, label=f'Mean: {np.mean(data):.3f}')
    ax.set_title(name)
    ax.set_xlabel(" ")#Час життя (t)")
    # ax.set_ylabel("Частота")
    ax.legend()

plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()