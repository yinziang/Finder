#coding:utf-8
from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F
from django.views.generic.list import ListView
from blog.models import Article
from datetime import datetime
from django.views.generic.edit import FormView
from forms import ArticlePublishForm

# Create your views here.
class ArticlePublishView(FormView):
    template_name = 'blog/article_publish.html'
    form_class = ArticlePublishForm
    # success_url = '/blog/'
    
    def form_valid(self, form):
        form.save(self.request.user.username)
        return super(ArticlePublishView, self).form_valid(form)  
    
    def get_success_url(self, **kwargs):
        username=self.request.user.username
        success_url = reverse('blog_home', args=(username,))
        return success_url
        

class ArticleEditView(FormView):
    template_name = 'blog/article_publish.html'
    form_class = ArticlePublishForm
    
    def get_initial(self, **kwargs):
        id = self.kwargs.get('id')
        try:
            self.article = Article.objects.get(id=id)
            if self.request.user.username==self.article.author:
                initial = {
                    'title': self.article.title,
                    'content': self.article.content_md,
                    'tags': self.article.tags,
                }
            else:
                raise Http404("您没有权限修改该文章!") 
            return initial
        except Article.DoesNotExist:
            raise Http404("文章不存在")
    
    def form_valid(self, form):
        form.save(self.request.user.username, self.article)
        return super(ArticleEditView, self).form_valid(form)
    
    def get_success_url(self, **kwargs):
        id = self.kwargs.get('id')
        success_url = reverse('blog_detail', args=(id,))
        return success_url
    

class ArticleListView(ListView):
    template_name = 'blog/home_all.html'
    
    def get_queryset(self, **kwargs):
        object_list = Article.objects.all()
        paginator = Paginator(object_list, 10)
        page = self.request.GET.get('page')
        try:
            object_list = paginator.page(page)
        except PageNotAnInteger:
            object_list = paginator.page(1)
        except EmptyPage:
            object_list = paginator.page(paginator.num_pages) 
        return object_list
        
def blog_home(request, username):
    object_list = Article.objects.filter(author=username)
    return render(request, 'blog/home.html', locals())
    
def detail(request, id):
    try:
        post = Article.objects.filter(id=str(id))
    except Article.DoesNotExist:
        raise Http404
    return render(request, 'blog/post.html', {'post': post})

def post_list(request):
    post_list = Article.objects.filter(author=request.user.username)
    return render(request, 'blog/post-list.html', locals())
    
def blog_del(request, id):
    blog = Article.objects.filter(id=id)
    blog.delete()
    post_list = Article.objects.filter(author=request.user.username)
    return render(request, 'blog/post-list.html', locals())

def tag_detail(request):
    tag_list = tag.objects.all().distinct()
    return render(request, 'blog/blog-sort.html', locals())