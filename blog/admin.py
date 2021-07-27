from django.contrib import admin
from .models import Category, Post, PostComment, Contact

admin.site.register(Category)
admin.site.register(PostComment)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'id', 'author', 'category', 'date_posted']


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'subject', 'timestamp']
