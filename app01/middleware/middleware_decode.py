import json

from django.utils.deprecation import MiddlewareMixin
from urllib.parse import parse_qs


class Md1(MiddlewareMixin):
    # 请求中间件
    def process_request(self, request):
        if request.method != 'GET' and request.META.get('CONTENT_TYPE') == 'application/json':
            # print(request.META.get('CONTENT_TYPE'))
            # data = request.body
            data = json.loads(request.body)
            # print(data)
            request.data = data
            # data_str = data.decode()
            # data_dict = parse_qs(data_str)
            # data_dict = {k: v[0] for k, v in data_dict.items()}
            # request.data = data_dict

    # 响应中间件
    def process_response(self, request, response):
        return response
