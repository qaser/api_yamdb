from django.contrib import admin

from .models import Comment, User, Title, Review, Genre, Category


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email',)


admin.site.register(User, UserAdmin)