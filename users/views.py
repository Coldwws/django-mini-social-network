from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from django.contrib.auth.models import User



def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request,'users/register.html',{'form':form})


def profile(request,username):
    profile_user = get_object_or_404(User,username=username)
    context = {'profile_user':profile_user}

    return render(request, 'users/profile.html', context)