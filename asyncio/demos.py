# -*- coding: utf-8 -*-
# @Time    : 2021/8/23 14:37
# @Author  : 10867
# @FileName: demos.py
# @Software: PyCharm
import asyncio

# """事件循环EventLoop: 事件循环是asyncio的核心，异步任务的运行、任务完成之后的回调、网络IO操作、子进程的运行，都是通过事件循环完成的。"""
# 同一个线程中只能有一个时间循环

# 1、事件循环的创建
#     （1）asyncio.get_running_loop()
#     （2）asyncio.get_event_loop()
#     （3）asyncio.set_event_loop(loop)
#     （4）asyncio.new_event_loop()

# 2、运行和停止事件循环
#     （1）loop.run_until_complete(future)。运行事件循环，直到future运行结束
#     （2）loop.run_forever()。在python3.7中已经取消了，表示事件循环会一直运行，直到遇到stop。
#     （3）loop.stop()。停止事件循环
#     （4）loop.is_running()。如果事件循环依然在运行，则返回True
#     （5）loop.is_closed()。如果事件循环已经close，则返回True
#     （6）loop.close()。关闭事件循环

# 3、创建Future和Task
#     （1）loop.create_future(coroutine) ，返回future对象
#     （2）loop.create_task(corootine) ，返回task对象
#     （3）loop.set_task_factory(factory)
#     （4）loop.get_task_factory()

# 4、事件循环时钟
# loop.time()。可以这么理解，事件循环内部也维护着一个时钟，可以查看事件循环现在运行的时间点是多少，就像普通的time.time()类似，它返回的是一个浮点数值

# 5、计划执行回调函数（CallBacks）
#     （1）loop.call_later(delay, callback, *args, context=None)
#     首先简单的说一下它的含义，就是事件循环在delay多长时间之后才执行callback函数，它的返回值是asyncio.TimerHandle类的一个实例对象。
#     （2）loop.call_at(when, callback, *args, context=None)
#     即在某一个时刻进行调用计划的回调函数，第一个参数不再是delay而是when，表示一个绝对的时间点，结合前面的loop.time使用，它的使用方法和call_later()很类似。它的返回值是asyncio.TimerHandle类的一个实例对象。
#     （3）loop.call_soon(callback, *args, context=None)
#     在下一个迭代的时间循环中立刻调用回调函数，用法同上面。它的返回值是asyncio.Handle类的一个实例对象。
#     （4）loop.call_soon_threadsafe(callback, *args, context=None)

#     总结注意事项：
#     （1）CallBack函数只能够定义为同步方法，不能够定义为async方法，及不能使用async和@asyncio.coroutine修饰；
#     （2）每一个CallBack方法只会调用一次，如果在同一个时刻有另个CallBack方法需要调用，则他们的执行顺序是不确定的；
#     （3）注意使用functools.partial（）去修饰带有关键字参数的CallBack方法；
#     （4）如何理解？对于一般的异步函数，我们需要将它放在时间循环里面，然后通过事件循环去循环调用它，
#     而因为CallBack并不是异步函数，它是定义为普通的同步方法，所以不能够放在时间循环里面，
#     但是如果我依然想要让事件循环去执行它怎么办呢？
#     那就不放进事件循环，直接让事件循环“立即、稍后、在什么时候”去执行它不就行了嘛，call的含义就是“执行”。


# 问答

# 1、很多个协程一起运行有创建新的线程吗？
#     协程运行时，都是在一个线程中运行的，没有创建新的线程

# 2、线程一定效率更高吗？
#     也不是绝对的，当然在一般情况下，异步方式的执行效率时更高的。那是不是一定会提高呢？ 也不一定，这与协程的调用方式相关
#     在有很多个异步方式的时候，一定要尽量避免直接调用，这和同步方式没什么区别，一定要通过事件循环loop，让时间循环在各个异步函数之间不停游走，这样在不会造成阻塞

# 3、协程会不会阻塞呢？
#     异步的方式依然会有阻塞，当我们定义很多个异步方法彼此之间有一来的时候
#     比如：我们必须要等到函数1执行完毕，函数2需要用到函数1的返回值，就会造成阻塞
#     这也是异步编程的难点之一，如何合理配置这些资源，尽量减少函数之间的依赖，这很重要

# 4、协程的4中状态
#     协程函数相比于一般的函数来说，我们可以将协程包装成任务Task，任务Task就在于可以跟踪它的状态，我就知道它具体执行到哪一步了，
#     一般来说，协程函数具有4种状态，可以通过相关的模块进行查看，请参见前面的文章，他的四种状态为：
#     Pending
#     Running
#     Done
#     Cacelled
#     创建future的时候，task为pending，
#     事件循环调用执行的时候当然就是running，
#     调用完毕自然就是done，
#     如果需要停止事件循环，中途需要取消，就需要先把task取消，即为cancelled。


# 多任务并发

# 1、使用gather同时注册多个任务，实现并发
# 2、使用wait可以同时注册多个任务，实现并发
# 3、使用as_completed可以同时注册多个任务，实现并发
