from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import News, Category
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class NewsAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = News
        fields = '__all__'


class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('id', 'title', 'category', 'created_at',
                    'updated_at', 'is_published', 'get_image')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'category')
    fields = ('title', 'category', 'content', 'image',
              'get_image', 'is_published', 'views',
              'created_at', 'updated_at')
    readonly_fields = ('get_image', 'created_at', 'updated_at',
                       'views')

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f"<img src={obj.image.url} width='75'>")
        else:
            return '-'

    get_image.short_description = 'Картинка'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)

admin.site.site_title = 'Управление новостями'
