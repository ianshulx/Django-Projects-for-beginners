from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Post
from .forms import PostForm

class PostList(ListView):
    model = Post
    context_object_name = "posts"
    template_name = 'post_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get("q", "")
        return context
    
    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            if Post.objects.filter(author__username__icontains=query).exists():
                return Post.objects.filter(author__username__icontains=query).order_by("-post_date", "-post_time", "-id")
            return Post.objects.filter(post_header__icontains=query).order_by("-post_date", "-post_time", "-id")
        return Post.objects.all().order_by("-post_date", "-post_time", "-id")
    

@method_decorator(login_required(login_url="/"), name="dispatch")
class UpdatePost(UpdateView):
    model = Post
    template_name = "update_post.html"
    fields = ["post_header", "post_text", "image"]

    def get_success_url(self):
        return reverse_lazy("blog:post", kwargs={"pk": self.object.id})
    

@login_required(login_url="/")
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect("blog:index")

def post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'post.html', {"post": post})

@login_required(login_url="/")
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/")
    else:
        form = PostForm()

    return render(request, "new_post.html", {"form": form})

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user.is_authenticated:
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
    else:
        return redirect("accounts:login")
        
    return redirect("blog:post", pk=pk)