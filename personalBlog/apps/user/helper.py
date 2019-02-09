import hashlib

from django.shortcuts import redirect

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
            return redirect("user:用户登录")
        else:
            # 调用原函数
            return func(request, *args, **kwargs)

    # 返回新函数名
    return verify_ligin
