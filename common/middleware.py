import time

from django.shortcuts import render
from django.core.cache import cache

from django.utils.deprecation import MiddlewareMixin


def testMiddleware(view_func):
    def wrapper(request):
        print('process—request 执行之前')
        res = view_func(request)
        print('process—response 执行之后')
        return res
    return wrapper

class BlockMiddleware(MiddlewareMixin):
    def process_request(self, request):
        user_ip = request.META['REMOTE_ADDR']
        request_key = 'Request-%s' % user_ip
        block_key = 'Block-%s' % user_ip
        #黑名单检查
        if cache.has_key(block_key):
            return render(request, 'blockers.html')

        now = time.time()
        #检查当前时间与前 3 次的时差是否小于 2 秒
        request_time = cache.get(request_key, [0] * 3)
        print('request_time', request_time)
        if now - request_time[0] < 1:
            cache.set(block_key, 1, 60)  #加入黑名单
            return render(request, 'blockers.html')
        else:
            #更新时间
            request_time.pop(0)
            request_time.append(now)
            cache.set(request_key, request_time)










