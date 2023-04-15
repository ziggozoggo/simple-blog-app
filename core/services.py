from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, Page
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import QuerySet
from core.models import Post
from core.forms import EmailPostForm


def data_list_paginator(data_list: QuerySet,
                        records_per_page: int,
                        request: WSGIRequest,
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
