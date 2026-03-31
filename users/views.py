from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .forms import RegisterForm, PostForm, CommentForm
from django.contrib.auth.models import User

from .models import Post, Like, Follow

from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView

class HomeView(TemplateView):
    template_name = 'home.html'

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()

    return render(request,'users/register.html',{'form':form})


class ProfileView(ListView):
    model = Post
    template_name = 'users/profile.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.profile_user = get_object_or_404(User, username=self.kwargs["username"])
        return Post.objects.filter(author=self.profile_user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = self.profile_user

        context["followers_count"] = self.profile_user.followers.count()
        context["following_count"] = self.profile_user.following.count()

        context["following_users"] = [f.following for f in self.profile_user.following.all()]
        context["followers_users"] = [f.follower for f in self.profile_user.followers.all()]

        if self.request.user.is_authenticated:
            context["is_following"] = self.request.user.following.filter(
                following = self.profile_user
            ).exists()
        else:
            context["is_following"] = False
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'users/create_post.html'
    success_url = reverse_lazy("feed")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class FeedView(ListView):
    model = Post
    template_name = 'users/feed.html'
    context_object_name = 'posts'
    ordering = ['-created_at']

    paginate_by = 7


class PostDetailView(DetailView):
    model = Post
    template_name = "users/post_detail.html"
    context_object_name = "post"
    pk_url_kwarg = "post_id"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["form"] = CommentForm()

        return context

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        form = CommentForm(request.POST)

        if form.is_valid():

            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = self.object
            comment.save()

        return redirect("post_detail", post_id=self.object.id)

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    model = Post
    form_class = PostForm
    template_name = "users/post_edit.html"
    pk_url_kwarg = "post_id"

    # проверяем что пользователь автор
    def test_func(self):

        post = self.get_object()

        return self.request.user == post.author

    def get_success_url(self):

        return reverse_lazy(
            "post_detail",
            kwargs={"post_id": self.object.id}
        )

@login_required
def like_post(request, post_id):

    post = get_object_or_404(Post, pk=post_id)

    like, created = Like.objects.get_or_create(
        user=request.user,
        post=post
    )

    if not created:
        like.delete()

    return redirect("feed")

def search_users(request):
    query = request.GET.get("q", "")
    results = []
    if query:
        results = User.objects.filter(
            username__icontains=query
        )
    context = {
        "results": results,
        "query": query
    }
    return render(
        request,
        "users/search_results.html",
        context
)

@login_required()
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, pk=user_id)
    follow,created = Follow.objects.get_or_create(
        follower = request.user,
        following = user_to_follow
    )
    if not created:
        follow.delete()
    return redirect("profile", username =user_to_follow.username)