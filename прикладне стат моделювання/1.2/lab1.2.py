import numpy as np

N = 100000
i = 10

def calc_exp(k, i_val=10):
    variance = (i_val + 8 - k) / (2 * i_val + 1)
    print(f"експонентний розподіл (k={k}):")
    print("дисперсія експонентного розподілу", variance)

    val = np.random.exponential(scale=np.sqrt(variance), size=N)    
    print("середнє значення змодельованих значень",np.average(val),"\n")

    return val 

def calc_norm(k, i_val=10):
    mean = (i_val + k) / (2 * i_val + 1)
    variance = (i_val + 7 - k) / (2 * i_val + 3)
    std_dev = np.sqrt(variance)
    print(f"нормальний розподіл (k={k}):")
    print("дисперсія", variance)
    print("мат сподівання", std_dev)
    val = np.clip(np.random.normal(mean, std_dev, size=N), 0, None) 
    print("середнє значення змодельованих значень",np.average(val),"\n")

    return val


t1=calc_norm(1)
t3=calc_norm(3)
t5=calc_norm(5)
t7=calc_norm(7)

t2=calc_exp(2)
t4=calc_exp(4)
t6=calc_exp(6)
t8=calc_exp(8)

print("t1", np.average(t1))
print("t3", np.average(t3))
print("t5", np.average(t5))
print("t7", np.average(t7))

print("t2", np.average(t2))
print("t4", np.average(t4))
print("t6", np.average(t6))
print("t8", np.average(t8))





# T = min(t1, max(min(t2, t3), max(t4, t5)), t6, max(t7, t8))
# проміжні блоки:
block_2_3 = np.minimum(t2, t3)
block_4_5 = np.maximum(t4, t5)
big_parallel_block = np.maximum(block_2_3, block_4_5)
block_7_8 = np.maximum(t7, t8)

print("t2",t2)
print("t3",t3)
print("block_2_3",np.minimum(t2, t3))

print("block_2_3",np.average(block_2_3))
print("block_4_5",np.average(block_4_5))
print("parallel_block",np.average(big_parallel_block))
print("block_7_8",np.average(block_7_8))









# загальний час життя для кожної ітерації
T_array = np.minimum.reduce([t1, big_parallel_block, t6, block_7_8])

reliability = np.mean(T_array)

print(f"Розрахована надійність виробу за {N} випробувань: {reliability:.4f}")


print("\n\n\n")

for i in range(10):
    print("Спроба", i+1)

    print("  числа:")
    print("   t1 =", round(t1[i], 3), " t2 =", round(t2[i], 3),
          " t3 =", round(t3[i], 3), " t4 =", round(t4[i], 3))
    print("   t5 =", round(t5[i], 3), " t6 =", round(t6[i], 3),
          " t7 =", round(t7[i], 3), " t8 =", round(t8[i], 3))

    print("  верх = min(t2, t3) =", round(block_2_3[i], 3))
    print("  низ = max(t4, t5) =", round(block_4_5[i], 3))

    print("  середина = max(верх, низ) =", round(big_parallel_block[i], 3))
    print("  кінець = max(t7, t8) =", round(block_7_8[i], 3))

    print("  фінал = min(t1, середина, t6, кінець) =",
          round(T_array[i], 3))

    print("--------------------")