from django.shortcuts import render,get_object_or_404,redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm



def post_comment(request,post_pk):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    # get_object_or_404用于报错返回一个404页面
    # 这个函数的作用是当获取的文章（Post）存在时，则获取；否则返回 404 页面给用户。
    post = get_object_or_404(Post,pk=post_pk)

    #当用户请求数据为POST类时将表单数据存储
    if request.method == 'POST':
        form = CommentForm(request.POST)

        #判断表单数据是否合法
        if form.is_valid():
            #commit=False表示仅把数据存进实例中而不是直接存进数据库中
            comment = form.save(commit=False)
            #将评论与文章关联起来
            comment.post = post
            #存入数据库
            comment.save()

            return redirect(post)

        else:
            #数据不合法，重新渲染详情页并且渲染表单
            #因为规定了post和comment的外键关系，所以可以用post.comment_set.all()方法查找某个文章下的全部评论
            #该方法类似于Comment.objects.filter(Post=post)
            comment_list = post.comment_set.all()
            context = {'post':post,
                       'form':form,
                       'comment_list':comment_list,}
            return render(request,'blog/detail.html',context=context)

    #如果不是POST请求，重定向到文章详情页
    return redirect(post)