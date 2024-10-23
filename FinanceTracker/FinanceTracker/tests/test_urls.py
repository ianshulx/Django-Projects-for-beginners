from django.test import SimpleTestCase
from django.urls import reverse, resolve
from FinTech.views import dashboard, income, expenses, edit_income, edit_expense, delete_expense, delete_income, expense_report, income_report, add_expense_category, add_income_category, remove_expense_category, remove_income_category, profile, settings, index, signup, login, logout



class TestUrls(SimpleTestCase):
    
    def test_dashboard_url(self):
        url = reverse('dashboard')
        #print(resolve(url))
        self.assertEqual(resolve(url).func, dashboard)

    def test_incomes_url(self):
        url = reverse('incomes')
        self.assertEqual(resolve(url).func, income)
        self.assertNotEqual(resolve(url).func, expenses)

    def test_expenses_url(self):
        url = reverse('expenses')
        self.assertEqual(resolve(url).func, expenses)        

    def test_edit_Income_url(self):
        url = reverse('edit-income', args=[1])
        self.assertEqual(resolve(url).func, edit_income)        

    def test_edit_Expense_url(self):
        url = reverse('edit-expense', args=[2])
        self.assertEqual(resolve(url).func, edit_expense)     

    def test_Expense_Report_url(self):
        url = reverse('expense-report', args=['string'])
        self.assertEqual(resolve(url).func, expense_report)      

    def test_remove_Income_url(self):
        url = reverse('remove-income-category', args=[1])
        self.assertNotEqual(resolve(url).func, income)      
        self.assertEqual(resolve(url).func, remove_income_category)   

    def test_profile_url(self):
        url = reverse('profile')
        self.assertEqual(resolve(url).func, profile)       
        self.assertNotEqual(resolve(url).func, settings)  

    def test_signup_url(self):
        url = reverse('signup')
        self.assertEqual(resolve(url).func, signup) 
        self.assertNotEqual(resolve(url).func, index)   
        self.assertNotEqual(resolve(url).func, login)  
        self.assertNotEqual(resolve(url).func, logout) 