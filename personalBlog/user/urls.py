from django.conf.urls import url

from user.views import UserRegister

urlpatterns = [
    url(r"^register/$", UserRegister.as_view(), name="用户注册")
]