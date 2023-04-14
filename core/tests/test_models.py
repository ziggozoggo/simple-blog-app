from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from core.models import Post


class TestModels(TestCase):
    """Проверка моделей 
    """

    def setUp(self) -> None:
        """Предварительные настройки для осуществляения проверок
        """
        self.c_date = datetime.now()
        self.post_title_name = 'post title'
        self.post_slug = 'post-title'
        self.user = User.objects.create(username='test_user')
        self.post = Post.objects.create(
            title=self.post_title_name,
            author=self.user,
            body='post body',
            status='PB',
        )

    def test_post_is_assignet_slug_on_creation(self):
        """Проверка генерации slug строки
        """
        self.assertEqual(self.post.slug, 'post-title')
        
    def test_post_is_get_absolute_url(self):
        """Проверка получения url объекта модели
        """
        self.assertEqual(self.post.get_absolute_url(), 
                         f'/blog/{self.c_date.year}/{self.c_date.month}/{self.c_date.day}/{self.post_slug}')
