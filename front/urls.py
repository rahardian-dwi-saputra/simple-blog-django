from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("about", views.about, name="about"),

    path("blog", views.blog, name="blog"),
    path("blog/detail/<slug:slug>/", views.detail_post, name="blog_detail"),
]