
# ============================================================
# AI Mid-Term Lab Project
# Network Attack Path Simulation using AI Search Algorithms
# ============================================================
# Group Members:
#   1. Zohaib Hanif Khokhar  - FA24-BCS-082
#   2. Mir Mustafa           - FA24-BCS-062
#   3. Ali Eshan             - FA24-BCS-075
# Course: Artificial Intelligence
# Institution: COMSATS University Islamabad
# ============================================================

import heapq
import math
from collections import deque

# ─────────────────────────────────────────────
# NETWORK GRAPH DEFINITION
# ─────────────────────────────────────────────
# Nodes represent network hosts/devices
# Edges represent connections with attack cost (weight)
# Heuristics represent estimated cost to reach target

graph = {
    'Internet':     {'Router': 3, 'Firewall': 2},
    'Firewall':     {'DMZ_Server': 4, 'IDS': 1},
    'IDS':          {'DMZ_Server': 2},
    'Router':       {'Switch': 5, 'Firewall': 1},
    'DMZ_Server':   {'Web_Server': 3, 'Mail_Server': 2},
    'Switch':       {'Workstation_A': 2, 'Workstation_B': 3, 'Database': 6},
    'Web_Server':   {'Database': 4, 'App_Server': 2},
    'Mail_Server':  {'App_Server': 3},
    'App_Server':   {'Database': 1},
    'Workstation_A':{'Database': 5},
    'Workstation_B':{'Database': 4},
    'Database':     {}
}

heuristics = {
    'Internet':      10,
    'Firewall':       9,
    'IDS':            8,
    'Router':         8,
    'DMZ_Server':     6,
    'Switch':         7,
    'Web_Server':     4,
    'Mail_Server':    5,
    'App_Server':     2,
    'Workstation_A':  5,
    'Workstation_B':  4,
    'Database':       0   # Goal node
}

START  = 'Internet'
GOAL   = 'Database'

# ─────────────────────────────────────────────
# 1. BFS — Breadth-First Search
# ─────────────────────────────────────────────
def bfs(graph, start, goal):
    queue   = deque([[start]])
    visited = set([start])
    nodes_explored = 0

    while queue:
        path = queue.popleft()
        node = path[-1]
        nodes_explored += 1

        if node == goal:
            cost = path_cost(path, graph)
            return path, cost, nodes_explored

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return None, float('inf'), nodes_explored

# ─────────────────────────────────────────────
# 2. DFS — Depth-First Search
# ─────────────────────────────────────────────
def dfs(graph, start, goal):
    stack   = [[start]]
    visited = set()
    nodes_explored = 0

    while stack:
        path = stack.pop()
        node = path[-1]

        if node in visited:
            continue
        visited.add(node)
        nodes_explored += 1

        if node == goal:
            cost = path_cost(path, graph)
            return path, cost, nodes_explored

        for neighbor in reversed(list(graph[node])):
            if neighbor not in visited:
                stack.append(path + [neighbor])

    return None, float('inf'), nodes_explored

# ─────────────────────────────────────────────
# 3. UCS — Uniform Cost Search
# ─────────────────────────────────────────────
def ucs(graph, start, goal):
    pq    = [(0, [start])]
    visited = {}
    nodes_explored = 0

    while pq:
        cost, path = heapq.heappop(pq)
        node = path[-1]

        if node in visited:
            continue
        visited[node] = cost
        nodes_explored += 1

        if node == goal:
            return path, cost, nodes_explored

        for neighbor, weight in graph[node].items():
            if neighbor not in visited:
                heapq.heappush(pq, (cost + weight, path + [neighbor]))

    return None, float('inf'), nodes_explored

# ─────────────────────────────────────────────
# 4. A* Search
# ─────────────────────────────────────────────
def astar(graph, start, goal, heuristics):
    pq    = [(heuristics[start], 0, [start])]
    visited = {}
    nodes_explored = 0

    while pq:
        f, g, path = heapq.heappop(pq)
        node = path[-1]

        if node in visited:
            continue
        visited[node] = g
        nodes_explored += 1

        if node == goal:
            return path, g, nodes_explored

        for neighbor, weight in graph[node].items():
            if neighbor not in visited:
                new_g = g + weight
                new_f = new_g + heuristics.get(neighbor, 0)
                heapq.heappush(pq, (new_f, new_g, path + [neighbor]))

    return None, float('inf'), nodes_explored

# ─────────────────────────────────────────────
# 5. Hill Climbing (Greedy)
# ─────────────────────────────────────────────
def hill_climbing(graph, start, goal, heuristics):
    path    = [start]
    visited = set([start])
    nodes_explored = 0

    while True:
        node = path[-1]
        nodes_explored += 1

        if node == goal:
            cost = path_cost(path, graph)
            return path, cost, nodes_explored

        neighbors = [(heuristics.get(n, float('inf')), n)
                     for n in graph[node] if n not in visited]

        if not neighbors:
            return None, float('inf'), nodes_explored  # stuck at local optimum

        neighbors.sort()
        best_h, best_node = neighbors[0]

        # Move only if heuristic improves
        if best_h >= heuristics.get(node, float('inf')):
            return None, float('inf'), nodes_explored  # local optimum

        visited.add(best_node)
        path.append(best_node)

# ─────────────────────────────────────────────
# 6. Minimax
# ─────────────────────────────────────────────
minimax_tree = {
    'root': {'children': ['A', 'B'], 'type': 'max'},
    'A':    {'children': ['A1', 'A2'], 'type': 'min'},
    'B':    {'children': ['B1', 'B2'], 'type': 'min'},
    'A1':   {'value': 3},
    'A2':   {'value': 5},
    'B1':   {'value': 2},
    'B2':   {'value': 9},
}

def minimax(node, tree, is_maximizing):
    data = tree[node]
    if 'value' in data:
        return data['value'], [node]

    children = data['children']
    results = [(minimax(c, tree, not is_maximizing), c) for c in children]

    if is_maximizing:
        best_val = max(r[0][0] for r in results)
    else:
        best_val = min(r[0][0] for r in results)

    for (val, path), child in results:
        if val == best_val:
            return best_val, [node] + path

    return best_val, [node]

# ─────────────────────────────────────────────
# 7. Alpha-Beta Pruning
# ─────────────────────────────────────────────
ab_nodes_explored = 0

def alpha_beta(node, tree, alpha, beta, is_maximizing):
    global ab_nodes_explored
    ab_nodes_explored += 1
    data = tree[node]

    if 'value' in data:
        return data['value'], [node]

    children = data['children']
    best_path = []

    if is_maximizing:
        max_val = float('-inf')
        for child in children:
            val, path = alpha_beta(child, tree, alpha, beta, False)
            if val > max_val:
                max_val = val
                best_path = [node] + path
            alpha = max(alpha, val)
            if beta <= alpha:
                break
        return max_val, best_path
    else:
        min_val = float('inf')
        for child in children:
            val, path = alpha_beta(child, tree, alpha, beta, True)
            if val < min_val:
                min_val = val
                best_path = [node] + path
            beta = min(beta, val)
            if beta <= alpha:
                break
        return min_val, best_path

# ─────────────────────────────────────────────
# UTILITY
# ─────────────────────────────────────────────
def path_cost(path, graph):
    cost = 0
    for i in range(len(path) - 1):
        cost += graph[path[i]].get(path[i+1], float('inf'))
    return cost

# ─────────────────────────────────────────────
# RUN ALL ALGORITHMS & COMPARE
# ─────────────────────────────────────────────
def run_all():
    print("=" * 65)
    print("  AI NETWORK ATTACK PATH SIMULATION")
    print("  Group Members:")
    print("    1. Zohaib Hanif Khokhar  — FA24-BCS-082")
    print("    2. Mir Mustafa           — FA24-BCS-062")
    print("    3. Ali Eshan             — FA24-BCS-075")
    print("=" * 65)
    print(f"\n  Start Node : {START}")
    print(f"  Goal  Node : {GOAL}")
    print("=" * 65)

    results = {}

    # BFS
    path, cost, exp = bfs(graph, START, GOAL)
    results['BFS'] = (path, cost, exp)
    print(f"\n[1] BFS")
    print(f"    Path     : {' -> '.join(path)}")
    print(f"    Cost     : {cost}")
    print(f"    Explored : {exp} nodes")

    # DFS
    path, cost, exp = dfs(graph, START, GOAL)
    results['DFS'] = (path, cost, exp)
    print(f"\n[2] DFS")
    print(f"    Path     : {' -> '.join(path)}")
    print(f"    Cost     : {cost}")
    print(f"    Explored : {exp} nodes")

    # UCS
    path, cost, exp = ucs(graph, START, GOAL)
    results['UCS'] = (path, cost, exp)
    print(f"\n[3] UCS")
    print(f"    Path     : {' -> '.join(path)}")
    print(f"    Cost     : {cost}")
    print(f"    Explored : {exp} nodes")

    # A*
    path, cost, exp = astar(graph, START, GOAL, heuristics)
    results['A*'] = (path, cost, exp)
    print(f"\n[4] A*")
    print(f"    Path     : {' -> '.join(path)}")
    print(f"    Cost     : {cost}")
    print(f"    Explored : {exp} nodes")

    # Hill Climbing
    path, cost, exp = hill_climbing(graph, START, GOAL, heuristics)
    results['Hill Climbing'] = (path, cost, exp)
    print(f"\n[5] Hill Climbing")
    if path:
        print(f"    Path     : {' -> '.join(path)}")
        print(f"    Cost     : {cost}")
    else:
        print(f"    Result   : Stuck at local optimum")
    print(f"    Explored : {exp} nodes")

    # Minimax
    val, path = minimax('root', minimax_tree, True)
    print(f"\n[6] Minimax")
    print(f"    Best Value : {val}")
    print(f"    Path       : {' -> '.join(path)}")

    # Alpha-Beta
    global ab_nodes_explored
    ab_nodes_explored = 0
    val, path = alpha_beta('root', minimax_tree, float('-inf'), float('inf'), True)
    print(f"\n[7] Alpha-Beta Pruning")
    print(f"    Best Value : {val}")
    print(f"    Path       : {' -> '.join(path)}")
    print(f"    Nodes Explored (pruned): {ab_nodes_explored}")

    # ── Comparison Table ──
    print("\n" + "=" * 65)
    print("  COMPARATIVE ANALYSIS")
    print("=" * 65)
    print(f"  {'Algorithm':<18} {'Cost':>6}  {'Nodes Explored':>15}  {'Optimal?':>9}")
    print(f"  {'-'*18} {'-'*6}  {'-'*15}  {'-'*9}")
    optimal_cost = results['UCS'][1]
    for algo, (p, c, e) in results.items():
        is_opt = "Yes" if c == optimal_cost else "No"
        cost_str = str(c) if p else "N/A"
        print(f"  {algo:<18} {cost_str:>6}  {e:>15}  {is_opt:>9}")
    print("=" * 65)

if __name__ == '__main__':
    run_all()
