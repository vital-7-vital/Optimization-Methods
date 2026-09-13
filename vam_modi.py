import numpy as np

def vam(cost, supply, demand):
    cost = np.array(cost, dtype=float)
    supply = supply.copy()
    demand = demand.copy()

    m = len(supply)
    n = len(demand)

    allocation = np.zeros((m, n))

    while sum(supply) > 0 and sum(demand) > 0:

        row_penalty = [-1] * m
        col_penalty = [-1] * n

        for i in range(m):
            if supply[i] > 0:
                values = [
                    cost[i][j]
                    for j in range(n)
                    if demand[j] > 0
                ]

                values.sort()

                if len(values) >= 2:
                    row_penalty[i] = values[1] - values[0]
                elif len(values) == 1:
                    row_penalty[i] = values[0]

        for j in range(n):
            if demand[j] > 0:
                values = [
                    cost[i][j]
                    for i in range(m)
                    if supply[i] > 0
                ]

                values.sort()

                if len(values) >= 2:
                    col_penalty[j] = values[1] - values[0]
                elif len(values) == 1:
                    col_penalty[j] = values[0]

        max_row = max(row_penalty)
        max_col = max(col_penalty)

        if max_row >= max_col:
            i = row_penalty.index(max_row)

            j = min(
                [j for j in range(n) if demand[j] > 0],
                key=lambda j: cost[i][j]
            )

        else:
            j = col_penalty.index(max_col)

            i = min(
                [i for i in range(m) if supply[i] > 0],
                key=lambda i: cost[i][j]
            )

        quantity = min(supply[i], demand[j])

        allocation[i][j] = quantity

        supply[i] -= quantity
        demand[j] -= quantity

    return allocation


def northwest_corner(supply, demand):
    supply = supply.copy()
    demand = demand.copy()

    m = len(supply)
    n = len(demand)

    allocation = np.zeros((m, n))

    i = 0
    j = 0

    while i < m and j < n:

        quantity = min(supply[i], demand[j])

        allocation[i][j] = quantity

        supply[i] -= quantity
        demand[j] -= quantity

        if supply[i] == 0:
            i += 1

        if demand[j] == 0:
            j += 1

    return allocation


def find_loop(allocation, start):
    m = len(allocation)
    n = len(allocation[0])

    def search(path):
        i, j = path[-1]

        for new_j in range(n):
            cell = (i, new_j)

            if new_j != j:
                if cell == start and len(path) >= 4:
                    return path

                if allocation[i][new_j] > 0 and cell not in path:
                    result = search(path + [cell])

                    if result:
                        return result

        for new_i in range(m):
            cell = (new_i, j)

            if new_i != i:
                if cell == start and len(path) >= 4:
                    return path

                if allocation[new_i][j] > 0 and cell not in path:
                    result = search(path + [cell])

                    if result:
                        return result

        return None

    return search([start])


def modi(cost, allocation):
    cost = np.array(cost, dtype=float)

    m = len(cost)
    n = len(cost[0])

    while True:

        u = [None] * m
        v = [None] * n

        u[0] = 0

        changed = True

        while changed:
            changed = False

            for i in range(m):
                for j in range(n):

                    if allocation[i][j] > 0:

                        if u[i] is not None and v[j] is None:
                            v[j] = cost[i][j] - u[i]
                            changed = True

                        elif v[j] is not None and u[i] is None:
                            u[i] = cost[i][j] - v[j]
                            changed = True

        delta = np.zeros((m, n))

        for i in range(m):
            for j in range(n):

                if allocation[i][j] == 0:
                    delta[i][j] = cost[i][j] - u[i] - v[j]

        entering = None
        minimum = 0

        for i in range(m):
            for j in range(n):

                if allocation[i][j] == 0:

                    if delta[i][j] < minimum:
                        minimum = delta[i][j]
                        entering = (i, j)

        if entering is None:
            break

        loop = find_loop(allocation, entering)

        if loop is None:
            break

        minus_cells = loop[1::2]

        theta = min(
            allocation[i][j]
            for i, j in minus_cells
        )

        for k, (i, j) in enumerate(loop):

            if k % 2 == 0:
                allocation[i][j] += theta
            else:
                allocation[i][j] -= theta

    return allocation


def total_cost(cost, allocation):
    total = 0

    for i in range(len(cost)):
        for j in range(len(cost[0])):
            total += cost[i][j] * allocation[i][j]

    return total


cost = [
    [19, 30, 50, 10],
    [70, 30, 40, 60],
    [40, 8, 70, 20]
]

supply = [7, 9, 18]

demand = [5, 8, 7, 14]

if sum(supply) != sum(demand):
    print("The transportation problem is not balanced.")

else:

    print("1. VAM")
    print("2. MODI")

    choice = int(input("Enter your choice: "))

    if choice == 1:

        allocation = vam(cost, supply, demand)

        print("\nVAM Initial Basic Feasible Solution:")
        print(allocation.astype(int))

        print(
            "\nTransportation Cost =",
            int(total_cost(cost, allocation))
        )

    elif choice == 2:

        allocation = northwest_corner(supply, demand)

        print("\nInitial Basic Feasible Solution:")
        print(allocation.astype(int))

        allocation = modi(cost, allocation)

        print("\nMODI Optimal Solution:")
        print(allocation.astype(int))

        print(
            "\nMinimum Transportation Cost =",
            int(total_cost(cost, allocation))
        )

    else:
        print("Invalid choice.")