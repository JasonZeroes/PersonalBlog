from django.contrib import admin

from blog.models import BlogClassify, BlogArticle, BlogTag, Carousel

admin.site.register(BlogClassify)
admin.site.register(BlogArticle)
admin.site.register(BlogTag)
admin.site.register(Carousel)

