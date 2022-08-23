# -*- coding: utf-8 -*-
# @Time    : 2022/3/25 10:05
# @Author  : 10867
# @FileName: task.py
# @Software: PyCharm
import asyncio


# async def nested():
#     return 42
#
#
# async def main():
#     # Nothing happens if we just call "nested()".
#     # A coroutine object is created but not awaited,
#     # so it *won't run at all*.
#     # nested()
#
#     # Let's do it differently now and await it:
#     print(await nested())  # will print "42".
#
#
# asyncio.run(main())


# async def nested(delay: int):
#     print(2)
#     await asyncio.sleep(delay)
#     return 42
#
#
# async def main():
#     # Schedule nested() to run soon concurrently
#     # with "main()".
#     task = asyncio.create_task(nested(3))
#
#     # "task" can now be used to cancel "nested()", or
#     # can simply be awaited to wait until it is complete:
#     await asyncio.sleep(0)
#     print(1)
#     # await task
#
#
# asyncio.run(main(), debug=True)


async def waiter(event):
    print('waiting for it ...')
    await event.wait()
    print('... got it!')


async def main():
    # Create an Event object.
    event = asyncio.Event()

    # Spawn a Task to wait until 'event' is set.
    waiter_task = asyncio.create_task(waiter(event))

    # Sleep for 1 second and set the event.
    await asyncio.sleep(1)
    event.set()

    # Wait until the waiter task is finished.
    await waiter_task


asyncio.run(main())

import webbrowser