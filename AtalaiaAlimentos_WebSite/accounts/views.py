from typing import Any
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.forms import LoginForm, UserForm


# Create your views here.
def register_view(request):
    if request.method == "POST":
        user_form = UserForm(request.POST)
        # Checking if the user data to be registered is valid
        if user_form.is_valid():
            user = user_form.save()
            print("Usuário cadastrado com sucesso!")
            if user:
                return redirect('login')
    else:
        user_form = UserForm() 
        print("Erro ao cadastrar novo usuário!")
        print(f'Erro: {user_form.errors}')
    
    return render(
        request,
        'register.html',
        {'user_form': user_form}
    )

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                print("Usuário Logado!")
                
                # # Obtém os grupos do usuário autenticado.add
                # user_group = user.groups.all()
                # for group in user_group:
                #     print("Usuário pertence ao grupo:", group.name)
                
                is_marketing_group = user.groups.filter(name='Marketing')
                if is_marketing_group:
                    print("Usuário pertence ao grupo Marketing!")
                    return redirect('logged')
                else:
                    return redirect('logged') 
    else:
        form = LoginForm()
        print("Erro ao logar")
    return render(request, 'login.html', {'form': form})
        

def logout_view(request):
    logout(request)
    return redirect('cars_list')

class LoggedView(LoginRequiredMixin, TemplateView):
    template_name = 'logpage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtém o nome do usuário logado
        user = self.request.user
        first_name = user.first_name if user.first_name else 'Usuário'
        # Adiciona a mensagem de boas-vindas ao contexto
        context['welcome_message'] = 'Bem-vindo, {}!'.format(first_name)
        return context

