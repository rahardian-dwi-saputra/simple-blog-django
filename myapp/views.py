from django.shortcuts import render, redirect

# Create your views here.
from . forms import RegisterForm, CategoryForm, PostForm

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from . models import Category, Post, ViewPost
from django.contrib.auth.models import User
from django.db.models import Q

from django.contrib import messages

from django.db.models import Count
from django.http import HttpResponseForbidden

from django.http import JsonResponse

from datetime import datetime

from django.http import HttpResponse

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

def my_profile(request):
    pass


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
def delete_category(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini")
    
    if request.POST.get('category_id', False):
        slug = request.POST['category_id']
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

    return redirect('category-list')

@login_required
def show_all_post(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini")
    
    categories = Category.objects.all().values('name','slug')
    context = {
        'categories':categories,
        'active':'Kelola Postingan'
    }
    return render(request,'allpost/index.html', context)

@login_required
def allpost_data(request):
    if not request.user.is_superuser:
        return JsonResponse({'message':'Anda tidak diizinkan mengakses halaman ini'})
    
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    queryset = Post.objects.select_related("category_id","author_id").prefetch_related('viewpost_set').annotate(view_post=Count('viewpost__post_id')).filter(is_publish=True)

    if request.GET.get('category', False):
        queryset = queryset.filter(category_id__slug=request.GET['category'])
    
    if request.GET.get('tanggal_awal', False):
        date_str = request.GET['tanggal_awal']
        date_obj = datetime.strptime(date_str, '%d-%m-%Y').date()
        queryset = queryset.filter(created_at__gte=date_obj)
    
    if request.GET.get('tanggal_akhir', False):
        date_str = request.GET['tanggal_akhir']
        date_obj = datetime.strptime(date_str, '%d-%m-%Y').date()
        queryset = queryset.filter(created_at__lte=date_obj)

    if search_value:
        queryset = queryset.filter(title__icontains=search_value) | queryset.filter(body__icontains=search_value)

    total = queryset.count()
    posts = queryset.order_by('-created_at')[start:start+length]

    data = []
    for i, post in enumerate(posts, start=start + 1):
        data.append({
            'DT_RowIndex': i,
            'title': post.title,
            'category': post.category_id.name,
            'author': post.author_id.get_full_name(),
            'view': post.view_post,
            'created_at': post.created_at.strftime('%d-%m-%Y %H:%M'),
            'action':'<a href="/allpost/detailpost/'+post.slug+'/" class="btn btn-primary btn-sm">'
                        '<i class="fa fa-eye"></i> Detail'
                    '</a>&nbsp;'
                    '<button type="button" class="btn btn-danger btn-sm" data-toggle="modal" data-slug="'+post.slug+'" data-target="#delete">'
                    '<i class="fa fa-trash"></i> Hapus'
                    '</button>',
        })

    return JsonResponse({
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,
        'data': data
    })

@login_required
def allpost_delete(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini")
    
    if request.POST.get('post_id', False):
        slug = request.POST['post_id']
        post = Post.objects.filter(slug=slug)
        if(post.exists()):
            ViewPost.objects.filter(post_id=post.get().id).delete()
            Post.objects.filter(slug=slug).delete()
            messages.success(request, 'Postingan berhasil dihapus')
        else:
            messages.error(request, 'Postingan tidak ditemukan')
    
    return redirect('all-post')

@login_required
def posts(request):
    categories = Category.objects.all().values('name','slug')
    context = {
        'categories':categories,
        'active':'Postingan Saya'
    }
    return render(request,'post/index.html', context)

@login_required
def post_data(request):
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    queryset = Post.objects.select_related("category_id").prefetch_related('viewpost_set').annotate(view_post=Count('viewpost__post_id')).filter(author_id=request.user.id)

    if request.GET.get('category', False):
        queryset = queryset.filter(category_id__slug=request.GET['category'])
    
    if request.GET.get('tampil', False):
        if request.GET['tampil'] == 'Ya':
            queryset = queryset.filter(is_publish=True)
        else:
            queryset = queryset.filter(is_publish=False)

    if request.GET.get('tanggal_awal', False):
        date_str = request.GET['tanggal_awal']
        date_obj = datetime.strptime(date_str, '%d-%m-%Y').date()
        queryset = queryset.filter(created_at__gte=date_obj)
    
    if request.GET.get('tanggal_akhir', False):
        date_str = request.GET['tanggal_akhir']
        date_obj = datetime.strptime(date_str, '%d-%m-%Y').date()
        queryset = queryset.filter(created_at__lte=date_obj)

    if search_value:
        queryset = queryset.filter(title__icontains=search_value) | queryset.filter(body__icontains=search_value)

    total = queryset.count()
    posts = queryset.order_by('-created_at')[start:start+length]

    data = []
    for i, post in enumerate(posts, start=start + 1):
        if post.is_publish:
            tampil = 'Ya'
        else:
            tampil = 'Tidak'

        data.append({
            'DT_RowIndex': i,
            'title': post.title,
            'category': post.category_id.name,
            'publish': tampil,
            'view': post.view_post,
            'created_at': post.created_at.strftime('%d-%m-%Y %H:%M'),
            'action':'<a href="/post/'+post.slug+'/" class="btn btn-primary btn-sm" title="Detail">'
                        '<i class="fa fa-eye"></i>'
                    '</a>&nbsp;'
                    '<a href="/post/edit/'+post.slug+'/" class="btn btn-warning btn-sm" title="Edit">'
                        '<i class="fa fa-edit"></i>'
                    '</a>&nbsp;'
                    '<button type="button" class="btn btn-danger btn-sm" data-toggle="modal" data-slug="'+post.slug+'" data-target="#delete">'
                    '<i class="fa fa-trash"></i>'
                    '</button>',
        })

    return JsonResponse({
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,
        'data': data
    })

@login_required
def create_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
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

@login_required
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
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.method == "POST":
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Postingan berhasil diedit')
                return redirect('list_posts') 
            except:
                pass

    context = {
        'title':'Edit Postingan',
        'active':'Postingan Saya',
        'action':'/post/edit/'+slug+'/',
        'form':form,
    }
    return render(request,'post/create.html', context)

@login_required
def delete_post(request):
    if request.POST.get('post_id', False):
        slug = request.POST['post_id']
        post = Post.objects.filter(slug=slug)
        if(post.exists()):
            ViewPost.objects.filter(post_id=post.get().id).delete()
            Post.objects.filter(slug=slug).delete()
            messages.success(request, 'Postingan berhasil dihapus')
        else:
            messages.error(request, 'Postingan tidak ditemukan')
    
    return redirect('list-posts')

@login_required
def users(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini")
    
    return render(request,'user/index.html', {'active':'Users'})

@login_required
def user_data(request):
    if not request.user.is_superuser:
        return JsonResponse({"message":"Anda tidak diizinkan mengakses halaman ini"})
    
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 10))
    search_value = request.GET.get('search[value]', '')

    # Query
    queryset = User.objects.filter(is_superuser=False)
    total = queryset.count()

    if search_value:
        queryset = queryset.filter(
            Q(username__icontains=search_value) |
            Q(email__icontains=search_value) |
            Q(first_name__icontains=search_value) |
            Q(last_name__icontains=search_value)
        )

    filtered = queryset.count()
    queryset = queryset[start:start+length]

    data = []
    for index, user in enumerate(queryset):
        data.append({
            'DT_RowIndex': start + index + 1,
            'full_name': user.get_full_name(),
            'username': user.username,
            'email': user.email,
            'last_name': user.date_joined.strftime('%d-%m-%Y %H:%M'),
            'action': '<a href="/users/'+str(user.id)+'/" class="btn btn-primary btn-sm" title="Detail"><i class="fa fa-eye"></i></a>'
        })

    return JsonResponse({
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': filtered,
        'data': data,
    })

@login_required
def detail_user(request, id):
    if not request.user.is_superuser:
        return HttpResponseForbidden("Anda tidak diizinkan mengakses halaman ini")
    
    user = User.objects.get(id=id)
    context={
        'active':'Users',
        'user':user
    }
    return render(request,'user/show.html', context)