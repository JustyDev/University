# Очередь (FILO)

class Stack:
    def __init__(self):
        self.data = []

    def push(self, item):
        self.data.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self.data.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self.data[-1]

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)

def reverse_words(sentence):
    stack = Stack()

    for word in sentence.split():
        stack.push(word)

    return ' '.join(stack.pop() for _ in range(stack.size()))

print("Перевёрнутые слова:", reverse_words("Я сдаю лабораторную работу"))
