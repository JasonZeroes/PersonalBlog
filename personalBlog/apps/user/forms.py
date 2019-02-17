from django import forms

from user.helper import set_password
from user.models import UserModel


# 创建一个验证粉丝用户注册的Form类
class UserRegisterForm(forms.Form):
    # >>>>>>1.验证手机号码字段
    phone = forms.CharField(error_messages={
        "required": "手机号码必须填写!"
    })
    # >>>>>>2.验证用户输入的密码
    password = forms.CharField(min_length=8,
                               max_length=16,
                               error_messages={
                                   "required": "密码必须要填写!",
                                   "min_length": "密码至少8个字符!",
                                   "max_length": "密码最多16个字符!"
                               })
    # >>>>>>3.验证用户第二次输入的密码
    password2 = forms.CharField(error_messages={
        "required": "密码必须填写!"
    })

    # >>>>>>4.定义一个方法,验证手机号码是否已经被注册
    def clean_phone(self):
        # 获取用户提交的手机号码
        phone = self.cleaned_data.get("phone")
        # 到数据库进行查看,看该手机号码是否已经被注册
        flag = UserModel.objects.filter(phone=phone).exists()
        # 对返回的结果进行判断
        if flag:
            # 在查询结果为True的情况下,抛出异常,提示用户该手机号码已经被注册,请前往登录界面,或者更换手机号码
            raise forms.ValidationError('该手机号码已经被注册!请前往登录界面登录!或者更换手机号码注册!')
        else:
            # 在查询结果为False的情况下
            return phone

    # >>>>>>5.定义一个方法,验证用户两次输入的密码是否一致
    def clean(self):
        # 首先获取用户两次输入的密码
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        # 在两次密码都为真的情况下, 判断两次的密码是否一致
        if password and password2 and password != password2:
            # 在两次密码不为空且不相等的情况下 执行
            raise forms.ValidationError({"password2": "两次输入的密码不一致!"})
        else:
            # 在密码相等和密码不为空的情况下 执行
            return self.cleaned_data


# 创建一个验证粉丝用户登录的Form类
class UserLoginModelForm(forms.ModelForm):
    class Meta:
        # 关联模型类
        model = UserModel
        # 选择所需要的
        fields = ['phone', 'password']
        # 自定义错误信息
        error_messages = {
            "phone": {
                "required": "手机号码必填!"
            },
            "password": {
                "required": "密码必填!"
            }
        }

    # 综合校验, 判读用户输入的手机号码和密码是否正确
    def clean(self):
        # >>>>>1.先后去用户传过来的电话号码
        phone = self.cleaned_data.get('phone')
        # >>>>>2.先到数据库中查看是否有该手机号码
        try:
            user = UserModel.objects.get(phone=phone)
        except UserModel.DoesNotExist:
            raise forms.ValidationError({"phone": "该手机号码未注册,请输入已经注册手机号码!或者前往注册页面注册!"})
        # >>>>>3.在手机号码合法的情况下, 验证密码的合法性
        password = self.cleaned_data.get('password')
        # 将用户传过来的密码进行加密处理,才能和数据库中的数据进行判断
        password = set_password(password)
        if user.password != password:
            # 在密码不正确的情况下
            raise forms.ValidationError("密码错误!")
        else:
            # 在密码正确的情况下
            # 1.<<< 先将查询到的用户信息保存到session之中
            self.cleaned_data["user"] = user
            # 2.<<< 再将清洗后的数据返回
            return self.cleaned_data


# 创建一个验证用户重置密码的Form类
class ResetPassWordForm(forms.Form):
    # 首先验证手机号码是否填写
    phone = forms.CharField(error_messages={
        "required": "手机号码必须填写!"
    })
    # 验证用户输入的密码
    password = forms.CharField(min_length=8,
                               max_length=16,
                               error_messages={
                                   "required": "密码必须填写!",
                                   "min_length": "密码最少8个字符!",
                                   "max_length": "密码最长为16个字符!"
                               })
    password2 = forms.CharField(error_messages={
        "required": "密码必须填写!"
    })

    # 定义一个方法, 验证用户侧手机号码是否已经注册
    def clean_phone(self):
        # 获取用户传来的手机号码
        phone = self.cleaned_data.get("phone")
        # 到数据库查询此手机号码是否已经存在
        flag = UserModel.objects.filter(phone=phone).exists()
        # 对查询结果进行判断
        if flag == 0:
            # 没有查询到对应的手机号码
            raise forms.ValidationError("该手机号码还未注册!请前往注册页面进行注册!")
        else:
            # 查询到了手机号码
            return phone

    # 定义一个方法, 验证两次输入的密码是否一致
    def clean(self):
        # 首先获取两次输入的密码
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        # 判断两次的密码是否都为真, 且两次的密码一致
        if password and password2 and password != password2:
            # 在两次密码为真且不相等的情况下执行
            raise forms.ValidationError({"password2": "两次输入的密码不一致!"})
        else:
            # 两次密码为真,且相等的情况下执行
            return self.cleaned_data
