import networkx as nx
import GenerateGraph
import CheckBroadcastTime
import pickle


"""
Reads Integer Solutions.txt and attempts to make a valid graph, which is then tested to see if it is as broadcast graph
"""


def main():

    file_path = "Integer Solutions.txt"

    with open(file_path, "r") as file:
        lines = file.readlines()

    data = []
    for line in lines[1:-3]:  # Skips the header and last three lines
        values = [int(value.strip()) for value in line.split("|") if value.strip()]
        data.append(values)

    for dataset in data:
        print("---------------------------")
        G = None
        max_attempts = 1000

        while not isinstance(G, nx.Graph) and max_attempts >= 0:
            max_attempts -= 1
            G = GenerateGraph.create_random_graph(dataset)

        if not isinstance(G, nx.Graph):
            # prints the error
            print(G)
            continue

        if not CheckBroadcastTime.is_broadcast_graph(G):
            print("Found a non broadcast graph")
            continue

        print("Found a broadcast graph!")
        file_name = "B24_35 edges.pkl"
        with open(file_name, "wb") as file:
            pickle.dump(G, file)


if __name__ == "__main__":
    main()
