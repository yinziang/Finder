#coding:utf-8

import datetime
import re
import markdown

from django import forms

from blog.models import Article

class ArticlePublishForm(forms.Form):
    title = forms.CharField(
        label = u'文章标题',
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control width:50%', 'placeholder':u'文章标题'}),
    )
    
    content = forms.CharField(
        label = u'内容',
        min_length=1,
        widget=forms.Textarea(),
    )
    
    tags = forms.CharField(
        label = u'标签',
        max_length=30,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':u'文章标签，以空格进行分隔'}),
    )
    
    def save(self, username, article=None):
        cd = self.cleaned_data
        title = cd['title']
        title_zh = title
        now = datetime.datetime.now()
        content_md = cd['content']
        content_html = markdown.markdown(cd['content'])
        re_title = '<h\d>(.+)</h\d>'
        data = content_html.split('\n')
        for line in data:
            title_info = re.findall(re_title, line)
            if title_info:
                title_zh = title_info[0]
                break
        url = '/article/%s' % (title)
        tags = cd['tags']
        if article:
            id_before = article.id
            created_before = article.created
            article.delete()
            article = Article(
                id = id_before,
                url = url,
                title = title,
                title_zh = title_zh,
                author = username,
                content_md = content_md,
                content_html = content_html,
                tags = tags,
                created = created_before,
                updated = now
            )
        else:
            article = Article(
                url=url,
                title=title,
                title_zh=title_zh,
                author=username,
                content_md=content_md,
                content_html=content_html,
                tags=tags,
                views=0,
                created=now,
                updated=now)
        article.save()  