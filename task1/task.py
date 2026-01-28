from typing import List, Tuple, Set

def main(s: str, e: str) -> Tuple[
        List[List[bool]],
        List[List[bool]],
        List[List[bool]],
        List[List[bool]],
        List[List[bool]]
    ]:
    lines = [line.strip() for line in s.splitlines() if line.strip()]
    edges = []
    nodes: Set[str] = set()
    for line in lines:
        parts = [p.strip() for p in line.split(',') if p.strip()!='']
        if len(parts) >= 2:
            a, b = parts[0], parts[1]
            edges.append((a, b))
            nodes.add(a)
            nodes.add(b)
    nodes.add(e)
    def _key(x):
        try:
            return int(x)
        except:
            return x
    nodes_sorted = sorted(nodes, key=_key)
    idx = {node: i for i, node in enumerate(nodes_sorted)}
    n = len(nodes_sorted)
    r1 = [[False]*n for _ in range(n)]
    parents = [set() for _ in range(n)]
    adj = [[] for _ in range(n)]
    for a, b in edges:
        i, j = idx[a], idx[b]
        r1[i][j] = True
        adj[i].append(j)
        parents[j].add(i)
    r2 = [[r1[j][i] for j in range(n)] for i in range(n)]
    r3 = [[False]*n for _ in range(n)]
    for src in range(n):
        visited = [False]*n
        stack = list(adj[src])
        while stack:
            u = stack.pop()
            if not visited[u]:
                visited[u] = True
                for v in adj[u]:
                    if not visited[v]:
                        stack.append(v)
        for dst in range(n):
            if dst != src and visited[dst] and not r1[src][dst]:
                r3[src][dst] = True
    r4 = [[r3[j][i] for j in range(n)] for i in range(n)]
    r5 = [[False]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            if parents[i] & parents[j]:
                r5[i][j] = r5[j][i] = True
    return (r1, r2, r3, r4, r5)

if __name__ == '__main__':
    csv_data = "1,2\n1,3\n3,4\n3,5"
    root = "1"
    r1, r2, r3, r4, r5 = main(csv_data, root)
    for name, mat in zip(['r1','r2','r3','r4','r5'], [r1,r2,r3,r4,r5]):
        print(f"{name}:")
        for row in mat:
            print(row)
        print()
