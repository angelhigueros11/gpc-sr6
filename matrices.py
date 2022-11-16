# Graficas por computador
# Angel Higueros - 20460
# SR6

def multmv(matrix, vector):
    if len(matrix) == len(vector):
        return [sum(matrix[i][j] * vector[j] for j in range(len(vector))) for i in range(len(matrix))]

    else:
        print("error matrix 1")


def mult(matrix1, matrix2):
    results = []
    try:
        for i in range(len(matrix1)):
            rows = [sum(matrix1[i][k] * matrix2[k][j]
                        for k in range(len(matrix1[0]))) for j in range(len(matrix2[0]))]

            results.append(rows)
        return results
    except Exception:
        print("error matrix 2")
