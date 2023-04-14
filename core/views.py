from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from .models import Post

# Create your views here.


def post_list(request):
    """Сформировать список опубликованных постов
    """
    post_list = Post.published.all()
    # Pagination with 1 post per page
    paginator = Paginator(post_list, 1)
    page_number = request.GET.get('page', 1)

    try:
        posts = paginator.page(page_number)
    except (EmptyPage, PageNotAnInteger):
        posts = paginator.page(paginator.num_pages)

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
                             publish__year = year,
                             publish__month = month,
                             publish__day = day)
    return render(request,
                  'core/post/detail.html',
                  {'post': post})
