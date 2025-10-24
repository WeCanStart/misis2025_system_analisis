from typing import List, Tuple
from task1.task import main as matrix_to_relations
import numpy as np

# calculate graph entropy using
# def main(csv_string: str) -> Tuple[
#         List[List[bool]],
#         List[List[bool]],
#         List[List[bool]],
#         List[List[bool]],
#         List[List[bool]]
#     ]:
#     # Получаем матрицу смежности из task0 (List[List[bool]])
#     adj_list = csv_to_matrix(csv_string)
#     adj = np.array(adj_list, dtype=bool)
#     n = adj.shape[0]

#     # r1 — непосредственное управление
#     r1 = adj.copy()
#     # r2 — непосредственное подчинение (транспонируем r1)
#     r2 = r1.T.copy()

#     # r3 — опосредованное управление: r1 * r1 (логическое матричное умножение)
#     r3 = np.matmul(r1, r1).astype(bool) & (~r1)
#     # r4 — опосредованное подчинение
#     r4 = r3.T

#     # r5 — соподчинённые: дети одного родителя
#     # пересечение строк r2 (логическое И)
#     r5 = np.zeros((n, n), dtype=bool)
#     for i in range(n):
#         for j in range(i+1, n):
#             if np.any(r2[i] & r2[j]):
#                 r5[i, j] = r5[j, i] = True

#     # Конвертируем всё обратно в списки списков
#     return tuple(mat.tolist() for mat in (r1, r2, r3, r4, r5))

# from task1.task

# and formula for particular node's and tuple's element entropy:
# calculate number of outgoing edges (n) and with s as number of nodes - 1 we have: H_ij = -n / s * log2(n / s)
# then result is sum of all H_ij (for all nodes and all tuple elements)

def main(csv_string: str) -> Tuple[int, int]:
    rs = matrix_to_relations(csv_string)
    H =  sum(sum(-sum(row) / (len(rs[0]) - 1) * (0 if sum(row) == 0 else np.log2(sum(row) / (len(rs[0]) - 1))) for row in r) for r in rs)
    return (H, H / len(rs) / (len(rs[0]) - 1))

if __name__ == '__main__':
    print(main('1,2\n1,3\n3,4\n3,5'))

# to execute this this file you need -m flag
# so use python -m task2.task