from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import transaction

from django.shortcuts import render, redirect

from django.views import View

from blog.models import Carousel, BlogArticle, BlogClassify, BlogTag

from comments.models import CommentsModel

from user.models import UserModel

from django.shortcuts import render

from user.helper import showhead


# 创建个人博客的主页
class BlogIndexView(View):
    # 当用户以GET的方式请求用户首页时
    def get(self, request):
        # 1.查询博客的轮播图片
        carousels = Carousel.objects.filter(show_status=True)

        # 2.查询博客文章的标题和详情
        blogarticles = BlogArticle.objects.filter(is_delete=False, blog_is_publish=True).order_by("-create_time")[:10]
        # 查询用户的头像
        try:
            user_id = request.session.get("id")
            user = UserModel.objects.get(pk=user_id)
        except:
            user = None
        # 3.查询标签
        tags = BlogTag.objects.all()

        # 实现分页功能 Paginator
        paginator = Paginator(blogarticles, 4)
        # 获取当前页面的页码
        page = request.GET.get("page", 1)
        # 获取对应页码的数据
        try:
            blogarticles = paginator.page(page)
        except PageNotAnInteger:
            # 页码不是整数的时候, 显示第一页
            blogarticles = paginator.page(1)
        except EmptyPage:
            # 页码为空的时候, 显示最后一页
            blogarticles = paginator.page(paginator.num_pages)

        # 查询出所有推荐文章的数据
        data = BlogArticle.objects.filter(is_delete=False, blog_is_publish=True).order_by("-blog_count")[:5]

        # 准备参数
        context = {
            "carousels": carousels,
            "blogarticles": blogarticles,
            "data": data,
            "user": user,
            "tags": tags
        }

        return render(request, "blog/index.html", context=context)


# 博客的详情
class BlogDetailView(View):
    # 用户以GET方式请求
    def get(self, request):
        # 获取博客id
        blog_id = int(request.GET.get("blog_id"))

        # 根据博客文章的id, 查询出博客的详细信息.及博客的评论与回复
        # 设置一个保存点
        sid = transaction.savepoint()
        try:
            blogarticle = BlogArticle.objects.get(pk=blog_id)
            classify = BlogClassify.objects.get(pk=blogarticle.blogclassify_id)
            # TODO 运行后台报错
            comments = CommentsModel.objects.filter(blogarticle_id=blog_id, parent=0)
            replies = CommentsModel.objects.filter(blogarticle_id=blog_id)
            # comments = CommentsModel.objects.get_queryset().order_by('id')
            # 读者请求一次详情, 博客的阅读量就增加1
            blogarticle.blog_count += 1
        except:
            # 如果出现异常,数据回滚
            transaction.savepoint_rollback()
            return redirect("blog:博客首页")

        # 实现分页功能 Paginator
        paginator = Paginator(list(comments), 2)
        # 获取当前页面的页码
        page = request.GET.get("page", 1)
        # 获取对应页码的数据
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            # 页码不是整数的时候, 显示第一页
            comments = paginator.page(1)
        except EmptyPage:
            # 页码为空的时候, 显示最后一页
            comments = paginator.page(paginator.num_pages)

        # 准备参数
        context = {
            "blogarticle": blogarticle,
            "classify": classify,
            "comments": comments,
            "user": showhead(request),
            "replies": replies
        }
        # 在没有错误的情况下, 提交数据
        transaction.savepoint_commit(sid)
        blogarticle.save()
        return render(request, "blog/article_detail.html", context=context)


# 创建一个类, 实现对文章的分类展示
class BlogListView(View):
    # 展示对应分类的所有文章
    def get(self, request, blogclassify_id):
        # 根据分类的id, 查询出对应的所有文章
        try:
            classify = BlogClassify.objects.get(pk=blogclassify_id)
            blogarticles = classify.blogarticle_set.filter(is_delete=False)
        except:
            return redirect("blog:博客首页")

        # 实现分页功能 Paginator
        paginator = Paginator(list(blogarticles), 2)
        # 获取当前页面的页码
        page = request.GET.get("page", 1)
        # 获取对应页码的数据
        try:
            blogarticles = paginator.page(page)
        except PageNotAnInteger:
            # 页码不是整数的时候, 显示第一页
            blogarticles = paginator.page(1)
        except EmptyPage:
            # 页码为空的时候, 显示最后一页
            blogarticles = paginator.page(paginator.num_pages)

        # 准备参数
        context = {
            "blogarticles": blogarticles,
            "classify": classify,
            "user": showhead(request)
        }
        return render(request, 'blog/articles.html', context=context)


# 创建一个类,用于实现标签查找文章
class TagSearch(View):
    # 接受请求参数,查询对应标签的文章
    def get(self, request, tag):
        # 1.接收参数
        tag = int(tag)

        # 2.根据tag查询对应的tag_id
        tag = BlogTag.objects.get(pk=tag)
        # 3.根据标签查找对应的文章
        blogarticles = BlogArticle.objects.filter(is_delete=False, blog_is_publish=True, blogtag=tag).order_by(
            "-create_time")

        # 实现分页功能 Paginator
        paginator = Paginator(blogarticles, 2)
        # 获取当前页面的页码
        page = request.GET.get("page", 1)
        # 获取对应页码的数据
        try:
            blogarticles = paginator.page(page)
        except PageNotAnInteger:
            # 页码不是整数的时候, 显示第一页
            blogarticles = paginator.page(1)
        except EmptyPage:
            # 页码为空的时候, 显示最后一页
            blogarticles = paginator.page(paginator.num_pages)

        # 4.准备参数
        context = {
            "blogarticles": blogarticles,
            "tag": tag,
            "user": showhead(request)
        }
        return render(request, "blog/tag_search.html", context)
