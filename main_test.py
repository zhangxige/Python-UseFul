from pprint import pprint

from Utils.Decorators_Utils import timer


@timer
def test_fun():
    test = {}
    for it in range(10):
        test[it] = it
    return test


if __name__ == "__main__":
    res = test_fun()
    pprint(res)
