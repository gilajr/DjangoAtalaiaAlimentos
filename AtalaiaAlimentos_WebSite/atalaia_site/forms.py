from django import forms

from atalaia_site.models import Product, Recipe


class RecipeForm(forms.ModelForm):

    class Meta:
        model = Recipe
        fields = ['title', 'time', 'revenue', 'description', 'ingredients', 'preparation', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10}),
            'ingredients': forms.Textarea(attrs={'rows': 10}),
            'peparation': forms.Textarea(attrs={'rows': 10}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].initial = ''
        self.fields['time'].initial = ''
        self.fields['revenue'].initial = ''
        self.fields['description'].initial = ''
        self.fields['ingredients'].initial = ''
        self.fields['preparation'].initial = ''
        self.fields['image'].initial = ''
    
    
class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['product', 'image', 'category', 'description', 'weight', 'unit', 'validity', 'conservation', 'nutricional_informations_image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 8}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].initial = ''
        self.fields['image'].initial = ''
        self.fields['description'].initial = ''
        self.fields['weight'].initial = ''
        self.fields['unit'].initial = ''
        self.fields['validity'].initial = ''
        self.fields['conservation'].initial = ''
        self.fields['nutricional_informations_image'].initial = ''
    
        
class ContactForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Seu Nome", "class": "form-control"})
    )
    email = forms.EmailField(
        widget=forms.TextInput(attrs={"placeholder": "Seu Email", "class": "form-control"})
    )
    phone = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Seu Telefone", "class": "form-control"})
    )
    subject_choices = (
        ('', 'Escolha um assunto'),
        ('Dúvidas', 'Dúvidas'),
        ('Sugestão', 'Sugestão'),
        ('Elogio', 'Elogio'),
        ('Reclamações', 'Reclamações'),
        ('SAC', 'SAC'),
    )
    subject = forms.ChoiceField(
        choices=subject_choices,
        widget=forms.Select(attrs={"class": "form-select"})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"placeholder": "Sua Mensagem", "class": "form-control"})
    )

    def send_email(self):
        # Aqui você pode adicionar a lógica para enviar o e-mail
        pass
