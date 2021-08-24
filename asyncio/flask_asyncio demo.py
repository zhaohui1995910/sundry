# -*- coding: utf-8 -*-
# @Time    : 2021/8/24 17:44
# @Author  : 10867
# @FileName: flask_asyncio demo.py
# @Software: PyCharm

import asyncio
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, request

app = Flask(__name__)
loop = asyncio.new_event_loop()
loop_executor = ThreadPoolExecutor(max_workers=5)
dict_map = {}


def thread_async_low(n):
    try:
        _loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_loop)

        _loop.run_until_complete(long_task(n))
    except Exception as e:
        print(e)


def thread_async(func):
    def make_decorater(*args):
        _loop = asyncio.new_event_loop()
        asyncio.set_event_loop(_loop)

        func_rsult = _loop.run_until_complete(func(*args))

        return func_rsult

    return make_decorater


@thread_async
async def long_task(n):
    print("start: %s" % n)
    await asyncio.sleep(5)
    dict_map[n] = n
    print("done: %s" % n)


async def long_task_low(n):
    print("start: %s" % n)
    await asyncio.sleep(5)
    dict_map[n] = n
    print("done: %s" % n)


@app.route('/jobs')
def run_jobs():
    # 交由线程去执行耗时任务
    print(dict_map)
    n = request.args.get('n')

    # 同步
    loop.run_until_complete(long_task_low(n))
    # 并发
    loop.run_until_complete(
        asyncio.wait([long_task_low(n), long_task_low(n), long_task_low(n)])
    )

    # 交由线程去执行耗时任务 (异步非阻塞)
    # loop_executor.submit(thread_async_low)
    loop_executor.submit(long_task, n)

    return 'long %s running.' % n


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
