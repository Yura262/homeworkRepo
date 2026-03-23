import numpy as np

N = 100000
i = 10

def calc_exp(k, i_val=10):
    variance = (i_val + 8 - k) / (2 * i_val + 1)
    return np.sqrt(variance) 

def calc_norm(k, i_val=10):
    mean = (i_val + k) / (2 * i_val + 1)
    variance = (i_val + 7 - k) / (2 * i_val + 3)
    std_dev = np.sqrt(variance)
    return mean, std_dev

t2 = np.random.exponential(scale=calc_exp(2), size=N)
t4 = np.random.exponential(scale=calc_exp(4), size=N)
t6 = np.random.exponential(scale=calc_exp(6), size=N)
t8 = np.random.exponential(scale=calc_exp(8), size=N)

t1 = np.clip(np.random.normal(*calc_norm(1), size=N), 0, None)
t3 = np.clip(np.random.normal(*calc_norm(3), size=N), 0, None)
t5 = np.clip(np.random.normal(*calc_norm(5), size=N), 0, None)
t7 = np.clip(np.random.normal(*calc_norm(7), size=N), 0, None)

# T = min(t1, max(min(t2, t3), max(t4, t5)), t6, max(t7, t8))
# проміжні блоки:
block_2_3 = np.minimum(t2, t3)
block_4_5 = np.maximum(t4, t5)
big_parallel_block = np.maximum(block_2_3, block_4_5)
block_7_8 = np.maximum(t7, t8)

print("block_2_3",np.average(block_2_3))
print("block_4_5",np.average(block_4_5))
print("big_parallel_block",np.average(big_parallel_block))
print("block_7_8",np.average(block_7_8))



# загальний час життя для кожної ітерації
T_array = np.minimum.reduce([t1, big_parallel_block, t6, block_7_8])

reliability = np.mean(T_array)

print(f"Розрахована надійність виробу за {N} випробувань: {reliability:.4f}")