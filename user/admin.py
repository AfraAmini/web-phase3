from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import ugettext_lazy as _

from blog import models as blogModel
from user import models
from user.models import BlogUser


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


class BlogUserCreationForm(UserCreationForm):
    class Meta:
        model = BlogUser
        fields = ('username', 'first_name', 'last_name',)


class BlogUserAdmin(UserAdmin):
    add_form = BlogUserCreationForm

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'username', 'password1', 'password2',),
        }),
    )

    fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email',),
        }),
    )


# class BlogUserAdmin(UserAdmin):
#     # form = BlogUserChangeForm
#     model = BlogUser
#     # list_display = ("first_name", "last_name", "email")
#     fieldsets = UserAdmin.fieldsets + (
#         (None, {'fields': ("first_name", "last_name")}),)
#     # fields = ("first_name", "last_name", "password", "email")
#     search_fields = ["first_name", "last_name"]


class BlogAdmin(admin.ModelAdmin):
    exclude = ("first_blog",)
    list_display = ("id", "author", "created_date")
    list_filter = ("user__first_name",)
    search_fields = ["user__first_name"]

    def author(self, blog):
        return "{} {}".format(blog.user.first_name, blog.user.last_name)


class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "title", "datetime")

    def author(self, post):
        return "{} {}".format(post.blog.user.first_name, post.blog.user.last_name)


class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "datetime")


admin.site.register(models.BlogUser, BlogUserAdmin)
admin.site.register(blogModel.Blog, BlogAdmin)
admin.site.register(blogModel.Post, PostAdmin)
admin.site.register(blogModel.Comment, CommentAdmin)
