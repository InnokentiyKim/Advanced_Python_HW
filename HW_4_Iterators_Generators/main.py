from Test.tests import test_1, test_2, test_4


def main():
    tests = [test_1, test_2, test_4]
    for i, test in enumerate(tests, start=1):
        try:
            test()
            print(f"Test #{i} successfully done")
        except Exception:
            print(f"Test #{i} failed")


if __name__ == '__main__':
    main()
