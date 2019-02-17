import hashlib

from django.http import JsonResponse
from django.shortcuts import redirect

from comments.helper import json_msg
from personalBlog.settings import SECRET_KEY


# 创建一个函数, 实现对粉丝用户提交的密码进行加密处理
def set_password(password):
    # 利用sha-256进行加密, 为进一步提高密码的安全性, 需要进行加盐处理
    # 将密码字符创循环10000次
    for _ in range(10000):
        password_str = "{}{}".format(password, SECRET_KEY)
        # 获取哈希对象
        h = hashlib.sha256(password_str.encode("utf-8"))
        # 将哈希对象转化为16进制的字符串
        password = h.hexdigest()
    # 将加密后的字符串返回
    return password


# 创建一个函数, 将用户的信息保存在session中
def login(request, user):
    # 从session中获取用户的id
    request.session["id"] = user.pk
    request.session["phone"] = user.phone
    # 设置浏览器的过期时间 7200秒
    request.session.set_expiry(7200)


# 创建一个函数, 实现检查用户的登录状态
def check_login(func):
    # 首先定义一个新的函数
    def verify_ligin(request, *args, **kwargs):
        # 验证session中是否有用户的登录信息
        if request.session.get('id') is None:
            # 将上次请求的地址保存到session中
            # 获得上次请求的referer地址值
            referer = request.META.get("HTTP_REFERER", None)
            # 判断上次请求的referer是否存在
            if referer:
                # 在存在的基础之下
                request.session["referer"] = referer
            # 判断请求是不是ajax请求
            if request.is_ajax():
                # 在用户地方为None, 且是ajax的请求的时候
                return JsonResponse(json_msg(1, "您还未登录!"))
            else:
                # 跳转到登录界面
                return redirect("user:用户登录")
        else:
            # 调用原函数
            return func(request, *args, **kwargs)
    # 返回新函数名
    return verify_ligin
