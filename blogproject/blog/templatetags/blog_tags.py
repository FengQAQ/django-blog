from django import template
from ..models import Post,Category


#实例化一个template.Library类，并将函数get_recent_posts装饰为register.simple_tag,
# 这样就可以在模板中使用语法{% get_recent_posts %}调用这个函数了
register = template.Library()

#最新文章
@register.simple_tag
def get_recent_posts(num=5):
    return Post.objects.all().order_by('-create_time')[:num]

#归档
@register.simple_tag
def archives():
    return Post.objects.dates('create_time','month',order='DESC')#返回创建时间，精确到月，降序排列

#分类
@register.simple_tag
def get_categories():
    return Category.objects.all()