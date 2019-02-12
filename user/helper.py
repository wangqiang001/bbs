from django.shortcuts import redirect, render

from user.models import User


def login_required(view_func):
    '''验证登录'''
    def check(request):
    # def wrapper(request):
        if 'uid' in request.session:
            res = view_func(request)
            return res
        else:
            return redirect('/user/login/')
    return check


def need_prem(prem):
    '''权限分级管理'''
    def deco(view_func):
        def wrapper(request):
            user = User.objects.get(pk=request.session['uid'])
            if user.has_prem(prem):
                return view_func(request)
            else:
                return render(request, 'blockers.html')
        return wrapper
    return deco


def need_prem_func(perm):
    '''权限分级管理'''
    def deco(view_func):
        def wrapper(request):
            user = User.objects.get(pk=request.session['uid'])
            if user.has_prem_func(prem):
                return view_func(request)
            else:
                return render(request, 'blockers.html')
        return wrapper
    return deco

# admin = Role.objects.create(name='admin')
# manager = Role.objects.create(name='manager')
# user = Role.objects.create(name='user')
#
# add_post = PermissionFunc.objects.create(name='add_post')
# add_comment = PermissionFunc.objects.create(name='add_comment')
# add_manager = PermissionFunc.objects.create(name='add_manager')
# del_post = PermissionFunc.objects.create(name='del_post')
# del_comment = PermissionFunc.objects.create(name='del_comment')
# del_manager = PermissionFunc.objects.create(name='del_manager')
# del_user = PermissionFunc.objects.create(name='del_user')

