from django.contrib import admin
from user import models
from blog import models as blogModel
from django.utils.translation import ugettext_lazy as _


class AuthorName(admin.SimpleListFilter):
    title = _('author name')

    parameter_name = 'username'

    def lookups(self, request, model_admin):
        return (set(
            ((blog.user.first_name, blog.user.last_name), "{} {}".format(blog.user.first_name, blog.user.last_name)) for
            blog in (model_admin.model.objects.all())))

    def queryset(self, request, queryset):
        print(self.value())
        return queryset.filter(user__first_name=self.value(), user__last_name=self.value())


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email")
    fieldsets = (
        (None, {'fields': ("first_name", "last_name")}),
        ("credentials", {'fields': ("email", "password")})
    )
    # fields = ("first_name", "last_name", "password", "email")
    search_fields = ["first_name", "last_name"]


class BlogAdmin(admin.ModelAdmin):
    exclude = ("first_blog",)
    list_display = ("id", "author", "created_date")
    list_filter = ("user__first_name",)
    search_fields = ["user__first_name"]

    def author(self, blog):
        return "{} {}".format(blog.user.first_name, blog.user.last_name)


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "title", "summary")

    def author(self, post):
        return "{} {}".format(post.blog.user.first_name, post.blog.user.last_name)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "text")


admin.site.register(models.BlogUser, UserAdmin)
admin.site.register(blogModel.Blog, BlogAdmin)
admin.site.register(blogModel.Post, PostAdmin)
admin.site.register(blogModel.Comment, CommentAdmin)
