from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.dispatch import receiver

#TODO: chequear los onstraints de los campos
#TODO: chequear el formato de domicilio

class Company(models.Model):
    """This class represents the Company model."""
    CONTADO = 'CTD'
    RESP_INSCR = 'RIN'
    CHOICES = ((CONTADO, 'contado'), (RESP_INSCR, 'Responsable Inscripto'))
    name = models.CharField(max_length=255, blank=False)
    razon_social = models.CharField(max_length=255)
    commercial_address = models.CharField(max_length=255)
    iibb = models.CharField(max_length=25)
    iva_condition =  models.CharField(max_length=3, choices=CHOICES, default=CONTADO)
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
    iibb = models.CharField(max_length=25)
    list_price= models.DecimalField(max_digits=10, decimal_places=2, default=0)
    surcharge = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True)
    iva_percentage = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    company_id = models.ForeignKey('Company', on_delete=models.CASCADE)
    #TODO: especificar el lugar a subir la foto, precio total
    picture = models.ImageField(upload_to=None, blank=True)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name)


class Client(models.Model):
    """This class represents the Client model."""
    CONTADO = 'CTD'
    CTA_CTE = 'CCT'
    CHOICES = ((CONTADO, 'Contado'), (CTA_CTE, 'Cuenta Corriente'))
    # TODO: elegir un nombre
    name_bussinessname = models.CharField(max_length=255, blank=False)
    commercial_address = models.CharField(max_length=255)
    cuit = models.CharField(max_length=11)
    #TODO: 2 opciones igual que compañia
    iva_condition = models.CharField(max_length=75)
    sale_condition = models.CharField(max_length=3, choices=CHOICES, default=CONTADO)
    company_id = models.ForeignKey('Company', on_delete=models.CASCADE)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.name_bussinessname)


class Presupuesto(models.Model):
    """This class represents the Presupuesto model."""
    date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    items = models.ManyToManyField(Product, through_fields=('presupuesto','product'),
                                          through='Item')
    #TODO: el descuento es un % del total
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_before_discounts = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_after_discounts = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        """Return a human readable representation of the model instance."""
        return "{}".format(self.date)


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
    # price = models.DecimalField(max_digits=10, decimal_places=2, default=0)


class Employee(models.Model):
    """This class represents the Employee model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_id = models.ForeignKey('Company', on_delete=models.CASCADE)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    """This receiver handles token creation immediately a new user is created."""
    if created:
        Token.objects.create(user=instance)
