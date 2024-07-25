from Tests.tests import test_1, test_2
from Examples.example import standardize_phone


def main():
    test_1()
    test_2()
    some_number = '8 924 3232345'
    standardize_phone(some_number)


if __name__ == '__main__':
    main()