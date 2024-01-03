from pprint import pprint
import os
import sys
from pathlib import Path

from Utils.Decorators_Utils import timer

# base root
FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative


@timer
def test_fun():
    test = {}
    for it in range(10):
        test[it] = it
    return test


class Solution:
    def help_zhouchang(self, n):
        if n == 0:
            return 0
        else:
            return (n * (n + 1) + (1 + n) * n / 2) * 4
    
    def help_all(self, n):
        if n == 0:
            return 0
        else:
            return self.help_all(n - 1) + self.help_zhouchang(n)

    def help_inner(self, n):
        return self.help_all(n) - self.help_zhouchang(n)

    def minimumPerimeter(self, neededApples: int) -> int:
        n = 1
        while n:
            if (self.help_inner(n) >= neededApples) or (self.help_zhouchang(n) >= neededApples):
                break
            n = n + 1
        return n * 4
    

if __name__ == "__main__":
    res = test_fun()
    pprint(res)
