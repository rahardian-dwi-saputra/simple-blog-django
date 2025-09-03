from django.db import models

from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.html import strip_tags

from django.core.validators import MinLengthValidator
from django.core.validators import RegexValidator

import os
from django.db.models.signals import post_delete
from django.db.models.signals import pre_save
from django.dispatch import receiver

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


# Delete image file after post is deleted
@receiver(post_delete, sender=Post)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

# delete the old file when replacing the image
@receiver(pre_save, sender=Post)
def delete_old_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return  # New instance, no old file to delete

    try:
        old_file = Post.objects.get(pk=instance.pk).image
    except Post.DoesNotExist:
        return

    new_file = instance.image
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
    email_verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username