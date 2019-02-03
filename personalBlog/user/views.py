from django.shortcuts import render


from django.views import View


# 创建一个视图类,实现用户的注册功能
class UserRegister(View):
    # 用户以GET方式请求用户注册界面
    def get(self, request):
        return render('')
