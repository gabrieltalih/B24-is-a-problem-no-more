import networkx as nx
import matplotlib.pyplot as plt
import CheckBroadcastTime


"""
First and second graph are broadcast graphs, while the third graph is not, but we use it for testing
"""
def main():
    for i in range(3):
        showBroacastGraph(i)
        CheckBroadcastTime.show_spanning_trees(graphs[i])


graphs = [None] * 3

# creates the four 6-cycles for each graph
for i in range(3):
    graphs[i] = nx.Graph()
    graphs[i].add_edges_from(
        [
            # cycle 1
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 0),
            # cycle 2
            (6, 7),
            (7, 8),
            (8, 9),
            (9, 10),
            (10, 11),
            (11, 6),
            # cycle 3
            (12, 13),
            (13, 14),
            (14, 15),
            (15, 16),
            (16, 17),
            (17, 12),
            # cycle 4
            (18, 19),
            (19, 20),
            (20, 21),
            (21, 22),
            (22, 23),
            (23, 18),
        ]
    )


# Adds the three 4-cycles to connects all four 6-cycles
# 12 vertices will be of degree 2, and 12 vertices will be of degree 4
graphs[0].add_edges_from(
    [
        # new cycle 1
        (0, 6),
        (6, 12),
        (12, 18),
        (18, 0),
        # new cycle 2
        (2, 8),
        (8, 14),
        (14, 20),
        (20, 2),
        # new cycle 3
        (4, 10),
        (10, 16),
        (16, 22),
        (22, 4),
    ]
)


# Alternates the connection across the 6-cylces horizontally and vertically to adjacent cycles
# All vertices will be of degree 3
graphs[1].add_edges_from(
    [
        # cycle 1 --> cycle 2 and 4
        (0, 6),
        (1, 19),
        (2, 8),
        (3, 21),
        (4, 10),
        (5, 23),
        # cycle 3 --> cycle 2 and 4
        (12, 18),
        (13, 7),
        (14, 20),
        (15, 9),
        (16, 22),
        (17, 11),
    ]
)

# Same as the second graph but missing an edge, not a broadcast graph
graphs[2].add_edges_from(
    [
        # cycle 1 --> cycle 2 and 4
        (0, 6),
        (1, 19),
        (2, 8),
        (3, 21),
        (4, 10),
        (5, 23),
        # cycle 3 --> cycle 2 and 4
        (12, 18),
        (13, 7),
        (14, 20),
        (15, 9),
        (16, 22),
        # missing edge
    ]
)


def getBroadcastGraph(index):
    return graphs[index]


def showBroacastGraph(index):
    # to display the graph properly
    hexagon_positions = {
        # cycle 1
        0: (0, 1),
        1: (0.5, 1.866),
        2: (1, 1),
        3: (1, 0),
        4: (0.5, -0.866),
        5: (0, 0),
        # cycle 2
        6: (2, 1.5),
        7: (2.5, 2.366),
        8: (3, 1.5),
        9: (3, 0.5),
        10: (2.5, -0.366),
        11: (2, 0.5),
        # cycle 3
        12: (2.5, -3),
        13: (3.0, -2.134),
        14: (3.5, -3),
        15: (3.5, -4),
        16: (3.0, -4.866),
        17: (2.5, -4),
        # cycle 4
        18: (0.5, -3.5),
        19: (1.0, -2.634),
        20: (1.5, -3.5),
        21: (1.5, -4.5),
        22: (1.0, -5.366),
        23: (0.5, -4.5),
    }
    nx.draw(
        graphs[index],
        pos=hexagon_positions,
        with_labels=True,
        font_weight="bold",
        node_color="skyblue",
        edge_color="gray",
    )

    plt.show()


if __name__ == "__main__":
    main()
