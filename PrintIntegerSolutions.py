import time


"""
Stores integer solutions of contraints in an output file
"""


# Set to True to apply new constraints
check_new_constraints_flag = True

file_name = "Integer Solutions.txt"
solution_count = 0
file_writer = None


# Writes found solutions to .txt file
def main():
    global solution_count
    global file_writer

    start_time = time.time()

    file_writer = open(file_name, "w")

    file_writer.write(
        " v2 | v3 | v4 | v5 | v6plus | delta | e23 | e24 | e25plus | e33 | e34 | e35plus | e44 | e45plus | e55plus \n"
    )

    check_vertices()

    file_writer.write("\nTotal count: " + str(solution_count))
    print("Total count: " + str(solution_count))

    end_time = time.time()
    runtime = end_time - start_time

    file_writer.write(f"\nRuntime: {runtime:.3f} seconds")
    print(f"Runtime: {runtime:.3f} seconds")

    file_writer.close()


# Makes sure the number of vertices is 24, and makes sure the total degree is 70
def check_vertices():
    for v2 in range((24) + 1):
        for v3 in range((24 - v2) + 1):
            for v4 in range((24 - v2 - v3) + 1):
                for v5 in range((24 - v2 - v3 - v4) + 1):
                    v6plus = 24 - v2 - v3 - v4 - v5

                    if v6plus > 0:
                        for delta in range(6, (23) + 1):
                            if (
                                2 * v2
                                + 3 * v3
                                + 4 * v4
                                + 5 * v5
                                + 6 * (v6plus - 1)
                                + delta * 1
                                <= 70
                            ):
                                if (
                                    2 * v2 + 3 * v3 + 4 * v4 + 5 * v5 + delta * v6plus
                                    >= 70
                                ):
                                    check_edges(v2, v3, v4, v5, v6plus, delta)

                    elif 2 * v2 + 3 * v3 + 4 * v4 + 5 * v5 == 70:
                        delta = 5 if v5 > 0 else (4 if v4 > 0 else 3)

                        check_edges(v2, v3, v4, v5, 0, delta)


# Make sure that number of edges agree with degrees of different vertices
def check_edges(v2, v3, v4, v5, v6plus, delta):
    for e23 in range(min(2 * v2, 3 * v3) + 1):
        for e24 in range(min(2 * v2, 4 * v4) + 1):
            e25plus = 2 * v2 - e23 - e24

            for e33 in range((3 * v3) // 2 + 1):
                for e34 in range(min(3 * v3 - 2 * e33 - e23, 4 * v4 - e24) + 1):
                    e35plus = 3 * v3 - e23 - 2 * e33 - e34

                    for e44 in range((4 * v4 - e24 - e34) // 2 + 1):
                        e45plus = 4 * v4 - e24 - e34 - 2 * e44
                        e55plus = (
                            35
                            - e23
                            - e24
                            - e25plus
                            - e33
                            - e34
                            - e35plus
                            - e44
                            - e45plus
                        )

                        if e55plus >= 0:
                            check_if_simple_graph(
                                v2,
                                v3,
                                v4,
                                v5,
                                v6plus,
                                delta,
                                e23,
                                e24,
                                e25plus,
                                e33,
                                e34,
                                e35plus,
                                e44,
                                e45plus,
                                e55plus,
                            )


# Constraints found by Gabriel Talih
# Checks if the number of edges gurantees no self-loops or multi-edges
def check_if_simple_graph(
    v2,
    v3,
    v4,
    v5,
    v6plus,
    delta,
    e23,
    e24,
    e25plus,
    e33,
    e34,
    e35plus,
    e44,
    e45plus,
    e55plus,
):
    v5plus = v5 + v6plus

    if not (e33 <= n_choose_2(v3)):
        return

    if not (e44 <= n_choose_2(v4)):
        return

    if not (e55plus <= n_choose_2(v5plus)):
        return
    
    # Include this constraint if we are strictly taking e55plus as only v5 connecting to v5plus
    # if not (e55plus <= n_choose_2(v5) + v5 * v6plus):
    #     return

    if not (e23 <= v2 * v3):
        return

    if not (e24 <= v2 * v4):
        return

    if not (e25plus <= v2 * v5plus):
        return

    if not (e34 <= v3 * v4):
        return

    if not (e35plus <= v3 * v5plus):
        return

    if not (e45plus <= v4 * v5plus):
        return

    check_old_constraints(
        v2,
        v3,
        v4,
        v5,
        v6plus,
        delta,
        e23,
        e24,
        e25plus,
        e33,
        e34,
        e35plus,
        e44,
        e45plus,
        e55plus,
    )


# Constraints found in "Tight lower bounds on broadcast function for n = 24 and 25"
def check_old_constraints(
    v2,
    v3,
    v4,
    v5,
    v6plus,
    delta,
    e23,
    e24,
    e25plus,
    e33,
    e34,
    e35plus,
    e44,
    e45plus,
    e55plus,
):
    global solution_count
    global file_writer

    if not (e23 <= min(2 * v3, v3 + e34 + e35plus, e25plus)):
        return

    if not (e24 <= min(3 * v4, 3 * v4 - ceiling_divide(v2 - e25plus, 2))):
        return

    if not (e25plus <= 4 * v5 + v6plus * (delta - 1) - ceiling_divide(e23, delta - 2)):
        return

    if not (e45plus + e55plus >= ceiling_divide(e23, delta - 2)):
        return

    if check_new_constraints_flag:
        return check_new_constraints(
            v2,
            v3,
            v4,
            v5,
            v6plus,
            delta,
            e23,
            e24,
            e25plus,
            e33,
            e34,
            e35plus,
            e44,
            e45plus,
            e55plus,
        )

    solution_count += 1
    file_writer.write(
        f" {v2:2} | {v3:2} | {v4:2} | {v5:2} | {v6plus:6} | {delta:5} | {e23:3} | {e24:3} | {e25plus:7} | {e33:3} | {e34:3} | {e35plus:7} | {e44:3} | {e45plus:7} | {e55plus:7} \n"
    )


# New constraints conjectured by Mohammad Hossein
def check_new_constraints(
    v2,
    v3,
    v4,
    v5,
    v6plus,
    delta,
    e23,
    e24,
    e25plus,
    e33,
    e34,
    e35plus,
    e44,
    e45plus,
    e55plus,
):
    global solution_count
    global file_writer

    v4plus = v4 + v5 + v6plus

    if not (9 <= v2 <= 12):
        return

    if not (5 <= delta <= 8):
        return

    if not (4 <= v4plus <= 9):
        return

    if not (3 <= v3 <= 11):
        return

    if not (v2 <= 6 * v4 - 2 * e24 + e25plus):
        return

    if not (v3 >= 27 - 2 * v2):
        return

    if not (2 * v2 <= e24 + 2 * e25plus):
        return

    if not (delta <= v2 - 2):
        return

    if not (5 * v2 <= 6 * v4 + 5 * e25plus):
        return

    if not (
        v4plus < v2 - 3
        or (v3 == 27 - 2 * v2 and v4 == v2 - 4 and v5 == 1 and v6plus == 0)
    ):
        return

    if not (e25plus >= 3):
        return

    if not (delta + v4plus <= v2 + 2):
        return

    if not (delta <= 2 * v2 + v3 - 22):
        return

    if not (delta <= v3 + 2):
        return

    if not (delta + v4plus <= 14):
        return

    solution_count += 1
    file_writer.write(
        f" {v2:2} | {v3:2} | {v4:2} | {v5:2} | {v6plus:6} | {delta:5} | {e23:3} | {e24:3} | {e25plus:7} | {e33:3} | {e34:3} | {e35plus:7} | {e44:3} | {e45plus:7} | {e55plus:7} \n"
    )


# preforms ceiling(a / b) but cleaner
def ceiling_divide(a, b):
    return (a + b - 1) // b


# preforms n choose 2
def n_choose_2(n):
    return (n * (n - 1)) // 2


if __name__ == "__main__":
    main()
