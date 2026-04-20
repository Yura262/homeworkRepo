# Завдання 2 (Модель SIS)
import matplotlib
from numpy.random import random
import networkx as nx
from matplotlib import pyplot as plt
import pycxsimulator

matplotlib.use('TkAgg')

# Параметри моделі 

p_i = 0.5  # Ймовірність зараження
p_r = 0.5  # Ймовірність одужання

p_i = 0.2  # Ймовірність зараження
p_r = 0.8  # Ймовірність одужання

p_i = 0.6  # Ймовірність зараження
p_r = 0.4  # Ймовірність одужання

def initialize():
    global G, nextG
    G = nx.karate_club_graph()
    G.pos = nx.spring_layout(G)

    for i in G.nodes:
        # Стан 0: S (сприйнятливий), Стан 1: I (інфікований)
        # Початково інфікуємо випадкову частину мережі
        G.nodes[i]['state'] = 1 if random() < 0.2 else 0

    nextG = G.copy()

def observe():
    global G
    plt.cla()
    colors = ['red' if G.nodes[i]['state'] == 1 else 'blue' for i in G.nodes]
    nx.draw(G, node_color=colors, pos=G.pos, with_labels=True)
    plt.title(f"SIS Model: p_i={p_i}, p_r={p_r}")

def update():
    global G, nextG

    for i in G.nodes():
        if G.nodes[i]['state'] == 1:
            # Інфікований індивід одужує з ймовірністю p_r
            if random() < p_r:
                nextG.nodes[i]['state'] = 0
            else:
                nextG.nodes[i]['state'] = 1
        else:
            # Перевіряємо чи є хоча б один інфікований сусід
            infected_neighbors = sum(1 for j in G.neighbors(i) if G.nodes[j]['state'] == 1)
            if infected_neighbors > 0:
                # Сприйнятливий заражається з ймовірністю p_i
                if random() < p_i:
                    nextG.nodes[i]['state'] = 1
                else:
                    nextG.nodes[i]['state'] = 0
            else:
                nextG.nodes[i]['state'] = 0

    # Синхронне оновлення станів
    for i in G.nodes():
        G.nodes[i]['state'] = nextG.nodes[i]['state']

pycxsimulator.GUI().start(func=[initialize, observe, update])