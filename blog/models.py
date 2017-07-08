from django.db import models

# Create your models here.
from user.models import BlogUser



class Blog(models.Model):
    user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {} {}".format(self.id, self.user.first_name, self.user.last_name)


class Post(models.Model):
    title = models.CharField(max_length=20)
    summary = models.TextField()
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return "{} {}".format(self.id, self.title)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return "{} {}".format(self.id, self.text)
