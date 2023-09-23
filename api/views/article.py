import random

from django.views import View
from django import forms
from django.http import JsonResponse
from markdown import markdown
from pyquery import PyQuery
from django.db.models import F

from api.views.login import clean_from
from app01.models import Tags, Articles, Cover


class AddArticleForm(forms.Form):
    title = forms.CharField(error_messages={'required': '请输入文章标题'})
    content = forms.CharField(error_messages={'required': '请输入文章内容'})
    abstract = forms.CharField(required=False)  # 不进行为空的验证
    cover_id = forms.IntegerField(required=False)
    category = forms.IntegerField(required=False)
    pwd = forms.CharField(required=False)
    recommend = forms.BooleanField(required=False)
    status = forms.IntegerField(required=False)

    # 文章简介
    def clean_abstract(self):
        abstract = self.cleaned_data['abstract']
        if abstract:
            return abstract
        # 截取正文的前30个字符
        content = self.cleaned_data['content']
        if content:
            # 将获取的文本解析为html格式
            doc = markdown(content)
            # 将html格式中间的文本提取出来,并获取前30个字符
            abstract = PyQuery(doc).text()[:30]
        return abstract

    # 文章封面
    def clean_cover_id(self):
        cover_id = self.cleaned_data['cover_id']
        if cover_id:
            return cover_id
        cover_set = Cover.objects.all().values('nid')
        cover_id = random.choice(cover_set)['nid']
        return cover_id

    # 文章分类
    def clean_category(self):
        category = self.cleaned_data['category']
        if category:
            return category
        self.cleaned_data.pop('category')

    # 文章密码
    def clean_pwd(self):
        pwd = self.cleaned_data['pwd']
        if pwd:
            return pwd
        self.cleaned_data.pop('pwd')


class ArticleView(View):
    # 发布文章
    def post(self, request):
        res = {
            'msg': '文章发布成功!',
            'code': 412,
            'data': None,
        }
        data = request.data
        data['status'] = 1
        form = AddArticleForm(data)
        if not form.is_valid():
            # 验证不通过
            res['msg'], res['self'] = clean_from(form)
            return JsonResponse(res)
        # 校验通过
        form.cleaned_data['author'] = "小徐"
        form.cleaned_data['source'] = "小徐个人博客"
        article_obj = Articles.objects.create(**form.cleaned_data)
        tags = data.get('tags')
        for tag in tags:
            tag_query = Tags.objects.filter(nid=tag)
            if tag_query:
                # 存在的
                article_obj.tag.add(tag)
            else:
                # 先创建 再多对多关联
                tag_obj = Tags.objects.create(title=tag)
                article_obj.tag.add(tag_obj.nid)
        res['code'] = 0
        res['data'] = article_obj.nid
        return JsonResponse(res)

    # 编辑文章
    def put(self, request, nid):
        res = {
            'msg': '文章编辑成功!',
            'code': 412,
            'data': None,
        }
        article_query = Articles.objects.filter(nid=nid)
        if not article_query:
            res['msg'] = '请求错误！'
            return JsonResponse(res)
        data = request.data
        data['status'] = 1
        form = AddArticleForm(data)
        if not form.is_valid():
            # 验证不通过
            res['msg'], res['self'] = clean_from(form)
            return JsonResponse(res)
        # 校验通过
        form.cleaned_data['author'] = "小徐"
        form.cleaned_data['source'] = "小徐个人博客"
        article_query.update(**form.cleaned_data)
        tags = data.get('tags')
        # 清空标签 再从新添加
        article_query.first().tag.clear()
        for tag in tags:
            tag_query = Tags.objects.filter(nid=tag)
            if tag_query:
                # 存在的
                article_query.first().tag.add(tag)
            else:
                # 先创建 再多对多关联
                tag_obj = Tags.objects.create(title=tag)
                article_query.first().tag.add(tag_obj.nid)
        res['code'] = 0
        res['data'] = article_query.first().nid
        return JsonResponse(res)


# 文章
# class ArticleView(View):
#     # 发布文章
#     def post(self, request):
#         res = {
#             'msg': '文章发布成功!',
#             'code': 412,
#             'data': None,
#         }
#         print(request.headers['Content-Type'])
#         data: dict = request.data
#         title = data.get('title')
#         if not title:
#             res['msg'] = '请输入文章标题'
#             return JsonResponse(res)
#
#         # recommend = data.get('recommend').title()
#         recommend = data.get('recommend')
#
#         content = data.get('content')
#         if not content:
#             res['msg'] = '请输入文章内容'
#             return JsonResponse(res)
#
#         extra = {
#             'title': title,
#             'content': content,
#             'recommend': recommend,
#             'status': 1,
#         }
#
#         abstract = data.get('abstract')
#         if not abstract:
#             # 将获取的文本解析为html格式
#             doc = markdown(content)
#             # 将html格式中间的文本提取出来,并获取前30个字符
#             abstract = PyQuery(doc).text()[:30]
#         extra['abstract'] = abstract
#
#         category = data.get('category_id')
#         if category:
#             extra['category'] = category
#
#         cover_id = data.get('cover_id')
#         if cover_id:
#             extra['cover_id'] = cover_id
#         else:
#             extra['cover_id'] = 1
#
#         pwd = data.get('pwd')
#         if pwd:
#             extra['pwd'] = pwd
#
#         # 添加文章
#         # article_obj = Articles.objects.create(**extra)
#         # 标签
#         tags = data.get('tags')
#         print(tags)
#         # if tags:
#         #     for tag in tags:
#         #         if not tag.isdigit():
#         #             tag_obj = Tags.objects.create(title=tag)
#         #             article_obj.tag.add(tag_obj)
#         #         else:
#         #             article_obj.tag.add(tag)
#         #
#         # res['code'] = 0
#         # res['data'] = article_obj.nid
#
#         return JsonResponse(res)

# 文章点赞
class ArticlesDiggView(View):
    def post(self, request, nid):
        # nid 是评论id
        res = {
            'msg': '点赞成功！',
            'code': 412,
            'data': 0,
        }
        comment_query = Articles.objects.filter(nid=nid)
        comment_query.update(digg_count=F('digg_count') + 1)

        digg_count = comment_query.first().digg_count

        res['code'] = 0
        res['data'] = digg_count
        return JsonResponse(res)


# 文章收藏
class ArticleCollectorView(View):
    def post(self, request, nid):
        # 判断登录
        # 同样的请求，收藏变取消
        res = {
            'msg': '文章收藏成功！',
            'code': 412,
            'isCollects': True,
            'data': 0
        }
        if not request.user.username:
            res['msg'] = '请登录'
            return JsonResponse(res)
        # 判断用户是否收藏文章了
        flag = request.user.collects.filter(nid=nid)
        num = 1
        res['code'] = 0
        if flag:
            # 用户已经收藏过了，取消收藏
            res['msg'] = '文章取消收藏成功！'
            res['isCollects'] = False
            request.user.collects.remove(nid)
            num = -1
        else:
            request.user.collects.add(nid)

        article_query = Articles.objects.filter(nid=nid)
        article_query.update(collects_count=F('collects_count') + num)
        collects_count = article_query.first().collects_count
        res['data'] = collects_count
        return JsonResponse(res)
