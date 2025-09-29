import collections


def read_graph_from_file(filename):
    """
    Читает описание графа из указанного файла.
    (Эта функция осталась без изменений)
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            if not first_line:
                print("Ошибка: Файл пуст.")
                return None, None, None

            n, m = map(int, first_line.split())

            edges = []
            for _ in range(m):
                line = f.readline()
                if not line:
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


def find_component(start_node, adj, visited):
    """
    Находит одну компоненту связности, начиная с start_node,
    используя поиск в ширину (BFS).
    Обновляет общее множество посещенных вершин.

    Аргументы:
        start_node (int): Вершина, с которой начинается поиск.
        adj (list): Список смежности графа.
        visited (set): Общее множество посещённых вершин.

    Возвращает:
        list: Список вершин, входящих в найденную компоненту.
    """
    # Если стартовая вершина уже посещена, она часть другой компоненты
    if start_node in visited:
        return []

    component_nodes = []
    queue = collections.deque([start_node])
    visited.add(start_node)  # Помечаем вершину как посещенную

    while queue:
        current_node = queue.popleft()
        component_nodes.append(current_node)

        for neighbor in adj[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return component_nodes


def main():
    """
    Основная функция для поиска всех компонент связности.
    """
    input_filename = "input2.txt"

    n, m, edges = read_graph_from_file(input_filename)

    if n is None:
        return

    # Создаём список смежности
    adj = [[] for _ in range(n + 1)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    # Множество для всех посещенных вершин во всех компонентах
    visited = set()
    all_components = []

    # Перебираем все вершины от 1 до N
    for i in range(1, n + 1):
        # Если вершина i еще не была посещена, значит мы нашли новую компоненту
        if i not in visited:
            # Находим все вершины в этой новой компоненте
            component = find_component(i, adj, visited)
            all_components.append(component)

    # Вывод результатов в требуемом формате

    # 1. Количество компонент связности
    print(len(all_components))

    # 2. Вывод каждой компоненты
    for component in all_components:
        # Хотя по условию порядок не важен, отсортируем для красоты
        component.sort()
        # Первая строка - количество вершин
        print(len(component))
        # Вторая строка - сами вершины
        print(*component)


if __name__ == "__main__":
    main()