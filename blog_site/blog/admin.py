from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from django.utils.html import format_html
from . import models


@admin.register(models.PostFilesModel)
class PostFilesAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'download_count', )
    search_fields = ['title', ]
    exclude = ['download_count', ]


@admin.register(models.BotUserModel)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('chat_id', 'first_name', 'last_name', 'username', 'created', 'updated')
    search_fields = ['chat_id', 'first_name', 'username', ]


@admin.register(models.CategoryModel)
class CategoryAdmin(DraggableMPTTAdmin):
    list_display = ('tree_actions', 'indented_title', 'parent',)
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', ]


@admin.register(models.PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'image_preview', 'author', 'category', 'publish', 'created',
                    'updated', 'views', 'status', ]
    list_filter = ['status', 'publish', 'author', ]
    search_fields = ['title', 'body', ]
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ['status', 'publish', ]
    exclude = ["author", 'views', ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()
        super().save_model(request, obj, form, change)

    def image_preview(self, obj):
        if obj.image:
            return format_html(f'<img src="{obj.image.url}" width="100"/>')
        else:
            return '(No image found)'

    image_preview.short_description = 'Превью'