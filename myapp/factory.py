import factory
from factory.django import DjangoModelFactory

from django.contrib.auth.models import User
from .models import Category, Post, ViewPost

from django.utils import timezone

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

User = get_user_model()

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    username = factory.Faker('user_name')
    password = factory.LazyFunction(lambda: make_password('testpassword123'))
    is_staff = False
    is_superuser = False

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