#coding:utf-8
from django.conf.urls import patterns, include, url 
from blog.views import ArticlePublishView, ArticleListView, ArticleEditView

urlpatterns = patterns('blog.views',
    url(r'^$', ArticleListView.as_view(), name='blog_index'),
    url(r'^(?P<id>\d+)/$', 'detail', name='blog_detail'),
    url(r'^(?P<id>\d+)/edit$', ArticleEditView.as_view(), name='blog_edit'),
    url(r'^user/(?P<username>\w+)/$', 'blog_home', name='blog_home' ),
    url(r'^article/publish$', ArticlePublishView.as_view(), name="article_publish"),
    url(r'^post/list/$', 'post_list', name="post_list"),
    url(r'^del/(?P<id>\d+)/$', 'blog_del', name='blog_del'),
    
)
