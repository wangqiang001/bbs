from django.core.cache import cache
from django.shortcuts import redirect

from common import redis
from post.models import Post


def page_cache(timeout=60):
    def deco(view_func):
        '''页面级别缓存'''
        def wrapper(request):
            url = request.get_full_path()   # 取到url和参数/post/list/?page=2
            session_id = request.session.session_key
            key = "PageCache-%s-%s" % (session_id, url)
            response = cache.get(key)
            if response is None:
                response = view_func(request)
                cache.set(key, response, timeout)
            return response
        return wrapper
    return deco


def get_top_n(num):
    '''
    获取阅读排行前n的文章数据
        Args :
        Return:
    '''
    origin_data = redis.zrevrange('ReadCounter', 0, num-1, withscores=True)
    cleaned_data = [[int(post_id), int(count)] for post_id, count in origin_data]
    #方法1
    # for item in cleaned_data:
    #     post = Post.objects.get(pk=item[0])
    #     item[0] = post

    #方法2
    # post_id_list = [post_id for post_id, _ in cleaned_data]
    # posts = Post.objects.filter(id__in=post_id_list)
    # posts = sorted(posts, key=lambda post: post_id_list.index(post.id))
    # for item, post in zip(cleaned_data, posts):
    #     item[0] = post

    #方法3
    post_id_list = [post_id for post_id, _ in cleaned_data]
    posts = Post.objects.in_bulk(post_id_list)
    for item in cleaned_data:
        post_id = item[0]
        item[0] = posts[post_id]
    return cleaned_data


