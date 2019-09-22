from django.urls import path

from base.views import (ProductView, CreateProductView, CompanyView, CreateCompanyView,
                        CreateParametersView, ParametersView, PresupuestoView, CreatePresupuestoView, ClientView, CreateClientView)
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('products/', ProductView.as_view(), name='products'),
    path('product/create/', CreateProductView.as_view()),

    path('parameters/', ParametersView.as_view()),
    path('parameters/create/', CreateParametersView.as_view()),

    path('company/', CompanyView.as_view()),
    path('company/create/', CreateCompanyView.as_view()),

    path('presupuesto/', PresupuestoView.as_view()),
    path('presupuesto/create/', CreatePresupuestoView.as_view()),

    path('client/', ClientView.as_view()),
    path('client/create/', CreateClientView.as_view()),

    path('get-token/', obtain_auth_token)
]
