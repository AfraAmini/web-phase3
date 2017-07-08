from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from blog.forms import PostForm, CommentForm
from blog.models import Post, Blog, Comment
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


@login_required
def blog_comments(request, blog_id):
    if 'post_id' not in request.GET:
        return JsonResponse({'status': -1, 'message': 'can not be empty'}, status=404)

    offset = int(request.GET.get('offset', 0))
    if 'count' in request.GET:
        count = int(request.GET.get('count'))
        comments = Comment.objects.filter(post__blog_id=blog_id, post_id=request.GET.get('post_id'))[
                   offset: offset + count]
    else:
        comments = Comment.objects.filter(post__blog_id=blog_id, post_id=request.GET.get('post_id'))[offset:]
    results = []
    for comment in comments:
        results.append({'datetime': comment.datetime.strftime('%a %b %d %H:%M:%S %Y'), 'text': comment.text, })
    return JsonResponse({'status': 0, 'comments': results})


@csrf_exempt
@login_required
def blog_comment(request, blog_id):
    if request.method == 'POST':
        if 'post_id' not in request.POST:
            return JsonResponse({'status': -1, 'message': 'can not be empty'}, status=404)
        form = CommentForm(request.POST)
        if form.is_valid():
            try:
                post = Post.objects.get(id=request.POST.get('post_id'), blog_id=blog_id)
                print(post)
            except:
                return JsonResponse({'status': -1, 'message': 'post does not exist'}, status=404)
            newCommment = Comment(text=form.cleaned_data['text'], post=post)
            newCommment.save()
            return JsonResponse({'status': 0, 'comment': {'datetime': newCommment.datetime.strftime('%a %b %d %H:%M:%S %Y'),
                                                          'text': newCommment.text}})
        else:
            return JsonResponse({'status': -1, 'message': 'can not be empty'})
