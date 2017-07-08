from django.conf.urls import url, include
from user.views import RegisterView, LoginView, test

urlpatterns = [
    url(r'^register/$', RegisterView.as_view()),
    url(r'^login/$', LoginView.as_view()),
    url(r'^test/$', test)
]
