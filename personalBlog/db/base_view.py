from django.utils.decorators import method_decorator
from django.views import View
from user.helper import check_login


# 定义一个基础检验类, 如果继承该类, 就要检验用户是否要登录
class VerifyLogin(View):
    @method_decorator(check_login)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
