from django.contrib import admin
from .models import Recipe, Product, ProductCategory

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('title',)  # Adicione uma vírgula após 'title' para garantir que seja uma tupla
    search_fields = ('title',)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product',)  # Adicione uma vírgula após 'product' para garantir que seja uma tupla
    search_fields = ('product',)
    
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Adicione uma vírgula após 'product' para garantir que seja uma tupla
    search_fields = ('name',)

# Registrar os modelos com suas classes de administração personalizadas
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory, ProductCategoryAdmin)
