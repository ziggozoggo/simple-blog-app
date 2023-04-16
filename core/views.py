from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from core.services import data_list_paginator, send_share_post_via_email, get_published_post_from_db
from django.core.handlers.wsgi import WSGIRequest
from .models import Post, Comment
from .forms import EmailPostForm, CommentForm


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
    # List of active comments for post_id
    comments = post.comments.filter(active=True)
    form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form
    }
    
    return render(request,
                  'core/post/detail.html',
                  context)


def post_share(request, post_id):
    """Рекомендовать пост другому пользователю по email
    """
    post = get_published_post_from_db(post_id)
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

# Допускается только POST запрос
# При использовании другого метода вернётся статус HTTP 405
@require_POST
def post_comment(request:WSGIRequest, post_id):
    """Добавить комментарий к посту
    """
    post = get_published_post_from_db(post_id)
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        # После коммита возвращаем на страницу поста с новым комментарием
        return redirect(post.get_absolute_url())
    
    context = {
        'post': post,
        'form': form,
    }

    return render(request, 'core/post/comment.html', context)
