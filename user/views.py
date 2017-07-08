import json

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt

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
            return JsonResponse({"status": "success"})
        return JsonResponse({"status": "ERROR"})


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
            return JsonResponse({'status': 'ok', 'X-Token': request.session.session_key})
        else:
            return HttpResponse("error")


def test(request):
    print(request.user.is_authenticated())
    return HttpResponse("asdfad");
