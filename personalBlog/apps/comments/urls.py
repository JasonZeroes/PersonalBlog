from django.conf.urls import url

from comments.views import Comments, Reply

urlpatterns = [
    url(r"^comments/$", Comments.as_view(), name="博客评论"),
    url(r"^reply/$", Reply.as_view(), name="博客评论回复"),
]
