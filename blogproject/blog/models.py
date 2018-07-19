# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


"""
在ORM(Object Relational Mapping 对象关系映射器)中
类对应表，属性对应列
本项目中共需3个表，文章(Post)、分类(Category)以及标签(Tag)
"""

class Category(models.Model):
    #django要求模型必须继承models.Model类
    #CharField指定了分类名name的属性类型，CharField是字符型
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(models.Model):
    #文章标题
    title = models.CharField(max_length=70)

    #文章正文
    text = models.TextField()

    #文章创建时间
    create_time = models.DateTimeField()

    #文章最后一次修改时间
    modified_time = models.DateTimeField()

    #文章摘要
    #blank=True表示可为空
    excerpt = models.CharField(max_length=200,blank=True)

    #规定一篇文章只能对应一个分类，一个分类下可以有多篇文章，使用ForeignKey，即一对多关系
    #规定一篇文章可以有多个标签，一个标签也可以对应多篇文章，使用ManyToManyField，表明多对多关系
    #规定文章可以没有标签
    category = models.ForeignKey(Category)
    tags =models.ManyToManyField(Tag, blank=True)

    #文章作者，这里User是从django.contrib.auth.models导入的
    #django.contrib.auth是django内置的应用，专门用于处理网站用户的注册、登录等流程，User是django已经写好的模型
    #规定一篇文章只能有一个作者，一个作者可以对应多篇文章，通过ForeignKey把文章和User关联起来
    author = models.ForeignKey(User)

    def __str__(self):
        return self.title

    #自定义 get_absolute_url方法用于生成详情页面的url
    def get_absolute_url(self):
        #reverse的第一个参数表示blog应用下的name=detail的函数
        #detail函数对应的规则是 post/(?P<pk>[0-9]+)/ 这个正则表达式
        #正则表达式部分会被后面传入的参数pk替换
        #如pk是123的话该函数返回/post/123/
        return reverse('blog:detail',kwargs={'pk':self.pk})
        