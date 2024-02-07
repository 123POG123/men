from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Men, Category, Tags


@admin.register(Men)
class MenAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ['title', 'cat', 'description', 'image', 'view_image', 'tag', 'data_of_bird',
              'is_published', 'slug', 'author']
    readonly_fields = ['view_image', ]
    list_display = ['title', 'view_image', 'cat', 'is_published']
    list_editable = ['is_published']
    actions = ['set_published', 'set_not_published']
    filter_horizontal = ['tag']
    list_per_page = 5

    @admin.action(description='Опубликовать')
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Men.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей.', messages.SUCCESS)

    @admin.display(description='Фото')
    def view_image(self, men: Men):
        if men.image:
            return mark_safe(f'<img src={men.image.url} width=50>')
        else:
            return 'нет фото'

    @admin.action(description='Снять с публикации')
    def set_not_published(self, request, queryset):
        count = queryset.update(is_published=Men.Status.DRAFT)
        self.message_user(request, f'Снято с публикации {count} записей.', messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tags)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}
