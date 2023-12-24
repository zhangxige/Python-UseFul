# coding: utf-8
from concurrent.futures import ThreadPoolExecutor
import time
import random
from pprint import pprint


# process function, you can use your function/process
def spider(args):
    (target_ind, page) = args
    time.sleep(page)
    print(f"crawl task{page} finished")
    return target_ind, page


# threadpool demo main
def demo_main():
    # inii threading pool
    executor = ThreadPoolExecutor(max_workers=4)

    # prepare input function data
    result_list = []
    input_data = [(i, random.randint(1, 10)) for i, _ in enumerate(range(10))]
    # execute all threads
    for result in executor.map(spider, input_data):
        i, res = result
        result_list.append((i, res))
        print("task : {} done, result : {}".format(i, res))
    # sort by index
    result_list.sort(key=lambda x: x[0])
    pprint(result_list)


if __name__ == '__main__':
    demo_main()
