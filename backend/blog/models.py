from django.db import models
from django.conf import settings
from slugify import slugify
from django_ckeditor_5.fields import CKEditor5Field


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name



class Post(models.Model):

    class Status(models.TextChoices):
        DRAFT     = 'draft',     'Draft'
        PUBLISHED = 'published', 'Published'
        ARCHIVED  = 'archived',  'Archived'

    author      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    category    = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    tags        = models.ManyToManyField(Tag, blank=True, related_name='posts')
    title       = models.CharField(max_length=200)
    slug        = models.SlugField(max_length=200, unique=True, blank=True)
    body        = CKEditor5Field('Text', config_name='extends')
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    status      = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)
    published_at= models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



class Comment(models.Model):
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    body       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Comment by {self.author.get_full_name()} on {self.post.title}'



class Like(models.Model):
    post       = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'{self.user.get_full_name()} liked {self.post.title}'

