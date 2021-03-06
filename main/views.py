from django.shortcuts import get_object_or_404, render
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from users.models import CustomUser
from .models import Post

def home(request):
    context = {'posts':Post.objects.all()}
    return render(request, 'main/index.html', context=context)

class PostListView(ListView):
    model = Post
    template_name = 'main/index.html' 
    context_object_name = 'posts' 
    ordering = ['-post_date']
    paginate_by = 4

class UserPostListView(ListView):
    model = Post
    template_name = 'main/user_posts.html' 
    context_object_name = 'posts' 
    paginate_by = 4

    def get_queryset(self):
        user = get_object_or_404(CustomUser, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-post_date')

class PostDetailView(DetailView):
    model = Post


class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content']
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def about(request):
    return render(request, 'main/about.html', {'title':'About'})