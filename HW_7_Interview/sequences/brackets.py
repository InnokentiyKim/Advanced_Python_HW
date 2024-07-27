from structures.stack import Stack


def is_balanced_brackets(brackets_str: str):
    brackets_seq = Stack()
    brackets_dict = {')': '(', ']': '[', '}': '{'}
    for bracket in brackets_str:
        if bracket in brackets_dict.values():
            brackets_seq.push(bracket)
        else:
            if not brackets_seq.is_empty() and brackets_seq.peek() == brackets_dict.get(bracket):
                brackets_seq.pop()
            else:
                return False
    return True if brackets_seq.is_empty() else False
