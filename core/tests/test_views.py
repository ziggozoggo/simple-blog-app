import json
from datetime import datetime
from django.test import Client, TestCase
from django.urls import reverse
from core.models import Post
from django.contrib.auth.models import User


class TestViews(TestCase):
    """Тестирование views
    """

    def setUp(self) -> None:
        """Временные тестовые данные
        """
        current_datetime = datetime.now()
        self.client = Client()
        self.list_url = reverse('core:post_list')
        self.detail_url = reverse('core:post_detail',
                                  args=[current_datetime.year,
                                        current_datetime.month,
                                        current_datetime.day,
                                        'post-title'])

        # Создание записи во временной БД
        self.user = User.objects.create(username='test_user')
        self.post = Post.objects.create(
            title='post title',
            author=self.user,
            body='post body',
            status='PB',
        )

    def test_posts_list_view(self):
        """Тест  GET view post_list
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/post/list.html')

    def test_post_detail_view(self):
        """Тест GET view post detail
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/post/detail.html')
