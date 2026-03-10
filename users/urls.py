from django.urls import path,include


from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/<str:username>/',views.profile, name='profile'),
]