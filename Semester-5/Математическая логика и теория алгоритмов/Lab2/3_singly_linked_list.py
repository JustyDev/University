# Узел связного списка
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class SinglyLinkedList:
    def __init__(self):
        self.head = None

    # Добавить в конец
    def append(self, item):
        node = Node(item)
        if not self.head:
            self.head = node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = node

    # Добавить в начало
    def prepend(self, item):
        node = Node(item)
        node.next = self.head
        self.head = node

    # Вставить по индексу
    def insert(self, index, item):
        if index == 0:
            self.prepend(item)
            return
        node = Node(item)
        current = self.head
        for _ in range(index - 1):
            if current is None:
                return  # Индекс вне диапазона
            current = current.next
        if current is None:
            return
        node.next = current.next
        current.next = node

    # Удалить по значению
    def remove(self, item):
        current = self.head
        prev = None
        while current:
            if current.data == item:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True  # Удалено
            prev = current
            current = current.next
        return False  # Не найдено

    # Найти элемент и вернуть индекс
    def find(self, item):
        index = 0
        current = self.head
        while current:
            if current.data == item:
                return index
            index += 1
            current = current.next
        return -1  # Не найдено

    # Вывести элементы
    def display(self):
        current = self.head
        while current:
            print(current.data, end=' ')
            current = current.next
        print()


lst = SinglyLinkedList()

lst.append('B')
lst.prepend('A')
lst.append('C')
lst.insert(2, 'X')
lst.display()
lst.remove('X')
lst.display()

print("Индекс 'C':", lst.find('C'))
