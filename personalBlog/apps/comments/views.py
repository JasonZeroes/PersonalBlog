from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from comments.helper import json_msg
from comments.models import CommentsModel
from db.base_view import VerifyLogin
from user.models import UserModel


# 创建一个类, 实现用户评论功能
class Comments(VerifyLogin):
    # 展示用户评论
    # def get(self, request):
    #     pass

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
            return JsonResponse(json_msg(1, "您已经被禁言!7天后解除限制!"))

        # 判断评论id是否存在
        parent_id = int(data.get("parent_id")[0])
        # try:
        #     CommentsModel.objects.get(pk=parent_id)
        # except CommentsModel.DoesNotExist:
        #     return JsonResponse(json_msg(2, "回复的评论不存在!"))

        # 判断评论的长度够不够
        content = ''.join(data.get("comment"))
        # if len(content) < 5:
        #     return JsonResponse(json_msg(3, "评论字符少于5个!"))
        # 将数据保存到数据库中
        CommentsModel.objects.create(
            content=content,
            parent_id=parent_id,
            user_id=user_id,
            blogarticle_id=blog_id
        )
        return JsonResponse(json_msg(0, "评论成功!"))
