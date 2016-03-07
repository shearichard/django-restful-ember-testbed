import datetime 

from django.db import models
from django.contrib.auth.models import User


class Reference(models.Model):
    '''
    Further information about a species
    '''
    url = models. URLField(max_length=1024)

    def __str__(self): 
        return self.url 

class Image(models.Model):
    '''
    Image showing the species
    '''
    url = models.URLField(max_length=1024)

    def __str__(self): 
        return self.url 

class CommonName(models.Model):
    '''
    Names other than the binomial_nomenclature
    applies to this Species
    '''
    name = models.CharField(max_length=200)

    def __str__(self): 
        return self.name

class Use(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self): 
        return self.name

class Subspecies(models.Model):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name_plural = "subspecies"

    def __str__(self): 
        return self.name

class Range(models.Model):
    '''
    Locations where the plant is found to grow naturally
    '''
    AFRICA = 'AF'
    ANTARCTICA = 'AN'
    ASIA = 'AS'
    EUROPE = 'EU'
    NORTHAMERICA = 'NA'
    OCEANIA = 'OC'
    SOUTHAMERICA = 'SA'
    OTHER = 'OT'

    CONTINTENT_CHOICES = (
        (AFRICA , 'Africa'),
        (ANTARCTICA , 'Antartica'),
        (ASIA , 'Asia'),
        (EUROPE , 'Europe'),
        (NORTHAMERICA , 'North America'),
        (OCEANIA , 'Oceania'),
        (OTHER , 'Other'),
    )

    continent = models.CharField(max_length=2,
                                 choices=CONTINTENT_CHOICES,
                                 default=OTHER)
    place_description = models.CharField(max_length=200)

    def __str__(self): 
        return "{} ({})".format(self.place_description, 
                                self.continent)


class Species(models.Model):
    '''
    A Species of plant
    '''
    binomial_nomenclature = models.CharField(max_length=200)
    subspecies = models.ForeignKey(Subspecies, blank=True, null=True)
    common_name = models.ManyToManyField(CommonName, blank=True)
    height_and_spread = models.CharField(max_length=100)
    range = models.ManyToManyField(Range, blank=True)
    use = models.ManyToManyField(Use, blank=True)
    further_reference = models.ManyToManyField(Reference, blank=True)
    image = models.ManyToManyField(Image, blank=True)
    created = models.DateTimeField(editable=False)
    modified = models.DateTimeField(editable=False)

    class Meta:
        verbose_name_plural = "species"
        permissions = (
            ("display_details_species_", "Can view details of a Species"),
        )

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = datetime.datetime.today()
        self.modified = datetime.datetime.today()
        return super(__class__, self).save(*args, **kwargs)

    def __str__(self): 
        return "{}".format(self.binomial_nomenclature) 

    @property
    def name(self): 
        return "{}".format(self.binomial_nomenclature) 

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    favourite_rose = models.ForeignKey(Species, blank=True, null=True)

    def __str__(self):
        return self.user.username

'''
from django.contrib.auth.models import AbstractUser
class UserProfile(AbstractUser):
    favourite_rose = models.ForeignKey(Species, blank=True, null=True)
from django.contrib.auth.models import AbstractUser
'''

