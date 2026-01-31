import json
from collections import defaultdict

def normalize(r):
    """Нормализация ранжировки: преобразование в список списков"""
    out = []
    for c in r:
        if isinstance(c, (list, tuple, set)):
            out.append(list(c))
        else:
            out.append([c])
    return out

def build_not_worse_matrix(r, idx):
    """
    Строит матрицу "не хуже" по алгоритму из документа
    M[i][j] = 1, если элемент j не хуже элемента i
    (т.е. j лучше или равен i в данной ранжировке)
    """
    n = len(idx)
    M = [[0] * n for _ in range(n)]
    
    # Нормализуем ранжировку
    r_norm = normalize(r)
    
    # На главной диагонали всегда 1 (каждый элемент не хуже себя)
    for i in range(n):
        M[i][i] = 1
    
    # Заполняем матрицу согласно ранжировке
    # Элементы в более правых группах лучше элементов в более левых группах
    for i in range(len(r_norm)):
        for j in range(i + 1, len(r_norm)):
            # Все элементы в группе j лучше всех элементов в группе i
            for elem_i in r_norm[i]:
                for elem_j in r_norm[j]:
                    row_i = idx[elem_i]
                    col_j = idx[elem_j]
                    # elem_j (в правой группе) не хуже elem_i (в левой группе)
                    M[row_i][col_j] = 1
    
    # Элементы в одной группе равны (неразличимы)
    for group in r_norm:
        if len(group) > 1:
            for elem1 in group:
                for elem2 in group:
                    if elem1 != elem2:
                        i1 = idx[elem1]
                        i2 = idx[elem2]
                        M[i1][i2] = 1
                        M[i2][i1] = 1
    
    return M

def logical_and_matrix(A, B):
    """Логическое умножение матриц (поэлементное AND)"""
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = 1 if A[i][j] and B[i][j] else 0
    return C

def find_contradictions(C, elems):
    """Находит противоречия из матрицы C (пары с взаимными 0)"""
    n = len(elems)
    contradictions = []
    
    for i in range(n):
        for j in range(i+1, n):
            if C[i][j] == 0 and C[j][i] == 0:
                contradictions.append([elems[i], elems[j]])
    
    return contradictions

def build_final_ranking(C, elems, contradictions):
    """
    Строит согласованную кластерную ранжировку
    согласно алгоритму из документа:
    1. Элементы с C[i][j]=1 и C[j][i]=1 - в один кластер
    2. Противоречивые пары (с взаимными 0) - в один кластер
    3. Строим частичный порядок между кластерами
    """
    n = len(elems)
    
    adj = [[] for _ in range(n)]
    
    for i in range(n):
        for j in range(i+1, n):
            if C[i][j] == 1 and C[j][i] == 1:
                adj[i].append(j)
                adj[j].append(i)
    
    for pair in contradictions:
        i = elems.index(pair[0])
        j = elems.index(pair[1])
        adj[i].append(j)
        adj[j].append(i)
    
    visited = [False] * n
    clusters = []
    elem_to_cluster = [0] * n
    
    for i in range(n):
        if not visited[i]:
            stack = [i]
            cluster = []
            while stack:
                v = stack.pop()
                if not visited[v]:
                    visited[v] = True
                    cluster.append(v)
                    for u in adj[v]:
                        if not visited[u]:
                            stack.append(u)
            cluster_idx = len(clusters)
            for elem_idx in cluster:
                elem_to_cluster[elem_idx] = cluster_idx
            clusters.append(cluster)
    
    k = len(clusters)
    cluster_order = [[0] * k for _ in range(k)]
    
    for i in range(n):
        for j in range(n):
            if C[i][j] == 1 and i != j:
                ci = elem_to_cluster[i]
                cj = elem_to_cluster[j]
                if ci != cj:
                    cluster_order[ci][cj] = 1
    
    for m in range(k):
        for i in range(k):
            for j in range(k):
                if cluster_order[i][m] and cluster_order[m][j]:
                    cluster_order[i][j] = 1
    
    indegree = [0] * k
    for i in range(k):
        for j in range(k):
            if cluster_order[i][j]:
                indegree[j] += 1
    
    result_order = []
    zero_degree = [i for i in range(k) if indegree[i] == 0]
    
    while zero_degree:
        current = zero_degree.pop(0)
        result_order.append(current)
        
        for j in range(k):
            if cluster_order[current][j]:
                indegree[j] -= 1
                if indegree[j] == 0:
                    zero_degree.append(j)
    
    for i in range(k):
        if indegree[i] > 0 and i not in result_order:
            result_order.append(i)
    
    final = []
    for cluster_idx in result_order:
        cluster_elems = [elems[elem_idx] for elem_idx in clusters[cluster_idx]]
        
        def sort_key(x):
            try:
                return (0, int(x))
            except:
                return (1, str(x))
        
        cluster_elems.sort(key=sort_key)
        
        if len(cluster_elems) > 1:
            final.append(cluster_elems)
        else:
            final.append(cluster_elems[0])
    
    return final

def main(s1: str, s2: str) -> str:
    r1 = json.loads(s1)
    r2 = json.loads(s2)
    
    elems = []
    seen = set()
    
    for r in [r1, r2]:
        for c in normalize(r):
            for e in c:
                if e not in seen:
                    seen.add(e)
                    elems.append(e)
    
    def elem_key(x):
        try:
            return (0, int(x))
        except:
            return (1, str(x))
    
    elems.sort(key=elem_key)
    
    idx = {elem: i for i, elem in enumerate(elems)}
    
    A = build_not_worse_matrix(r1, idx)
    B = build_not_worse_matrix(r2, idx)
    
    C = logical_and_matrix(A, B)
    
    contradictions = find_contradictions(C, elems)
    
    final_ranking = build_final_ranking(C, elems, contradictions)
    
    return json.dumps(final_ranking, ensure_ascii=False)
