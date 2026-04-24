import networkx as nx
import matplotlib.pyplot as plt
import random

def simulate_diffusion(G, initial_nodes, p, k_steps):
    """
    Симуляція поширення інформації в графі.
    """
    # Множина інфікованих вузлів
    infected = set(initial_nodes)
    
    # Зберігаємо історію інфікування для візуалізації
    history = [set(infected)]
    
    for step in range(k_steps):
        new_infected = set()
        for node in infected:
            # Для орієнтованого графа перевіряємо лише тих, до кого йде ребро
            for neighbor in G.successors(node):
                if neighbor not in infected and random.random() < p:
                    new_infected.add(neighbor)
        
        infected.update(new_infected)
        history.append(set(infected))
        
    return infected, history

# 1. Створюємо граф карате клубу та перетворюємо його на орієнтований
G_undirected = nx.karate_club_graph()
G = G_undirected.to_directed()

# 2. Початкові параметри
initial_sources = [0, 33] # Вузли-джерела (президенти клубу)
probability_p = 0.3       # Імовірність передачі
steps_k = 3               # Кількість кроків

# 3. Запуск симуляції
final_infected, diffusion_history = simulate_diffusion(G, initial_sources, probability_p, steps_k)

print(f"Початкові вузли: {initial_sources}")
print(f"Інфіковані вузли після {steps_k} кроків: {sorted(list(final_infected))}")
print(f"Загальна кількість інфікованих: {len(final_infected)}")

# 4. Візуалізація результату
plt.figure(figsize=(10, 7))
pos = nx.spring_layout(G_undirected, seed=42)

# Розділяємо вузли за кольором
node_colors = ['red' if node in final_infected else 'lightblue' for node in G.nodes()]

nx.draw(G_undirected, pos, node_color=node_colors, with_labels=True, 
        node_size=500, font_weight='bold', edge_color='gray')
plt.title(f"Поширення інформації після {steps_k} кроків (Червоні - інфіковані)")
plt.show()