from django.shortcuts import render, redirect

from django.views import View
from blog.models import Carousel, BlogArticle, BlogClassify


# 创建个人博客的主页
class BlogIndexView(View):
    # 当用户以GET的方式请求用户首页时
    def get(self, request):
        # 1.查询博客的轮播图片
        carousels = Carousel.objects.filter(show_status=True)

        # 2.查询博客文章的标题和详情
        blogarticles = BlogArticle.objects.filter(is_delete=False, blog_is_publish=True).order_by("-create_time")

        # 查询出所有文章分类
        data = BlogClassify.objects.filter(is_delete=False)

        # 准备参数
        context = {
            "carousels": carousels,
            "blogarticles": blogarticles,
            "data": data
        }

        return render(request, "blog/index.html", context=context)


# 博客的详情
class BlogDetailView(View):
    # 用户以GET方式请求
    def get(self, request, blog_id):
        # 根据博客文章的id, 查询出博客的详细信息.
        try:
            blogarticle = BlogArticle.objects.get(pk=blog_id)
        except:
            return redirect("blog:博客首页")
        # 准备参数
        context = {
            "blogarticle": blogarticle
        }
        return render(request, "blog/article_detail.html", context=context)


# 创建一个类, 实现对文章的分类展示
class BlogListView(View):
    # 展示对应分类的所有文章
    def get(self, request, blogclassify_id):
        # 根据分类的id, 查询出对应的所有文章
        try:
            classify = BlogClassify.objects.get(pk=blogclassify_id)
            blogarticles = classify.blogarticle_set.all()

        except:
            return redirect("blog:博客首页")
        # 准备参数
        context = {
            "blogarticles": blogarticles,
        }
        return render(request, 'blog/articles.html', context=context)
