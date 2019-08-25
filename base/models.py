from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver

#TODO: chequear los onstraints de los campos
#TODO: chequear el formato de domicilio

class Company(models.Model):
    """This class represents the Company model."""
    name = models.CharField(max_length=255, blank=False)
    razon_social = models.CharField(max_length=255)
    commercial_address = models.CharField(max_length=255)
    #TODO: tambien chequear este largo
    iibb = models.CharField(max_length=25)
    iva_condition = models.CharField(max_length=75)
    cuit = models.CharField(max_length=13)
    activity_start_date = models.DateField()


    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)

class Parameters(models.Model):
    """This class represents the Parameters model."""
    surcharge = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.surcharge)


class Product(models.Model):
    """This class represents the product model."""
    name = models.CharField(max_length=255, blank=False)
    title = models.CharField(max_length=255)
    #TODO: chequear el largo del codigo
    product_code = models.CharField(max_length=13)
    wholesaler_code = models.CharField(max_length=13)
    #TODO: tambien chequear este largo
    iibb = models.CharField(max_length=25)
    iva =  models.DecimalField(max_digits=10, decimal_places=2, default=0)
    list_price= models.DecimalField(max_digits=10, decimal_places=2, default=0)
    surcharge = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    company_id = models.ForeignKey('Company', on_delete=models.CASCADE)
    #TODO: especificar el lugar a subir la foto
    picture = models.ImageField(upload_to=None)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)



class Client(models.Model):
    """This class represents the Client model."""
    CONTADO = 'CTD'
    CTA_CTE = 'CCT'
    CHOICES = ((CONTADO, 'contado'), (CTA_CTE, 'Cuenta corriente'))
    name_bussinessname = models.CharField(max_length=255, blank=False)
    commercial_address = models.CharField(max_length=255)
    #TODO: tambien chequear este largo
    cuit = models.CharField(max_length=13)
    iva_condition = models.CharField(max_length=75)
    sale_condition = models.CharField(max_length=3, choices=CHOICES, default=CONTADO)
    company_id = models.ForeignKey('Company', on_delete=models.CASCADE)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name_bussinessname)


class Presupuesto(models.Model):
    """This class represents the Presupuesto model."""
    date = models.DateField()
    product_id = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    #TODO: a ser determinado en la vista
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    #TODO: lo pongo en la vista, sacandolo del modelo producto?
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    #TODO: el descuento es un % o un monto?
    discounts = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.date)


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_id = models.ForeignKey('Company', on_delete=models.CASCADE)


# This receiver handles token creation immediately a new user is created.
@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
