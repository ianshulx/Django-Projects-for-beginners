from django.test import TestCase
from django.contrib.auth.models import User
from FinTech.models import IncomeCategory, ExpenseCategory

class CategoryModelTest(TestCase):
    
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def test_income_category_creation(self):
        # Create an IncomeCategory instance
        income_category = IncomeCategory.objects.create(name='Salary', user=self.user)
        
        # Check if the category was created successfully
        self.assertEqual(income_category.name, 'Salary')
        self.assertEqual(income_category.user, self.user)
        self.assertIsInstance(income_category, IncomeCategory)

    def test_expense_category_creation(self):
        # Create an ExpenseCategory instance
        expense_category = ExpenseCategory.objects.create(name='Food', user=self.user)
        
        # Check if the category was created successfully
        self.assertEqual(expense_category.name, 'Food')
        self.assertEqual(expense_category.user, self.user)
        self.assertIsInstance(expense_category, ExpenseCategory)

    def test_income_category_str_method(self):
        # Create an IncomeCategory instance
        income_category = IncomeCategory.objects.create(name='Salary', user=self.user)
        
        # Check if the string representation is correct
        self.assertEqual(str(income_category), 'Salary')

    def test_expense_category_str_method(self):
        # Create an ExpenseCategory instance
        expense_category = ExpenseCategory.objects.create(name='Food', user=self.user)
        
        # Check if the string representation is correct
        self.assertEqual(str(expense_category), 'Food')

    def test_income_category_user_relationship(self):
        # Create an IncomeCategory instance
        income_category = IncomeCategory.objects.create(name='Bonus', user=self.user)
        
        # Check if the user relationship is correct
        self.assertEqual(income_category.user.username, 'testuser')
        self.assertEqual(self.user.user_inc_catg.count(), 1)  # Check that the user has 1 income category

    def test_expense_category_user_relationship(self):
        # Create an ExpenseCategory instance
        expense_category = ExpenseCategory.objects.create(name='Transport', user=self.user)
        
        # Check if the user relationship is correct
        self.assertEqual(expense_category.user.username, 'testuser')
        self.assertEqual(self.user.user_exp_catg.count(), 1)  # Check that the user has 1 expense category
