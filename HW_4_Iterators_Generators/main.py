from Source.Iterators import FlatIterator, CommonFlatIterator
from Source.Generators import flat_generator, common_flat_generator
from Test.tests import test_1, test_2, test_3, test_4

nested_list = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]

list_of_lists_2 = [
    [['a'], ['b', 'c']],
    ['d', 'e', [['f'], 'h'], False],
    [1, 2, None, [[[[['!']]]]], []]
]

nested = [[['!']], [[0], [[1], [2]]], False]

def main():
    for item in FlatIterator(nested_list):
        print(item)
    for item in flat_generator(nested_list):
        print(item)
    for item in common_flat_generator(list_of_lists_2):
        print(item)
    # for item in CommonFlatIterator(nested_list):
    #     print(item)
    print(test_1())
    print(test_2())
    print(test_4())
    print("tests done")


if __name__ == '__main__':
    main()
