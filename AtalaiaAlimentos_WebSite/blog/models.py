from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=30)
    
    class Meta:
        verbose_name_plural = "categories"
        
    def __str__(self):
        return self.name
    
class Post(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='atalaia_site/', null=True, blank=True)
    instagram_video = models.TextField(null=True, blank=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField("Category")
    is_published = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.title}"

    
