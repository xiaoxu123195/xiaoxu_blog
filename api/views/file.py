from django.views import View
from django.http import JsonResponse
from app01.models import Avatars, Cover, UserInfo
from django.core.files.uploadedfile import InMemoryUploadedFile
from app01.models import avatar_delete, cover_delete
from django.db.models import Q


class AvatarView(View):
    def post(self, request):
        res = {
            'code': 412,
            'msg': '文件上传不合法'
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        file: InMemoryUploadedFile = request.FILES.get('file')
        name: str = file.name
        white_file_type = [
            'jpg', 'jpeg', 'png'
        ]
        if name.split('.')[-1] not in white_file_type:
            return JsonResponse(res)
        kb = file.size / 1024 / 1024
        if kb > 2:
            res['msg'] = '图片大小超过2MB'
            return JsonResponse(res)
        Avatars.objects.create(url=file)
        res['code'] = 0
        res['msg'] = 'success'
        return JsonResponse(res)

    def delete(self, request, nid):
        res = {
            'code': 412,
            'msg': '图片删除成功'
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        avatar_query = Avatars.objects.filter(nid=nid)
        if not avatar_query:
            res['msg'] = '头像已被删除'
            return JsonResponse(res)
        # 判断图片是不是在使用
        obj: Avatars = avatar_query.first()
        userquery = UserInfo.objects.filter(Q(sign_status=1) | Q(sign_status=2))
        for user in userquery:
            if obj.url.url == user.avatar_url:
                res['msg'] = '该图片正在使用'
                return JsonResponse(res)
        avatar_delete(avatar_query.first())
        avatar_query.delete()

        res['code'] = 0
        return JsonResponse(res)


class CoverView(View):
    def post(self, request):
        res = {
            'code': 412,
            'msg': '文件上传不合法'
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        file: InMemoryUploadedFile = request.FILES.get('file')
        name: str = file.name
        white_file_type = [
            'jpg', 'jpeg', 'png'
        ]
        if name.split('.')[-1] not in white_file_type:
            return JsonResponse(res)
        kb = file.size / 1024 / 1024
        if kb > 2:
            res['msg'] = '图片大小超过2MB'
            return JsonResponse(res)
        Cover.objects.create(url=file)
        res['code'] = 0
        res['msg'] = 'success'
        return JsonResponse(res)

    def delete(self, request, nid):
        res = {
            'code': 412,
            'msg': '图片删除成功'
        }
        if not request.user.is_superuser:
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        cover_query = Cover.objects.filter(nid=nid)
        if not cover_query:
            res['msg'] = '图片已被删除'
            return JsonResponse(res)
        cover_delete(cover_query.first())
        cover_query.delete()

        res['code'] = 0
        return JsonResponse(res)
