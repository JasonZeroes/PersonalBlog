from django.db import models


# 创建一个基础的模型类,此模型类包含大部分表所需的字段,是提取的公共部分
class BaseModel(models.Model):
    # 准备每个表所需要的字段
    is_delete = models.BooleanField(default=False, verbose_name="是否删除")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")

    class Meta:
        # 将当前类设置为抽象类, 在执行迁移时,不会被迁移
        abstract = True
