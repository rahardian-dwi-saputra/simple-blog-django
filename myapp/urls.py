from django.urls import path
from . import views

# import class View


urlpatterns = [
    path("register", views.register, name="register"),
    path("login/", views.loginView, name="login"),
    path("logout/", views.logoutView, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/detailpost/<slug:slug>/", views.show_post, name="dashboard-post-show"),

    path("category", views.categories, name="category-list"),
    path("category/create", views.create_category, name="category-create"),
    path("category/<slug:slug>/", views.update_category, name="category-update"),
    #path("category/delete/<slug:slug>/", views.delete_category, name="category-delete"),
    path("category/delete", views.delete_category, name="category-delete"),

    path("allpost", views.show_all_post, name="all-post"),
    path('allpost/json/', views.allpost_data, name='all-post-json'),
    path('allpost/detailpost/<slug:slug>/', views.show_post, name='all-post-detail'),
    path('allpost/deletepost', views.allpost_delete, name='all-post-delete'),

    path("post", views.posts, name="list-posts"),
    path('api/posts/', views.post_data, name='post-data'),
    path("post/create", views.create_post, name="create_post"),
    path("post/<slug:slug>/", views.show_post, name="detail_post"),
    path("post/edit/<slug:slug>/", views.update_post, name="update_post"),
    #path("post/delete/<slug:slug>/", views.delete_post, name="delete_post"),
    path("post/delete", views.delete_post, name="delete_post"),

    path("users", views.users, name="users"),
    path('api/users/', views.user_data, name='user_data'),
    path("users/<int:id>/", views.detail_user, name="detail-user"),
]