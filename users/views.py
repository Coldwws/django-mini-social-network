from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm, PostForm, CommentForm
from django.contrib.auth.models import User

from .models import Post,Like


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

    posts = Post.objects.filter(author = profile_user)
    context = {'profile_user':profile_user,'posts':posts}


    return render(request, 'users/profile.html', context)

@login_required()
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)

            post.author = request.user
            post.save()
            return redirect('feed')
    else:
        form = PostForm()
    return render(request,'users/create_post.html',{'form':form})

def feed(request):
    posts = Post.objects.all().order_by('-created_at')
    context = {'posts':posts}

    return render(request,'users/feed.html',context)

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()

    return render(request,'users/post_detail.html',{'post':post,'form':form})


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if post.author != request.user:
        return redirect('feed')

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = PostForm(instance=post)

    return render(request,'users/post_edit.html',{'form':form})

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    like,created= Like.objects.get_or_create(user=request.user,post=post)
    if not created:
        like.delete()

    return redirect('feed')

def search_users(request):
    query = request.GET.get('q','')
    results = []
    if query:
        results = User.objects.filter(username__icontains=query)
    context = {'results':results,
               'query':query}
    return render(request, "users/search_results.html",context)