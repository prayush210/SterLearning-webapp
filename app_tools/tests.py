from app_tools.views import MortgageForm
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from app_tools.views import mortgage


class MortgageFormTest(TestCase):

    # Test if the form is valid with correct data
    def test_form_valid_data(self):
        form = MortgageForm(data={
            'loan_amount': 100000.0,
            'home_value': 150000.0,
            'downpayment': 50000.0,
            'interest_rate': 3.5,
            'duration_years': 30,
            'monthly_hoa': 100.0,
            'annual_property_tax': 2000.0,
            'annual_home_insurance': 1000.0
        })
        self.assertTrue(form.is_valid())

    # Test if the form is invalid with missing data
    def test_form_invalid_data(self):
        form = MortgageForm(data={
            'loan_amount': 100000.0,
            'home_value': 150000.0,
            'downpayment': 50000.0,
            # 'interest_rate': 3.5,
            'duration_years': 30,
            'monthly_hoa': 100.0,
            'annual_property_tax': 2000.0,
            'annual_home_insurance': 1000.0
        })
        self.assertFalse(form.is_valid())


class MortgageViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        user = get_user_model()
        self.user = user.objects.create_user(username='testuser', password='12345')

    # Test if the mortgage view returns a 200 status code
    def test_mortgage_view(self):
        request = self.factory.get('/mortgage')
        request.user = self.user
        response = mortgage(request)
        self.assertEqual(response.status_code, 200)
