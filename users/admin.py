from django.contrib import admin
from .models import Profile,Follow,Like,Comment

admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Comment)