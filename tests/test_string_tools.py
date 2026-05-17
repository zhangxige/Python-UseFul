import sys
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from Python_package.myutils.string_tools import reverse_string, to_upper


class TestStringTools:
    def test_reverse_string(self):
        assert reverse_string("hello") == "olleh"
        assert reverse_string("") == ""
        assert reverse_string("a") == "a"
        assert reverse_string("ab") == "ba"

    def test_to_upper(self):
        assert to_upper("hello") == "HELLO"
        assert to_upper("Hello World") == "HELLO WORLD"
        assert to_upper("") == ""
