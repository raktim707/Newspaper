from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, UpdateView, CreateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, render
from .models import Article, Comment
from .forms import CommentForm

class ArticleListView(ListView):
    model = Article
    template_name='article_list.html'

class ArticleDetailView(LoginRequiredMixin,DetailView):
    model = Article
    template_name='article_detail.html'
    login_url = 'login'

class ArticleCreateView(LoginRequiredMixin,CreateView):
    model = Article
    template_name='article_new.html'
    fields=('title', 'body',)
    login_url = 'login'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class ArticleUpdateView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Article
    fields = ('title', 'body',)
    template_name='article_edit.html'
    login_url = 'login'

    def test_func(self):
        obj = self.get_object()
        return obj.author == self.request.user

class ArticleDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Article
    template_name='article_delete.html'
    success_url=reverse_lazy('article_list')
    login_url = 'login'
    
    def test_func(self):
        obj=self.get_object()
        return obj.author==self.request.user

def CommentView(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        form =CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author= request.user
            comment.save()
            return redirect('article_detail', pk=article.pk)
    else:
        form = CommentForm()
    return render(request, 'comment_form.html', {'form' : form})