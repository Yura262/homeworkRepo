# Завдання 1
import networkx as nx
import matplotlib.pyplot as plt

n = 4
m = n - 1

# Генерація графів
K_n = nx.complete_graph(n)
K_nm = nx.complete_bipartite_graph(n, m)
C_m = nx.cycle_graph(m)

# Перевірка на планарність
print(f"K_n планарний: {nx.check_planarity(K_n)[0]}")
print(f"K_n,m планарний: {nx.check_planarity(K_nm)[0]}")
print(f"C_m планарний: {nx.check_planarity(C_m)[0]}")

# Візуалізація графів
plt.figure(figsize=(15, 5))

plt.subplot(131)
plt.title(f"K_{n}")
nx.draw_circular(K_n, node_size=30, node_color="blue")

plt.subplot(132)
plt.title(f"K_{n},{m}")
nx.draw_spring(K_nm, node_size=30, node_color="green")

plt.subplot(133)
plt.title(f"C_{m}")
nx.draw_circular(C_m, node_size=30, node_color="red")

plt.show()

# Об'єднання графів в один. 
# Використовуємо disjoint_union_all для автоматичного перейменування вершин, 
# щоб уникнути конфліктів ідентифікаторів
G_combined = nx.disjoint_union_all([K_n, K_nm, C_m])

# Додавання довільних ребер (мостів) між компонентами
# Компонента 1 (K_n) має вершини від 0 до 3
# Компонента 2 (K_nm) має вершини від 4 до 10
# Компонента 3 (C_m) має вершини від 11 до 13
G_combined.add_edge(0, 4)
G_combined.add_edge(10, 11)



color_map = []
for node in G_combined:
    if node < 4:  # K_n nodes (0-3)
        color_map.append('blue')
    elif node < 11:  # K_nm nodes (4-10)
        color_map.append('green')
    else:  # C_m nodes (11-13)
        color_map.append('red')
        
plt.figure(figsize=(10, 8))
pos = nx.spring_layout(G_combined, seed=42) # seed for consistent layout

nx.draw(G_combined, pos, with_labels=True, node_color=color_map, 
        edge_color='gray', node_size=500, font_size=10)
plt.title("Combined Graph with Bridges")
plt.show()



# Виведення результатів
print(f"\nКількість вершин у новому графі: {G_combined.number_of_nodes()}")
print(f"Кількість ребер у новому графі: {G_combined.number_of_edges()}")

print("\nСписок вершин:")
print(list(G_combined.nodes()))

print("\nСписок ребер:")
print(list(G_combined.edges()))

print("\nСписок суміжності:")
for line in nx.generate_adjlist(G_combined):
    print(line)