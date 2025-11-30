# Узел для двусвязного списка
class DNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def append(self, item):
        node = DNode(item)
        if not self.head:  # Если список пуст
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node

    def prepend(self, item):
        node = DNode(item)
        if not self.head:
            self.head = node
            self.tail = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node

    def insert(self, index, item):
        if index == 0:
            self.prepend(item)
            return
        node = DNode(item)
        current = self.head
        for _ in range(index - 1):
            if current is None:
                return
            current = current.next
        if current is None or current.next is None:
            self.append(item)
            return
        node.next = current.next
        node.prev = current
        current.next.prev = node
        current.next = node

    def remove(self, item):
        current = self.head
        while current:
            if current.data == item:
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                return True
            current = current.next
        return False

    def display_forward(self):
        current = self.head
        while current:
            print(current.data, end=' ')
            current = current.next
        print()

    def display_backward(self):
        current = self.tail
        while current:
            print(current.data, end=' ')
            current = current.prev
        print()

# Демонстрация
dll = DoublyLinkedList()
dll.append(1)
dll.append(2)
dll.append(3)
dll.prepend(0)
dll.insert(2, 1.5)
dll.display_forward()
dll.display_backward()
dll.remove(2)
dll.display_forward()
