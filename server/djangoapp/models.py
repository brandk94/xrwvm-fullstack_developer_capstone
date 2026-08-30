# Uncomment the following imports before adding the Model code

from django.db import models
from django.utils.timezone import now
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(max_length=100) # name of car make
    description = models.TextField() # extended description of car make

    def __str__(self):
    # Formatted string representing car make entry
        string = """
        Name: {name}, 
        Description: {description}
        """.format(
            name=self.name, description=self.description
        )
        return string


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many
# Car Models, using ForeignKey field)
# - Name
# - Type (CharField with a choices argument to provide limited choices
# such as Sedan, SUV, WAGON, etc.)
# - Year (IntegerField) with min value 2015 and max value 2023
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE) # Many-to-One relationship
    name = models.CharField(max_length=100)
    CAR_TYPES = [
        ('SEDAN', 'Sedan'),
        ('SUV', 'SUV'),
        ('WAGON', 'Wagon'),
        ('TRUCK', 'Truck'),
    ]
    type = models.CharField(max_length=10, choices=CAR_TYPES, default='SUV')
    year =  models.IntegerField(default=2026,
        validators = [
            MaxValueValidator(2026),
            MinValueValidator(2015)
        ]
    )

    def __str__(self):
    # Formatted string representing car model entry
        string = """
        Car Make: {make},
        Name: {name},
        Type: {type},
        Year: {year},
        """.format(
            make=self.car_make, name=self.name, 
            type=self.type, year=self.year
        )
        return string

