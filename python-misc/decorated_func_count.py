#!/usr/bin/env python
# coding=utf-8
"""
@author: yunlizhou
@file: decorated_func_count.py
@time: 2020/1/30 07:40
限制在一定时间访问的次数
"""
import time
from functools import wraps


def api_count(expired=10, limit=10):
    def decorator(func):
        "cache for function result, which is immutable with fixed arguments"
        # 10s调用一次 or 10s调用10次
        print("initial cache for %s" % func.__name__)
        cache = {}

        @wraps(func)
        def decorated_func(*args, **kwargs):
            # 函数的名称作为key
            key = func.__name__
            result = None
            # 判断是否存在缓存
            if key in cache.keys():
                (result, updateTime, count) = cache[key]
                # 过期时间固定为10秒
                if time.time() - updateTime < expired and count < limit:
                    count += 1
                    print("limit call 10s", key, count)
                    result = func(*args, **kwargs)
                    cache[key] = (result, time.time(), count)
                    return result

                else:
                    print("超时或者超过{}次,请限制访问频次 ".format(limit))
                    time.sleep(2)
                    result = None
            else:
                print("no cache for ", key)
            # 如果过期，或则没有缓存调用方法
            if result is None:
                result = func(*args, **kwargs)
                cache[key] = (result, time.time(), 1)
            return result

        return decorated_func

    return decorator


@api_count(expired=20, limit=20)
def func(x):
    print('call func', x)


if __name__ == '__main__':

    for i in range(500):
        func(i)
