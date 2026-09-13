import numpy as np

M = 1000000
EPS = 1e-9


def solve_big_m(c, A, b, signs):
    m = len(A)
    n = len(c)

    for i in range(m):
        if b[i] < 0:
            A[i] = [-x for x in A[i]]
            b[i] = -b[i]

            if signs[i] == "<=":
                signs[i] = ">="
            elif signs[i] == ">=":
                signs[i] = "<="

    table = [row[:] for row in A]
    names = [f"x{i + 1}" for i in range(n)]
    basis = [None] * m
    artificial = []

    for i in range(m):

        if signs[i] == "<=":
            col = [0] * m
            col[i] = 1

            for r in range(m):
                table[r].append(col[r])

            names.append(f"s{i + 1}")
            basis[i] = len(names) - 1

        elif signs[i] == ">=":
            col = [0] * m
            col[i] = -1

            for r in range(m):
                table[r].append(col[r])

            names.append(f"e{i + 1}")

            col = [0] * m
            col[i] = 1

            for r in range(m):
                table[r].append(col[r])

            names.append(f"a{i + 1}")
            artificial.append(len(names) - 1)
            basis[i] = len(names) - 1

        elif signs[i] == "=":
            col = [0] * m
            col[i] = 1

            for r in range(m):
                table[r].append(col[r])

            names.append(f"a{i + 1}")
            artificial.append(len(names) - 1)
            basis[i] = len(names) - 1

        else:
            print("Invalid constraint sign.")
            return

    table = np.array(table, dtype=float)
    table = np.column_stack((table, np.array(b, dtype=float)))

    objective = np.zeros(len(names) + 1)
    objective[:n] = -np.array(c, dtype=float)

    for j in artificial:
        objective[j] = M

    for i in range(m):
        if basis[i] in artificial:
            objective -= M * table[i]

    table = np.vstack((table, objective))

    for _ in range(1000):

        entering = np.argmin(table[-1, :-1])

        if table[-1, entering] >= -EPS:
            break

        ratios = []

        for i in range(m):
            if table[i, entering] > EPS:
                ratios.append(table[i, -1] / table[i, entering])
            else:
                ratios.append(np.inf)

        leaving = np.argmin(ratios)

        if ratios[leaving] == np.inf:
            print("The problem is unbounded.")
            return

        pivot = table[leaving, entering]

        table[leaving] /= pivot

        for i in range(m + 1):
            if i != leaving:
                table[i] -= table[i, entering] * table[leaving]

        basis[leaving] = entering

    solution = np.zeros(len(names))

    for i in range(m):
        solution[basis[i]] = table[i, -1]

    for j in artificial:
        if solution[j] > 1e-6:
            print("The problem is infeasible.")
            return

    print("\nOptimal Solution")

    for i in range(n):
        print(f"x{i + 1} = {solution[i]:.4f}")

    print(f"Maximum Z = {np.dot(c, solution[:n]):.4f}")


print("BIG-M SIMPLEX METHOD")
print()

n = int(input("Enter number of decision variables: "))
m = int(input("Enter number of constraints: "))

c = list(map(float, input("Enter objective function coefficients: ").split()))

A = []
b = []
signs = []

for i in range(m):
    row = list(
        map(
            float,
            input(f"Enter coefficients of constraint {i + 1}: ").split()
        )
    )

    sign = input(
        f"Enter sign of constraint {i + 1} (<=, >=, =): "
    ).strip()

    rhs = float(
        input(f"Enter RHS of constraint {i + 1}: ")
    )

    A.append(row)
    signs.append(sign)
    b.append(rhs)

if len(c) != n or any(len(row) != n for row in A):
    print("Invalid number of coefficients.")
else:
    solve_big_m(c, A, b, signs)