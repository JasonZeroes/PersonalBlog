# 自定义添加搜索内容
from haystack.generic_views import SearchView
from requests import request

from user.helper import showhead


class MySearch(SearchView):
    def get_queryset(self):
        queryset = super(MySearch, self).get_queryset()
        # further filter queryset based on some set of criteria
        return queryset.filter(is_delete=False)

    def get_context_data(self, *args, **kwargs):
        context = super(MySearch, self).get_context_data(*args, **kwargs)
        # do something
        context["user"] = showhead(request)

        return context
