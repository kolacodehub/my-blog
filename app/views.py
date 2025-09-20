from typing import Any
from django.db.models import QuerySet
from app.models import Article
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
import time

# Create your views here.

class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = "app/article_create.html"
    fields = ['title', 'status', 'content', 'twitter_post']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
         # Set the creator to the currently logged-in user
        form.instance.creator = self.request.user
        return super().form_valid(form)
    
class ArticleListView(LoginRequiredMixin, ListView):
    model = Article
    template_name = "app/home.html"
    context_object_name = 'articles'
    paginate_by = 5

    def get_queryset(self) -> QuerySet[Any]:
        time.sleep(2)
        search = self.request.GET.get('search')
        # Get articles created by the logged-in user
        query_set = super().get_queryset().filter(creator=self.request.user)
        # Show only articles created by the logged-in user
        if search:
            query_set = query_set.filter(title__search=search)
        return query_set.order_by('-created_at')

class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    template_name = "app/article_update.html"
    fields = ['title', 'status', 'content', 'twitter_post']
    success_url = reverse_lazy('home')
    context_object_name = 'articles'

    def test_func(self) -> bool:
         # Ensure that only the creator can update the article
        return self.request.user == self.get_object().creator #type:ignore

class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = "app/article_delete.html"
    success_url = reverse_lazy('home')
    context_object_name = 'articles'

    def test_func(self) -> bool:
         # Ensure that only the creator can update the article
        return self.request.user == self.get_object().creator #type:ignore
    
    def post(self, request, *args, **kwargs):
        # Add a message to confirm deletion
        messages.success(request, "Article deleted successfully.", extra_tags='destructive')
        return super().post(request, *args, **kwargs)
