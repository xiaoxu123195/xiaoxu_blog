from django.urls import path, re_path
from api.views import login, article, comment, news, mood, user, file, api_email, history

urlpatterns = [
    path("login/", login.LoginView.as_view()),  # 登录
    path("sign/", login.SignView.as_view()),  # 注册
    path("article/", article.ArticleView.as_view()),  # 发布文章
    re_path(r"article/(?P<nid>\d+)", article.ArticleView.as_view()),  # 修改文章
    re_path(r"article/comment/(?P<nid>\d+)", comment.CommentView.as_view()),  # 发布评论
    re_path(r"comment/digg/(?P<nid>\d+)", comment.CommentDiggView.as_view()),  # 评论点赞

    re_path(r"article/digg/(?P<nid>\d+)", article.ArticlesDiggView.as_view()),  # 文章点赞
    re_path(r"article/collects/(?P<nid>\d+)", article.ArticleCollectorView.as_view()),  # 文章收藏

    path("news/", news.NewsView.as_view()),  # 新闻
    path("moods/", mood.MoodsView.as_view()),  # 发布心情
    re_path(r"moods/(?P<nid>\d+)", mood.MoodsView.as_view()),  # 删除心情
    re_path(r"mood_comments/(?P<nid>\d+)", mood.MoodCommentsView.as_view()),  # 发布心情评论
    path("edit_password/", user.EditPasswordView.as_view()),  # 修改密码
    path("edit_avatar/", user.EditAvatarView.as_view()),  # 修改头像
    path("upload/avatar/", file.AvatarView.as_view()),  # 上传头像
    path("upload/cover/", file.CoverView.as_view()),  # 上传封面
    re_path("upload/avatar/(?P<nid>\d+)", file.AvatarView.as_view()),  # 删除头像
    re_path("upload/cover/(?P<nid>\d+)", file.CoverView.as_view()),  # 删除封面
    path("send_email/", api_email.ApiEmail.as_view()),  # 发送邮件
    path("cancel_collection/", user.CancelCollection.as_view()),  # 取消收藏

    path('history/', history.HistoryView.as_view()),  # 发布记录
    re_path(r'history/(?P<nid>\d+)/', history.HistoryView.as_view()),  # 编辑记录
]
