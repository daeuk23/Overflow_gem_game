class Stack:
    def __init__(self, cap=10):
        # Initialize the Stack class with a capacity.
        self._values = [None] * cap
        self._size = 0
        self._capacity = cap

    def capacity(self):
        # Returns capacity of the stack(_capacity).
        return self._capacity

    def push(self, data):
        # Add data to the top of the stack.
        if self._size == self._capacity:
            new_capacity = self._capacity * 2
            new_values = [None] * new_capacity

            for i in range(self._size):
                new_values[i] = self._values[i]
            self._values = new_values
            self._capacity = new_capacity
        self._values[self._size] = data
        self._size += 1

    def pop(self):
        # Remove and return the top item from the stack.
        if self.is_empty():
            raise IndexError('pop() used on empty stack')
        data = self._values[self._size - 1]
        self._values[self._size - 1] = None
        self._size -= 1
        return data

    def get_top(self):
        # Return the top item from the stack without removing it.
        if self.is_empty():
            return None
        return self._values[self._size - 1]

    def is_empty(self):
        # Return True if the stack is empty, False otherwise.
        return self._size == 0

    def __len__(self):
        # Return the number of items in the stack.
        return self._size


class Queue:
    def __init__(self, cap=10):
        # Initialize the Queue class with a capacity.
        self._capacity = cap
        self._queue = [None] * cap
        self._size = 0
        self._front = 0

    def capacity(self):
        # Returns capacity.
        return self._capacity

    def enqueue(self, data):
        # Adds data to the back of the Queue.
        if self._size == self._capacity:
            # Perform resizing manually
            new_capacity = self._capacity * 2
            new_queue = [None] * new_capacity
            for i in range(self._size):
                new_queue[i] = self._queue[(self._front + i) % self._capacity]
            self._queue = new_queue
            self._front = 0
            self._capacity = new_capacity
        back = (self._front + self._size) % self._capacity
        self._queue[back] = data
        self._size += 1

    def dequeue(self):
        # Removes the oldest value from the Queue.
        if self.is_empty():
            raise IndexError('dequeue() used on empty queue')
        data = self._queue[self._front]
        self._queue[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return data

    def get_front(self):
        # Returns the oldest value from the Queue without removing it.
        if self.is_empty():
            return None
        return self._queue[self._front]

    def is_empty(self):
        # Returns True if Queue is empty, False otherwise.
        return self._size == 0

    def __len__(self):
        # Returns the number of values in the Queue.
        return self._size
 

class Deque:
    def __init__(self, cap=10):
        # Initialize the Deque class with a capacity.
        self._capacity = cap
        self._deque = [None] * cap
        self._size = 0
        self._front = 0

    def capacity(self):
        # Returns capacity.
        return self._capacity

    def push_front(self, data):
        # Adds data to the front of the Deque.
        if self._size == self._capacity:
            self._expand_capacity()
        self._front = (self._front - 1) % self._capacity
        self._deque[self._front] = data
        self._size += 1

    def push_back(self, data):
        # Adds data to the back of the Deque.
        if self._size == self._capacity:
            self._expand_capacity()
        back = (self._front + self._size) % self._capacity
        self._deque[back] = data
        self._size += 1

    def pop_front(self):
        # Removes and returns the value from the front of the Deque.
        if self.is_empty():
            raise IndexError('pop_front() used on empty deque')
        data = self._deque[self._front]
        self._deque[self._front] = None
        self._front = (self._front + 1) % self._capacity
        self._size -= 1
        return data

    def pop_back(self):
        # Removes and returns the value from the back of the Deque.
        if self.is_empty():
            raise IndexError('pop_back() used on empty deque')
        back = (self._front + self._size - 1) % self._capacity
        data = self._deque[back]
        self._deque[back] = None
        self._size -= 1
        return data

    def get_front(self):
        # Returns the value from the front of the Deque without removing it.
        if self.is_empty():
            return None
        return self._deque[self._front]

    def get_back(self):
        # Returns the value from the back of the Deque without removing it.
        if self.is_empty():
            return None
        back = (self._front + self._size - 1) % self._capacity
        return self._deque[back]

    def is_empty(self):
        # Returns True if Deque is empty, False otherwise.
        return self._size == 0

    def __len__(self):
        # Returns the number of values in the Deque.
        return self._size

    def __getitem__(self, k):
        # Returns the k'th value from the front of the Deque without removing it.
        if k < 0 or k >= self._size:
            raise IndexError('Index out of range')
        idx = (self._front + k) % self._capacity
        return self._deque[idx]

    def _expand_capacity(self):
        # Expands the capacity of the Deque by doubling its current capacity.
        new_capacity = self._capacity * 2
        new_deque = [None] * new_capacity
        for i in range(self._size):
            new_deque[i] = self._deque[(self._front + i) % self._capacity]
        self._deque = new_deque
        self._front = 0
        self._capacity = new_capacity
