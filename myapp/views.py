from django.shortcuts import render, redirect

# Create your views here.
from . forms import RegisterForm, CategoryForm, PostForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from . models import Category, Post, ViewPost

from django.contrib import messages

from django.db.models import Count
from django.http import HttpResponseForbidden


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Registerasi berhasil")
            return redirect('login')
        
    return render(request,'authentication/register.html',{'form':form})

def loginView(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Username atau Password kamu salah. Silahkan coba kembali.')

    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        return render(request,'authentication/login.html')

def logoutView(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    post = Post.objects.filter(author_id=request.user.id)
    traffic = ViewPost.objects.filter(post_id__in=post.values_list('id')).count()

    popular_post = Post.objects.select_related("category_id").prefetch_related('viewpost_set').annotate(view_post=Count('viewpost__post_id')).filter(author_id=request.user.id, is_publish=True).values('slug','title','category_id__name','created_at','view_post').order_by('-view_post')[:4]
    
    context = {
        'active':'Dashboard',
        'total_post': post.count(),
        'publish_post': post.filter(is_publish=True).count(),
        'total_traffic': traffic,
        'popular_post': popular_post,
    }
    return render(request,'dashboard.html', context)

@login_required
def categories(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini")
    
    categories = Category.objects.all().values('name','slug')
    return render(request,'category/index.html', {'categories':categories,'active':'Category'})

@login_required
def create_category(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini")
    
    form = CategoryForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Data kategori berhasil ditambahkan')
                return redirect('/category') 
            except:
                pass

    context = {
        'title':'Tambah Kategori Baru',
        'active':'Category',
        'action':'/category/create',
        'form':form,
    }

    return render(request,'category/create.html', context)

@login_required
def update_category(request, slug):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini")
    
    category = Category.objects.get(slug=slug)
    data = {
        'name':category.name,
    }
    form = CategoryForm(request.POST or None,initial=data,instance=category)
    if request.method == "POST":
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Data kategori berhasil diedit')
                return redirect('/category') 
            except:
                pass

    context = {
        'title':'Edit Data Kategori',
        'active':'Category',
        'action':'/category/'+slug+'/',
        'form':form,
    }
    return render(request,'category/create.html', context)

@login_required 
def delete_category(request, slug):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini")
    
    category = Category.objects.filter(slug=slug)
    if(category.exists()):
        post = Post.objects.filter(category_id=category.get().id)
        if(post.exists()):
            messages.error(request, 'Data kategori tidak dapat dihapus karena sedang digunakan')
        else:
            Category.objects.filter(slug=slug).delete()
            messages.success(request, 'Data kategori berhasil dihapus')
    else:
        messages.error(request, 'Data kategori tidak ditemukan')

    return redirect('/category')

def show_all_post(request):
    categories = Category.objects.all().values('name','slug')
    context = {
        'categories':categories
    }
    return render(request,'allpost/index.html', context)


def posts(request):
    categories = Category.objects.all().values('name','slug')
    posts = Post.objects.select_related("category_id").all()
    print(posts)
    context = {
        'categories':categories,
        'posts':posts,
        'active':'Postingan Saya'
    }
    return render(request,'post/index.html', context)

@login_required
def create_post(request):
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author_id = request.user
            instance.save()
            messages.success(request, 'Postingan baru berhasil ditambahkan')
            return redirect('list_posts') 
           
    context = {
        'title':'Buat Postingan Baru',
        'active':'Postingan Saya',
        'form':form,
        'action':'/post/create'
    }

    return render(request,'post/create.html', context)

def show_post(request, slug):
    post = Post.objects.select_related("category_id","author_id").prefetch_related('viewpost_set').get(slug=slug)
    #tes = Post.objects.prefetch_related('viewpost_set').all() 
    context = {
        'active':'Postingan Saya',
        'post':post,
        'back':'/post'
    }
    return render(request,'post/show.html', context)

def update_post(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(request.POST or None,instance=post)
    if request.method == "POST":
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Data kategori berhasil diedit')
                return redirect('/category') 
            except:
                pass

    context = {
        'title':'Edit Postingan',
        'active':'Postingan Saya',
        'action':'/post/'+slug+'/edit',
        'form':form,
    }
    return render(request,'post/create.html', context)

def delete_post(request, slug):
    post = Post.objects.filter(slug=slug)
    if(post.exists()):
        Post.objects.filter(slug=slug).delete()
        messages.success(request, 'Postingan berhasil dihapus')
    else:
        messages.error(request, 'Postingan tidak ditemukan')
    
    return redirect('/post')