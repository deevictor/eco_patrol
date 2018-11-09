from copy import deepcopy

from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import User

from mezzanine.blog.models import BlogPost
from mezzanine.blog.admin import BlogPostAdmin
from mezzanine.generic.models import ThreadedComment
from mezzanine.core.admin import DisplayableAdmin



User._meta.verbose_name_plural = u'Пользователи'
BlogPost._meta.verbose_name_plural = u'Новости'
BlogPost._meta.verbose_name = u'Новость'

admin.site.unregister(BlogPost)
blogpost_fieldsets = deepcopy(DisplayableAdmin.fieldsets)
# blogpost_fieldsets[0][1]["fields"].insert(1, "categories")
blogpost_fieldsets[0][1]["fields"].extend(["content"])
blogpost_list_display = ["title", "user", "status", "admin_link"]
# blogpost_fieldsets[0][1]["fields"].insert(-2, "featured_image")
# blogpost_list_display.insert(0, "admin_thumb")
blogpost_fieldsets = list(blogpost_fieldsets)
blogpost_list_filter = deepcopy(DisplayableAdmin.list_filter)
# blogpost_list_filter = deepcopy(DisplayableAdmin.list_filter) + ("categories",)


class NewsPostAdmin(BlogPostAdmin):
    fieldsets = blogpost_fieldsets
    list_display = blogpost_list_display
    list_filter = blogpost_list_filter

admin.site.register(BlogPost, NewsPostAdmin)

MODELS_TO_UNREGISTER = (
    ThreadedComment,
    # Site,
)


for model in MODELS_TO_UNREGISTER:
    try:
        del admin.site._registry[model]
    except KeyError:
        pass