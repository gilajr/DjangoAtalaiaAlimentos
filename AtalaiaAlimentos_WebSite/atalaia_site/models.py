from django.db import models
from django.utils.text import slugify
from django.utils import timezone

class Recipe(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, default='', null=False, blank=False)
    time = models.CharField(max_length=6, default='')
    revenue = models.CharField(max_length=10)
    description = models.TextField(max_length=3000, default='', null=False, blank=False)
    ingredients = models.TextField(max_length=3000, null=False, blank=False)
    preparation = models.TextField(max_length=3000, null=False, blank=False)
    image = models.ImageField(upload_to='atalaia_site/', null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(default="", null=False, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Verifica se o slug já está preenchido ou se o título mudou
        if not self.slug or self.slug != slugify(self.title):
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    

class  ProductCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Product(models.Model):
    
    id = models.AutoField(primary_key=True)
    product = models.CharField(max_length=3000, null=False, blank=False)
    image = models.ImageField(upload_to='atalaia_site/', null=True, blank=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.PROTECT, related_name='product_category')
    description = models.TextField(max_length=3000, default='', null=False, blank=False)
    weight = models.CharField(max_length=13, null=False, blank=False)
    unit = models.CharField(max_length=2, null=False, blank=False)
    validity = models.CharField(max_length=8, null=False, blank=False)
    conservation = models.CharField(max_length=18, null=False, blank=False)
    nutricional_informations_image = models.ImageField(upload_to='atalaia_site/', null=True, blank=True)
    slug = models.SlugField(default="", null=False, unique=True)
    
    def __str__(self):
        return f"{self.product}"
    
    def save(self, *args, **kwargs):
        # Verifica se o slug já está preenchido ou se o título mudou
        if not self.slug or self.slug != slugify(self.product):
            self.slug = slugify(self.product)
        super().save(*args, **kwargs)
    
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    
    SUBJECT_CHOICES = (
        ('', 'Escolha um assunto'),
        ('Dúvidas', 'Dúvidas'),
        ('Sugestão', 'Sugestão'),
        ('Elogio', 'Elogio'),
        ('Reclamações', 'Reclamações'),
        ('SAC', 'SAC'),
    )
    
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    message = models.TextField()

    def __str__(self):
        return f"Message from {self.name}"