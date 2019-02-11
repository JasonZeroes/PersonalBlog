from django.conf.urls import url

from comments.views import Comments

urlpatterns = [
    url(r"^comments/$", Comments.as_view(), name="博客评论"),
]
