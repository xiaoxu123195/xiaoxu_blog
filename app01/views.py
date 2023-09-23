from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from app01.utils.random_code import random_code
from django.contrib import auth
from django.db.models import F
from app01.utils.pagination import Pagination
from app01.models import Articles, Tags, Cover, Advert, Avatars, Moods, History, NavTags
from app01.utils.sub_comment import sub_comment_list


# 主页
def index(request):
    article_list = Articles.objects.filter(status=1).order_by('-change_date')
    frontend_list = article_list.filter(category=1)[:6]
    backend_list = article_list.filter(category=2)[:6]

    query_params = request.GET.copy()

    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=article_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=4,
        pager_page_count=7
    )
    article_list = article_list[pager.start:pager.end]

    advert_list = Advert.objects.filter(is_show=True)

    return render(request, "index.html", locals())


# 搜索
def search(request):
    search_key = request.GET.get('key', '')
    order = request.GET.get('order', '')
    tag = request.GET.get('tag', '')
    word = request.GET.getlist('word')
    query_params = request.GET.copy()
    article_list = Articles.objects.filter(title__contains=search_key)

    # 字数搜索
    if len(word) == 2:
        article_list = article_list.filter(word__range=word)

    if tag:
        article_list = article_list.filter(tag__title=tag)

    if order:
        try:
            article_list = article_list.order_by(order)
        except Exception:
            pass

    # 分页器

    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=article_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=10,
        pager_page_count=7
    )
    article_list = article_list[pager.start:pager.end]
    return render(request, 'search.html', locals())


# 文章
def article(request, nid):
    article_query = Articles.objects.filter(nid=nid)
    article_query.update(look_count=F('look_count') + 1)
    if not article_query:
        return redirect('/')
    articles = article_query.first()
    comment_list = sub_comment_list(nid)
    return render(request, 'article.html', locals())


# 新闻
def news(request):
    return render(request, "news.html", locals())


# 心情
def moods(request):
    # 查询所有头像
    avatar_list = Avatars.objects.all()
    # 查询所有心情
    mood_list = Moods.objects.all().order_by('-create_date')
    query_params = request.GET.copy()

    # 分页器
    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=mood_list.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=4,
        pager_page_count=7
    )
    mood_list = mood_list[pager.start:pager.end]
    return render(request, 'moods.html', locals())


# 回忆录
def history(request):
    history_list = History.objects.all().order_by('-create_date')
    return render(request, 'history.html', locals())


# 网站导航
def sites(request):
    # 取所有的标签
    tag_all = NavTags.objects.all()
    tag_list = tag_all.exclude(navs__isnull=True)

    return render(request, 'sites.html', locals())


@csrf_exempt
def login(request):
    return render(request, "login.html")


# 获取随机验证码
def get_random_code(request):
    data, valid_code = random_code()
    request.session['valid_code'] = valid_code
    return HttpResponse(data)


@csrf_exempt
def sign(request):
    return render(request, 'sign.html')


def logout(request):
    auth.logout(request)
    return redirect('/')


# 个人中心
def backend(request):
    if not request.user.username:
        # 判定没有登陆
        return redirect('/')
    # 拿到用户收藏的文章
    user = request.user
    collects_query = user.collects.all()

    return render(request, 'backend/backend.html', locals())


# 添加文章
def add_article(request):
    # 拿到所有的分类，标签
    tag_list = Tags.objects.all()
    # 拿到所有的文章封面
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            "url": cover.url.url,
            "nid": cover.nid
        })
    category_list = Articles.category_choice
    return render(request, 'backend/add_article.html', locals())


# 编辑头像
def edit_avatar(request):
    user = request.user
    sign_status = user.sign_status
    # 查询所有头像
    avatar_list = Avatars.objects.all()
    if sign_status == 0:
        # 用户名登录
        avatar_id = request.user.avatar.nid
    else:
        # qq或邮箱登录
        avatar_url = request.user.avatar_url
        for i in avatar_list:
            if i.url.url == avatar_url:
                avatar_id = i.nid
    return render(request, 'backend/edit_avatar.html', locals())


# 修改密码
def reset_password(request):
    return render(request, 'backend/reset_password.html', locals())


# 头像列表
def avatar_list(request):
    avatar_query = Avatars.objects.all()
    return render(request, 'backend/avatar_list.html', locals())


# 文章封面
def cover_list(request):
    cover_query = Cover.objects.all()
    return render(request, 'backend/cover_list.html', locals())


# 编辑文章
def edit_article(request, nid):
    article_obj = Articles.objects.get(nid=nid)
    tags = [str(tag.nid) for tag in article_obj.tag.all()]
    # 拿到所有的分类，标签
    tag_list = Tags.objects.all()
    # 拿到所有的文章封面
    cover_list = Cover.objects.all()
    c_l = []
    for cover in cover_list:
        c_l.append({
            "url": cover.url.url,
            "nid": cover.nid
        })
    category_list = Articles.category_choice
    return render(request, 'backend/edit_article.html', locals())


# 后台管理主页
def admin_home(request):
    return render(request, 'admin_home.html')
