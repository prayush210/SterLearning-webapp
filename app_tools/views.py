from django.shortcuts import render
import requests
from django import forms
# Create your views here.

class MortgageForm(forms.Form):
    loan_amount = forms.FloatField(required=False) # compulsory

    home_value = forms.FloatField(required=False) # compulsory
    downpayment = forms.FloatField(required=False) # compulsory

    interest_rate = forms.FloatField(required=True)
    # compulsory, percentage as decimal, ie 3.5% is entered as 3.5

    duration_years = forms.FloatField(required=False) # optional
    monthly_hoa = forms.FloatField(required=False) # optional
    annual_property_tax = forms.FloatField(required=False) # optional
    annual_home_insurance = forms.FloatField(required=False) # optional

    # def clean(self):
    #     cleaned_data = super().clean()
    #     loanamt = cleaned_data.get("loan_amount")
    #     homeval = cleaned_data.get("home_value")
    #     downpay = cleaned_data.get("downpayment")
    #     if (not bool(loanamt)) or not (bool(homeval) and bool(downpay)):
    #         print("compulsory field missing")
    #     return cleaned_data

# TODO:
#### keep submitted details in form
def mortgage(request):
    context = {}

    if request.method == 'GET':
        form = MortgageForm(request.GET)
        api_url = 'https://api.api-ninjas.com/v1/mortgagecalculator?'

        context['submissions'] = form.data 
        dict = context["submissions"].dict()

        for key, value in dict.items():
            if bool(value):
                api_url += (key + "=" + value + "&")

        response = requests.get(api_url, headers={
            'X-Api-Key': 'iDj1OIcpx1Ulk/xRIBmk9Q==qnEkfnb7lGtejdWX'})

        if response.status_code == requests.codes.ok:
            results = response.json()
            context['results'] = results
        else:
            context['errorcode'] = response.status_code
            context['error'] = response.json()
            print(response.json())

    context['form'] = MortgageForm()
    return render(request, "mortgage.html", context)
