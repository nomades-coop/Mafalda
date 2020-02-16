from django.conf import settings
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from rest_framework_swagger.views import get_swagger_view

from .views import (
    PresupuestoView,
    ParametersView,
    ProductView,
    ClientView,
    search_view,
    drop_auth_token
)


schema_view = get_swagger_view(title='Mafalda API')

router = DefaultRouter()
router.register(r'presupuesto', PresupuestoView, basename='Presupuesto')
router.register(r'parameter', ParametersView)
router.register(r'product', ProductView, basename='Product')
router.register(r'client', ClientView, basename='Client')
# router.register(r'employee', EmployeeView)
# router.register(r'company', CompanyView)


urlpatterns = [
    path('docs', schema_view),
    path('', include(router.urls)),
    path('search/', search_view, name='search_view'),
    path('get-token/', obtain_auth_token),
    path('drop-token/', drop_auth_token, name='drop_auth_token'),
]
