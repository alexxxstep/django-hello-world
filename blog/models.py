from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Define a custom manager for the Post model to filter published posts


class PublishedManager(models.Manager):
    def get_queryset(self):
        # Override the get_queryset method to filter for published posts
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


# Define the Post model to represent blog posts
class Post(models.Model):

    # Define a nested class to represent the status choices for a post
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)  # Title of the post
    # SEO-friendly URL for the post
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    # Author of the post (foreign key to User model)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()  # Body text of the post
    # Datetime when the post is published
    publish = models.DateTimeField(default=timezone.now)
    # Datetime when the post is created (set automatically on creation)
    created = models.DateTimeField(auto_now_add=True)
    # Datetime when the post is last updated (set automatically on save)
    updated = models.DateTimeField(auto_now=True)
    # Status of the post (draft or published)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT)
    objects = models.Manager()  # Default manager for the model
    published = PublishedManager()  # Custom manager to retrieve published posts
    tags = TaggableManager()

    class Meta:
        ordering = ['-publish']  # Default ordering: newest posts first
        indexes = [
            # Index to improve query performance on publish field
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        # String representation of the model instance (title of the post)
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])


class Comment(models.Model):
    post = models.ForeignKey(Post, 
                             on_delete=models.CASCADE, 
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]
        
    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
