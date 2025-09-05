from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.db.models import Min, Max
from demtpy import TOPSIS, AHP
from .forms import FindHouseWeightForm
from.models import House, Company, RealEstate, HouseWeights
import numpy as np

# Create your views here.
def landing(request):
    return render(request, 'sirumah/landing.html')    

def contact(request):
    return render(request, 'sirumah/contact.html')

def company(request):
    companies = Company.objects.all()

    return render(
        request, 
        'sirumah/company.html',
        {
            'companies': companies
        }
        )

def company_property(request, company_id: int):
    
    company = get_object_or_404(Company, pk=company_id)
    real_estate = company.realestate_set.annotate(min_price=Min('house__price'), max_price=Max('house__price'))

    return render(request, 'sirumah/company_property.html', {
        'company': company,
        'real_estate': real_estate,
    })

def company_house(request, company_id: int, real_estate_id: int):
    company = get_object_or_404(Company, pk=company_id)
    real_estate = get_object_or_404(RealEstate, pk=real_estate_id)

    if real_estate.company != company:
        raise Http404("The company has no authority over the property")
    
    houses = real_estate.house_set.prefetch_related('attributes')
    
    for house in houses:
        facility = []
        specification = []
        
        for attr in house.attributes.all():
            if attr.attribute_type == 'facility':
                facility.append(attr)
            elif attr.attribute_type == 'spec':
                specification.append(attr)
            
        house.facility = facility
        house.specification = specification

    return render(request, 'sirumah/property.html', {
        'company': company,
        'real_estate': real_estate,
        'houses': houses,
    })

def find_house(request):
    houses = House.objects.all()[:10]

    if request.method == 'POST':
        form = FindHouseWeightForm(request.POST)
        if form.is_valid():
            if not houses.exists():
                return render(request, 'sirumah/find_house.html', {
                    'form': form,
                    'houses': houses,
                    'error_message': 'Mohon maaf tidak ada data rumah yang tersedia.',
                })

            location_weight = form.cleaned_data['location']
            price_weight = form.cleaned_data['price']
            building_area_weight = form.cleaned_data['building_area']
            land_area_weight = form.cleaned_data['land_area']
            specification_weight = form.cleaned_data['specification']
            facility_weight = form.cleaned_data['facility']

            # Comparison matrix weights
            criteria_weights = list(form.cleaned_data.values())[:6]
            criteria_weights = np.array(criteria_weights, dtype=float)

            comparison_matrix = criteria_weights[:, np.newaxis] / criteria_weights[np.newaxis, :]

            ahp = AHP(comparison_matrix=comparison_matrix)

            if not ahp.is_consistency:
                return render(request, 'sirumah/find_house.html', {
                    'form': form,
                    'houses': houses,
                    'error_message': 'Bobot yang diberikan tidak konsisten. Silakan sesuaikan kembali.',
                })

            # criteria preferences -1 for cost, 1 for benefit
            criteria_preferences = [1, -1, 1, 1, 1, 1]
            # criteria_weights = [location_weight, price_weight, building_area_weight, land_area_weight, specification_weight, facility_weight]

            house_weights = HouseWeights.objects.all()
            weights = list(house_weights.values_list('location', 'price', 'building_area', 'land_area', 'specification', 'facility'))
            
            topsis = TOPSIS(weights, criteria_preferences, ahp.weights)
            ranked_houses = topsis.get_score() # return list[float]

            houses_with_scores = list(zip(house_weights, ranked_houses))
            houses_with_scores.sort(key=lambda x: x[1], reverse=True) # sort by score descending
            houses_recomendation = [hw[0].house for hw in houses_with_scores][:3]

            return render(request, 'sirumah/find_house.html', {
                'form': form,
                'houses': houses,
                'house_recomendation': houses_recomendation,
            })
    else:
        form = FindHouseWeightForm()

    return render(request, 'sirumah/find_house.html', {
        'houses': houses,
        'form': form,
    })