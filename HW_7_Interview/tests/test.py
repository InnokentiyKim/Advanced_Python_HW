from sequences.brackets import is_balanced_brackets


true_sequences = [
    '(((([{}]))))',
    '[([])((([[[]]])))]{()}',
    '{{[()]}}'
]

false_sequences = [
    '}{}',
    '{{[(])]}}',
    '[[{())}]'
]


def test_true_sequences(sequences: list[str]):
    """
    Тестирование функции is_balanced_brackets со сбалансированными последовательностями.
    """
    print("Testing true sequences...")
    for i, sequence in enumerate(sequences, start=1):
        try:
            assert is_balanced_brackets(sequence)
            print(f"Test #{i} successfully passed")
        except AssertionError:
            print(f"Test #{i} failed")


def test_false_sequences(sequences: list[str]):
    """
    Тестирование функции is_balanced_brackets с несбалансированными последовательностями.
    """
    print("Testing false sequences...")
    for i, sequence in enumerate(sequences, start=1):
        try:
            assert not is_balanced_brackets(sequence)
            print(f"Test #{i} successfully passed")
        except AssertionError:
            print(f"Test #{i} failed")
