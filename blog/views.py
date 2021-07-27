from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, HttpResponseRedirect, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Category, Post, PostComment
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import ContactForm
from django.contrib import messages


class PostListView(ListView):
    model = Post
    template_name = 'blog/blog_home.html'
    paginate_by = 5
    # context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all(),
            'category': self.request.GET.get('q'),
        })
        return context

    def get_queryset(self):
        category = self.request.GET.get('q')
        if category is None:
            return Post.objects.all()
        else:
            category = category.strip()
            return Post.objects.filter(Q(title__icontains=category) | Q(category__name__icontains=category) |
                                       Q(author__username__icontains=category))


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(UserPostListView, self).get_context_data(**kwargs)
        context.update({
            'categories': Category.objects.all(),
            'category': self.request.GET.get('q'),
            'username': get_object_or_404(User, username=self.kwargs.get('username')),
        })
        return context

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        posts = Post.objects.filter(author=user)
        category = self.request.GET.get('q')
        if category is None:
            return posts
        else:
            category = category.strip()
            return posts.filter(Q(title__icontains=category) | Q(category__name__icontains=category))


class PostDetailView(DetailView):  # for blog post details view
    model = Post

    def get(self, request, *args, **kwargs):
        post = Post.objects.filter(slug=self.kwargs.get('slug')).first()

        comments = PostComment.objects.filter(post=post, parent=None)  # filtering actual comments
        replies = PostComment.objects.filter(post=post).exclude(parent=None)  # filtering replies

        reply_dict = {}
        for reply in replies:
            if reply.parent.serial_no not in reply_dict.keys():  # checking if reply parent is in dictionary
                reply_dict[reply.parent.serial_no] = [reply]  # appending parent if not present
            else:
                reply_dict[reply.parent.serial_no].append(reply)  # appending reply to existing parent

        # print(request.user)  # checking AnonymousUser or authenticated user
        context = {'object': post, 'comments': comments, 'reply_dict': reply_dict}
        if context['object'] is None:
            return HttpResponse("404 - Not Found")

        return render(request, 'blog/post_detail.html', context)


def post_comment(request):
    if request.method == "POST":
        comment = request.POST.get('comment')
        user = request.user
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        parent_serial_no = request.POST.get('parent_serial_no')

        if len(comment) == 0:
            return HttpResponseRedirect(reverse('blog:post-detail', kwargs={'slug': post.slug}))

        if parent_serial_no == "":
            comment = PostComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Comment posted successfully")
        else:
            parent = PostComment.objects.get(serial_no=parent_serial_no)
            comment = PostComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Reply posted successfully")

        return HttpResponseRedirect(reverse('blog:post-detail', kwargs={'slug': post.slug}))
    else:
        return HttpResponse("404 - Not Found")


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'category', 'sub_heading', 'content', 'thumbnail']
    extra_context = {'title': 'Create Post'}
    # template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'category', 'sub_heading', 'content', 'thumbnail']
    extra_context = {'title': 'Update Post'}
    # template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    extra_context = {'title': 'Delete Post'}
    success_url = '/'
    # template_name = 'blog/post_confirm_delete.html'

    # def get_success_url(self):
    #     return reverse('/')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST, label_suffix='')
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for contacting. We will try to reach you out as soon as possible.")
            return redirect('blog:contact')
    else:
        form = ContactForm(label_suffix='')
    return render(request, 'blog/contact.html', {'title': 'Contact', 'form': form})
