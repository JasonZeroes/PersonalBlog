from django.shortcuts import render

from django.views import View


# 创建个人博客的主页
class BlogIndexView(View):
    # 当用户以GET的方式请求用户首页时
    def get(self, request):
        return render(request, "blog/index.html")

