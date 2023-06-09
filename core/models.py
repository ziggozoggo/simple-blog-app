from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


# По умолчанию для запросов используется менеджер objects, который выбирает все 
# объекты из базы данных.
# Мы можем задать собственный менеджер,
# например - для получения только опубликованных постов
class PublishedManager(models.Manager):
    """Кастомный менеджер для модели Post для выбора только опубликованных записей
    """
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)



class Post(models.Model):
    """Структура хранения сообщения блога
    """
    class Status(models.TextChoices):
        """Справочник взможных статусов сообщения
        """
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250, verbose_name='Title')
    slug = models.SlugField(max_length=250, verbose_name='Slug',
                            unique_for_date='publish')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='blog_posts')
    body = models.TextField(verbose_name='Content')
    tags = TaggableManager()
    publish = models.DateTimeField(
        default=timezone.now, verbose_name='Publish Date')
    created = models.DateTimeField(
        auto_now_add=True, verbose_name='Created at')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated at')
    status = models.CharField(max_length=2,
                              choices=Status.choices,
                              default=Status.DRAFT)

    #### Менеджеры класса Post ####
    objects = models.Manager() # менеджер по умолчанию; управляется Meta - default_manager_name
    published = PublishedManager() # кастомный менеджер, определённый выше
    
    class Meta:
        # Сортировка по дате публикации в обратном порядке
        ordering = ['-publish',]
        # Список индексов БД
        indexes = [
            models.Index(fields=['-publish']),
        ]
        # Именование в админке
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def get_absolute_url(self):
        """Создать ссылку на каждый объект модели 
        """
        # core - urls.py -> app_name
        # post_detail - urls.py -> name == post_detail
        return reverse("core:post_detail", 
                       args=[self.publish.year,
                             self.publish.month,
                             self.publish.day,
                             self.slug])
    
    # Создадим slug-field автоматически; дополним метод save
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
     
    
    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    """Комментарии к постам блога
    """
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created'])
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'
    




