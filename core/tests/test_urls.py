from django.test import SimpleTestCase
from django.urls import reverse, resolve
from core.views import post_list, post_detail, post_share, post_comment

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

    def test_blog_post_share_resolve(self):
        """Проверка url core:post_share
        """
        url = reverse('core:post_share',
                      args=['5'])
        self.assertEqual(resolve(url).func, post_share)

    def test_post_comment_resolve(self):
        """Проверка url core:post_comment
        """
        url = reverse('core:post_comment', args=['5'])
        self.assertEqual(resolve(url).func, post_comment)



        