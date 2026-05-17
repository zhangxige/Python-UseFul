import sys
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from Python_package.myutils.math_tools import add, multiply, is_odd


class TestMathTools:
    def test_add(self):
        assert add(1, 2) == 3
        assert add(-1, 1) == 0
        assert add(0, 0) == 0

    def test_multiply(self):
        assert multiply(3, 4) == 12
        assert multiply(-2, 3) == -6
        assert multiply(0, 5) == 0

    def test_is_odd(self):
        assert is_odd(1) is True
        assert is_odd(2) is False
        assert is_odd(0) is False
