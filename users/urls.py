from django.urls import path,include


from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/<str:username>/',views.profile, name='profile'),
    path('feed/',views.feed,name='feed'),
    path('post/create/', views.create_post, name='create_post'),
    path('post/<int:post_id>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:post_id>/',views.post_detail, name='post_detail'),
]