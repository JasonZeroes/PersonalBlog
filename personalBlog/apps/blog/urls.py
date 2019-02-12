from django.conf.urls import url

from blog.views import BlogIndexView, BlogDetailView, BlogListView

urlpatterns = [
    url(r"^index/$", BlogIndexView.as_view(), name="博客首页"),
    url(r"^detail/$", BlogDetailView.as_view(), name="博客详情"),
    url(r"^list/(?P<blogclassify_id>\d+)/$", BlogListView.as_view(), name="博客分类列表"),
]