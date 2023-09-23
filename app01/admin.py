from django.contrib import admin
from app01.models import Articles  # 文章表
from app01.models import Tags  # 标签表
from app01.models import Cover  # 文章封面表
from app01.models import Comment  # 文章评论
from app01.models import Avatars  # 文章头像
from app01.models import UserInfo  # 用户
from app01.models import Advert  # 广告
from app01.models import Menu  # 站点背景
from app01.models import MenuImg, History  # 站点背景图
from django.utils.safestring import mark_safe


# 文章
class ArticlesAdmin(admin.ModelAdmin):
    def get_cover(self):
        if self.cover:
            return mark_safe(f'<img src="{self.cover.url.url}" style="height:60px; border-radius:5px">')
        return
    get_cover.short_description = '文章封面'   # 自定义字段标题

    def get_tags(self):
        tag_list = ', '.join([i.title for i in self.tag.all()])
        return tag_list
    get_tags.short_description = '文章标签'

    def get_title(self):
        return mark_safe(f'<a href="/article/{self.nid}/" target="_blank">{self.title}</a>')
    get_title.short_description = '文章'

    def get_edit_delete_btn(self):
        return mark_safe(f"""
            <a href="/backend/edit_article/{self.nid}/" target="_blank">编辑</a>
            <a href="/admin/app01/articles/{self.nid}/delete/">删除</a>
        """)
    get_edit_delete_btn.short_description = '操作'

    list_display = [
        get_title,
        get_cover,
        get_tags,
        'look_count',
        'digg_count',
        'comment_count',
        'collects_count',
        'word',
        'change_date',
        get_edit_delete_btn
    ]

    def action_word(self, request, queryset):
        for obj in queryset:
            word = len(obj.content)
            obj.word = word
            obj.save()

    action_word.short_description = '获取文章字数'
    action_word.type = 'success'
    actions = [action_word]


admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Tags)
admin.site.register(Cover)
admin.site.register(Comment)
admin.site.register(Avatars)
admin.site.register(UserInfo)


# 广告
class AdvertAdmin(admin.ModelAdmin):

    def get_img(self):
        if self.img:

            return mark_safe(f"""<img src="{self.img.url}" style="height:60px; border-radius:5px">""")

    get_img.short_description = '用户上传'

    list_display = ['title', 'href', get_img, 'is_show', 'author', 'img_list']


admin.site.register(Advert, AdvertAdmin)


# 站点背景图
class MenuImgAdmin(admin.ModelAdmin):
    def get_img(self):
        if self.url:
            return mark_safe(f"""<img src="{self.url.url}" style="height:60px; border-radius:5px">""")
    get_img.short_description = '背景图'
    list_display = ['url', get_img]


admin.site.register(MenuImg, MenuImgAdmin)


# 站点背景
class MenuAdmin(admin.ModelAdmin):

    def get_menu_url(self: Menu):
        lis = [f"<img src='{i.url.url}' style='height:60px; border-radius:5px; margin-right:5px; margin-bottom:5px;'>" for i in self.menu_url.all()]
        return mark_safe(''.join(lis))

    get_menu_url.short_description = '图片组'
    list_display = ['menu_title', 'menu_title_en',
                    'title', 'abstract', 'rotation',
                    'abstract_time', 'menu_rotation', 'menu_time', get_menu_url]


admin.site.register(Menu, MenuAdmin)


# 回忆录
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['nid', 'title', 'content', 'create_date']


admin.site.register(History, HistoryAdmin)
