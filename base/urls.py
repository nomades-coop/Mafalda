from django.conf import settings
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_swagger.views import get_swagger_view

from .views import (PresupuestoView, CompanyView,
                        ParametersView, ProductView,
                        ClientView, EmployeeView)


schema_view = get_swagger_view(title='Mafalda API')

router = DefaultRouter()
router.register(r'presupuesto', PresupuestoView, basename='Presupuesto')
router.register(r'company', CompanyView)
router.register(r'parameter', ParametersView)
router.register(r'product', ProductView, basename='Product')
router.register(r'client', ClientView)
router.register(r'employee', EmployeeView)


urlpatterns = [
    path('docs', schema_view),
    path('', include(router.urls)),
    path('get-token/', obtain_auth_token)
]
