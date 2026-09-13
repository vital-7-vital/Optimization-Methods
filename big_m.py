import numpy as np

M = 1000000

def big_m_simplex(c, A, b, signs):
    n = len(c)
    rows = len(A)

    tableau = []
    var_names = [f"x{i+1}" for i in range(n)]

    artificial = []

    for i in range(rows):
        row = list(A[i])

        if signs[i] == "<=":
            row += [1]
            var_names.append(f"s{len(var_names) - n + 1}")

        elif signs[i] == ">=":
            row += [-1]
            var_names.append(f"s{len(var_names) - n + 1}")
            row += [1]
            artificial.append(len(var_names))
            var_names.append(f"a{len(artificial)}")

        elif signs[i] == "=":
            row += [1]
            artificial.append(len(var_names) + 1)
            var_names.append(f"a{len(artificial)}")

        tableau.append(row)

    total_vars = len(var_names)

    for i in range(rows):
        while len(tableau[i]) < total_vars:
            tableau[i].append(0)

    objective = [-x for x in c]

    while len(objective) < total_vars:
        objective.append(0)

    for index in artificial:
        objective[index - 1] = M

    tableau = np.array(tableau, dtype=float)
    b = np.array(b, dtype=float)

    tableau = np.column_stack((tableau, b))
    objective = np.append(objective, 0)

    for i in range(rows):
        basic_artificial = False

        for j in artificial:
            if abs(tableau[i][j - 1] - 1) < 1e-9:
                if np.count_nonzero(tableau[:, j - 1]) == 1:
                    basic_artificial = True
                    objective -= M * tableau[i]

        if basic_artificial:
            break

    tableau = np.vstack((tableau, objective))

    while True:
        last_row = tableau[-1]

        entering = np.argmin(last_row[:-1])

        if last_row[entering] >= -1e-9:
            break

        ratios = []

        for i in range(rows):
            if tableau[i][entering] > 1e-9:
                ratios.append(tableau[i][-1] / tableau[i][entering])
            else:
                ratios.append(np.inf)

        leaving = np.argmin(ratios)

        if ratios[leaving] == np.inf:
            print("The problem is unbounded.")
            return

        pivot = tableau[leaving][entering]
        tableau[leaving] /= pivot

        for i in range(rows + 1):
            if i != leaving:
                tableau[i] -= tableau[i][entering] * tableau[leaving]

    solution = np.zeros(n)

    for j in range(n):
        column = tableau[:-1, j]

        if np.count_nonzero(abs(column) > 1e-9) == 1:
            row = np.where(abs(column - 1) < 1e-9)[0]

            if len(row) == 1:
                solution[j] = tableau[row[0], -1]

    for index in artificial:
        if tableau[:-1, index - 1].max() > 1e-9:
            print("The problem is infeasible.")
            return

    print("Optimal Solution")
    print()

    for i in range(n):
        print(f"x{i+1} =", round(solution[i], 4))

    print("Maximum Z =", round(np.dot(c, solution), 4))


c = [3, 2]

A = [
    [1, 1],
    [1, 0],
    [0, 1]
]

b = [4, 1, 1]

signs = ["<=", ">=", ">="]

big_m_simplex(c, A, b, signs)