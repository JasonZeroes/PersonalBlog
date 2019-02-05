from django.conf.urls import url

from user.views import UserRegister, UserLoginView

urlpatterns = [
    url(r"^register/$", UserRegister.as_view(), name="用户注册"),
    url(r"^login/$", UserLoginView.as_view(), name="用户登录"),
]