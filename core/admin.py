from django.contrib import admin
from .models import Post, Comment

# Подключение модели к админке по умолчанию:
# admin.site.register(Post)

# Расширенное управление моделью в админке
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # Столбцы структуры в админке
    list_display = ['title', 'slug', 'author', 'publish', 'status']
    # Фильтры в админке
    list_filter = ['status', 'created', 'publish', 'author']
    # Поиск в админке
    search_fields = ['title', 'body']
    # Правило автоматического заполнения полей; 
    # В данном случае - slug заполняется автоматически из поля title
    prepopulated_fields = {'slug':('title',)}
    # Изменение виджета выбора автора при создании/изменении поста в админке
    raw_id_fields = ['author']
    # Инструмент быстрого фильтра по дате в админке (над таблицей)
    date_hierarchy = 'publish'
    # Порядок вывода данных в таблицу админки
    ordering = ['status', 'publish']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']