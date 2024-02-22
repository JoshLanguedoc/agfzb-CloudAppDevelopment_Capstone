from django.core.validators import MinValueValidator
from django.db import models
from django.utils.timezone import now

class CarMake(models.Model): 
    #Car Make/Manufacturer model
    name = models.CharField(max_length=20) 
    description = models.TextField()
    country = models.CharField(max_length=20)
    #A manufacturers can have one parent manufacturer
    parentcompany = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        #return object string representation (name, parent company (if one), country, description)
        return "Name: " + self.name + "," +\
            "Parent Company: " + str(self.parentcompany) + "," +\
            "Country: " + self.country + "," +\
            "Description: " + self.description

class CarModel(models.Model):
    #Car Model model
    
    #Variables for storing body type values
    BUG = 'buggy'
    CON = 'convertible'
    COU = 'coupe'
    FLO = 'flower car'
    HTD = 'hatchback3dr'
    HFD = 'hatchback5dr'
    HEA = 'hearse'
    LIM = 'limousine'
    MIC = 'microvan'
    MIN = 'minivan'
    PAN = 'panel van'
    PIC = 'pickup truck'
    ROA = 'roadster'
    SED = 'sedan'
    STA = 'station wagon'
    SUV = 'suv'

    BODY_TYPE_CHOICES = [ #list of (body type, human readable value)
        (BUG, 'Buggy'),
        (CON, 'Convertible'),
        (COU, 'Coupe'),
        (FLO, 'Flower Car'),
        (HTD, 'Hatchback (3DR)'),
        (HFD, 'Hatchback (5DR)'),
        (HEA, 'Hearse'),
        (LIM, 'Limousine'),
        (MIC, 'Microvan'),
        (MIN, 'Minivan'),
        (PAN, 'Panel Van'),
        (PIC, 'Pickup Truck'),
        (ROA, 'Roadster'),
        (SED, 'Sedan'),
        (STA, 'Station wagon'),
        (SUV, 'Sport Utility Vehicle (SUV)')
    ]
    
    #variables for stroing transmission type
    CVS = 'CVS'
    AUT = 'automatic'
    SEM = 'semiautomatic'
    ONE = '1speedmanual'
    TWO = '2speedmanual'
    THR = '3speedmanual'
    FOU = '4speedmanual'
    FIV = '5speedmanual'
    SIX = '6speedmanual'
    SEV = '7speedmanual'
    
    TRANSMISSION_TYPES_CHOICES = [ #list of (transmission types, human readable values)
        (CVS, 'Continously Variable (CVS/CVT)'),
        (AUT, 'Automatic'),
        (SEM, 'Semiautomatic (optional manual mode)'),
        (ONE, '1 Speed (Manual)'),
        (TWO, '2 Speed (Manual)'),
        (THR, '3 Speed (Manual)'),
        (FOU, '4 Speed (Manual)'),
        (FIV, '5 Speed (Manual)'),
        (SIX, '6 Speed (Manual)'),
        (SEV, '7 Speed (Manual)')
    ]

    FWD = 'frontwheeldrive'
    RWD = 'rearwheeldrive'
    AWD = 'allwheeldrive'
    IWD = '4wheeldrive'

    DRIVETRAIN_TYPES_CHOICES = [
        (FWD, "Front Wheel Drive (FWD)"),
        (RWD, "Rear Wheel Drive (RWD)"),
        (AWD, "All Wheel Drive (AWD)"),
        (IWD, "4 Wheel Drive (4WD)")
    ]

    ELC = 'electric'
    GAS = 'gas'
    DEI = 'Deisel'

    FUEL_TYPES_CHOICES = [
        (ELC, "Electric"),
        (GAS, "Gasoline"),
        (DEI, "Deisel")
    ]

    name = models.CharField(max_length=50)  
    year = models.PositiveIntegerField(validators=[MinValueValidator(1900, message="Henry Ford's Model T was one of the first mass production automobiles ever and was delivered to it's first customer in 1908. Please input a production year later than 1900.")])
    exteriorcolour = models.CharField(max_length=25)
    interiorcolour = models.CharField(max_length=25)
    mileage = models.PositiveIntegerField()
    engine = models.CharField(max_length=50)
    trimlevel = models.CharField(max_length=25)
    description = models.TextField()
    dealerid = models.IntegerField()
    
    bodytype = models.CharField(
        max_length=20,
        choices=BODY_TYPE_CHOICES,
        default=SED
    )

    transmissiontype = models.CharField(
        max_length=15,
        choices=TRANSMISSION_TYPES_CHOICES,
        default=AUT
    )

    drivetraintype = models.CharField(
        max_length=15,
        choices=DRIVETRAIN_TYPES_CHOICES,
        default=FWD
    )

    fueltype = models.CharField(
        max_length=15,
        choices=FUEL_TYPES_CHOICES,
        default=GAS
    )

    make = models.ForeignKey(CarMake, null=False, on_delete=models.CASCADE)
    
    def __str__(self):
        #return object string representation (name, make, body type, year, engine, transmission, description)
        return "Name: " + self.name + "," +\
            "Make: " + str(self.make) + "," +\
            "Trim Level: " + self.trimlevel + "," +\
            "Body Type: " + self.bodytype + "," +\
            "Year: " + str(self.year) + "," +\
            "Exterior Colour: " + self.exteriorcolour + "," +\
            "Interior Colour: " + self.interiorcolour + "," +\
            "Engine: " + self.engine + "," +\
            "Fuel Type: " + self.fueltype + "," +\
            "Transmission: " + self.transmissiontype + "," +\
            "Drive Train: " + self.drivetraintype + "," +\
            "Mileage: " + str(self.mileage) + "," +\
            "Description: " + self.description + "," +\
            "Dealer Id: " + str(self.dealerid)





class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReviews:
    
    def __init__(self, dealership, name, purchase, review, sentiment, id, purchase_date = "", car_make = "", car_model = "", car_year = ""):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id
    
    def __str__(self):
        return "Dealership: " + self.dealership + \
            "Review: "  + self.review


# <HINT> Create a plain Python class `DealerReview` to hold review data
