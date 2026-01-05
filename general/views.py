from django.shortcuts import render
from django.http import HttpResponse
from companies import models, forms

def index(request):
    companies = models.Companies.objects.all()
    
    create_company_form = forms.CreateCompanyForm()

    if request.method == 'POST':
        create_company_form = forms.CreateCompanyForm(request.POST)
        if create_company_form.is_valid():
            cd = create_company_form.cleaned_data
            print(f'name "{cd['name']}", desc "{cd['description']}"')
            new_company = models.Companies(name=cd['name'], description=cd['description'])
            new_company.save()

            roles = models.Memberships.Roles
            member = models.Memberships(user=request.user, company=new_company, role=roles.SuperAdmin)
            member.save()

    return render(request,'general/index.html', {'companies_list':companies, "create_company_form":create_company_form})

def login(request):
    return HttpResponse('Roky_bot login page') 

