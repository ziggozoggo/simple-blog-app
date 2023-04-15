from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404
from .models import Post
from .forms import EmailPostForm

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

def post_share(request, post_id):
    """Рекомендовать пост другому пользователю по email
    """
    post = get_object_or_404(Post, id=post_id, 
                             status=Post.Status.PUBLISHED)
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n"\
                      f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'my_blog@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm
    
    context = {
        'post': post,
        'form': form,
        'sent': sent,
    }

    return render(request, 'core/post/share.html', context)