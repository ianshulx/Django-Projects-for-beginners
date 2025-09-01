from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, ListView,
                                  TemplateView, UpdateView)

from .forms import TaskForm
from .models import Task

# Create your views here.


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "tasks/signup.html"
    success_url = reverse_lazy("login")


class HomeView(TemplateView):
    template_name = "tasks/home.html"


class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by("due_date")


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)

        messages.success(self.request, "Task created successfully.")
        return response


class TaskUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def test_func(self):
        task = self.get_object()
        return task.user == self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Task Updated successfully.")
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task_list")

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(request, f"Task '{obj.title}' deleted successfully.")
        return super().delete(request, *args, **kwargs)
