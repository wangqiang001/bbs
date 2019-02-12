from math import ceil

from django.core.cache import cache
from django.shortcuts import render,redirect

from common import redis
from post.helper import page_cache, get_top_n
from post.models import Post, Comment, Tag
# Create your views here.
from user.helper import login_required, need_prem


@page_cache(60*2)
def post_list(request):
    page = int(request.GET.get("page", 1))
    total = Post.objects.count()
    per_page = 10
    pages = ceil(total / per_page)
    start = (page - 1) * per_page
    end = start + per_page
    posts = Post.objects.all()[start : end]
    return render(request, "post_list.html", {"posts": posts, "pages": range(pages)})


@login_required
@need_prem('manager')
def create_post(request):
    if request.method == 'POST':
        uid = request.session['uid']
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(uid=uid, title=title, content=content)
        return redirect("/post/read/?post_id=%d" % post.id)
    else:
        return render(request, 'create_post.html', {})


def edit_post(request):
    if request.method == 'POST':
        post_id = int(request.POST.get("post_id"))
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.get(id=post_id)
        post.title = title
        post.content = content
        post.save()

        #创建tag
        str_tags = request.POST.get('tags')
        tag_names = [t.strip() for t in str_tags.title().replace('，', ',').split(',')]
        post.update_tags(tag_names)

        # 更新帖子缓存
        # key = "Post-%s" % post_id
        # post = cache.set(key)
        return redirect("/post/read/?post_id=%d" % post.id)
    else:
        post_id = int(request.GET.get("post_id"))
        post = Post.objects.get(id=post_id)
        tags = ','.join([t.name for t in post.tags])
        return render(request, "edit_post.html", {"post" : post, "tags": tags})


def read_post(request):
    post_id = int(request.GET.get("post_id"))
    redis.zincrby('ReadCounter', post_id) #增加帖子阅读排行
    # key = "Post-%s" % post_id
    # post = cache.get(key)
    # print('从缓存获取',post)
    # if post is None:
    #     post = Post.objects.get(id=post_id)
    #     cache.set(key, post)
    #     print('从数据库获取',post)
    # post = Post.objects.get(id=post_id)
    # post = Post.get(id=post_id)     #ORM级别的缓存
    post = Post.objects.get(id=post_id)
    return render(request, "read_post.html", {"post" : post})

def delete_post(request):
    post_id = int(request.GET.get("post_id"))
    Post.objects.get(id=post_id).delete()
    redis.zrem('ReadCounter', post_id) #同时从帖子阅读排行删除
    return redirect("/")


def search(request):
    keyword = request.POST.get("keyword")
    print(keyword)
    posts = Post.objects.filter(content__contains=keyword)
    print("-----------",posts)
    return render(request, "search.html", {"posts" : posts})


def top10(request):
    rank_data = get_top_n(10)
    return render(request, 'top10.html', {'rank_data': rank_data})

@login_required
def comment(request):
    uid = request.session['uid']
    post_id = request.POST.get('post_id')
    content = request.POST.get('content')
    Comment.objects.create(uid=uid, post_id=post_id, content=content)
    return  redirect('/post/read/?post_id=%s' % post_id)

