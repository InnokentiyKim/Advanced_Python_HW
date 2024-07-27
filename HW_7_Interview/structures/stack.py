class Stack:
    def __init__(self):
        self.stack = []

    def is_empty(self):
        return not self.stack

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if self.stack:
            self.stack.pop()

    def peek(self):
        if self.stack:
            return self.stack[-1]

    def size(self):
        return len(self.stack)
