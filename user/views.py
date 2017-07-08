import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from blog.models import Blog
from user.forms import UserForm
from user.models import BlogUser


class RegisterView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        form = UserForm(request.POST)

        if form.is_valid():
            newUser = BlogUser()
            newUser.first_name = form.cleaned_data['first_name']
            newUser.last_name = form.cleaned_data['last_name']
            newUser.email = form.cleaned_data['email']
            newUser.set_password(form.cleaned_data['password'])
            newUser.username = form.cleaned_data['email']
            newUser.save()

            #create new blog for each user
            newBlog = Blog(user = newUser)
            newBlog.save()

            return JsonResponse({"status": 0})
        print((form.errors['__all__']))
        return JsonResponse({"status": -1, "message": form.errors['__all__'][0]})


class LoginView(View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        username = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({'status': 0, 'X-Token': request.session.session_key})
        else:
            return JsonResponse({'status': -1, 'message': 'user not found'})


def test(request):
    print(request.user.is_authenticated())
    return HttpResponse("asdfad")

def login_decorator(func):
    def decorated(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return JsonResponse({'status': -1, 'message': 'no/wrong token'})
        return func(request, *args, **kwargs)
    return decorated



@csrf_exempt
@login_decorator
def blogid(request):
    blogs = Blog.objects.filter(user = request.user).order_by('created_date')
    if(len(blogs) > 0):
        return JsonResponse({'status': 0, 'id': blogs[0].id})
    else:
        return JsonResponse({'status': -1, 'message': 'this user has no blogs yet'})



