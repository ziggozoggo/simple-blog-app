from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from django.db.models import Count
from taggit.models import Tag
from core.models import Post
from core.forms import EmailPostForm


def data_list_paginator(data_list: QuerySet,
                        request: WSGIRequest,
                        records_per_page=settings.PAGINATOR_POSTS_PER_PAGE,
                        req_param='page') -> Page:
    """Реализует пагинатор для переданного списка объектов Queryset

    Args:
        post_list (django.db.models.QuerySet): список объектов
        records_per_page (int): число объектов на одной странице
        request (django.core.handlers.wsgi.WSGIRequest): запрос
        req_param (str): параметр строки запроса, page по умолчанию
    """

    paginator = Paginator(data_list, records_per_page)
    # Номер страницы из строки GET запроса ../?page=2
    page_number = request.GET.get(req_param, 1)

    try:
        paginated_res = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        paginated_res = paginator.page(paginator.num_pages)

    return paginated_res


def send_share_post_via_email(post: Post, form: EmailPostForm, request: WSGIRequest) -> None:
    """Отправить информацию о посте по электронной почте

    Args:
        post (core.models.Post): пост
        form (core.forms.EmailPostForm): форма
        request (WSGIRequest): запрос
    """

    cd = form.cleaned_data
    post_url = request.build_absolute_uri(
        post.get_absolute_url()
    )
    subject = f"{cd['name']} recommends you read {post.title}"
    message = f"Read {post.title} at {post_url}\n\n"\
        f"{cd['name']}\'s comments: {cd['comments']}"
    send_mail(subject, message, settings.EMAIL_SITE_ADDRESS, [cd['to']])


def get_published_post_from_db(post_id):
    """Получить опубликованный пост по ИД либо вернуть HTTP 404
    """
    post = get_object_or_404(Post, id=post_id,
                            status=Post.Status.PUBLISHED)
    return post

def get_similar_posts(post: Post) -> QuerySet:
    """Получить список похожих постов
    """
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return similar_posts

def get_list_post(tag_slug):
    """Получить список постов и, если указан тэг - отфильтровать 
    список по этому тэгу.
    """
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
        return post_list, tag
    return post_list, tag



    
