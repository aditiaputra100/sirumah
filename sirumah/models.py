from django.db import models

# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=100, null=False, unique=True)
    phone_number = models.CharField(max_length=16, null=False, unique=True)
    email = models.EmailField(max_length=100, null=False, unique=True)
    province = models.CharField(max_length=20, null=False,)
    district = models.CharField(max_length=100, null=False,)
    subdistrict = models.CharField(max_length=50, null=False,)
    village = models.CharField(max_length=50, null=False,)
    address = models.CharField(max_length=150, null=False)

    def __str__(self):
        return self.name


class RealEstate(models.Model):
    company = models.ForeignKey(Company, null=True, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100, null=False, unique=True)
    # location = models.CharField(max_length=100, null=False,)
    province = models.CharField(max_length=20, null=False, default="")
    district = models.CharField(max_length=100, null=False, default="")
    subdistrict = models.CharField(max_length=50, null=False, default="")
    village = models.CharField(max_length=50, null=False, default="")
    

    def __str__(self):
        return self.name


class House(models.Model):
    real_estate = models.ForeignKey(RealEstate, null=False, on_delete=models.CASCADE)
    house_type = models.CharField(max_length=10, null=False)
    price = models.IntegerField(null=False)
    building_area = models.FloatField(null=False)
    land_area = models.FloatField(null=False)
    # facility = models.TextField(null=False)
    # spesification = models.TextField(null=False)

    def __str__(self):
        return self.house_type
    

class HouseAttribute(models.Model):
    ATTRIBUTE_TYPE_CHOICE = [
        ('facility', 'Facility'),
        ('spec', 'Specification'),
    ]

    house = models.ForeignKey(House, on_delete=models.CASCADE, related_name='attributes')
    attribute_type = models.CharField(max_length=10, choices=ATTRIBUTE_TYPE_CHOICE)
    name = models.CharField(max_length=100, null=False)
    value = models.CharField(max_length=255, null=False)

    def __str__(self):
        return f"{self.house.house_type} - {self.name}: {self.value}"
    

class HouseWeights(models.Model):
    house = models.OneToOneField(House, null=False, on_delete=models.CASCADE, unique=True, primary_key=True)
    location = models.IntegerField(null=False)
    price = models.IntegerField(null=False)
    building_area = models.IntegerField(null=False)
    land_area = models.IntegerField(null=False)
    specification = models.IntegerField(null=False)
    facility = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.house.house_type} | {self.house.real_estate.name} - Weights"


class Criteria(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return f"{self.name}"


class SubCriteria(models.Model):
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True, null=False)

    def __str__(self):
        return f"{self.name}"


class SubCriteriaWeight(models.Model):
    sub_criteria = models.OneToOneField(SubCriteria, on_delete=models.CASCADE)
    weight = models.IntegerField(null=False)

    def __str__(self):
        return f"{self.sub_criteria.name}"