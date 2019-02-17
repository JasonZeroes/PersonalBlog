from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from comments.forms import CommentsForm
from comments.helper import json_msg
from comments.models import CommentsModel
from db.base_view import VerifyLogin
from user.models import UserModel


# 创建一个类, 实现用户评论功能
class Comments(VerifyLogin):
    # 用户添加用户的评论到表中
    def post(self, request):
        # 接受参数
        data = request.POST
        data = dict(data)
        # 获取当前用户的id
        user_id = request.session.get('id')
        blog_id = int(data.get("blog_id")[0])
        # 判断该用户是否具备评价资格
        if UserModel.objects.get(pk=user_id).user_status != 1:
            return JsonResponse(json_msg(2, "您已经被禁言!7天后解除限制!"))

        # 判断评论id是否存在
        parent_id = int(data.get("parent_id")[0])
        # try:
        #     CommentsModel.objects.get(pk=parent_id)
        # except CommentsModel.DoesNotExist:
        #     return JsonResponse(json_msg(3, "回复的评论不存在!"))

        # 主要是对评论内容进行判断合法性
        content = data.get("content")
        content = ''.join(content)
        # 判断评论的长度够不够
        # 创建form对象, 验证评论内容的合法性
        data["content"] = content
        form = CommentsForm(data)
        # 判断数据的合法性
        if form.is_valid():
            # 数据合法的情况下
            # 将数据保存到数据库中
            CommentsModel.objects.create(
                content=content,
                parent_id=parent_id,
                user_id=user_id,
                blogarticle_id=blog_id
            )
            return JsonResponse(json_msg(0, "评论成功!", data=blog_id))
        else:
            return JsonResponse(json_msg(4, "评论字符少于5个!", data=blog_id))


# 创将一个类, 实现对评论的回复功能
class Reply(VerifyLogin):
    # 用户添加用户的评论到表中
    def post(self, request):
        # 接受参数
        data = request.POST
        data = dict(data)
        # 获取当前用户的id
        user_id = request.session.get('id')
        blog_id = int(data.get("blog_id")[0])
        # 判断该用户是否具备评价资格
        if UserModel.objects.get(pk=user_id).user_status != 1:
            return JsonResponse(json_msg(2, "您已经被禁言!7天后解除限制!"))

        # 判断评论id是否存在
        parent_id = int(data.get("parent_id")[0])
        try:
            CommentsModel.objects.get(pk=parent_id)
        except CommentsModel.DoesNotExist:
            return JsonResponse(json_msg(3, "回复的评论不存在!"))

        # 主要是对评论内容进行判断合法性
        content = data.get("reply")
        content = ''.join(content)
        # 判断评论的长度够不够
        # 创建form对象, 验证评论内容的合法性
        data["content"] = content
        form = CommentsForm(data)
        # 判断数据的合法性
        if form.is_valid():
            # 数据合法的情况下
            # 将数据保存到数据库中
            CommentsModel.objects.create(
                content=content,
                parent_id=parent_id,
                user_id=user_id,
                blogarticle_id=blog_id
            )
            return JsonResponse(json_msg(0, "回复成功!", data=blog_id))
        else:
            return JsonResponse(json_msg(4, "回复字符少于5个!", data=blog_id))

