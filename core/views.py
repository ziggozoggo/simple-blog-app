from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from . import services
from django.core.handlers.wsgi import WSGIRequest
from .models import Post
from .forms import EmailPostForm, CommentForm


def post_list(request, tag_slug=None):
    """Сформировать список опубликованных постов:
        1. Весь список
        2. Список по заданному тэгу
    """
    post_list, tag = services.get_list_post(tag_slug)
    # Число постов на стронице settings.PAGINATOR_POSTS_PER_PAGE
    posts = services.data_list_paginator(post_list, request)
    context = {
        'posts': posts,
        'tag': tag
    }
    return render(request,
                  'core/post/list.html',
                  context
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
    # Tags
    tags = post.tags.all()
    
    # List of active comments for post_id
    comments = post.comments.filter(active=True)
    form = CommentForm()

    # List of similar posts
    similar_posts = services.get_similar_posts(post)

    context = {
        'post': post,
        'comments': comments,
        'form': form,
        'tags': tags,
        'similar_posts': similar_posts,
    }

    return render(request,
                  'core/post/detail.html',
                  context)


def post_share(request, post_id):
    """Рекомендовать пост другому пользователю по email
    """
    post = services.get_published_post_from_db(post_id)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            services.send_share_post_via_email(post, form, request)
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
def post_comment(request: WSGIRequest, post_id):
    """Добавить комментарий к посту
    """
    post = services.get_published_post_from_db(post_id)
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
