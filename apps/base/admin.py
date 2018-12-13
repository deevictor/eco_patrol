from copy import deepcopy

from django.contrib import admin
from django.contrib.auth.models import User
from mezzanine.blog.admin import BlogPostAdmin
from mezzanine.blog.models import BlogPost
from mezzanine.core.admin import DisplayableAdmin
from mezzanine.generic.models import ThreadedComment

User._meta.verbose_name_plural = 'Пользователи'
BlogPost._meta.verbose_name_plural = 'Новости'
BlogPost._meta.verbose_name = 'Новость'

admin.site.unregister(BlogPost)
blogpost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
blogpost_fieldsets[0][1]['fields'].extend(['content'])
blogpost_list_display = ['title', 'user', 'status', 'admin_link']
blogpost_fieldsets = list(blogpost_fieldsets)
blogpost_list_filter = deepcopy(DisplayableAdmin.list_filter)


class NewsPostAdmin(BlogPostAdmin):
    fieldsets = blogpost_fieldsets
    list_display = blogpost_list_display
    list_filter = blogpost_list_filter


admin.site.register(BlogPost, NewsPostAdmin)

MODELS_TO_UNREGISTER = (
    ThreadedComment,
)

for model in MODELS_TO_UNREGISTER:
    admin.site.unregister(model)
