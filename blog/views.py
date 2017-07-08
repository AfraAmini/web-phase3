from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from blog.models import Post
from user.views import login_decorator


@login_decorator
def blog_posts(request):
    blog_id = request.GET.get('id')
    offset = request.GET.get('offset', 0)
    if 'count' in request.GET:
        count = request.GET.get('count')
        posts = Post.objects.filter(blog_id = blog_id)[offset: offset+count]
    else:
        posts = Post.objects.filter(blog_id = blog_id)[offset:]
    print(posts)
    return HttpResponse("hi")


