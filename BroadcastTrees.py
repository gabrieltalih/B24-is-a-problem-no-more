import networkx as nx
import matplotlib.pyplot as plt
import CheckBroadcastTime


"""
File contains all broadcast trees of 24 vertices, source vertex degree 2
"""


def main():
    attempts = 0
    for tree in trees:
        spanning_tree = None
        while not spanning_tree:

            if attempts > 1000:
                raise ValueError("Issue with broadcast tree or algorithm, or unlucky probability")
            
            attempts += 1
            spanning_tree = CheckBroadcastTime.generate_spanning_tree(tree, 0, 5)

        node_colors = [
            "red" if node == 0 else "skyblue" for node in spanning_tree.nodes
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

    print(attempts,"attempts total,", attempts / 12,"average attempts")


trees = [None] * 12

for i in range(12):
    trees[i] = nx.Graph()
    trees[i].add_edges_from(
        [
            (0, 1),
            (0, 2),
            (1, 3),
            (1, 4),
            (1, 5),
            (1, 6),
            (2, 7),
            (2, 8),
            (2, 9),
            (3, 10),
            (3, 11),
            (3, 12),
            (4, 13),
            (4, 14),
            (5, 15),
            (7, 16),
            (7, 17),
            (8, 18),
            (10, 19),
            (10, 20),
            (11, 21),
            (13, 22),
            (16, 23),
            (19, 24),
        ]
    )

trees[0].remove_node(9)
trees[1].remove_node(18)
trees[2].remove_node(17)
trees[3].remove_node(23)
trees[4].remove_node(6)
trees[5].remove_node(15)
trees[6].remove_node(14)
trees[7].remove_node(22)
trees[8].remove_node(12)
trees[9].remove_node(21)
trees[10].remove_node(20)
trees[11].remove_node(24)

for i in range(12):
    trees[i] = nx.convert_node_labels_to_integers(trees[i])


def getBroadcastTree(index):
    return trees[index]


def showBroadcastTree(index):
    tree = trees[index]

    node_colors = [
        "red" if node == 0 else "skyblue" for node in tree.nodes
    ]

    pos = nx.kamada_kawai_layout(tree)

    nx.draw(
        tree,
        pos=pos,
        with_labels=True,
        font_weight="bold",
        node_color=node_colors,
        edge_color="gray",
    )

    plt.show()


if __name__ == "__main__":
    main()
