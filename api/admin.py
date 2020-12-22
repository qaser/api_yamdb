from django.contrib import admin

from .models import Comment, User, Title, Review, Genre, Category


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email',)

class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year',)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'text',)

admin.site.register(User, UserAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)