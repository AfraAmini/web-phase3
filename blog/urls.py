from django.conf.urls import url

from blog.views import blog_posts

urlpatterns = [
    url(r'^posts/$', blog_posts),
]
