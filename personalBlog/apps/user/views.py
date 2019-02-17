from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.views import View

from db.base_view import VerifyLogin
from user.forms import UserRegisterForm, UserLoginModelForm, ResetPassWordForm
from user.helper import set_password, login
from user.models import UserModel


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
        return render(request, "user/personal.html")


# 定义一个类, 实现编辑个人信息
class EditPersoninfo(VerifyLogin):
    def get(self, request):
        return render(request, "user/edit_personal.html")
