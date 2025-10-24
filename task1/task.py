import numpy as np
from task0.task import main as csv_to_matrix
from typing import List, Tuple

def main(csv_string: str) -> Tuple[
        List[List[bool]],
        List[List[bool]],
        List[List[bool]],
        List[List[bool]],
        List[List[bool]]
    ]:
    # Получаем матрицу смежности из task0 (List[List[bool]])
    adj_list = csv_to_matrix(csv_string)
    adj = np.array(adj_list, dtype=bool)
    n = adj.shape[0]

    # r1 — непосредственное управление
    r1 = adj.copy()
    # r2 — непосредственное подчинение (транспонируем r1)
    r2 = r1.T.copy()

    # r3 — опосредованное управление: r1 * r1 (логическое матричное умножение)
    r3 = np.matmul(r1, r1).astype(bool) & (~r1)
    # r4 — опосредованное подчинение
    r4 = r3.T

    # r5 — соподчинённые: дети одного родителя
    # пересечение строк r2 (логическое И)
    r5 = np.zeros((n, n), dtype=bool)
    for i in range(n):
        for j in range(i+1, n):
            if np.any(r2[i] & r2[j]):
                r5[i, j] = r5[j, i] = True

    # Конвертируем всё обратно в списки списков
    return tuple(mat.tolist() for mat in (r1, r2, r3, r4, r5))

# Пример
if __name__ == '__main__':
    csv_data = '''1,2
    1,3
    3,4
    3,5'''

    r1, r2, r3, r4, r5 = main(csv_data)

    for name, mat in zip(['r1','r2','r3','r4','r5'], [r1,r2,r3,r4,r5]):
        print(f"{name}:")
        for row in mat:
            print(row)
        print()
