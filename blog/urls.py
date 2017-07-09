from django.conf.urls import url

from blog.views import blog_posts, blog_post, blog_comments, blog_comment

urlpatterns = [
    url(r'^(?P<blog_id>\d+)/posts$', blog_posts),
    url(r'^(?P<blog_id>\d+)/post$', blog_post),
    url(r'^(?P<blog_id>\d+)/comments$', blog_comments),
    url(r'^(?P<blog_id>\d+)/comment$', blog_comment),
]
