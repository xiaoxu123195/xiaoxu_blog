from django.views import View
from django.http import JsonResponse
from django import forms
from api.views.login import clean_from
from django.core.mail import send_mail
import random
from my_blog import settings
from django.core.handlers.wsgi import WSGIRequest


class EmailForm(forms.Form):
    email = forms.EmailField(error_messages={'required': '请输入邮箱', 'invalid': '请输入正确的邮箱'})


class ApiEmail(View):
    def post(self, request: WSGIRequest):
        res = {
            'code': 412,
            'msg': '验证码获取成功！',
            'self': None,
        }
        form = EmailForm(request.data)
        if not form.is_valid():
            res['msg'], res['self'] = clean_from(form)
            return JsonResponse(res)
        # 校验成功发送邮箱，设置超时时间
        valid_email_code = ''.join(random.sample('0123456789', 4))
        send_mail(
            '【xiaoxu博客】请完善的的信息',
            f'【xiaoxu博客】你现在正在绑定邮箱，邮箱验证码为 {valid_email_code}',
            settings.EMAIL_HOST_USER,
            [form.cleaned_data.get('email')],
            False)
        res['code'] = 0
        return JsonResponse(res)
