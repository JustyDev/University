import collections


def read_graph_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            # Читаем первую строку, чтобы получить N и M
            first_line = f.readline()
            if not first_line:  # Проверка на пустой файл
                print("Ошибка: Файл пуст.")
                return None, None, None

            n, m = map(int, first_line.split())

            edges = []
            # Читаем M строк с рёбрами
            for _ in range(m):
                line = f.readline()
                if not line:  # Если рёбер в файле меньше чем M
                    break
                u, v = map(int, line.split())
                edges.append((u, v))

            return n, m, edges

    except FileNotFoundError:
        print(f"Ошибка: Файл '{filename}' не найден.")
        return None, None, None
    except (ValueError, IndexError):
        print(f"Ошибка: Некорректный формат данных в файле '{filename}'.")
        return None, None, None


def main():
    input_filename = "input1.txt"

    # Читаем граф из файла
    n, m, edges = read_graph_from_file(input_filename)

    # Если при чтении файла произошла ошибка, завершаем работу
    if n is None:
        return

    # Создаём список смежности для представления графа.
    # Размер n + 1, так как вершины нумеруются с 1 до N.
    adj = [[] for _ in range(n + 1)]

    # Заполняем список смежности на основе прочитанных рёбер.
    for u, v in edges:
        adj[u].append(v)
        if u != v:  # Если ребро не является петлей
            adj[v].append(u)

    # Цель — найти компоненту связности, содержащую вершину 1.
    start_node = 1

    # Множество для хранения посещённых вершин
    visited = set()

    # Очередь для алгоритма Поиска в ширину (BFS)
    queue = collections.deque()

    # По условию, N >= 1, поэтому вершина 1 всегда существует.
    if n > 0:
        visited.add(start_node)
        queue.append(start_node)

    # Список для сбора всех вершин в найденной компоненте
    component_nodes = []

    # Цикл Поиска в ширину (BFS)
    while queue:
        current_node = queue.popleft()
        component_nodes.append(current_node)

        for neighbor in adj[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    component_nodes.sort()

    print(len(component_nodes))
    print(*component_nodes)


if __name__ == "__main__":
    main()