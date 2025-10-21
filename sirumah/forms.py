from django import forms
from .models import Criteria, SubCriteria

def get_dyanamic_form():
    class DynamicCriteriaForm(forms.Form):
        pass


    SUBCRITERIA_CHOICE = {
        "Harga": [
            (0, 'Subsidi (<= 240 juta)'),
            (1, 'Komersil (> 240 juta)')
        ],
    }

    for crt in Criteria.objects.all():
        subcriteria: SubCriteria = crt.subcriteria_set.all()
        
        if len(subcriteria) > 0:
            field = forms.ModelChoiceField(queryset=subcriteria, required=True)
        else:
            field = forms.ChoiceField(choices=SUBCRITERIA_CHOICE.get(crt.name, [
                (0, "Subcriteria 1"),
                (1, "Subcriteria 2"),
                (2, "Subcriteria 3")
            ]), required=True)
    
        DynamicCriteriaForm.base_fields[crt.name] = field
    
    return DynamicCriteriaForm


class FindHouseForm(forms.Form):
    LOCATION_CHOICE = [
        (0, 'Dekat dengan pusat kota (< 5 km)'),
        (1, 'Sedang (5 - 10 km)'),
        (2, 'Jauh (> 10 km)'),
    ]
    PRICE_CHOICE = [
        (0, 'Subsidi (<= 240 juta)'),
        (0, 'Komersil (> 240 juta)'),
    ]

    location = forms.ChoiceField(choices=LOCATION_CHOICE, required=True,)
    price = forms.ChoiceField(choices=PRICE_CHOICE, required=True,)
    # building_area = forms.IntegerField(label='Luas Bangunan', required=True, min_value=1, max_value=9)
    # land_area = forms.IntegerField(label='Luas Tanah', required=True, min_value=1, max_value=9)
    # specification = forms.IntegerField(label='Spesifikasi', required=True, min_value=1, max_value=9)
    # facility = forms.IntegerField(label='Fasilitas', required=True, min_value=1, max_value=9)


class PriorityForm(forms.Form):
    priorities = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Pilih prioritas utama Anda:",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # load semua kriteria dari DB
        self.fields['priorities'].choices = [
            (c.id, c.name) for c in Criteria.objects.all()
        ]


class FindHouseWeightForm(forms.Form):
    location = forms.IntegerField(label='Lokasi', required=True, min_value=1, max_value=9)
    price = forms.IntegerField(label='Harga', required=True, min_value=1, max_value=9)
    building_area = forms.IntegerField(label='Luas Bangunan', required=True, min_value=1, max_value=9)
    land_area = forms.IntegerField(label='Luas Tanah', required=True, min_value=1, max_value=9)
    specification = forms.IntegerField(label='Spesifikasi', required=True, min_value=1, max_value=9)
    facility = forms.IntegerField(label='Fasilitas', required=True, min_value=1, max_value=9)
    sub_location_c1 = forms.IntegerField(label='Sub Lokasi C1', required=False, min_value=1, max_value=9)
    sub_location_c2 = forms.IntegerField(label='Sub Lokasi C2', required=False, min_value=1, max_value=9)
    sub_location_c3 = forms.IntegerField(label='Sub Lokasi C3', required=False, min_value=1, max_value=9)
    sub_price_c1 = forms.IntegerField(label='Sub Harga C1', required=False, min_value=1, max_value=9)
    sub_price_c2 = forms.IntegerField(label='Sub Harga C2', required=False, min_value=1, max_value=9)
    sub_price_c3 = forms.IntegerField(label='Sub Harga C3', required=False, min_value=1, max_value=9)
    sub_building_area_c1 = forms.IntegerField(label='Sub Luas Bangunan C1', required=False, min_value=1, max_value=9)
    sub_building_area_c2 = forms.IntegerField(label='Sub Luas Bangunan C2', required=False, min_value=1, max_value=9)
    sub_building_area_c3 = forms.IntegerField(label='Sub Luas Bangunan C3', required=False, min_value=1, max_value=9)
    sub_land_area_c1 = forms.IntegerField(label='Sub Luas Tanah C1', required=False, min_value=1, max_value=9)
    sub_land_area_c2 = forms.IntegerField(label='Sub Luas Tanah C2', required=False, min_value=1, max_value=9)
    sub_land_area_c3 = forms.IntegerField(label='Sub Luas Tanah C3', required=False, min_value=1, max_value=9)
    sub_specification_c1 = forms.IntegerField(label='Sub Spesifikasi C1', required=False, min_value=1, max_value=9)
    sub_specification_c2 = forms.IntegerField(label='Sub Spesifikasi C2', required=False, min_value=1, max_value=9)
    sub_specification_c3 = forms.IntegerField(label='Sub Spesifikasi C3', required=False, min_value=1, max_value=9)
    sub_facility_c1 = forms.IntegerField(label='Sub Fasilitas C1', required=False, min_value=1, max_value=9)
    sub_facility_c2 = forms.IntegerField(label='Sub Fasilitas C2', required=False, min_value=1, max_value=9)
    sub_facility_c3 = forms.IntegerField(label='Sub Fasilitas C3', required=False, min_value=1, max_value=9)