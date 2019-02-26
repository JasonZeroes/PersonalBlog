# 导入全文检索框架索引类
from haystack import indexes
from requests import request

from blog.models import BlogArticle
from user.helper import showhead


class BlogArticleIndex(indexes.SearchIndex, indexes.Indexable):
    # 设置需要检索的主要字段内容 索引字段在模板中指定
    text = indexes.CharField(document=True, use_template=True)

    # 获取检索对应对的模型类
    def get_model(self):
        return BlogArticle

    # 设置检索需要使用的查询集
    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        context = {
            "user": showhead(request)
        }
        data = self.get_model().objects.filter(is_delete=False)

        return self.get_model().objects.filter(is_delete=False)
