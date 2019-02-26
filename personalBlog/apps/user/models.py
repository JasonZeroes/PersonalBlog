from django.core.validators import RegexValidator
from django.db import models

from db.base_model import BaseModel


# 创建一个用户的模型类
class UserModel(BaseModel):
    # 准备用户表所需要的字段
    phone = models.CharField(max_length=11,
                             validators=[
                                 RegexValidator(r"^1[3-9]\d{9}", "手机号码格式不正确!")
                             ],
                             verbose_name="用户手机号码")
    password = models.CharField(max_length=64, verbose_name="用户密码")
    nickname = models.CharField(max_length=100, default="莫言", verbose_name="用户昵称")
    sex = models.SmallIntegerField(choices=((1, "男"), (2, "女"), (3, "保密")), default=3, verbose_name="用户性别")
    user_status = models.SmallIntegerField(choices=((1, "正常"),
                                                    (2, "禁止评论"),
                                                    (3, "禁止登陆")),
                                           default=1, verbose_name="用户状态")

    user_integral = models.DecimalField(max_digits=9, decimal_places=2, default=1000, verbose_name="用户积分")

    user_buyblogarticle = models.ManyToManyField(to="blog.BlogArticle", verbose_name="用户购买博客文章")

    # intro = models.CharField(max_length=255, default="留下点你的个性再走呗!", verbose_name="用户个人简介")
    # # 添加一个用户头像的字段
    head = models.ImageField(upload_to="head/%Y%m/%d", default="head/avatar.jpg", verbose_name="用户头像")

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = "user"
        verbose_name = "用户管理"
        verbose_name_plural = verbose_name


# 创建一个用户留言的类
class BoardModel(BaseModel):
    content = models.TextField(verbose_name="留言内容")
    parent = models.ForeignKey(to="self", default=0, verbose_name="留言id")
    user = models.ForeignKey(to="user.UserModel", verbose_name="留言用户id")

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = "用户留言管理"
        verbose_name_plural = verbose_name
