# coding: utf-8
from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.base.mixins import AdminYMapMixin

from .models import Category, Image, Label, Comment


class CategoryAdmin(admin.ModelAdmin):
    """Отображает категории меток."""

    list_display = ('title', 'get_color', )

    def get_color(self, obj):
        return mark_safe(
            f'<div style="background: {obj.color}">{obj.color}</div>'
        )


class ImageInline(admin.TabularInline):
    """Отображает фотографии метки"""
    model = Image
    extra = 0


class CommentInline(admin.StackedInline):
    """Отображает комментарии к меткам"""
    model = Comment
    extra = 0
    readonly_fields = ('submit_date',)


class LabelAdmin(AdminYMapMixin, admin.ModelAdmin):
    """Отображает метки для карты."""

    list_display = (
        'name', 'category', 'phone', 'name', 'pub_time', 'approved', 'in_top'
    )
    list_editable = ('approved', 'in_top')
    inlines = [ImageInline, CommentInline]


admin.site.register(Category, CategoryAdmin)
admin.site.register(Label, LabelAdmin)
