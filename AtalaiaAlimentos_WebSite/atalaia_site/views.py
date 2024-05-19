import datetime
from django.core.mail import EmailMessage, send_mail
from django.forms import modelform_factory
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.shortcuts import get_object_or_404, redirect, render, reverse
from atalaia_site.forms import ContactForm
from atalaia_site.models import Product, ProductCategory
from atalaia_alimentos_web import settings
from .models import Product, Recipe
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.utils.text import slugify

def set_cookies(response, key, value, days_expire=7):
    if days_expire is None:
        max_age = 365 * 24 * 60 * 60
    else:
        max_age = days_expire * 24 * 60 * 60
    expires = datetime.datetime.strftime(
        datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
        "%a, %d-%b-%Y %H:%%M:%S GMT",
    )
    response.set_cookie(
        key,
        value,
        max_age=max_age,
        expires=expires,
        domain=settings.COOKIE_DOMAIN,
        secure=settings.SESSION_COOKIE_SECURE or None,
    )
    
def cookie_view(request):
    response =  HttpResponse("Termos aceitos!")
    set_cookies(response, 'name', 'jujule')
    return response


def accept_terms(request):
    response = HttpResponse("Termos aceitos.")
    response.set_cookie('terms_accepted', 'true')
    return response

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_maintenance', {'products': products})


##################################################################################################################################################

class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pega as três últimas receitas cadastradas, ordenadas por data de criação
        latest_recipes = Recipe.objects.order_by('-created_at')[:3]
        context['recipes'] = latest_recipes
        return context
    
class TrabalheConoscoView(TemplateView):
    template_name = 'trabalhe_conosco.html'
    
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from .forms import ContactForm, ProductForm, RecipeForm  # Importe o formulário de contato

class ContactView(TemplateView):
    template_name = 'contact.html'
    success_url = 'success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['contact_form'] = ContactForm()  # Passar o formulário para o contexto do template
        return context

    def post(self, request, *args, **kwargs):
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            # Capturar os dados do formulário
            name = contact_form.cleaned_data['name']
            email = contact_form.cleaned_data['email']
            phone = contact_form.cleaned_data['phone']
            subject = contact_form.cleaned_data['subject']
            message = contact_form.cleaned_data['message']
            
            # Construir o corpo do e-mail
            email_body = f"""
            Nome: {name}
            Email: {email}
            Telefone: {phone}
            Assunto: {subject}
            Mensagem: {message}
            """
            print(f'A mensagem enviada: {email_body}')
            
            # Envie o e-mail
            send_mail(
                'Nova mensagem de contato',  # Assunto do e-mail
                email_body,  # Corpo do e-mail
                'rpa@atalaiaalimentos.ind.br',  # Seu endereço de e-mail
                ['gil.lopes@atalaiaalimentos.ind.br'],  # Lista de destinatários (neste caso, o e-mail interno)
                fail_silently=False,  # Não falhar silenciosamente em caso de erro
            )
            
            # Limpar os campos do formulário após o envio bem-sucedido
            contact_form = ContactForm()
            
            messages.success(request, "Mensagem enviada com sucesso! Obrigado!")
            return render(request, self.success_url)
        else:
            # Se o formulário não for válido, renderize novamente o template de contato com os erros
            messages.error(request, 'Falha no envio da mensagem. Por favor, verifique os campos e tente novamente.')
            context = self.get_context_data()
            context['contact_form'] = contact_form  # Passar o formulário de volta para o template com erros, se houver
            return render(request, self.template_name, {'contact_form': contact_form})

    def get(self, request, *args, **kwargs):
        # Lidar com solicitações GET
        context = self.get_context_data()
        return render(request, self.template_name, context)
        


def last_recipes(request):
    # Pega as três últimas receitas cadastradas, ordenadas por data de criação
    latest_recipes = Recipe.objects.order_by('-created_at')[:3]
    return render(request, '_recipes.html', {'recipes': latest_recipes})

class RecipesListView(ListView):
    model = Recipe
    template_name = 'recipes.html'
    content_object_name = 'recipes'
    paginate_by = 6
    
    def get_queryset(self):
        recipes = super().get_queryset().order_by('-created_at')
        title_query = self.request.GET.get('title')
        
        if title_query:
            recipes = recipes.filter(title__icontains=title_query)

            
        return recipes
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = self.get_queryset()
        return context

class ProductListView(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 9
    
    def get_queryset(self):
        products = super().get_queryset().order_by('category')
        search = self.request.GET.get('search')
    
        if search:
            products = products.filter(product__icontains=search)
            
        return products
    
class TrayProductListView(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        products = super().get_queryset().order_by('category')
        category_name = 'Bandeja'  # Set the category name here
        search = self.request.GET.get('search')

        if category_name:
            category = get_object_or_404(ProductCategory, name=category_name)
            products = products.filter(category=category)

        if search:
            products = products.filter(product__icontains=search)

        return products
    
    
class ChilledProductListView(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        products = super().get_queryset().order_by('category')
        category_name = 'Resfriado'  # Set the category name here
        search = self.request.GET.get('search')

        if category_name:
            category = get_object_or_404(ProductCategory, name=category_name)
            products = products.filter(category=category)

        if search:
            products = products.filter(product__icontains=search)

        return products

      
class FrozenProductListView(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        products = super().get_queryset().order_by('category')
        category_name = 'Congelado'  # Set the category name here
        search = self.request.GET.get('search')

        if category_name:
            category = get_object_or_404(ProductCategory, name=category_name)
            products = products.filter(category=category)

        if search:
            products = products.filter(product__icontains=search)

        return products
    
    
class SausageProductListView(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        products = super().get_queryset().order_by('category')
        category_name = 'Linguiça'  # Set the category name here
        search = self.request.GET.get('search')

        if category_name:
            category = get_object_or_404(ProductCategory, name=category_name)
            products = products.filter(category=category)

        if search:
            products = products.filter(product__icontains=search)

        return products
    
    
class PaoDeQueijoView(TemplateView):
    template_name = 'pao_de_queijo.html'
    
class BreadProductListView(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        products = super().get_queryset().order_by('category')
        category_name = 'Pão de Queijo'  # Set the category name here
        search = self.request.GET.get('search')

        if category_name:
            category = get_object_or_404(ProductCategory, name=category_name)
            products = products.filter(category=category)

        if search:
            products = products.filter(product__icontains=search)

        return products
    
class ProductDetailView(DetailView):
    model = Product
    template_name='product_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
def load_product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    data = {
        'product': product.product,
        'description': product.description,
        'weight': product.weight,
        'unit': product.unit,
        'validity': product.validity,
        'conservation': product.conservation,
        'nutricional_informations_image': product.nutricional_informations_image,
    }
    return JsonResponse(data)
    
class InstitutionalView(View):
    def get(self, request):
        return render(request, 'institutional.html', {})
    
    
class PrivacyView(View):
    def get(self, request):
        return render(request, 'privacy.html', {})
    

###############################################################################################################################################

class NewProductView(ListView):
    model = Product
    template_name = 'product_add.html'
    context_object_name = 'products'

    def get(self, request):
        new_product_form = ProductForm()
        products = self.get_queryset()
        return render(
            request,
            'product_add.html',
            {'new_product_form': new_product_form, 'products': products}
        )

    def post(self, request, *args, **kwargs):
        new_product_form = ProductForm(request.POST, request.FILES)
        products = self.get_queryset()

        if new_product_form.is_valid():
            product = new_product_form.save(commit=False)
            product.slug = slugify(product.product)
            product.save()
            return redirect('new_product')

        return render(
            request,
            self.template_name,
            {'new_product_form': new_product_form,
             'products': products},
        )


class ProductMaintenance(ListView):
    model = Product
    template_name = 'product_maintenance.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        products = super().get_queryset().order_by('category')
        search = self.request.GET.get('search')

        if search:
            products = products.filter(product_icontains=search)

        return products

    def get(self, request):
        new_product_form = ProductForm()
        products = self.get_queryset()
        return render(
            request,
            'product_maintenance.html',
            {'new_product_form': new_product_form, 'products': products}
        )

    def post(self, request, *args, **kwargs):
        new_product_form = ProductForm(request.POST, request.FILES)
        products = self.get_queryset()

        if new_product_form.is_valid():
            product = new_product_form.save(commit=False)
            product.slug = slugify(product.product)
            product.save()
            messages.success(request, 'Produto adicionado com sucesso.')
            return redirect('product_maintenance')

        return render(
            request,
            self.template_name,
            {'new_product_form': new_product_form,
             'products': products},
        )
        
        
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_maintenance', {'products': products})

class ProductEditView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'product_maintenance.html'

    def get_initial(self):
        initial = super().get_initial()
        product = self.get_object()
        initial['product'] = product.product
        initial['image'] = product.image
        initial['category'] = product.category
        initial['description'] = product.description
        initial['weight'] = product.weight
        initial['unit'] = product.unit
        initial['validity'] = product.validity
        initial['conservation'] = product.conservation
        initial['nutricional_information_image'] = product.nutricional_informations_image
        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        product = self.get_object()
        kwargs['instance'] = product
        return kwargs

    def get_object(self, queryset=None):
        obj = get_object_or_404(Product, id=self.kwargs['id'])
        return obj

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('product_maintenance')
    

class RecipeMaintenance(ListView):
    model = Recipe
    template_name = 'recipe_maintenance.html'
    context_object_name = 'recipes'
    paginate_by = 9

    def get_queryset(self):
        recipe = super().get_queryset().order_by('title')
        search = self.request.GET.get('search')

        if search:
            recipe = recipe.filter(recipe_icontains=search)

        return recipe

    def get(self, request):
        new_recipe_form = RecipeForm()
        recipes = self.get_queryset()
        return render(
            request,
            'recipe_maintenance.html',
            {'new_recipe_form': new_recipe_form, 'recipes': recipes}
        )

    def post(self, request, *args, **kwargs):
        new_recipe_form = RecipeForm(request.POST, request.FILES)
        recipes = self.get_queryset()

        if new_recipe_form.is_valid():
            recipe = new_recipe_form.save(commit=False)
            recipe.slug = slugify(recipe.recipe)
            recipe.save()
            return redirect('new_recipe')

        return render(
            request,
            self.template_name,
            {'new_recipe_form': new_recipe_form,
             'recipes': recipes},
        )
        

class NewRecipeView(ListView):
    model = Recipe
    template_name = 'recipe_add.html'
    context_object_name = 'recipes'

    def get(self, request):
        new_recipe_form = RecipeForm()
        recipes = self.get_queryset()
        return render(
            request,
            'recipe_add.html',
            {'new_recipe_form': new_recipe_form, 'recipes': recipes}
        )

    def post(self, request, *args, **kwargs):
        new_recipe_form = RecipeForm(request.POST, request.FILES)
        recipes = self.get_queryset()

        if new_recipe_form.is_valid():
            recipe = new_recipe_form.save(commit=False)
            recipe.slug = slugify(recipe.title())
            recipe.save()
            return redirect('new_recipe')

        return render(
            request,
            self.template_name,
            {'new_recipe_form': new_recipe_form,
             'recipes': recipes},
        )
        
        
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipe_maintenance', {'recipes': recipes})


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'components/_product_update_form.html'  # Nome do template para a página de edição do produto

    def get_object(self, queryset=None):
        # Obtém o objeto do produto com base no ID fornecido na URL
        selected_product = get_object_or_404(Product, id=self.kwargs['pk'])
        print(f'Produto: {selected_product.product}')
        print(f'Descrição: {selected_product.description}')
        return selected_product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_product = self.get_object()
        context['selected_product'] = selected_product
        return context

    def form_valid(self, form):
        # Salva o formulário e retorna o resultado do método form_valid da classe pai
        return super().form_valid(form)


class RecipeEditView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipe_maintenance.html'

    def get_initial(self):
        initial = super().get_initial()
        recipe = self.get_object()
        initial['title'] = recipe.title
        initial['time'] = recipe.time
        initial['revenue'] = recipe.revenue
        initial['description'] = recipe.description
        initial['ingredients'] = recipe.ingredients
        initial['preparation'] = recipe.preparation
        initial['image'] = recipe.image

        return initial

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        product = self.get_object()
        kwargs['instance'] = product
        return kwargs

    def get_object(self, queryset=None):
        obj = get_object_or_404(Product, id=self.kwargs['id'])
        return obj

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class RecipeUpdateView(UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'edit_recipe.html'

    def get_object(self, queryset=None):
        # Obtém o objeto do produto com base no ID fornecido na URL
        return get_object_or_404(Recipe, id=self.kwargs['id'])

    def form_valid(self, form):
        # Salva o formulário e retorna o resultado do método form_valid da classe pai
        return super().form_valid(form)


class RecipeDeleteView(DeleteView):
    model = Recipe
    template_name = 'recipe_confirm_delete.html'
    success_url = reverse_lazy('recipe_maintenance')
    