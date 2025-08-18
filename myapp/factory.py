import factory
from factory.django import DjangoModelFactory

from django.contrib.auth.models import User
from .models import Category, Post, ViewPost

from django.utils import timezone

class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post
    
    title = factory.Faker('sentence', nb_words=5)
    slug = factory.Faker('slug')
    category_id = factory.Iterator(Category.objects.all())
    author_id = factory.Iterator(User.objects.all())
    is_publish = factory.Faker('boolean')
    excerpt = factory.Faker('paragraph', nb_sentences=1)
    body = factory.Faker('paragraph', nb_sentences=3)

class ViewPostFactory(DjangoModelFactory):
    class Meta:
        model = ViewPost
    
    post_id = factory.Iterator(Post.objects.all())
    ip_visitor = factory.Faker('ipv4')
    access_at = factory.Faker('date_time_between', start_date='-1y', end_date='now', tzinfo=timezone.get_current_timezone())