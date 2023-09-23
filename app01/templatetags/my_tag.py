from django import template

from app01.models import Tags, Menu
from app01.utils.search import Search
from django.utils.safestring import mark_safe

# 注册
register = template.Library()


# 自定义过滤器
# @register.filter
# def add1(item):
#     return int(item) + 1


@register.inclusion_tag('my_tag/headers.html')
def banner(menu_name, articles=None):

    if articles:
        # 说明是文章详情页
        cover = articles.cover.url.url
        img_list = [cover]
        return locals()

    # print(menu_name)
    menu_obj = Menu.objects.get(menu_title_en=menu_name)
    img_list = [i.url.url for i in menu_obj.menu_url.all()]
    menu_time = menu_obj.menu_time

    if not menu_obj.menu_rotation:
        # 不轮播
        img_list = img_list[0:1]
        menu_time = 0

    # img_list = [
    #     "http://127.0.0.1:8000/static/my/img/header/1678166508143.jpg",
    #     "http://127.0.0.1:8000/static/my/img/header/1678166508130.jpg",
    #     "http://127.0.0.1:8000/static/my/img/header/1678166508115.jpg",
    #     "http://127.0.0.1:8000/static/my/img/header/1678166508104.jpg",
    #     "http://127.0.0.1:8000/static/my/img/header/1678166508080.png",
    #     "http://127.0.0.1:8000/static/my/img/header/1678166508062.jpg",
    #     "http://127.0.0.1:8000/static/my/img/header/1678166508051.jpg",
    # ]

    return locals()


@register.simple_tag
def generate_order_html(request, key):
    order = request.GET.get(key, '')
    order_list = []
    if key == 'order':
        order_list = [
            ('-change_date', '综合排序'),
            ('-create_date', '最新发布'),
            ('-look_count', '最多浏览'),
            ('-digg_count', '最多点赞'),
            ('-collects_count', '最多收藏'),
            ('-comment_count', '最多评论')
        ]
    elif key == 'word':
        order = request.GET.getlist(key, '')
        order_list = [
            ([''], '全部字数'),
            (['0', '100'], '100字以内'),
            (['100', '500'], '500字以内'),
            (['500', '1000'], '1000字以内'),
            (['1000', '3000'], '3000字以内'),
            (['3000', '5000'], '5000字以内'),
            (['5000', '100000'], '5千字以上')
        ]
    elif key == 'tag':
        tag_list = Tags.objects.exclude(articles__isnull=True)
        order_list.append(('', '全部标签'))
        for tag in tag_list:
            order_list.append((tag.title, tag.title))
        # order_list = [
        #     ('', '全部标签'),
        #     ('python', 'python'),
        #     ('javascript', 'javascript'),
        #     ('django', 'django'),
        #     ('css', 'css'),
        #     ('爬虫', '爬虫')
        # ]
    query_params = request.GET.copy()
    order = Search(
        key=key,
        order=order,
        order_list=order_list,
        query_params=query_params
    )
    return mark_safe(order.order_html())


@register.simple_tag
def generate_drawing(drawing: str):
    if not drawing:
        return ''
    drawing = drawing.replace('；', ';').replace('\n', ';')
    drawing_list = drawing.split(';')
    html_s = ''
    for i in drawing_list:
        html_s += f'<img src="{i}" alt="">'

    return mark_safe(html_s)


@register.simple_tag
def generate_li(content: str):
    if not content:
        return ''
    drawing = content.replace('；', ';').replace('\n', ';')
    drawing_list = drawing.split(';')
    html_s = ''
    for i in drawing_list:
        html_s += f'<li>{i}</li>'

    return mark_safe(html_s)
