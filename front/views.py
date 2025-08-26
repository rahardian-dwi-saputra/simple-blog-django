from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from myapp.models import Post

from django.db.models import Count

def index(request):
    posts = Post.objects.prefetch_related('viewpost_set').annotate(view_post=Count('viewpost__post_id')).filter(is_publish=True).values('slug','title','excerpt','image','view_post').order_by('-view_post')[:4]
    
    context={
        'posts': posts,
        'active': 'Home'
    }
    return render(request,'home.html', context)

def about(request):
    return render(request,'about.html', {'active':'About'})