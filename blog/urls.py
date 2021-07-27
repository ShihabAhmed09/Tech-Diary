from django.urls import path
from . import views
from .views import (PostListView, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, UserPostListView)

app_name = 'blog'
urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    path('post/<slug:slug>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<slug:slug>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('post_comment/', views.post_comment, name='post-comment'),  # API to post a comment
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    # if post-create not work, it's because of post/<slug:slug>/ or detail view, then just change the name as
    # post/new/create. basically it's try to match 'new' as a slug..
]
