from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=15, widget=forms.TextInput(attrs={
        'class': 'input', 'placeholder': '用户名/邮箱'
    }))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '密码'
    }))

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username == password:
            raise forms.ValidationError('用户名与密码不能相同！')

        return password

class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='用户名', max_length=15, widget=forms.TextInput(attrs={
        'class': 'input', 'placeholder': '用户名/邮箱'
    }))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '密码'
    }))
    password1 = forms.CharField(label='再次输入密码', min_length=6, widget=forms.PasswordInput(attrs={
        'class': 'input', 'placeholder': '再次输入密码'
    }))

    class Meta:
        model = User
        fields = ('username', 'password')

    def clean_username(self):
        """验证用户是否存在"""

        username = self.cleaned_data.get('username')
        exists = User.objects.filter(username=username).exists()
        if exists:
            raise forms.ValidationError('用户名已经存在！')
        return username

    def clean_password1(self):
        """验证密码是否相等"""

        if self.cleaned_data['password'] != self.cleaned_data['password1']:
            raise forms.ValidationError('两次密码输入不一致！')
        return self.cleaned_data['password1']