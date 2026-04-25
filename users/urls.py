from django.urls import path
from .views import *

urlpatterns = [

    path("", HomeView.as_view(), name="home"),

    path("register/", register, name="register"),

    path("feed/", FeedView.as_view(), name="feed"),

    path("create/", CreatePostView.as_view(), name="create_post"),

    path("post/<int:post_id>/", PostDetailView.as_view(), name="post_detail"),

    path("post/<int:post_id>/edit/", PostEditView.as_view(), name="post_edit"),

    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path("profile/<str:username>/", ProfileView.as_view(), name="profile"),

    path("like/<int:post_id>/", like_post, name="like_post"),

    path("search/", search_users, name="search_users"),
    path('follow/<int:user_id>/', follow_user, name='follow_user'),

    path('feed/following/',FollowingFeedView.as_view(), name='following_feed'),
]