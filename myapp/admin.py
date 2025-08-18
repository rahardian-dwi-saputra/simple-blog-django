from django.contrib import admin

# Register your models here.
from . models import Category, Post

class FieldAdmin(admin.ModelAdmin):
    readonly_fields = ['id','slug']

admin.site.register(Category, FieldAdmin)
admin.site.register(Post, FieldAdmin)