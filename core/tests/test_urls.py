from django.test import SimpleTestCase
from django.urls import reverse, resolve
from core.views import post_list, post_detail

class TestUrls(SimpleTestCase):
    """Тестирование доступности urls
    """
    def test_blog_list_is_resolve(self):
        """Проверка url core:post_list
        """
        url = reverse('core:post_list')
        self.assertEqual(resolve(url).func, post_list)

    def test_blog_post_detail_resolve(self):
        """Проверка url core:post_detail
        """
        url = reverse('core:post_detail', 
                      args=['2022', '12', '5', 'some-slug'])
        self.assertEqual(resolve(url).func, post_detail)



        