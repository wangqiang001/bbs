from django.shortcuts import redirect


def login_required(view_func):
    '''验证登录'''
    # def check(request):
    def wrapper(request):
        if 'uid' in request.session:
            res = view_func(request)
            return res
        else:
            return redirect('/user/login/')
    return wrapper