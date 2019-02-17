from django.core.paginator import Paginator, PageNotAnInteger
from django.shortcuts import render, redirect

from django.views import View
from blog.models import Carousel, BlogArticle, BlogClassify

from comments.models import CommentsModel


# 创建个人博客的主页
class BlogIndexView(View):
    # 当用户以GET的方式请求用户首页时
    def get(self, request):
        # 1.查询博客的轮播图片
        carousels = Carousel.objects.filter(show_status=True)

        # 2.查询博客文章的标题和详情
        blogarticles = BlogArticle.objects.filter(is_delete=False, blog_is_publish=True).order_by("-create_time")

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
    def get(self, request):
        # 获取博客id
        blog_id = int(request.GET.get("blog_id"))

        # 根据博客文章的id, 查询出博客的详细信息.及博客的评论与回复
        try:
            blogarticle = BlogArticle.objects.get(pk=blog_id)
            classify = BlogClassify.objects.get(pk=blogarticle.blogclassify_id)
            comments = CommentsModel.objects.filter(blogarticle_id=blog_id)
        except:
            return redirect("blog:博客首页")

        # 实现分页功能 Paginator
        paginator = Paginator(comments, 10)
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
            "comments": comments
        }
        return render(request, "blog/article_detail.html", context=context)

    # def post(self, request, blog_id):
    #     # 接受参数
    #     data = request.POST
    #     data = dict(data)
    #     # 获取当前用户的id
    #     user_id = request.session.get('id')
    #     blog_id = int(data.get("blog_id")[0])
    #     # 判断该用户是否具备评价资格
    #     if UserModel.objects.get(pk=user_id).user_status != 1:
    #         return JsonResponse(json_msg(1, "您已经被禁言!7天后解除限制!"))
    #
    #     # 判断评论id是否存在
    #     parent_id = int(data.get("parent_id")[0])
    #     # try:
    #     #     CommentsModel.objects.get(pk=parent_id)
    #     # except CommentsModel.DoesNotExist:
    #     #     return JsonResponse(json_msg(2, "回复的评论不存在!"))
    #
    #     # 判断评论的长度够不够
    #     content = ''.join(data.get("comment"))
    #     # if len(content) < 5:
    #     #     return JsonResponse(json_msg(3, "评论字符少于5个!"))
    #     # 将数据保存到数据库中
    #     CommentsModel.objects.create(
    #         content=content,
    #         parent_id=parent_id,
    #         user_id=user_id,
    #         blogarticle_id=blog_id
    #     )
    #     return JsonResponse(json_msg(0, '评论成功!', data=blog_id))


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

        # 准备参数
        context = {
            "blogarticles": blogarticles,
            "classify": classify
        }
        return render(request, 'blog/articles.html', context=context)
