from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from companies.services import get_all_companies

@csrf_exempt
def main_home_page_view(request):
    companies = get_all_companies()
    return render(request,'general/index.html', {'companies_list':companies})


