from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect

from user.forms import RegisterForm
# Create your views here.

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(user.password)
            user.save()
            return redirect("/user/login")
        else:
            return render(request, "register.html", {"error": form.errors})
    else:
        return render(request, "register.html", {})

def login(request):
    
    return render(request, "login.html", {})

def logout(request):
    return render(request, "logout.html", {})

def user_info(request):
    return render(request, "user_info.html", {})





