from django.views import View
from django.http import JsonResponse
from django import forms
from api.views.login import clean_from
from app01.models import Comment, Articles
from django.db.models import F
from api.utils.find_root_comment import find_root_comment
from app01.utils.sub_comment import find_root_sub_comment


class CommentView(View):
    # 发布评论
    def post(self, request, nid):
        res = {
            'msg': '文章评论成功！',
            'code': 412,
            'self': None
        }
        data = request.data
        if not request.user.username:
            res['msg'] = '请登录'
            return JsonResponse(res)

        content = data.get('content')
        if not content:
            res['msg'] = '请输入文章内容'
            res['self'] = 'content'
            return JsonResponse(res)

        # 文章评论核验成功 pid是子评论的
        pid = data.get('pid')

        # 文章评论数加1
        Articles.objects.filter(nid=nid).update(comment_count=F('comment_count') + 1)

        if pid:
            # 有pid的话就不是根评论
            comment_obj = Comment.objects.create(
                content=content,
                user=request.user,
                article_id=nid,
                parent_comment_id=pid
            )
            # 根评论加1
            # 找最终的根评论
            root_comment_obj = find_root_comment(comment_obj)
            root_comment_obj.comment_count += 1
            root_comment_obj.save()
            # Comment.objects.filter(nid=pid).update(comment_count=F('comment_count') + 1)
        else:
            Comment.objects.create(
                content=content,
                user=request.user,
                article_id=nid
            )
        res['code'] = 0

        return JsonResponse(res)

    # 删除评论
    def delete(self, request, nid):
        # 自己发布的评论才能删除，或者是超级管理员
        res = {
            'msg': '评论删除成功',
            'code': 412
        }
        # 登录人
        login_user = request.user
        comment_query = Comment.objects.filter(nid=nid)
        # 评论人
        comment_user = comment_query.first().user

        aid = request.data.get('aid')
        # 子评论的最终根评论id
        pid = request.data.get('pid')
        print(aid, pid, nid)
        if not (login_user == comment_user or login_user.is_superuser):
            res['msg'] = '用户验证失败'
            return JsonResponse(res)
        # 文章评论数减1
        lis = []
        find_root_sub_comment(comment_query.first(), lis)
        Articles.objects.filter(nid=aid).update(comment_count=F('comment_count') - len(lis) - 1)

        if pid:
            Comment.objects.filter(nid=pid).update(comment_count=F('comment_count') - len(lis) - 1)

        comment_query.delete()
        res['code'] = 0
        return JsonResponse(res)


class CommentDiggView(View):
    def post(self, request, nid):
        # nid 是评论id
        res = {
            'msg': '点赞成功！',
            'code': 412,
            'data': 0,
        }
        if not request.user.username:
            res['msg'] = '请登录'
            return JsonResponse(res)
        Comment.objects.filter(nid=nid).update(digg_count=F('digg_count') + 1)

        digg_count = Comment.objects.filter(nid=nid).first().digg_count

        res['code'] = 0
        res['data'] = digg_count
        return JsonResponse(res)
