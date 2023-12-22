import CheckBroadcastTime
import pickle
import os


"""
Use this code to read a potential broadcast graph found
"""


def main():
    file_name = "B24_35 edges.pkl"

    while True:
        file_name = input("Enter the file name: ")
    
        if os.path.exists(file_name):
            break
        else:
            print("File does not exist. Please enter a valid file name.")

    with open(file_name, "rb") as file:
        loaded_graph = pickle.load(file)

    if CheckBroadcastTime.is_broadcast_graph(loaded_graph, max_attempts=300):
        print("We found one :)")
    
    CheckBroadcastTime.show_broadcast_spanning_trees(loaded_graph)


if __name__ == "__main__":
    main()
