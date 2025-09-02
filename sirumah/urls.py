from django.urls import path
from .views import landing, contact, company, company_property, company_house, find_house

urlpatterns = [
    path('', landing, name='home'),
    path('contact', contact, name='contact'),
    path('company', company, name='company'),
    path('company/<int:company_id>', company_property, name='company_property'),
    path('company/<int:company_id>/<int:real_estate_id>', company_house, name='company_house'),
    path('find_house', find_house, name='find_house'),

]