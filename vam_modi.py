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
    basis = set()

    i = 0
    j = 0

    while i < m and j < n:

        quantity = min(supply[i], demand[j])

        allocation[i][j] = quantity
        basis.add((i, j))

        supply[i] -= quantity
        demand[j] -= quantity

        if supply[i] == 0 and demand[j] == 0:

            if i < m - 1 and j < n - 1:
                basis.add((i, j + 1))

            i += 1
            j += 1

        elif supply[i] == 0:
            i += 1

        elif demand[j] == 0:
            j += 1

    return allocation, basis


def find_loop(basis, start, m, n):

    def search(path, horizontal):

        i, j = path[-1]

        if horizontal:
            cells = [(i, col) for col in range(n) if col != j]
        else:
            cells = [(row, j) for row in range(m) if row != i]

        for cell in cells:

            if cell == start and len(path) >= 4:
                return path + [start]

            if cell in basis and cell not in path:

                result = search(
                    path + [cell],
                    not horizontal
                )

                if result:
                    return result

        return None

    result = search([start], True)

    if result:
        return result

    return search([start], False)


def modi(cost, allocation, basis):
    cost = np.array(cost, dtype=float)

    m = len(cost)
    n = len(cost[0])

    basis = set(basis)

    while True:

        u = [None] * m
        v = [None] * n

        u[0] = 0

        changed = True

        while changed:

            changed = False

            for i, j in basis:

                if u[i] is not None and v[j] is None:
                    v[j] = cost[i][j] - u[i]
                    changed = True

                elif v[j] is not None and u[i] is None:
                    u[i] = cost[i][j] - v[j]
                    changed = True

        opportunity = np.full((m, n), np.inf)

        for i in range(m):
            for j in range(n):

                if (i, j) not in basis:
                    opportunity[i][j] = (
                        cost[i][j] - u[i] - v[j]
                    )

        minimum = opportunity.min()

        if minimum >= 0:
            break

        entering = np.unravel_index(
            np.argmin(opportunity),
            opportunity.shape
        )

        loop = find_loop(
            basis,
            entering,
            m,
            n
        )

        if loop is None:
            break

        loop = loop[:-1]

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

        basis.add(entering)

        zero_cells = [
            cell
            for cell in minus_cells
            if abs(allocation[cell[0]][cell[1]]) < 1e-9
        ]

        if zero_cells:
            basis.remove(zero_cells[0])

    return allocation


def total_cost(cost, allocation):

    total = 0

    for i in range(len(cost)):
        for j in range(len(cost[0])):
            total += cost[i][j] * allocation[i][j]

    return total


print("TRANSPORTATION PROBLEM")
print()

m = int(input("Enter number of sources: "))
n = int(input("Enter number of destinations: "))

cost = []

print("\nEnter transportation costs row by row:")

for i in range(m):
    row = list(
        map(
            float,
            input(f"Source {i + 1}: ").split()
        )
    )

    cost.append(row)

supply = list(
    map(
        float,
        input("\nEnter supply values: ").split()
    )
)

demand = list(
    map(
        float,
        input("Enter demand values: ").split()
    )
)

if len(supply) != m or len(demand) != n:
    print("Invalid supply or demand values.")

elif any(len(row) != n for row in cost):
    print("Invalid cost matrix.")

elif sum(supply) != sum(demand):
    print("The transportation problem is not balanced.")

else:

    print("\n1. VAM")
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

        allocation, basis = northwest_corner(
            supply,
            demand
        )

        print("\nInitial Basic Feasible Solution:")
        print(allocation.astype(int))

        allocation = modi(
            cost,
            allocation,
            basis
        )

        print("\nMODI Optimal Solution:")
        print(allocation.astype(int))

        print(
            "\nMinimum Transportation Cost =",
            int(total_cost(cost, allocation))
        )

    else:
        print("Invalid choice.")