# 解决新闻页面的请求问题
import requests
from django.views import View
from django.http import JsonResponse


url = 'https://api.codelife.cc/api/top/list'


class NewsView(View):
    def post(self, request):
        headers = request.headers
        try:
            res = requests.post(url, data=request.data, headers={
                'signaturekey': headers['Signaturekey']
            })
        except Exception:
            return {'code': '501', 'msg':'请求异常', 'data': []}

        return JsonResponse(res.json())
