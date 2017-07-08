from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from blog.forms import PostForm
from blog.models import Post, Blog
from user.views import login_required


@login_required
def blog_posts(request, blog_id):
    offset = int(request.GET.get('offset', 0))
    if 'count' in request.GET:
        count = int(request.GET.get('count'))
        posts = Post.objects.filter(blog_id=blog_id)[offset: offset + count]
    else:
        posts = Post.objects.filter(blog_id=blog_id)[offset:]
    results = []
    for post in posts:
        results.append({'id': post.id, 'title': post.title, 'summary': post.summary,
                        'datetime': post.datetime.strftime('%a %b %d %H:%M:%S %Y')})
    return JsonResponse({'status': 0, 'posts': results})


@csrf_exempt
@login_required
def blog_post(request, blog_id):
    if request.method == 'GET':
        try:
            post = get_object_or_404(Post, id=request.GET.get('id', 0), blog_id=blog_id)
            return JsonResponse({'status': 0, 'post': {'title': post.title, 'summary': post.summary,
                                                       'text': post.text,
                                                       'datetime': post.datetime.strftime('%a %b %d %H:%M:%S %Y')}})
        except Post.DoesNotExist:
            return JsonResponse({'status': -1, 'message': 'not found'})
    elif request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            try:
                blog = Blog.objects.get(id=blog_id, user=request.user)
            except:
                return JsonResponse({'status': -1, 'message': 'blog does not exist'}, status=404)
            newPost = Post(title=form.cleaned_data['title'], summary=form.cleaned_data['summary'],
                           text=form.cleaned_data['text'], blog=blog)
            newPost.save()
            return JsonResponse({'status': 0, 'post_id': newPost.id})
        else:
            return JsonResponse({'status': -1, 'message': 'can not be empty'})



