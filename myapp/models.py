from django.db import models

from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.html import strip_tags

from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator

# Create your models here.
class Category(models.Model):
    alphanumeric_with_spaces = RegexValidator(
            r'^[a-zA-Z ]*$',
            'Only alpha characters and spaces are allowed.'
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(
        max_length=200, 
        unique=True,
        validators=[
            MinLengthValidator(5, 'This field must be at least 5 characters long.'),
            alphanumeric_with_spaces
        ]
    )
    slug = models.SlugField(max_length=200, blank=True, editable=False)

    class Meta:
        db_table = 'categories'
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self):
        return "{}".format(self.name)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

class Post(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(
        max_length=250,
        unique=True,
        validators=[
            MinLengthValidator(5, 'This field must be at least 5 characters long.'),
        ]
    )
    slug = models.CharField(max_length=250, blank=True, editable=False)
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='category_id')
    author_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column='author_id')
    is_publish = models.BooleanField(default=True)
    excerpt = models.TextField(blank=True, editable=False)
    image = models.ImageField(upload_to='post_images/',blank=True,null=True)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'posts'
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return "{}".format(self.title)
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        excerpt = (strip_tags(self.body))
        if len(excerpt) > 200:
            excerpt = excerpt[0:200]

        self.excerpt = excerpt
        super(Post, self).save(*args, **kwargs)


class ViewPost(models.Model):
    id = models.BigAutoField(primary_key=True)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, db_column='post_id')
    ip_visitor = models.GenericIPAddressField()
    access_at = models.DateTimeField()

    class Meta:
        db_table = 'view_posts'
        verbose_name = 'view post'
        verbose_name_plural = 'view posts'