from django.db import models
from db.base_model import BaseModel



# 创建一个用户评论的模型
class CommentsModel(BaseModel):
    content = models.TextField(verbose_name="评论内容")
    parent = models.ForeignKey(to="self", default=0, verbose_name="评论的id")
    user = models.ForeignKey(to="user.UserModel", verbose_name="用户id")
    blogarticle = models.ForeignKey(to="blog.BlogArticle", verbose_name="博客文章id")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "博客评论管理"
        verbose_name_plural = verbose_name

