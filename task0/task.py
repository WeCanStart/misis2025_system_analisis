from collections import defaultdict

def solve(csv_string):
    edges = csv_string.strip().split('\n')
    
    graph = defaultdict(set)
    
    for edge in edges:
        a_i, a_j = map(int, edge.split(','))
        graph[a_i].add(a_j)
    
    cols = sorted(set(graph.keys()).union(*graph.values()))
    
    rows = sorted(set(graph.keys()) | {2})
    
    result = [
        [a_j in graph[a_i] for a_j in cols]
        for a_i in rows
    ]
    
    return result

# example
# print(solve('''1,2
# 1,3
# 3,4
# 3,5'''))
