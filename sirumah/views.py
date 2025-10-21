from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.db.models import Min, Max, Prefetch
from pymcdm.methods import TOPSIS
from .forms import FindHouseWeightForm, FindHouseForm, PriorityForm, get_dyanamic_form
from.models import House, Company, RealEstate, HouseWeights, Criteria, SubCriteria
from .utils.ahp import AHP
import numpy as np
import json

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
    # Get previous navigation url
    previous_url = request.META.get('HTTP_REFERER', '/')

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
        'previous_url': previous_url,
        'company': company,
        'real_estate': real_estate,
        'houses': houses,
    })

def find_house(request):
    real_estates = RealEstate.objects.annotate(min_price=Min('house__price'), max_price=Max('house__price')).all()
    criteria = Criteria.objects.all()
    criteria_list = ["Lokasi", "Harga", "Luas Bangunan", "Luas Lahan", "Spesifikasi", "Fasilitas"]
    show_modal = "priority" not in request.session

    if request.method == 'POST':
        priority_order = json.loads(request.POST.get("priority_order", "[]"))

        if len(priority_order) > 0:
            request.session["priority"] = priority_order
            
            houses_recomendation = get_ranking_house(priority_order, criteria_list)

            return render(request, 'sirumah/find_house.html', {
                'real_estates': real_estates,
                'criteria': criteria,
                'house_recomendation': houses_recomendation,
            })

    priority_order = request.session['priority'] if not show_modal else []
    houses_recomendation = None

    if len(priority_order) > 0:
        houses_recomendation = get_ranking_house(priority_order, criteria_list)

    return render(request, 'sirumah/find_house.html', {
        'real_estates': real_estates,
        'criteria': criteria,
        'show_modal': show_modal,
        'house_recomendation': houses_recomendation,
    })

def get_ranking_house(priority, criteria):
    scores = np.ones(len(criteria))

    priority_value = len(criteria)
    for idx, name in enumerate(priority):
        pos = criteria.index(name)

        scores[pos] = priority_value - idx
    
    scores = normalize_priorities(scores)

    ahp = AHP(scoring=scores)
    weights = ahp.weights

    house_weights = HouseWeights.objects.all()
    alt_weights = house_weights.values_list('location', 'price', 'building_area', 'land_area', 'specification', 'facility')
    criteria_preference = [-1, -1, 1, 1, 1, 1]

    topsis = TOPSIS()
    ranked_houses = topsis(alt_weights, weights, criteria_preference)

    houses_with_scores = list(zip(house_weights, ranked_houses))
    houses_with_scores.sort(key=lambda x: x[1], reverse=True) # sort by score descending

    return [hw[0].house for hw in houses_with_scores][:3]

def normalize_priorities(weights):
    weights = np.array(weights, dtype=int)
    n = len(weights)

    used = set(weights[weights > 1])

    available = [i for i in range(n, 0, -1) if i not in used]

    for i in range(n):
        if weights[i] == 1:
            weights[i] = available.pop(0)
    
    # dapatkan urutan ranking
    ranks = sorted(range(len(weights)), key=lambda i: weights[i], reverse=True)
    result = [0] * len(weights)

    for rank, idx in enumerate(ranks):
        result[idx] = rank + 1

    return result