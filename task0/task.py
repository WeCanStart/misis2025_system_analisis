from collections import defaultdict
from typing import List

def main(csv_string: str) -> List[List[bool]]:
    edges = csv_string.strip().split('\n')
    
    graph = defaultdict(set)
    all_nodes = set()
    
    for edge in edges:
        a_i, a_j = map(int, edge.split(','))
        graph[a_i].add(a_j)
        all_nodes.update([a_i, a_j])
    
    # Список всех узлов в отсортированном порядке
    nodes = sorted(all_nodes)
    n = len(nodes)
    idx = {node: i for i, node in enumerate(nodes)}
    
    # Квадратная матрица n x n
    result = [[False]*n for _ in range(n)]
    
    # Заполняем матрицу
    for a_i, neighbors in graph.items():
        i = idx[a_i]
        for a_j in neighbors:
            j = idx[a_j]
            result[i][j] = True
    
    return result

# Пример
if __name__ == '__main__':
    csv_data = '''1,2
    1,3
    3,4
    3,5'''

    matrix = main(csv_data)
    for row in matrix:
        print(row)
