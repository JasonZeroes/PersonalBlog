from django.contrib import admin

# Register your models here.
from comments.models import CommentsModel

admin.site.register(CommentsModel)