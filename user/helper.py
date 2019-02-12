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



