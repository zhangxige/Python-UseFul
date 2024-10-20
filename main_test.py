import os
import sys
from pathlib import Path

from Utils.Decorators_Utils import timer

# base root
# ref: https://github.com/ultralytics/yolov5/blob/master/segment/predict.py
FILE = Path(__file__).resolve()
ROOT = FILE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))


@timer
def test_fun():
    test = {}
    for it in range(10):
        test[it] = it
    return test


if __name__ == "__main__":
    test_fun()
    pass
