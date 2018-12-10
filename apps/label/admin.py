# coding: utf-8
from django.contrib import admin
from django.utils.safestring import mark_safe

from apps.base.mixins import AdminYMapMixin
from .models import Category, Comment, Decision, Image, Label


class CategoryAdmin(admin.ModelAdmin):
    """Отображает категории меток."""

    list_display = ('title', 'get_color',)

    def get_color(self, obj):
        return mark_safe(
            f'<div style="background: {obj.color}">{obj.color}</div>'
        )

    get_color.short_description = 'Цвет метки'


class ImageInline(admin.TabularInline):
    """Отображает фотографии метки"""

    model = Image
    fields = ('label', 'image', 'image_thumb',),
    readonly_fields = ('image_thumb',)
    extra = 0

    def image_thumb(self, obj):
        return mark_safe(
            f'<img src="{obj.image.url}" height="200" />'
        )

    image_thumb.short_description = 'Предпросмотр'


class DecisionInline(admin.TabularInline):
    model = Decision
    fields = ('label', 'decision', 'decision_thumb',),
    readonly_fields = ('decision_thumb',)
    extra = 0

    def decision_thumb(self, obj):
        return mark_safe(
            f'<img src="{obj.decision.url}" height="200" />'
        )

    decision_thumb.short_description = 'Предпросмотр'


class CommentInline(admin.StackedInline):
    """Отображает комментарии к меткам"""

    model = Comment
    extra = 0
    readonly_fields = ('submit_date',)


class LabelAdmin(AdminYMapMixin, admin.ModelAdmin):
    """Отображает метки для карты."""

    list_display = (
        'name', 'category', 'phone',
        'pub_time', 'approved', 'in_top',
        'solved',
    )
    list_editable = ('approved', 'in_top', 'solved')
    list_filter = (
        'category', 'approved', 'in_top',
        'solved', 'pub_time',
    )
    search_fields = ('category',)
    inlines = [DecisionInline, ImageInline, CommentInline]
    actions = ('mark_approved', 'mark_in_top',)

    def mark_approved(self, request, queryset):
        queryset.update(approved=True)

    def mark_in_top(self, request, queryset):
        queryset.update(in_top=True)

    mark_approved.short_description = 'Одобрить выбранные метки'
    mark_in_top.short_description = 'Вывести в топ выбранные метки'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Label, LabelAdmin)
