from django.contrib import admin
from django import forms
from .models import Company, RealEstate, House, HouseAttribute, HouseWeights, Criteria, SubCriteria


class HouseAttributeInline(admin.TabularInline): 
    model = HouseAttribute
    extra = 2 


class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name", "province", "district", "subdistrict", "village",]


class HouseAdmin(admin.ModelAdmin):
    list_display = ['house_type', 'price', 'real_estate']
    list_filter = ['real_estate']
    inlines = [HouseAttributeInline]


class HouseInline(admin.StackedInline):
    model = House
    extra = 3


class RealEstateAdmin(admin.ModelAdmin):
    list_display = ["name", "province", "district", "subdistrict", "village", "house_count"]
    inlines = [HouseInline] 

    def house_count(self, obj):
        return obj.house_set.count()
    

# class HouseWeightsAdmin(admin.ModelAdmin):
#     list_display = ('house', 'location', 'price', 'building_area', 'land_area', 'specification', 'facility')

#     def formfield_for_foreignkey(self, db_field, request, **kwargs):
#         if db_field.name == "house":
#             kwargs["queryset"] = House.objects.select_related('real_estate').all()
#             kwargs["label_from_instance"] = lambda obj: f"{obj.house_type} | {obj.real_estate.name}"
#         return super().formfield_for_foreignkey(db_field, request, **kwargs)


# 🔹 Custom ModelChoiceField biar label bisa diubah
class HouseChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return f"{obj.house_type} | {obj.real_estate.name}"

# 🔹 Custom Form untuk HouseWeights
class HouseWeightsForm(forms.ModelForm):
    house = HouseChoiceField(queryset=House.objects.select_related('real_estate').all())

    class Meta:
        model = HouseWeights
        fields = '__all__'

# 🔹 Custom Admin
class HouseWeightsAdmin(admin.ModelAdmin):
    form = HouseWeightsForm
    list_display = ('house', 'location', 'price', 'building_area', 'land_area', 'specification', 'facility')


class SubCriteriaInline(admin.TabularInline):
    model = SubCriteria
    extra = 3


class CriteriaAdmin(admin.ModelAdmin):
    list_display = ('name', 'sub_criteria_count')
    inlines = [SubCriteriaInline]

    def sub_criteria_count(self, obj):
        return obj.subcriteria_set.count()


# Register your models here.
admin.site.register(Company, CompanyAdmin)
admin.site.register(RealEstate, RealEstateAdmin)
admin.site.register(House, HouseAdmin)
admin.site.register(HouseWeights, HouseWeightsAdmin)
admin.site.register(Criteria, CriteriaAdmin)