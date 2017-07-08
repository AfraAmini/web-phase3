from django import forms
from django.forms import ModelForm

from blog.models import Post
from user.models import BlogUser

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'summary', 'text']
