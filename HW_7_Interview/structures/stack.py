class Stack:
    """
    Класс для работы со стеком.
    """
    def __init__(self):
        self.stack = []

    def is_empty(self):
        """
        Проверяет, пустой ли стек.
        Возвращает:
            bool: True, если стек пустой, False в противном случае.
        """
        return not self.stack

    def push(self, item):
        """
        Добавляет элемент в конец стека.
        Параметры:
            item: Элемент, который добавляется в стек.
        Возвращает:
            None
        """
        self.stack.append(item)

    def pop(self):
        """
        Удаляет и возвращает конечный элемент из стека.
        Если стек пуст, он не изменяет стек и возвращает None.
        Возвращает:
            Конечный элемент стека, если стек не пуст, в противном случае None.
        """
        if self.stack:
            self.stack.pop()

    def peek(self):
        """
        Возвращает последний элемент стека, если стек не пуст, иначе None.
        """
        if self.stack:
            return self.stack[-1]

    def size(self):
        """
        Возвращает (int) размер стека.
        """
        return len(self.stack)
