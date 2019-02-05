from django.conf.urls import url

from blog.views import BlogIndexView

urlpatterns = [
    url(r"^index/$", BlogIndexView.as_view(), name="博客首页"),
]