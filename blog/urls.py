from django.conf.urls import url

from blog.views import blog_posts, blog_post

urlpatterns = [
    url(r'^(?P<blog_id>\d+)/posts/$', blog_posts),
    url(r'^(?P<blog_id>\d+)/post/$', blog_post),
]
