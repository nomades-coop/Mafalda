from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validar_cuit(cuit):
    # validaciones minimas
    if len(cuit) != 11 :
        return False

    base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

    # calculo el digito verificador:
    aux = 0
    for i in range(10):
        aux += int(cuit[i]) * base[i]

    aux = 11 - (aux - (int(aux / 11) * 11))

    if aux == 11:
        aux = 0
    if aux == 10:
        aux = 9

    return aux == int(cuit[10])

def cuit_validator(cuit):
    if validar_cuit(cuit) == False:
        raise ValidationError(
            _('%(cuit)s no es un cuit válido'),
            params={'cuit': cuit},
        )