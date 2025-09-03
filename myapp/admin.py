from django.contrib import admin

# Register your models here.
from . models import Category, Post
from . models import UserProfile

class FieldAdmin(admin.ModelAdmin):
    readonly_fields = ['id','slug']

admin.site.register(Category, FieldAdmin)
admin.site.register(Post, FieldAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo','email_verified_at')