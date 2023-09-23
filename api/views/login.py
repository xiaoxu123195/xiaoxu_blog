from django import forms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from app01.models import UserInfo, Avatars
from django.contrib import auth
from django.views import View
import random


class LoginBaseForm(forms.Form):
    # 重写init方法
    def __init__(self, request=None, *args, **kwargs):
        # 做自己想做的事情
        self.request = request
        super().__init__(*args, **kwargs)

    # 局部钩子
    def clean_code(self):
        code: str = self.cleaned_data.get('code')
        valid_code: str = self.request.session.get('valid_code')
        if code.upper() != valid_code.upper():
            self.add_error('code', '验证码输入错误！')
        return code


# 登录的字段验证
class LoginForm(LoginBaseForm):
    name = forms.CharField(error_messages={'required': '请输入用户名'})
    pwd = forms.CharField(error_messages={'required': '请输入密码'})
    code = forms.CharField(error_messages={'required': '请输入验证码'})

    # 全局钩子
    def clean(self):
        name = self.cleaned_data.get('name')
        pwd = self.cleaned_data.get('pwd')
        user = auth.authenticate(username=name, password=pwd)
        if not user:
            self.add_error('pwd', '用户名或密码错误')
            return self.cleaned_data
        # 把用户对象放到cleaned_data中
        self.cleaned_data['user'] = user
        return self.cleaned_data


# 注册的字段验证
class SignForm(LoginBaseForm):
    name = forms.CharField(error_messages={'required': '请输入用户名'})
    pwd = forms.CharField(error_messages={'required': '请输入密码'})
    re_pwd = forms.CharField(error_messages={'required': '请输入确认密码'})
    code = forms.CharField(error_messages={'required': '请输入验证码'})

    def clean(self):
        pwd = self.cleaned_data.get('pwd')
        re_pwd = self.cleaned_data.get('re_pwd')
        if pwd != re_pwd:
            self.add_error('re_pwd', '两次密码不一致')
        return self.cleaned_data

    def clean_name(self):
        name = self.cleaned_data.get('name')
        user_query = UserInfo.objects.filter(username=name)
        if user_query:
            self.add_error('name', '该用户已注册')
        return name


# 登陆失败的可复用代码
def clean_from(form):
    err_dict: dict = form.errors
    # 拿到所有错误的字段名称
    err_valid = list(err_dict.keys())[0]
    # 拿到第一个字段的第一个错误信息
    err_msg = err_dict[err_valid][0]
    return err_msg, err_valid


# CBV
class LoginView(View):
    @csrf_exempt
    def post(self, request):
        res = {
            'code': 425,
            'msg': "登录成功!",
            'self': None
        }
        data = request.data
        form = LoginForm(request=request, data=data)
        if not form.is_valid():
            # 验证不通过
            res['msg'], res['self'] = clean_from(form)
            return JsonResponse(res)
        # 写登陆操作
        user = form.cleaned_data.get('user')
        # 登陆操作
        auth.login(request, user)
        res['code'] = 0
        return JsonResponse(res)


class SignView(View):
    @csrf_exempt
    def post(self, request):
        res = {
            'code': 425,
            'msg': "注册成功!",
            'self': None
        }
        data = request.data
        form = SignForm(request=request, data=data)
        if not form.is_valid():
            # 验证不通过
            res['msg'], res['self'] = clean_from(form)
            return JsonResponse(res)
        # 写注册操作 注册成功 create_user/create_superuser
        user = UserInfo.objects.create_user(
            username=request.data.get('name'),
            password=request.data.get('pwd')
        )
        # 随机为用户选择一个头像
        avatar_list = [i.nid for i in Avatars.objects.all()]
        user.avatar_id = random.choice(avatar_list)
        user.save()
        # 注册之后直接登录
        auth.login(request, user)
        res['code'] = 0
        return JsonResponse(res)
