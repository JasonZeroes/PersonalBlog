from django.shortcuts import render

from django.views import View
from blog.models import Carousel, BlogArticle


# 创建个人博客的主页
class BlogIndexView(View):
    # 当用户以GET的方式请求用户首页时
    def get(self, request):
        # 1.查询博客的轮播图片
        carousels = Carousel.objects.filter(show_status=True)

        # 2.查询博客文章的标题和详情
        blogarticles = BlogArticle.objects.filter(is_delete=False, blog_is_publish=True).order_by("-create_time")

        # 准备参数
        context = {
            "carousels": carousels,
            "blogarticles": blogarticles
        }

        return render(request, "blog/index.html", context=context)

