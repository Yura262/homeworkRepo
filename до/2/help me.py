import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

INF = float('inf')

class TSPNode:
    def __init__(self, matrix, lower_bound, path, edges_included, edges_excluded, node_id, parent_id=None, action_text=""):
        self.matrix = matrix
        self.lower_bound = lower_bound
        self.path = path  # Ordered list of visited nodes
        self.edges_included = edges_included
        self.edges_excluded = edges_excluded
        self.node_id = node_id
        self.parent_id = parent_id
        self.action_text = action_text # Text for the graph edge (e.g., "Include (1,5)")

def reduce_matrix(matrix):
    """Reduces the matrix and returns the reduction cost and the new matrix."""
    m = matrix.copy()
    n = m.shape[0]
    cost = 0
    
    # Row reduction
    for i in range(n):
        min_val = np.min(m[i])
        if min_val != INF and min_val > 0:
            cost += min_val
            m[i] -= min_val
            
    # Column reduction
    for j in range(n):
        min_val = np.min(m[:, j])
        if min_val != INF and min_val > 0:
            cost += min_val
            m[:, j] -= min_val
            
    return cost, m

def calculate_penalties(matrix):
    """Calculates penalties for all zeros and returns the edge with the max penalty."""
    n = matrix.shape[0]
    max_penalty = -1
    best_edge = None
    
    for i in range(n):
        for j in range(n):
            if matrix[i, j] == 0:
                # Find min in row i excluding col j
                row_min = np.min(np.concatenate((matrix[i, :j], matrix[i, j+1:])))
                # Find min in col j excluding row i
                col_min = np.min(np.concatenate((matrix[:i, j], matrix[i+1:, j])))
                
                penalty = row_min + col_min
                if penalty > max_penalty:
                    max_penalty = penalty
                    best_edge = (i, j)
                    
    return best_edge, max_penalty

def solve_tsp_branch_and_bound(initial_matrix):
    print("--- STARTING TSP BRANCH AND BOUND ---")
    
    # Initialize tree visualization data
    tree_graph = nx.DiGraph()
    node_counter = 0
    
    # Step 1: Initial Reduction
    initial_cost, reduced_m = reduce_matrix(initial_matrix)
    
    root = TSPNode(
        matrix=reduced_m, 
        lower_bound=initial_cost, 
        path=[], 
        edges_included=[], 
        edges_excluded=[], 
        node_id=node_counter
    )
    
    tree_graph.add_node(root.node_id, label=f"Root\nLB: {root.lower_bound}")
    
    # Priority Queue for nodes (simplification: list sorted by lower_bound)
    active_nodes = [root]
    best_tour_cost = INF
    best_tour = []
    
    while active_nodes:
        # Sort by lower bound (Best-First Search)
        active_nodes.sort(key=lambda x: x.lower_bound)
        current_node = active_nodes.pop(0)
        
        print(f"\n--- Exploring Node {current_node.node_id} (LB: {current_node.lower_bound}) ---")
        
        # Pruning
        if current_node.lower_bound >= best_tour_cost:
            print(f"Node {current_node.node_id} pruned. LB {current_node.lower_bound} >= Best Cost {best_tour_cost}")
            continue

        # Check if we have a complete tour (simplified check: matrix is 2x2 or fully mapped)
        if len(current_node.edges_included) == initial_matrix.shape[0] - 1: # N-1 edges means 1 left
            print(f"Found a complete tour candidates! Updating best cost if better.")
            # In a full implementation, you'd extract the final edge and check the total cost here
            # For this visualization script, we will stop expanding this branch.
            if current_node.lower_bound < best_tour_cost:
                best_tour_cost = current_node.lower_bound
            continue

        # Find best zero to branch on
        best_edge, penalty = calculate_penalties(current_node.matrix)
        if best_edge is None:
            continue
            
        r, c = best_edge
        print(f"Selected edge for branching: ({r+1}, {c+1}) with penalty {penalty}")
        
        # --- BRANCH 1: EXCLUDE EDGE ---
        node_counter += 1
        m_exclude = current_node.matrix.copy()
        m_exclude[r, c] = INF
        
        exclude_cost, m_exclude_reduced = reduce_matrix(m_exclude)
        new_lb_exclude = current_node.lower_bound + exclude_cost
        
        print(f"  -> Branch Exclude ({r+1},{c+1}): New LB = {new_lb_exclude}")
        
        exclude_node = TSPNode(
            matrix=m_exclude_reduced,
            lower_bound=new_lb_exclude,
            path=current_node.path,
            edges_included=current_node.edges_included,
            edges_excluded=current_node.edges_excluded + [(r, c)],
            node_id=node_counter,
            parent_id=current_node.node_id,
            action_text=f"Exclude ({r+1},{c+1})"
        )
        active_nodes.append(exclude_node)
        tree_graph.add_node(exclude_node.node_id, label=f"Node {exclude_node.node_id}\nLB: {exclude_node.lower_bound}")
        tree_graph.add_edge(current_node.node_id, exclude_node.node_id, label=exclude_node.action_text)

        # --- BRANCH 2: INCLUDE EDGE ---
        node_counter += 1
        m_include = current_node.matrix.copy()
        
        # Prevent subtours (simplified: block the direct reverse path)
        m_include[c, r] = INF 
        
        # Cross out row r and col c
        m_include[r, :] = INF
        m_include[:, c] = INF
        m_include[r, c] = INF # Also block the cell itself
        
        include_cost, m_include_reduced = reduce_matrix(m_include)
        new_lb_include = current_node.lower_bound + include_cost
        
        print(f"  -> Branch Include ({r+1},{c+1}): New LB = {new_lb_include}")
        
        include_node = TSPNode(
            matrix=m_include_reduced,
            lower_bound=new_lb_include,
            path=current_node.path,
            edges_included=current_node.edges_included + [(r, c)],
            edges_excluded=current_node.edges_excluded,
            node_id=node_counter,
            parent_id=current_node.node_id,
            action_text=f"Include ({r+1},{c+1})"
        )
        active_nodes.append(include_node)
        tree_graph.add_node(include_node.node_id, label=f"Node {include_node.node_id}\nLB: {include_node.lower_bound}")
        tree_graph.add_edge(current_node.node_id, include_node.node_id, label=include_node.action_text)

        # To prevent an infinite loop in this demo, limit nodes
        if node_counter > 20:
            print("Node limit reached for visualization purposes.")
            break

    draw_tree(tree_graph)

def draw_tree(G):
    """Draws the branch and bound tree using Matplotlib and NetworkX."""
    plt.figure(figsize=(12, 8))
    
    # Use a hierarchical layout (dot) if PyGraphviz is installed, 
    # otherwise fallback to a standard spring layout
    try:
        from networkx.drawing.nx_agraph import graphviz_layout
        pos = graphviz_layout(G, prog='dot')
    except ImportError:
        print("Graphviz not found. Using default layout. For a true tree layout, 'pip install pygraphviz'.")
        pos = nx.spring_layout(G)
        
    node_labels = nx.get_node_attributes(G, 'label')
    edge_labels = nx.get_edge_attributes(G, 'label')
    
    nx.draw(G, pos, with_labels=True, labels=node_labels, node_size=3000, 
            node_color='lightblue', font_size=9, font_weight='bold', 
            edge_color='gray', arrows=True)
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=8)
    
    plt.title("Branch and Bound Decision Tree")
    plt.axis('off')
    plt.show()

if __name__ == "__main__":
    # Your specific matrix
    matrix = np.array([
        [INF, 40,  34,  50,  10,  44],
        [18,  INF, 3,   38,  52,  10],
        [23,  12,  INF, 47,  42,  5 ],
        [54,  29,  56,  INF, 9,   2 ],
        [17,  31,  23,  8,   INF, 4 ],
        [28,  53,  58,  15,  41,  INF]
    ], dtype=float)
    
    solve_tsp_branch_and_bound(matrix)