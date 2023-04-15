from django.test import SimpleTestCase
from core.forms import EmailPostForm

class TestForms(SimpleTestCase):
    """Проверка форм
    """
    def test_email_post_form_valid_data(self):
        """Проверка заполнения формы корректными данными
        """
        form = EmailPostForm(data={
            'name': 'Test name',
            'email': 'sender@email.com',
            'to': 'recipient@some.domain.ru',
            'comments': 'Some comment на разных языках',
        })
        self.assertTrue(form.is_valid())

    def test_email_post_form_invald_data(self):
        """Проверка заполнения формы некорретными данными
        """
        form = EmailPostForm(data={
            'name': 'Test name',
            'email': 'sender',
            'comments': 'Some comment на разных языках',
        })
        self.assertFalse(form.is_valid())
        self.assertEquals(len(form.errors), 2)
    


