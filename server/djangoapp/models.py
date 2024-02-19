from django.db import models
from django.utils.timezone import now

class CarMake(models.Model): 
    #Car Make/Manufacturer model
    name = models.CharField(max_length=20) 
    description = models.TextField()
    country = models.CharField(max_length=20)
    #A manufacturers can have one parent manufacturer
    parentcompany = models.ForeignKey('self', null= True, on_delete=models.CASCADE)

    def __str__(self):
        #return object string representation (name, parent company (if one), country, description)
        return "Name: " + self.name + "," +\
            "Parent Company: " + self.parentcompany + "," +\
            "Country: " + self.Country + "," +\
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
        (HFD, 'Hatchback (5DR)')
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
        (CVS, 'Continually Variable Speed (CVS)'),
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

    name = models.CharField(max_length=50)  
    year = models.PositiveInteger(validators=[MinValueValidator(1900, message="Henry Ford's Model T was one of the first mass production automobiles ever and was delivered to it's first customer in 1908. Please input a production year later than 1900.")])
    engine = models.CharField(max_length=50)
    description = models.TextField()
    
    bodytype = models.CharField(
        max_length=20,
        choices=BODY_TYPE_CHOICES,
        default=SEDAN
    )
    transmissiontype = moels.CharField(
        max_length=15,
        choices=TRANSMISSION_TYPES_CHOICES,
        default=AUTO
    )

    make = models.ForeignKey(CarMake, null=false, on_delete=models.CASCADE)
    
    
    def __str__(self):
        #return object string representation (name, make, body type, year, engine, transmission, description)
        return "Name: " + self.name + "," +\
            "Make: " + self.make + "," +\
            "Body Type: " + self.bodytype + "," +\
            "Year: " + self.year + "," +\
            "Engine: " + self.engine + "," +\
            "Transmission: " + self.transmissiontype + "," +\
            "Description: " + self.description





# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
