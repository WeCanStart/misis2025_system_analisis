def solve(csv_string):
    # Разбиваем входную строку на отдельные рёбра
    edges = csv_string.strip().split('\n')
    
    # Создаём словарь для хранения графа
    graph = defaultdict(set)
    
    # Заполняем граф
    for edge in edges:
        a_i, a_j = map(int, edge.split(','))
        graph[a_i].add(a_j)
    
    # Находим все уникальные вершины
    all_vertices = sorted(set(graph.keys()).union(*graph.values()))
    
    # Создаём результат в виде кортежа кортежей булевых значений
    result = tuple(
        tuple(a_j in graph[a_i] for a_j in all_vertices)
        for a_i in all_vertices
    )
    
    return result
