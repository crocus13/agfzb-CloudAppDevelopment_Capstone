from django.db import models

from django.core import serializers

from django.utils.timezone import now

import uuid

import json


# from django.conf import settings


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object

# class CarMake(models.Model):
#     # CharField for Name
#     name = models.CharField(null=False, max_length=100, default='Make')
#     # CharField for Description
#     # description = models.CharField(null=False, max_length=500, default='Fuel efficient')
#     description = models.CharField(max_length=500)

#     def __str__(self):
#         return "Name: " + self.name + ", " + \
#             "Description: " + self.description

    # id = models.AutoField(primary_key=True) 



class CarMake(models.Model):
    id = models.IntegerField(default=1,primary_key=True)
    name = models.CharField(null=False, max_length=100, default='Make') 
    description = models.CharField(max_length=500)

    def __str__(self):
        return "Name: " + self.name




# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

# class CarModel(models.Model):
#     SEDAN = 'Sedan'
#     SUV = 'SUV'
#     WAGON = 'Wagon'
#     TYPE_CHOICES = [
#         (SEDAN, 'Sedan'),
#         (SUV, 'SUV'),
#         (WAGON, 'Wagon')
#     ]
#     carMake = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
#     name = models.CharField(null=False, max_length=50, default='850')
#     # carmake = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
#     dealerId = models.IntegerField(null=True)
#     # dealerId = models.IntegerField()

#     type = models.CharField(null=False, max_length=50, choices=TYPE_CHOICES, default=SEDAN)
#     year = models.DateField(null=True)

#     def __str__(self):

#         return  "Name: " + self.name + ", " + \
#             "CarMake: " + str(self.carMake) + ", " + \
#             "DealerId: " + str(self.dealerId) + ", " + \
#             "Type: " + self.type + ", " + \
#             "Year: " + str(self.year)

#     id = models.AutoField(primary_key=True) 



class CarModel(models.Model): 
    id = models.IntegerField(default=1,primary_key=True)
    name = models.CharField(null=False, max_length=100, default='Car')

    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    MINIVAN = 'Minivan'
    CAR_TYPES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        (MINIVAN, 'Minivan')
    ]

    type = models.CharField(null=False,max_length=50,choices=CAR_TYPES,default=SEDAN)
    make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    year = models.DateField(default=now)

    def __str__(self):
        return "Name: " + self.name



# <HINT> Create a plain Python class `CarDealer` to hold dealer data
# class CarDealer:

    # def __init__(self, address, city, full_name, state,id, lat, long, short_name, st, zip):
    #     # Dealer address
    #     self.address = address
    #     # Dealer city
    #     self.city = city
    #     # Dealer Full Name
    #     self.full_name = full_name
    #     # Dealer id
    #     self.id = id
    #     # Location lat
    #     self.lat = lat
    #     # Location long
    #     self.long = long
    #     # Dealer short name
    #     self.short_name = short_name
    #     # Dealer st
    #     self.st = st
    #     # Dealer zip
    #     self.zip = zip
    #     # Dealer state
    #     self.state = state

    # def __str__(self):
    #     return "Dealer name: " + self.full_name + "," + \
    #         "address: " + self.address + "," + \
    #         "city: " + self.city + "," + \
    #         "id: " + self.id + "," + \
    #         "lat: " + self.lat + "," + \
    #         "long: " + self.long + "," + \
    #         "short_name: " + self.short_name + "," + \
    #         "st: " + self.st + "," + \
    #         "zip: " + self.zip + "," + \
    #         "state: " + self.state

class CarDealer:

    def __init__(self, address, city, id, lat, long, st, zip, full_name):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city

        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long

        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

        # Full name
        self.full_name = full_name

    def __str__(self):
        return "Dealer name: " + self.full_name






# <HINT> Create a plain Python class `DealerReview` to hold review data
# class DealerReview:
#     def __init__(self, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year, sentiment):
#         self.name = name
#         self.dealership = dealership
#         self.review = review
#         self.purchase = purchase
#         self.purchase_date = purchase_date
#         self.car_make = car_make
#         self.car_model = car_model
#         self.car_year = car_year
#         self.sentiment = sentiment

#     def __str__(self):
#         return "Review: " + self.review

class DealerReview:

    def __init__(self, dealership, name, purchase, review):
        # Required attributes
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        # Optional attributes
        self.purchase_date = ""
        # self.purchase_date = purchase_date

        self.purchase_make = ""
        self.purchase_model = ""
        self.purchase_year = ""
        self.sentiment = ""
        self.id = ""

    def __str__(self):
        return "Review: " + self.review

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)


class ReviewPost:

    def __init__(self, dealership, name, purchase, review):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = ""
        # self.purchase_date = purchase_date

        self.car_make = ""
        self.car_model = ""
        self.car_year = ""

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                            sort_keys=True, indent=4)
