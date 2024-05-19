from django.contrib import admin
from django.urls import path
from blog.views import PostDetailView, PostListView, posts_view
from atalaia_site.views import BreadProductListView, ChilledProductListView, ContactView, FrozenProductListView, IndexView, InstitutionalView, NewProductView, NewRecipeView, PaoDeQueijoView, PrivacyView, ProductDeleteView, ProductEditView, ProductMaintenance, ProductUpdateView, RecipeDeleteView, RecipeEditView, RecipeMaintenance, RecipeUpdateView, RecipesListView, SausageProductListView, TrayProductListView, accept_terms, cookie_view, last_recipes, ProductListView, ProductDetailView, TrabalheConoscoView, load_product_detail
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import login_view, logout_view, register_view, LoggedView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('last_recipes/', last_recipes, name='last_recipes'),
    path('recipes/', RecipesListView.as_view(), name='recipes_list'),
    path('recipe_maintenance/', RecipeMaintenance.as_view(), name='recipe_maintenance'),
    path('add_recipe', NewRecipeView.as_view(), name= 'add_recipe'),
    path('edit_recipe/<int:id>/', RecipeEditView.as_view(), name='edit_recipe'),
    path('update_recipe/<int:id>/', RecipeUpdateView.as_view(), name='update_recipe'),
    path('delete_recipe/<int:pk>/', RecipeDeleteView.as_view(), name='delete_recipe'),
    path('product/', ProductListView.as_view(), name='products_list'),
    path('tray_product/', TrayProductListView.as_view(), name='tray_products_list'),
    path('chilled_product/', ChilledProductListView.as_view(), name='chilled_products_list'),
    path('frozen_product/', FrozenProductListView.as_view(), name='frozen_products_list'),
    path('sausage_product/', SausageProductListView.as_view(), name='sausage_products_list'),
    path('bread_product/', BreadProductListView.as_view(), name='bread_products_list'),
    path('pao_de_queijo/', PaoDeQueijoView.as_view(), name="pao_de_queijo"),
    path('product_maintenance/', ProductMaintenance.as_view(), name='product_maintenance'),
    path('add_product', NewProductView.as_view(), name= 'add_product'),
    path('edit_product/<int:id>/', ProductEditView.as_view(), name='edit_product'),
    path('update_product/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('delete_product/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:pk>/', load_product_detail, name='load_product_detail'),
    path('institucional/', InstitutionalView.as_view(), name='institucional'),
    path('trabalhe_conosco/', TrabalheConoscoView.as_view(), name='trabalhe_conosco'),
    path('fale_conosco/', ContactView.as_view(), name='fale_conosco'),
    path('privacy/', PrivacyView.as_view(), name='privacy'),
    path('accept-terms/', accept_terms, name='accept_terms'),
    path('register/', register_view, name='register'),  
    path('login/', login_view, name='login'),  
    path('logout/', logout_view, name='logout'),  
    path('logged/', LoggedView.as_view(), name='logged'),
    path('blog/', PostListView.as_view(), name='blog'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
