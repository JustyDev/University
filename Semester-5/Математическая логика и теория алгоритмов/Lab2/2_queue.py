# очередь (FIFO)

from collections import deque

class Queue:
    def __init__(self):
        self.data = deque()

    def enqueue(self, item):
        self.data.append(item)

    def dequeue(self):
        if self.is_empty():
            return None
        return self.data.popleft()

    def peek(self):
        if self.is_empty():
            return None
        return self.data[0]

    def is_empty(self):
        return not self.data

    def size(self):
        return len(self.data)

# Пример обслуживания клиентов
q = Queue()

q.enqueue("Клиент1")
q.enqueue("Клиент2")
q.enqueue("Клиент3")

while not q.is_empty():
    print("Обслуживается:", q.dequeue())
