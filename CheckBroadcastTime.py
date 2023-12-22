import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
import math
import random


"""
Checks if a graph is a broadcast graph, by attempting to generate minimum broadcast time 
spanning trees from every node
"""


# Checks if we can a minimum broadcast time at every node
# If possible, graph is a broadcast graph
def is_broadcast_graph(G, max_attempts=200, max_broadcast_time=-1):
    G = nx.convert_node_labels_to_integers(G)
    broadcast_time = max(math.ceil(math.log2(G.number_of_nodes())), max_broadcast_time)
    total_attempts = 0

    for source in G.nodes:
        allowed_attempts = max_attempts
        total_attempts += 1
        spanning_tree = is_broadcast_spanning_tree_possible(G, source, broadcast_time)
        while not spanning_tree and allowed_attempts > 0:
            total_attempts += 1
            allowed_attempts -= 1

            spanning_tree = is_broadcast_spanning_tree_possible(
                G, source, broadcast_time
            )

        if not spanning_tree:
            print("Fails at node", source)
            return False

    print("Average attempts per source: ", total_attempts / G.number_of_nodes())
    return True


# Newest Version
# Checks if we can create spanning tree of minimum broadcast time from a source
# of any degree
def is_broadcast_spanning_tree_possible(G, source, broadcast_time):
    queue = deque([source])
    visited = [False] * G.number_of_nodes()
    visited[source] = True

    # stores the degree needed for each node to fulfill a broadcast spanning tree
    expected_degree = [0] * G.number_of_nodes()
    expected_degree[source] = broadcast_time

    # preprocessing as the source is already visited
    # reduces the degree of the source's neighbours, since we work with the available degree
    remaining_degree = [degree for node, degree in G.degree]
    for source_neighbor in G.neighbors(source):
        remaining_degree[source_neighbor] -= 1

    while queue:
        current_node = queue.popleft()

        unvisited_neighbors = [
            neighbor for neighbor in G.neighbors(current_node) if not visited[neighbor]
        ]
        random.shuffle(unvisited_neighbors)
        sorted_neighbors = sorted(
            unvisited_neighbors, key=lambda x: remaining_degree[x], reverse=True
        )

        for neighbor in sorted_neighbors:
            if expected_degree[current_node] == 0:
                break

            expected_degree[current_node] -= 1
            expected_degree[neighbor] = expected_degree[current_node]

            visited[neighbor] = True
            queue.append(neighbor)

            for second_neighbor in G.neighbors(neighbor):
                remaining_degree[second_neighbor] -= 1

    # Checks if every node was visited
    return visited.count(False) == 0


# Shows all spanning tree
def show_broadcast_spanning_trees(G, max_attempts=200, max_broadcast_time=-1):
    G = nx.convert_node_labels_to_integers(G)
    failed_nodes = 0
    broadcast_time = max(math.ceil(math.log2(G.number_of_nodes())), max_broadcast_time)

    for source in G.nodes:
        allowed_attempts = max_attempts
        spanning_tree = generate_broadcast_spanning_tree(G, source, broadcast_time)

        while not spanning_tree and allowed_attempts > 0:
            allowed_attempts -= 1
            spanning_tree = generate_broadcast_spanning_tree(G, source, broadcast_time)

        if not spanning_tree:
            failed_nodes += 1
            print("No broadcast spanning tree found at node", source)
            continue

        node_colors = [
            "red" if node == source else "skyblue" for node in spanning_tree.nodes
        ]

        pos = nx.kamada_kawai_layout(spanning_tree)

        nx.draw(
            spanning_tree,
            pos=pos,
            with_labels=True,
            font_weight="bold",
            node_color=node_colors,
            edge_color="gray",
        )

        plt.show()

    if failed_nodes > 0:
        print("Could not find broadcast spanning tree for", failed_nodes, "nodes")
    else:
        print("Found a broadcast spanning tree for every node")


# Same logic as is_broadcast_spanning_tree_possible(), but returns the broadcast spanning tree if it is found
def generate_broadcast_spanning_tree(G, source, broadcast_time):
    # creates a tree
    Tree = nx.Graph()

    queue = deque([source])
    visited = [False] * G.number_of_nodes()
    visited[source] = True

    expected_degree = [0] * G.number_of_nodes()
    expected_degree[source] = broadcast_time

    remaining_degree = [degree for node, degree in G.degree]
    for source_neighbor in G.neighbors(source):
        remaining_degree[source_neighbor] -= 1

    while queue:
        current_node = queue.popleft()

        unvisited_neighbors = [
            neighbor for neighbor in G.neighbors(current_node) if not visited[neighbor]
        ]
        random.shuffle(unvisited_neighbors)
        sorted_neighbors = sorted(
            unvisited_neighbors, key=lambda x: remaining_degree[x], reverse=True
        )

        for neighbor in sorted_neighbors:
            if expected_degree[current_node] == 0:
                break

            # Adds edge for each visited vertex
            Tree.add_edge(current_node, neighbor)

            expected_degree[current_node] -= 1
            expected_degree[neighbor] = expected_degree[current_node]

            visited[neighbor] = True
            queue.append(neighbor)

            for second_neighbor in G.neighbors(neighbor):
                remaining_degree[second_neighbor] -= 1

    # Returns the spanning tree if every vertex is visited
    if visited.count(False) > 0:
        return None

    return Tree


# Version 2, code works, but only applies to v2 vertices and hard to grasp
"""
# Checks if we can create spanning tree of broadcast time 5, when starting at a vertex 2
def is_spanning_tree_possible_version_2(G, source):
    Tree = nx.Graph()
    queue = deque([source]) 
    visited = [False] * 24

    expected_degree = [0] * 24
    expected_degree[source] = 5

    # preprocessing as the source is already visited
    # reduces the degree of the source's neighbours, since we work with the available degree
    visited[source] = True
    remaining_degree = [degree for node, degree in G.degree]
    for source_neighbor in G.neighbors(source):
        remaining_degree[source_neighbor] -= 1
    
    # Node where we can skip a branch
    skip_node = [False] * G.number_of_nodes()
    skip_happened = False

    while queue:
        current_node = queue.popleft()

        expected_degree[current_node] -= 1

        unvisited_neighbors = [
            neighbor for neighbor in G.neighbors(current_node) if not visited[neighbor]
        ]
        random.shuffle(unvisited_neighbors)
        sorted_neighbors = sorted(
            unvisited_neighbors, key=lambda x: remaining_degree[x], reverse=True
        )

        print([(n,remaining_degree[n]) for n in sorted_neighbors])

        for neighbor in sorted_neighbors:
            if skip_node[current_node] and expected_degree[current_node] == 0:
                break

            if expected_degree[current_node] == -1:
                break

            if remaining_degree[neighbor] < expected_degree[current_node] - 1:
                return False

            if remaining_degree[neighbor] == expected_degree[current_node] - 1:
                if skip_happened:
                    return False
                skip_happened = True
                skip_node[neighbor] = True

            Tree.add_edge(current_node, neighbor)
            expected_degree[neighbor] = expected_degree[current_node]
            expected_degree[current_node] -= 1

            visited[neighbor] = True
            queue.append(neighbor)

            for second_neighbor in G.neighbors(neighbor):
                remaining_degree[second_neighbor] -= 1

            

        if current_node == source:
            continue
        if expected_degree[current_node] > 1:
            return False
        if expected_degree[current_node] == 1 and not skip_node[current_node]:
            return False

    # Makes sure every node is visited
    if visited.count(False) > 0:
        return False
    
    return Tree
    # return visited.count(False) == 0
"""

# Version 1, code does not run as intended, and complexity was higher
"""
def is_spanning_tree_possible_version_1(G, source):
    remaining_degree = [degree + 1 for node, degree in G.degree]
    stack = list(G.neighbors(source))

    visited = [False] * 24
    visited[source] = True

    max_branch_degrees = [0] * 24

    root_branch_degree = 5
    branch_degree_sum = 0

    # shuffles then sorts by degree
    neighbors = list(G.neighbors(source))
    random.shuffle(neighbors)
    sorted_neighbors = sorted(
        neighbors, key=lambda x: remaining_degree[x], reverse=True
    )

    for neighbor in sorted_neighbors:
        max_branch_degrees[neighbor] = root_branch_degree
        remaining_degree[neighbor] = min(remaining_degree[neighbor], root_branch_degree)
        branch_degree_sum += remaining_degree[neighbor]
        root_branch_degree -= 1

    missing_branch_allowed = True
    skip_node = [False] * 24
    if branch_degree_sum == 8:
        missing_branch_allowed = False
        if remaining_degree[stack[0]] > remaining_degree[stack[1]]:
            skip_node[stack[1]] = True
        else:
            skip_node[stack[0]] = True

    while stack:
        current_node = stack.pop()

        # skips already visited nodes
        if visited[current_node]:
            continue

        visited[current_node] = True
        max_branch_degrees[current_node] -= 1

        neighbors = list(G.neighbors(current_node))
        random.shuffle(neighbors)
        sorted_neighbors = sorted(
            neighbors, key=lambda x: remaining_degree[x], reverse=True
        )

        # print([remaining_degree[n] for n in sorted_neighbors])

        for neighbor in sorted_neighbors:
            if skip_node[current_node] and max_branch_degrees[current_node] == 1:
                break

            if max_branch_degrees[current_node] == 0:
                break

            if remaining_degree[neighbor] < max_branch_degrees[current_node] - 1:
                return False

            if remaining_degree[neighbor] == max_branch_degrees[current_node] - 1:
                if not missing_branch_allowed:
                    return False
                missing_branch_allowed = False
                skip_node[neighbor] = True

            
            max_branch_degrees[current_node] -= 1
            max_branch_degrees[neighbor] = max_branch_degrees[current_node]
            stack.append(neighbor)

            for second_neighbor in G.neighbors(neighbor):
                remaining_degree[second_neighbor] -= 1

        if max_branch_degrees[current_node] > 1:
            return False
        if max_branch_degrees[current_node] == 1 and not skip_node[current_node]:
            return False

    print(visited.count(True))

    return True
"""

# Attempted to find a hueristic on nodes being of a certain distance, however
# it turns out this was almost always true, therefore not useful.
"""
def satisfies_distance(G, source):
    visited = set()
    distances = [None] * 24
    distances[source] = 0

    queue = deque([source])

    while queue:
        current_node = queue.popleft()

        if current_node in visited:
            continue

        visited.add(current_node)
        neighbors = G.neighbors(current_node)
        next_distance = distances[current_node] + 1

        for neighbor in neighbors:
            if distances[neighbor] is None:
                distances[neighbor] = next_distance
                queue.append(neighbor)

    d_count = [0] * 6

    for d in distances:
        d_count[d] += 1

    if not d_count[1] + d_count[2] >= 3:
        return False

    if not d_count[1] + d_count[2] + d_count[3] >= 6:
        return False

    if not d_count[1] + d_count[2] + d_count[3] + d_count[4] >= 12:
        return False

    return True
"""