class FlatIterator:
    def __init__(self, list_of_lists):
        self.list_of_lists = list_of_lists

    def __iter__(self):
        self.start = 0
        self.end = len(self.list_of_lists)
        self.item_start = 0
        self.item_end = len(self.list_of_lists[0]) if self.list_of_lists[0] else 0
        return self

    def get_next_item(self):
        self.start += 1
        if self.start >= self.end:
            raise StopIteration
        self.item_start = 0
        self.item_end = len(self.list_of_lists[self.start])

    def __next__(self):
        if self.item_start == self.item_end:
            self.get_next_item()
        self.item_start += 1
        return self.list_of_lists[self.start][self.item_start-1]


class CommonFlatIterator:
    def __init__(self, list_of_lists):
        self.list_of_lists = list_of_lists

    def __iter__(self):
        return self

    def __next__(self):
        pass

