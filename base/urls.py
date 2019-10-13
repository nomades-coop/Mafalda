from django.conf import settings
from django.urls import path, include

from base.views import (ProductView, CreateProductView, CompanyView, CreateCompanyView,
                        CreateParametersView, ParametersView, PresupuestoView, CreatePresupuestoView,
                        ClientView, CreateClientView, DetailsPresupuestoView)
# from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('products/', ProductView.as_view(), name='products'),
    path('product/create/', CreateProductView.as_view()),

    path('parameters/', ParametersView.as_view()),
    path('parameters/create/', CreateParametersView.as_view()),

    path('company/', CompanyView.as_view()),
    path('company/create/', CreateCompanyView.as_view()),

    path('presupuesto/', PresupuestoView.as_view()),
    path('presupuesto/create/', CreatePresupuestoView.as_view({'post':'create'})),
    path('presupuesto/<int:pk>/',DetailsPresupuestoView.as_view()),

    path('client/', ClientView.as_view()),
    path('client/create/', CreateClientView.as_view()),

    # path('get-token/', obtain_auth_token)
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns