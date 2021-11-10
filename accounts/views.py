from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

# Create your views here.

def login_view(request):
    if request.method=="POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user != None:
            login(request, user)
            return redirect('/')
        else:
            print("Error")
    return render(request, 'registration/login.html')


def logout_view(request):
    logout(request)
    return redirect('/login')
