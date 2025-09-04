from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from myapp.models import Post

from django.db.models import Count
from django.core.paginator import Paginator

def index(request):
    posts = Post.objects.prefetch_related('viewpost_set').annotate(view_post=Count('viewpost__post_id')).filter(is_publish=True).values('slug','title','excerpt','image','view_post').order_by('-view_post')[:4]
    users = User.objects.prefetch_related('post_set','userprofile_set').annotate(total=Count('post__author_id')).filter(post__is_publish=True).values('first_name','last_name','userprofile__photo','username','total').order_by('-total')[:3]

    context={
        'posts': posts,
        'users':users,
        'active': 'Home'
    }
    return render(request,'home.html', context)

def about(request):
    return render(request,'about.html', {'active':'About'})

def blog(request):
    posts = Post.objects.select_related("category_id","author_id").prefetch_related('viewpost_set').annotate(view_post=Count('viewpost__post_id')).filter(is_publish=True).order_by('-created_at')
    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context={
        'page_obj':page_obj,
        'active': 'Blog',
        'title':'Semua Postingan'
    }
    return render(request,'blog/all_blog.html', context)

def detail_post(request, slug):
    post = Post.objects.select_related("category_id","author_id").prefetch_related('viewpost_set').annotate(view_post=Count('viewpost__post_id')).get(slug=slug)
    context={
        'post': post,
        'active': 'Blog'
    }
    return render(request,'blog/blog_detail.html', context)