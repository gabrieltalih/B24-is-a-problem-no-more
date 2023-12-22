import networkx as nx
import random


"""
Contains code to generate graphs based on the constraint solutions
"""


# Matches every e23 edge with an e25plus edge to make it possible such that the
# broadcast time for any v2 vertex is 5
# Additionally matches e35plus edges to not connect to e23 and e25plus on the same v2 node
def match_e23_e25plus_and_e35plus_edges(
    G,
    expected_vertex_degree,
    e23,
    e25plus,
    e35plus,
    v2,
    start_index_v3,
    v3,
    start_index_v5plus,
    v5plus,
    max_attempts=5000,
):
    not_allowed_edges = nx.Graph()
    allowed_attempts = max_attempts

    # Number of e23 edges <= number of v2
    for v in range(e23):
        index_i = start_index_v3 + random.randint(0, v3 - 1)
        index_j = start_index_v5plus + random.randint(0, v5plus - 1)

        while (
            G.degree(index_i) >=  expected_vertex_degree[index_i]
            or G.degree(index_j) >= expected_vertex_degree[index_j]
        ):
            if allowed_attempts < 0:
                return False
            index_i = start_index_v3 + random.randint(0, v3 - 1)
            index_j = start_index_v5plus + random.randint(0, v5plus - 1)
            allowed_attempts -= 1

        G.add_edge(v, index_i)
        G.add_edge(v, index_j)
        not_allowed_edges.add_edge(index_i,index_j)
        e25plus -= 1

    allowed_attempts = max_attempts

    # adds e35plus edges as to not make a triangle between a v2, v3 and v5plus vertex
    while e35plus > 0:
        if allowed_attempts < 0:
            return False

        allowed_attempts -= 1
        index_i = start_index_v3 + random.randint(0, v3 - 1)
        index_j = start_index_v5plus + random.randint(0, v5plus - 1)

        if (
            G.degree(index_i) < 3
            and G.degree(index_j) < expected_vertex_degree[index_j]
            and not G.has_edge(index_i, index_j)
            and not not_allowed_edges.has_edge(index_i,index_j)
        ):
            G.add_edge(index_i, index_j)
            e35plus -= 1
    

    # adds remaining e25plus edges
    return add_eij_edges(
        G, expected_vertex_degree, e25plus, 0, v2, start_index_v5plus, v5plus
    )


def add_eii_edges(
    G, expected_vertex_degree, eii, start_index_vi, vi, max_attempts=3000
):
    allowed_attempts = max_attempts

    while eii > 0:
        if allowed_attempts < 0:
            return False

        allowed_attempts -= 1
        index_i = start_index_vi + random.randint(0, vi - 1)
        index_j = start_index_vi + random.randint(0, vi - 1)

        if (
            index_i != index_j
            and G.degree(index_i) < expected_vertex_degree[index_i]
            and G.degree(index_j) < expected_vertex_degree[index_j]
            and not G.has_edge(index_i, index_j)
        ):
            G.add_edge(index_i, index_j)
            eii -= 1

    return True


def add_eij_edges(
    G,
    expected_vertex_degree,
    eij,
    start_index_vi,
    vi,
    start_index_vj,
    vj,
    max_attempts=3000,
):
    allowed_attempts = max_attempts

    while eij > 0:
        if allowed_attempts < 0:
            return False

        allowed_attempts -= 1
        index_i = start_index_vi + random.randint(0, vi - 1)
        index_j = start_index_vj + random.randint(0, vj - 1)

        if (
            G.degree(index_i) < expected_vertex_degree[index_i]
            and G.degree(index_j) < expected_vertex_degree[index_j]
            and not G.has_edge(index_i, index_j)
        ):
            G.add_edge(index_i, index_j)
            eij -= 1

    return True


def create_random_graph(values):
    # expected array format and index:
    #  0 |  1 |  2 |  3 |    4   |   5   |  6  |  7  |    8    |  9  |  10 |    11   |  12 |    13   |   14
    # v2 | v3 | v4 | v5 | v6plus | delta | e23 | e24 | e25plus | e33 | e34 | e35plus | e44 | e45plus | e55plus

    if len(values) != 15:
        raise ValueError("Array must have exactly 15 elements")

    expected_vertex_degree = [None] * 24

    expected_degree_index = 0

    for degree in range(2, 6):
        # sets v2 number of nodes to degree 2, sets v3 number of nodes
        # to degree 3 etc.
        for i in range(values[degree - 2]):
            expected_vertex_degree[expected_degree_index] = degree
            expected_degree_index += 1

    # sets v6plus number of nodes to max degree
    for i in range(values[4]):
        expected_vertex_degree[expected_degree_index] = values[5]
        expected_degree_index += 1

    G = nx.Graph()

    G.add_nodes_from(range(24))

    v2 = values[0]
    v3 = values[1]
    v4 = values[2]
    v5plus = values[3] + values[4]

    v5 = values[3]
    v6plus = values[4]
    max_degree = values[5]

    start_index_v2 = 0
    start_index_v3 = v2
    start_index_v4 = v2 + v3
    start_index_v5plus = v2 + v3 + v4

    e23 = values[6]
    e24 = values[7]
    e25plus = values[8]
    e33 = values[9]
    e34 = values[10]
    e35plus = values[11]
    e44 = values[12]
    e45plus = values[13]
    e55plus = values[14]

    if not match_e23_e25plus_and_e35plus_edges(
        G,
        expected_vertex_degree,
        e23,
        e25plus,
        e35plus,
        v2,
        start_index_v3,
        v3,
        start_index_v5plus,
        v5plus,
    ):
        return "Error adding e23, e25plus and e35plus edges"

    eii_parameters = [
        [e33, start_index_v3, v3],
        [e44, start_index_v4, v4],
        [e55plus, start_index_v5plus, v5plus],
    ]

    for eii_parameter_set in eii_parameters:
        if not add_eii_edges(G, expected_vertex_degree, *eii_parameter_set):
            return "eii edge could not be added"

    eij_parameters = [
        [e24, start_index_v2, v2, start_index_v4, v4],
        [e34, start_index_v3, v3, start_index_v4, v4],
        [e45plus, start_index_v4, v4, start_index_v5plus, v5plus],
    ]

    for eij_parameter_set in eij_parameters:
        if not add_eij_edges(G, expected_vertex_degree, *eij_parameter_set):
            return "eij edge could not be added"

    if G.number_of_edges() != 35:
        return "Edges does not equal 35", G.number_of_edges()

    if not nx.is_connected(G):
        return "Graph is not connected"

    if nx.diameter(G) > 5:
        return "Not a broadcast graph, diameter > 5"

    degrees = dict(G.degree())
    final_degrees = degrees.values()

    max_degree_found = max(final_degrees)

    if max_degree_found != max_degree:
        return "No vertex of max degree found"

    v2_count = 0
    v3_count = 0
    v4_count = 0
    v5_count = 0
    v6plus_count = 0

    for degree in final_degrees:
        if degree == 2:
            v2_count += 1
        elif degree == 3:
            v3_count += 1
        elif degree == 4:
            v4_count += 1
        elif degree == 5:
            v5_count += 1
        elif degree >= 6:
            v6plus_count += 1

    if (
        v2_count != v2
        or v3_count != v3
        or v4_count != v4
        or v5_count != v5
        or v6plus_count != v6plus
    ):
        return "Vertex degree counts don't match constraints"

    return G
