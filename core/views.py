from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from core.services import data_list_paginator, send_share_post_via_email
from .models import Post
from .forms import EmailPostForm


def post_list(request):
    """Сформировать список опубликованных постов
    """
    post_list = Post.published.all()
    posts = data_list_paginator(post_list, 1, request)
    return render(request,
                  'core/post/list.html',
                  {'posts': posts}
                  )


def post_detail(request, year, month, day, post):
    """Вывести данные заданного опубликованного поста
    """
    post = get_object_or_404(Post,
                             status=Post.Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    return render(request,
                  'core/post/detail.html',
                  {'post': post})


def post_share(request, post_id):
    """Рекомендовать пост другому пользователю по email
    """
    post = get_object_or_404(Post, id=post_id,
                             status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            send_share_post_via_email(post, form, request)
            sent = True
    else:
        form = EmailPostForm

    context = {
        'post': post,
        'form': form,
        'sent': sent,
    }

    return render(request, 'core/post/share.html', context)
