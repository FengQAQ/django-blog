from django.db import models

#构建评论数据库模型
class Comment(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255)
    url = models.URLField()
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('blog.Post')

    #返回最新的20条评论
    def __str__(self):
        return self.text[:20]