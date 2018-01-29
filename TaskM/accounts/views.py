from django.shortcuts import render
from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout,
)
from .forms import UserLoginForm

def login_view(request):
    title = 'Task Management System User Login'
    form = UserLoginForm(request.POST or None)
    context = {
        'form':form,
        'title':title,
               }
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

    return render(request, 'login.html',context )


def register_view(request):
    return render(request, '.html', {})


def logout_view(request):
    return render(request, 'login.html', {})
