from django.shortcuts import render
from .forms import UrlForm
from django.views.generic import FormView
from django.urls import reverse_lazy
import pyshorteners

            
class Urlgenerate(FormView):
    template_name = 'home.html'
    form_class = UrlForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        link = form.cleaned_data['link']
        try:
            s = pyshorteners.Shortener()
            self.success_url += f'?link={s.tinyurl.short(link)}'
        except Exception as e:
              self.success_url += f'?link=Give Valid Url'
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        link_param = self.request.GET.get('link')
        if link_param:
            context['link'] = link_param
        return context

