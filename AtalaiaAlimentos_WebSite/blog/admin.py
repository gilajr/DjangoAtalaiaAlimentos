from django.contrib import admin
from blog.models import Category, Post

class CategoryAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_on', 'is_published')
    list_filter = ('is_published', 'categories')
    search_fields = ('title', 'body')


admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
