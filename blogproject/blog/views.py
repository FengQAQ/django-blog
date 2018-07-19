import markdown
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .models import Post,Category
from comments.forms import CommentForm

#博客首页
def index(request):
    post_list = Post.objects.all().order_by('-create_time')
    #order_by：根据create_time排序，-号表示逆序

    return render(request,'blog/index.html',context={'post_list':post_list})



#文章详情页
def detail(request,pk):
    #get_object_or_404方法默认调用django的get方法，如果查询对象不存在会抛出一个404异常
    post = get_object_or_404(Post,pk=pk)
    post.text = markdown.markdown(post.text,
                                    extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',#语法高亮
                                        'markdown.extensions.toc',#自动生成目录
                                        'markdown.extensions.tables',#表格处理
                                    ])
    form = CommentForm()
    #获取这篇文章下的全部评论
    comment_list = post.comment_set.all()
    #获取评论数量
    comment_num = post.comment_set.count()
    context={'post':post,
             'form':form,
             'comment_list':comment_list,
             'comment_num':comment_num,}
    return render(request,'blog/detail.html',context=context)

#归档视图
def archives(request, year, month):
    post_list = Post.objects.filter(create_time__year=year,
                                    ).order_by('-create_time')
                                        #精确到月份时会出现查询不到数据的问题，大致是由于Mysql时区设置问题，目前尚未解决
                                        # filter(create_time__month=month,
                                        #      ).order_by('-create_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})

#分类视图
def category(request,pk):
    cate=get_object_or_404(Category,pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-create_time')
    return render(request,'blog/index.html',context={'post_list':post_list})