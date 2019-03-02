from django.conf.urls import url

from user.views import UserRegister, UserLoginView, ResetPassWord, PersonalCenter, EditPersoninfo, Board, Revert, \
    QuitLogin

urlpatterns = [
    url(r"^register/$", UserRegister.as_view(), name="用户注册"),
    url(r"^login/$", UserLoginView.as_view(), name="用户登录"),
    url(r"^resetpassword/$", ResetPassWord.as_view(), name="用户重置密码"),
    url(r"^personal/$", PersonalCenter.as_view(), name="用户个人中心"),
    url(r"^edit/$", EditPersoninfo.as_view(), name="用户编辑个人信息"),
    url(r"^board/$", Board.as_view(), name="用户留言"),
    url(r"^revert/$", Revert.as_view(), name="用户留言回复"),
    url(r"^quit/$", QuitLogin.as_view(), name="用户退出登录"),
]