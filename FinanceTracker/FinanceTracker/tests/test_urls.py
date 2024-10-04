from django.test import SimpleTestCase
from django.urls import reverse, resolve
from FinTech.views import dashboard, income, expenses, edit_income, edit_expense, delete_expense


class TestUrls(SimpleTestCase):
    
    def test_dashboard_url(self):
        url = reverse('dashboard')
        #print(resolve(url))
        self.assertEqual(resolve(url).func, dashboard)