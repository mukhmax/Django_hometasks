from django.contrib import admin
from django.forms import BaseInlineFormSet, ValidationError
from .models import Article, Tag, Scope


class ScopeFormset(BaseInlineFormSet):
    def clean(self):
        is_main_num = 0
        for form in self.forms:
            if form.cleaned_data.get('is_main'):
                is_main_num += 1
        if is_main_num < 1:
            raise ValidationError('Укажите основной раздел')
        elif is_main_num > 1:
            raise ValidationError('Основным может быть только один раздел')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'published_at']
    inlines = [ScopeInline,]


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
