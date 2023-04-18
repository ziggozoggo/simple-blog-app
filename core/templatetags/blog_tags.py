import markdown
from django.utils.safestring import mark_safe
from django import template
from django.db.models import Count
from core.models import Post

register = template.Library()

# simple_tag - возвращает строку
# inclusion_tag - возвращает шаблон
@register.simple_tag
def total_posts():
    """Количество опубликованных постов
    """
    return Post.published.count()

@register.inclusion_tag('core/post/latest_posts.html')
def show_latest_posts(count=5):
    """Список последних опубликованных постов
    """
    latest_posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': latest_posts}

@register.simple_tag
def get_most_commented_posts(count=5):
    """Список постов с наибольшим числом комментариев
    """
    return Post.published.annotate(
        total_comments=Count('comments')
    ).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    """Фильтр для работы с markdown строками
    """
    return mark_safe(markdown.markdown(text))
