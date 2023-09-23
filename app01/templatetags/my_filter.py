from django import template
import datetime
import pendulum
from app01.models import Avatars, Cover
from django.utils.safestring import mark_safe

# 注册
register = template.Library()


# 用户是否收藏了文章
@register.filter
def is_user_collects(article, request):
    if str(request.user) == 'AnonymousUser':
        # 没有登陆
        return ''
    if article in request.user.collects.all():
        return 'show'
    return ''


@register.filter
def is_article_list(article_list):
    if len(article_list):
        return 'search_content'
    return 'no_content'


# 时间格式化
@register.filter
def date_humaniz(date: datetime.datetime):
    pendulum.set_locale('zh')
    tz = pendulum.now().tz
    time_difference = pendulum.parse(date.strftime('%Y-%m-%d %H:%M:%S'), tz=tz).diff_for_humans()
    return time_difference


# 使用头像的总和
@register.filter
def to_calculate_avatar(avatar: Avatars):
    count = avatar.moodcomment_set.count() + avatar.moods_set.count() + avatar.userinfo_set.count()
    if count:
        return ''
    return 'no_use_avatar'


@register.filter
def to_calculate_cover(cover: Cover):
    count = cover.articles_set.count()
    if count:
        return ''
    return 'no_use_cover'


@register.filter
def get_tags(tag_list):
    return mark_safe(''.join([f"<i>{i.title}</i>" for i in tag_list]))


# 用户收藏的文章id列表
@register.filter
def get_coll_nid(lis):
    return [i.nid for i in lis]
