from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from utils.validators import cuit_validator

#TODO: chequear los onstraints de los campos
#TODO: chequear el formato de domicilio

class Company(models.Model):
    """This class represents the Company model."""
    CONTADO = 'CTD'
    RESP_INSCR = 'RIN'
    CHOICES = ((CONTADO, 'Contado'), (RESP_INSCR, 'Responsable Inscripto'))
    name = models.CharField(max_length=255, blank=False)
    razon_social = models.CharField(max_length=255)
    commercial_address = models.CharField(max_length=255)
    iibb = models.CharField(max_length=11)
    iva_condition =  models.CharField(max_length=3, choices=CHOICES, default=RESP_INSCR)
    cuit = models.CharField(max_length=11,validators=[cuit_validator])
    activity_start_date = models.DateField()

    class Meta(object):
        verbose_name_plural = 'Companies'

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)


class Parameters(models.Model):
    """This class represents the Parameters model."""
    surcharge = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta(object):
        verbose_name_plural = 'Parameters'

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.surcharge)

# TODO:manager del modelo para sobreescribir el método .objects.all(). que solo traiga los objetos
# de la compañia

# TODO: ver la logica del surcharge. ahora: si es 0 le pone el de parameters.
class Product(models.Model):
    """This class represents the product model."""
    name = models.CharField(max_length=255, blank=False)
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, blank=True, null=True)
    #TODO: chequear el largo del codigo
    product_code = models.CharField(max_length=13)
    wholesaler_code = models.CharField(max_length=13)
    iibb = models.CharField(max_length=25)
    list_price= models.DecimalField(max_digits=10, decimal_places=2)
    surcharge = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    iva_percentage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    #TODO: que es este company id? es un SaaS, de otra compañia no pueden ver el prod de la mia
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    #TODO: especificar el lugar a subir la foto, precio total
    # picture = models.ImageField(upload_to=None, blank=True, null=True)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)

    class Meta(object):
        ordering = ['name']


class Client(models.Model):
    """This class represents the Client model."""
    CONTADO = 'CTD'
    CTA_CTE = 'CCT'
    INSCR = 'INS'
    EXC = 'EXC'
    CF = 'CFI'
    CHOICES_SALE = ((CONTADO, 'Contado'), (CTA_CTE, 'Cuenta Corriente'))
    CHOICES_IVA = ((INSCR, 'Inscripto'), (EXC, 'Exento'), (CF, 'Consumidor Final'))
    # TODO: elegir un nombre
    name_bussinessname = models.CharField(max_length=255, blank=False)
    commercial_address = models.CharField(max_length=255)
    cuit = models.CharField(max_length=11,validators=[cuit_validator])
    iva_condition = models.CharField(max_length=3, choices=CHOICES_IVA,default=CF)
    sale_condition = models.CharField(max_length=3, choices=CHOICES_SALE, default=CONTADO)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name_bussinessname)
    
    class Meta(object):
        ordering = ['name_bussinessname']


class Presupuesto(models.Model):
    """This class represents the Presupuesto model."""
    date = models.DateField(auto_now_add=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(Product, through_fields=('presupuesto','product'),
                                          through='Item')
    #TODO: el descuento es un % del total. Aclararlo en el front
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_before_discounts = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_after_discounts = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='presupuestos')

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.date)

    class Meta(object):
        ordering = ['-date']

class Item(models.Model):
    """
    This class acts as an intermediate table for the many to many relationship between Product and Presupuesto models,
    and adds the quantity of the product field.
    """
    presupuesto = models.ForeignKey(Presupuesto, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Employee(models.Model):
    # TODO: cada user tiene que ser un employee. Extender elmodelo usuario para que tenga una fk a employee
    """This class represents the Employee model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey('Company', on_delete=models.CASCADE)

    class Meta(object):
        verbose_name_plural = 'Employee'


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """This receiver handles token creation immediately a new user is created."""
    if created:
        Token.objects.create(user=instance)
