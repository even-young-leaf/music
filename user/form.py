# user的form.py
from django.contrib.auth.forms import UserCreationForm
from .models import MyUser
from django import forms

# 定义模型 MyUser 的数据表单
class MyUserCreationForm(UserCreationForm):
    # 重写初始化方法
    # 设置自定义字段 password1 和 password2 的样式和属性
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput(
            attrs={'class': 'txt tabinput',
                   'placeholder': '密码, 4-16位数字/字母/符号(空格除外)'})
        self.fields['password2'].widget = forms.PasswordInput(
            attrs={'class': 'txt tabinput', 'placeholder': '重复密码'})

    class Meta(UserCreationForm.Meta):
        model = MyUser
        # 在注册页面添加模型字段：手机号码和密码
        fields = UserCreationForm.Meta.fields + ('mobile',)
        # 设置模型字段的样式和属性
        widgets = {
            'mobile': forms.widgets.TextInput(
                attrs={'class': 'txt tabinput', 'placeholder': '手机号'}),
            'username': forms.widgets.TextInput(
                attrs={'class': 'txt tabinput', 'placeholder': '用户名'}),
         }