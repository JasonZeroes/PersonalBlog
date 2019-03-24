from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from django.views import View

from comments.forms import CommentsForm
from comments.helper import json_msg
from db.base_view import VerifyLogin
from user.forms import UserRegisterForm, UserLoginModelForm, ResetPassWordForm
from user.helper import set_password, login, showhead, check_login
from user.models import UserModel, BoardModel


# 创建一个视图类,实现用户的注册功能
class UserRegister(View):
    # 用户以GET方式请求用户注册界面
    def get(self, request):
        return render(request, 'user/register.html')

    # 当用户以POST方式提交数据的时候执行此函数
    def post(self, request):
        # 1.接受参数
        data = request.POST
        # 2.验证参数的合法性
        # >>>>1.创建一个form表单验证的对象,来进行数据合法性的验证
        form = UserRegisterForm(data)
        if form.is_valid():
            # 在数据合法的情况下执行
            # 接受清洗后的数据
            # 1.<<<< 接收手机号码
            phone = form.cleaned_data.get("phone")
            # 2.<<<< 接收密码
            password = form.cleaned_data.get("password")
            # 3.将密码加密
            password = set_password(password)
            # 将接受的数据,保存到数据当中
            UserModel.objects.create(phone=phone, password=password)
            # 保存到数据库成功
            return redirect("user:用户登录")
        else:
            # 在数据不合法的情况下
            return render(request, 'user/register.html', {"form": form})


# 创建一个视图类, 实现用户的登录
class UserLoginView(View):
    # 当用户以GET方式请求,请求该页面时
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        # 接受用户提交的数据
        data = request.POST
        # 判断数据的合法性
        # 创建一个form验证对象
        form = UserLoginModelForm(data)
        # 判断数据的合法性
        if form.is_valid():
            # 在数据合法的情况下
            # 1.<<< 将回传数据的用户信息, 保存在session中
            user = form.cleaned_data.get("user")
            # 2.<<< 将用户信息保存到数据session中
            login(request, user)
            # 判断用户发起要求登录的网址是否存在
            referer = request.session.get("referer")
            # 判断referer是否存在
            if referer:
                return redirect(referer)
            else:
                return redirect('blog:博客首页')
        else:
            # 在数据合法的情况下
            return render(request, 'user/login.html', {"form": form})


# 定义一个类,完成用户重置密码的功能(前提要检查用户是否已经登录)
class ResetPassWord(View):
    # 展示重置密码界面
    def get(self, request):
        return render(request, 'user/resetpassword.html')

    def post(self, request):
        # 1.接受参数
        data = request.POST
        # 2.验证参数的合法性
        # >>>>1.创建一个form表单验证的对象,来进行数据合法性的验证
        form = ResetPassWordForm(data)
        if form.is_valid():
            # 在数据合法的情况下执行
            # 接受清洗后的数据
            # 1.<<<< 接收手机号码
            phone = form.cleaned_data.get("phone")
            # 2.<<<< 接收密码
            password = form.cleaned_data.get("password")
            # 3.将密码加密
            password = set_password(password)
            # 将接受的数据,保存到数据当中
            UserModel.objects.filter(phone=phone).update(password=password)
            # 保存到数据库成功
            return redirect("user:用户登录")
        else:
            # 在数据不合法的情况下
            return render(request, 'user/resetpassword.html', {"form": form})


# 定义一个类用户展示用户的个人中心
class PersonalCenter(VerifyLogin):
    def get(self, request):
        user_id = request.session.get("id")
        # 查询用户信息
        data = UserModel.objects.get(pk=user_id)
        # 准备参数
        context = {
            "data": data
        }
        return render(request, "user/personal.html", context=context)


# 定义一个类, 实现编辑个人信息
class EditPersoninfo(VerifyLogin):
    def get(self, request):
        user_id = request.session.get("id")
        # 查询用户信息
        data = UserModel.objects.get(pk=user_id)
        # 准备参数
        context = {
            "data": data
        }
        return render(request, "user/edit_personal.html", context=context)

    def post(self, request):
        # 接受参数
        data = request.POST
        # 接收头像参数
        head = request.FILES.get("head")
        # 获取用户的id
        user_id = request.session.get("id")
        user = UserModel.objects.get(pk=user_id)
        # 判断头像的数据合法性
        if head is not None:
            # 保存用户头像
            user.head = head
        user.save()
        user.sex = data.get("sex")
        user.nickname = data.get("nickname")
        user.phone = data.get("phone")
        user.save()
        return redirect("user:用户个人中心")


# 创建一个用户留言板
class Board(View):
    # 展示留言板
    def get(self, request):
        # 查询所有的留言
        boards = BoardModel.objects.filter(is_delete=False, parent=0)
        replies = BoardModel.objects.filter(is_delete=False)

        # 实现分页功能 Paginator
        paginator = Paginator(list(boards), 3)
        # 获取当前页面的页码
        page = request.GET.get("page", 1)
        # 获取对应页码的数据
        try:
            boards = paginator.page(page)
        except PageNotAnInteger:
            # 页码不是整数的时候, 显示第一页
            boards = paginator.page(1)
        except EmptyPage:
            # 页码为空的时候, 显示最后一页
            boards = paginator.page(paginator.num_pages)
        # 将留言传到前台
        context = {
            "boards": boards,
            "user": showhead(request),
            "replies": replies
        }
        return render(request, "board/board.html", context=context)

    def post(self, request):
        # 接受用户传来的数据
        data = request.POST
        data = dict(data)
        # 获取当前用户的id
        user_id = request.session.get("id")
        if user_id is None:
            return JsonResponse(json_msg(1, "您还未登录!"))
        # 判断用户的权限是否足够
        if UserModel.objects.get(pk=user_id).user_status != 1:
            return JsonResponse(json_msg(2, "您已经被禁言!7天后解除限制!"))
        # 获取留言的id
        parent_id = int(data.get("parent_id")[0])

        # 判断留言的合法性
        content = data.get("content")
        content = "".join(content)

        # 判断留言长度是否足够
        data["content"] = content
        # 创建form验证对象
        form = CommentsForm(data)
        # 判断
        if form.is_valid():
            # 数据合法  将数据保存到数据库
            BoardModel.objects.create(
                content=content,
                user_id=user_id,
                parent_id=parent_id
            )
            return JsonResponse(json_msg(0, "留言成功!"))
        else:
            # 数据不合法
            return JsonResponse(json_msg(3, "评论不能为空!"))


# 创建一个类实现留言回复
class Revert(VerifyLogin):
    # 展示留言板
    def get(self, request):
        # 查询所有的留言
        boards = BoardModel.objects.filter(is_delete=False, parent=0)
        replies = BoardModel.objects.filter(is_delete=False)

        # 实现分页功能 Paginator
        paginator = Paginator(list(boards), 3)
        # 获取当前页面的页码
        page = request.GET.get("page", 1)
        # 获取对应页码的数据
        try:
            boards = paginator.page(page)
        except PageNotAnInteger:
            # 页码不是整数的时候, 显示第一页
            boards = paginator.page(1)
        except EmptyPage:
            # 页码为空的时候, 显示最后一页
            boards = paginator.page(paginator.num_pages)

        # 将留言传到前台
        context = {
            "boards": boards,
            "user": showhead(request),
            "replies": replies
        }
        return render(request, "board/board.html", context=context)

    def post(self, request):
        # 接受参数
        data = request.POST
        data = dict(data)
        # 获取当前用户的id
        user_id = request.session.get('id')
        # 判断该用户是否具备评价资格
        if UserModel.objects.get(pk=user_id).user_status != 1:
            return JsonResponse(json_msg(2, "您已经被禁言!7天后解除限制!"))

        # 判断评论id是否存在
        parent_id = int(data.get("parent_id")[0])
        try:
            BoardModel.objects.get(pk=parent_id)
        except BoardModel.DoesNotExist:
            return JsonResponse(json_msg(3, "回复的留言不存在!"))

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
            BoardModel.objects.create(
                content=content,
                parent_id=parent_id,
                user_id=user_id,
            )
            return JsonResponse(json_msg(0, "回复成功!"))
        else:
            return JsonResponse(json_msg(4, "回复不能为空!"))

        # TODO  用户个人中心 搜索页的头像问题, 退出登录


# 创建一个类, 实现对用户个人登录信息的删除
class QuitLogin(VerifyLogin):
    def post(self, request):
        # 清除session中的登录信息
        request.session.flush()
        return JsonResponse(json_msg(0, "清除登录成功!"))
