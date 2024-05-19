# from django.contrib import admin
# from django.contrib.auth.models import User
# from django.contrib.auth.admin import UserAdmin

# from accounts.forms import UserForm
# from .models import RHProfile, MarketingProfile

# admin.site.register(RHProfile)
# admin.site.register(MarketingProfile)

# class CustomUser(UserAdmin):
#     def add_view(self, request, form_url='', extra_content=None):
#         # Verifique se o usuário atual é um superusuário
#         if request.user.is_superuser:
#             self.form = UserForm
            
#         return super().add_view(request, form_url, extra_content)
    
    
# admin.site.unregister(User)
# admin.site.register(User, CustomUser)


