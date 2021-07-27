from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    sub_heading = models.CharField(max_length=500, null=True, blank=True)
    content = RichTextUploadingField()
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    date_posted = models.DateTimeField(default=timezone.now)
    thumbnail = models.ImageField(upload_to='blog/thumbnails', null=True, blank=True,
                                  default='blog/thumbnails/thumbnail.png')
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return f'{self.title} by {self.author}'

    def get_absolute_url(self):  # redirects to post details after creating a post successfully
        return reverse('blog:post-detail', kwargs={'slug': self.slug})  # reverse() return the full path as a string

    def save(self, *args, **kwargs):
        if self.slug is None:
            slug = slugify(self.title)

            has_slug = Post.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.title) + '-' + str(count)
                has_slug = Post.objects.filter(slug=slug).exists()

            self.slug = slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_posted']


class PostComment(models.Model):
    serial_no = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.comment[:15]} by {self.user}, serial no: {self.serial_no}'


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.name}, {self.email} at {self.timestamp}'
