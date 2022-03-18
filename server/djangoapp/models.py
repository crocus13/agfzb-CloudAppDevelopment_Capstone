from django.db import models
from django.utils.timezone import now
# from django.conf import settings
# import uuid


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    # CharField for Name
    name = models.CharField(null=False, max_length=30, default='Honda ')
    # CharField for Description
    description = models.CharField(null=False, max_length=200, default='Fuel efficient')

    def __str__(self):
        return "Name: " + self.name + ", " + "Description: " + self.description

    id = models.AutoField(primary_key=True) 







# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object

class CarModel(models.Model):
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon')
    ]
    name = models.CharField(null=False, max_length=50, default='850')
    carMake = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    dealerId = models.IntegerField()
    type = models.CharField(null=False, max_length=20, choices=TYPE_CHOICES, default=SEDAN)
    year = models.DateField(null=True)

    def __str__(self):

        return "Name: " + self.name + "," + \
            "CarMake: " + str(self.carMake) + "," + \
            "DealerId: " + str(self.dealerId) + "," + \
            "Type: " + self.type + "," + \
            "Year: " + str(self.year)

    id = models.AutoField(primary_key=True) 



# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, state,id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer st
        self.st = st
        # Dealer zip
        self.zip = zip
        # Dealer state
        self.state = state

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
