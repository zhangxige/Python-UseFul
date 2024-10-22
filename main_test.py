import os
import sys
from pathlib import Path
from typing import List

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


class solution_merge_interval:

    # intervals 形如 [[1,3],[2,6]...]
    def merge_interval(self, intervals):
        if not intervals:
            return []
        # 按区间的 start 升序排列
        intervals.sort(key=lambda intv: intv[0])
        res = []
        res.append(intervals[0])
        for i in range(1, len(intervals)):
            curr = intervals[i]
            # res 中最后一个元素的引用
            last = res[-1]
            if curr[0] <= last[1]:
                # 找到最大的 end
                last[1] = max(last[1], curr[1])
            else:
                # 处理下一个待合并区间
                res.append(curr)
        return res

    def test(self):
        a_l = [[1, 4], [3, 7], [9, 11], [14, 15]]
        res = self.merge_interval(a_l)
        print(res)


class leetcode_908:
    def smallestRangeI(self, nums: List[int], k: int) -> int:
        mx, mi = max(nums), min(nums)
        return max(0, mx - mi - k * 2)

    def test(self):
        nums = [1, 3, 6]
        k = 3
        res = self.smallestRangeI(nums, k)
        print(res)


class leetcode_910:
    def smallestRangeII(self, nums: List[int], k: int) -> int:
        nums.sort()
        ans = nums[-1] - nums[0]
        for i in range(1, len(nums)):
            x, y = nums[i - 1], nums[i]
            mx = max(x + k, nums[-1] - k)
            mn = min(nums[0] + k, y - k)
            ans = min(ans, mx - mn)
        return ans

    def test(self):
        nums = [1, 3, 6]
        k = 3
        res = self.smallestRangeII(nums, k)
        print(res)


class leetcode_3184:
    def countCompleteDayPairs(self, hours: List[int]) -> int:
        res = 0
        for i in range(len(hours) - 1):
            for j in range(i + 1, len(hours)):
                res += 1 if (hours[i] + hours[j]) % 24 == 0 else 0
        return res

    def test(self):
        a = [12, 12, 30, 24, 24]
        a = [72, 48, 24, 3]
        res = self.countCompleteDayPairs(a)
        print(res)


class erfen_solution:
    def help(self, s_list: List[int], target: int, num: int) -> bool:
        res = True
        for it in s_list:
            if it <= target:
                num -= 1
            else:
                sub_num = it // target if it % target == 0 else it // target + 1
                num -= sub_num
            if num < 0:
                res = False
                break
        return res

    def method(self, num: int, st_list: List[int]) -> int:
        left = 1
        right = max(st_list)
        while left < right:
            mid = (left + right) // 2 + 1
            if self.help(st_list, mid, num):
                right = mid - 1
            else:
                left = mid
        return left + 1

    def test(self):
        n = 8
        s = [101, 51, 1, 20, 40]
        res = self.method(n, s)
        print(res)


if __name__ == "__main__":
    a = leetcode_3184()
    a.test()
