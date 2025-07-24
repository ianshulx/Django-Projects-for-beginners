from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Article, Comment
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from .forms import ArticleForm, CommentForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth.forms import UserCreationForm


# Create your views here.


def Home(request):
    articles = Article.objects.all()
    context = {"articles": articles}
    return render(request, "articles/home.html", context)


# use function-based view
def ArticleDetails(request, pk):
    article = Article.objects.get(id=pk)
    comments = article.comments.all()
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.writer = request.user
            comment.save()
            return redirect("article_details", pk=article.pk)
    context = {"article": article, "comments": comments, "comment_form": form}

    return render(request, "articles/article_details.html", context)


# Class-based views just for training

# class ArticleDetials(DetailView):
#     model = Article
#     template_name = "articles/article_details.html"


def AddArticle(request):
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.save()
            return redirect("article_details", pk=article.pk)

    context = {"form": form}
    return render(request, "articles/add_article.html", context)


# Class-Based View for training
# class AddArticle(CreateView):
#     model = Article
#     fields = ["title", "body"]
#     template_name = "articles/add_article.html"


#     def form_valid(self, form):
#         form.instance.author = self.request.user
#         return super().form_valid(form)


def EditArticle(request, pk):
    article = Article.objects.get(id=pk)
    form = ArticleForm(instance=article)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect("article_details", pk=article.pk)
    context = {"form": form}
    return render(request, "articles/edit_article.html", context)


# Class-Based View for Training
# class EditArticle(UpdateView):
#     model = Article
#     fields = ["title", "body"]
#     template_name = "articles/edit_article.html"


def DeleteArticle(request, pk):

    article = Article.objects.get(id=pk)
    if request.method == "POST":
        article.delete()
        return redirect("/")
    context = {"article": article}
    return render(request, "articles/delete_article.html", context)


# Class-Based View for training
# class DeleteArticle(DeleteView):
#     model = Article
#     template_name = "articles/delete_article.html"
#     success_url = reverse_lazy("/")


###################


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


def ChangePassword(request):
    return render(request, "registration/password_change_form.html")
