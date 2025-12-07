class Heap:
    def __init__(self):
        self.data = []

    def push(self, item, priority):
        self.data.append((priority, item))
        self._up(len(self.data) - 1)

    def _up(self, idx):
        while idx > 0:
            parent = (idx - 1) // 2
            if self.data[parent][0] > self.data[idx][0]:
                self.data[parent], self.data[idx] = self.data[idx], self.data[parent]
                idx = parent
            else:
                break

    def pop(self):
        if not self.data:
            return None
        top = self.data[0][1]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self._down(0)
        return top

    def _down(self, idx):
        size = len(self.data)
        while 2 * idx + 1 < size:
            left = 2 * idx + 1
            right = left + 1
            smallest = idx
            if self.data[left][0] < self.data[smallest][0]:
                smallest = left
            if right < size and self.data[right][0] < self.data[smallest][0]:
                smallest = right
            if smallest == idx:
                break
            self.data[idx], self.data[smallest] = self.data[smallest], self.data[idx]
            idx = smallest

    def peek(self):
        return self.data[0][1] if self.data else None

    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        return len(self.data)

# Heap sort
def heap_sort(arr):
    heap = MinHeap()
    for val in arr:
        heap.push(val, val)
    return [heap.pop() for _ in range(heap.size())]

# Демонстрация кучи
print("\nMinHeap:")
heap = MinHeap()
for v in [5, 1, 8, 3]:
    heap.push(f"item{v}", v)
print("Peek:", heap.peek())
print("Heap Pop:")
while not heap.is_empty():
    print(heap.pop())
print("Heap Sort [7,3,9,1,2]:", heap_sort([7,3,9,1,2]))
