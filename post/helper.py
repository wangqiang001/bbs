from django.core.cache import cache

def page_cache(timeout=60):
    def deco(view_func):
        '''页面级别缓存'''
        def wrapper(request):
            url = request.get_full_path()
            session_id = request.session.session_key
            key = "PageCache-%s-%s" % (session_id, url)
            response = cache.get(key)
            if response is None:
                response = view_func(request)
                cache.set(key, response, timeout)
            return response
        return wrapper
    return deco




