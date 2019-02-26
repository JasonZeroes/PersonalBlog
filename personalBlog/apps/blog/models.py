from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from db.base_model import BaseModel


# 创建一个博客文章的分类模型
class BlogClassify(BaseModel):
    # 准备博客文章分类的字段
    class_name = models.CharField(max_length=100, verbose_name="博客文章分类名称")

    def __str__(self):
        return self.class_name

    class Meta:
        verbose_name = "博客文章分类管理"
        verbose_name_plural = verbose_name


# 创建一个博客文章的模型
class BlogArticle(BaseModel):
    # 准备博客文章所需的字段
    blog_title = models.CharField(max_length=200, verbose_name="博客标题")
    blog_brief = RichTextUploadingField(max_length=250, verbose_name="博客摘要")
    blog_content = RichTextUploadingField(verbose_name="博客内容")
    blog_img = models.ImageField(upload_to="blogarticle/%Y%m/%d", null=True, blank=True, verbose_name="博客图片地址")
    blog_status = models.SmallIntegerField(choices=((1, "0积分"),
                                                    (2, "20积分"),
                                                    (3, "30积分"),
                                                    (4, "50积分")), default=1, verbose_name="博客权限")
    blog_is_publish = models.BooleanField(choices=((True, "发表"),
                                                    (False, "未发表")), default=False, verbose_name="博客状态")
    blogclassify = models.ForeignKey(to="BlogClassify", verbose_name="博客分类id")
    blogtag = models.ManyToManyField(to="BlogTag", verbose_name="博客标签")
    blog_count = models.IntegerField(default=0, verbose_name="博客阅读量")

    def __str__(self):
        return self.blog_title

    class Meta:
        verbose_name = "博客文章管理"
        verbose_name_plural = verbose_name


# 创建一个博客的标签模型
class BlogTag(BaseModel):
    # 准备标签所需要的字段
    tag_name = models.CharField(max_length=100, verbose_name="标签名称")

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = "博客标签管理"
        verbose_name_plural = verbose_name


# 创建一个博客首页轮播模型
class Carousel(BaseModel):
    carousel_name = models.CharField(max_length=200, verbose_name="轮播名称")
    img_url = models.ImageField(upload_to="carousel/%Y%m/%d", verbose_name="轮播图片地址")
    order = models.SmallIntegerField(default=0, verbose_name="轮播图片排序")
    show_status = models.BooleanField(choices=((True, "显示"), (False, "不显示")), default=False)
    blogarticle = models.ForeignKey(to="BlogArticle", verbose_name="博客文章")

    def __str__(self):
        return self.carousel_name

    class Meta:
        verbose_name = "轮播管理"
        verbose_name_plural = verbose_name
