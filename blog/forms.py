from django import forms
from django.forms import ModelForm

from blog.models import Post, Comment
from user.models import BlogUser

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'summary', 'text']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
