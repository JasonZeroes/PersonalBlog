from django import forms


# 创建一个用户提交的评价内容验证Form类
class CommentsForm(forms.Form):
    content = forms.CharField(min_length=5,
                              error_messages={
                                  "required": "评论内容必填!",
                                  "min_length": "最短长度为5个字符!"
                              })
