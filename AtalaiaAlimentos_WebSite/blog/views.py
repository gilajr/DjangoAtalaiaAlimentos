from django.shortcuts import render
from .models import Post, Category
from django.views.generic import DetailView, ListView

def posts_view(request):
    # posts = Post.objects.filter(is_published=True).prefetch_related('categories')
    posts = Post.objects.all().order_by("-created_on")
    context = {'posts': posts}
    return render(request, 'blog.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = super().get_queryset().order_by("-created_on")
        search_query = self.request.GET.get('search', None)
        
        if search_query:
            queryset = queryset.filter(title__icontains=search_query)
            
        return queryset


class PostDetailView(DetailView):
    model = Post
    template_name='post_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        post_categories = post.categories.all()
        context['post_categories'] = post_categories
        return context