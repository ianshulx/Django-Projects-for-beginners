from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
from unittest.mock import patch, MagicMock
from FinTech.models import IncomeCategory, ExpenseCategory, Income, Expense, Budget, Account
import json


class TestViews(TestCase):
    
    def setUp(self):
        # Create a user and log them in
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')
        
        # Create an account for the user
        self.account = Account.objects.create(user=self.user, balance=500)
        
        # Create expense categories for the user
        self.catg_food = ExpenseCategory.objects.create(user=self.user, name='Food')
        self.catg_transport = ExpenseCategory.objects.create(user=self.user, name='Transport')

        # Create expenses for the user
        self.expense1 = Expense.objects.create(user=self.user, amount=50, category=self.catg_food, date=date.today())
        self.expense2 = Expense.objects.create(user=self.user, amount=20, category=self.catg_transport, date=date.today())
        self.expense3 = Expense.objects.create(user=self.user, amount=30, category=self.catg_food, date=date.today())
    
    def test_dashboard_view_expenses_and_balance(self):
        # Call the dashboard view
        response = self.client.get(reverse('dashboard'))
        
        # Check if the response is 200 OK
        self.assertEqual(response.status_code, 200)
        
        # Check if the account balance is passed correctly to the template
        self.assertContains(response, self.account.balance)
        
        # Check if the expenses by category are calculated correctly
        context = response.context
        expected_expenses = {
            'Food': 80,  # 50 + 30
            'Transport': 20  # 20
        }
        
        # Verify that the output dictionary has correct totals
       # self.assertEqual(context['catg_list'], ['Food', 'Transport'])
        self.assertEqual(context['catg_total_list'], [80, 20])
