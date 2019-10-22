from django.conf import settings
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from rest_framework_swagger.views import get_swagger_view

from base.views import (PresupuestoView, CompanyView,
                        ParametersView, ProductView,
                        ClientView, EmployeeView)

# from base.views import (ProductView, CreateProductView, CompanyView, CreateCompanyView,
#                         CreateParametersView, ParametersView, PresupuestoView, PresupuestoViewSet,
#                         ClientView, CreateClientView, DetailsPresupuestoView)
# from rest_framework.authtoken.views import obtain_auth_token

schema_view = get_swagger_view(title='Mafalda API')

router = DefaultRouter()
router.register(r'presupuesto', PresupuestoView)
router.register(r'company', CompanyView)
router.register(r'parameter', ParametersView)
router.register(r'product', ProductView)
router.register(r'client', ClientView)
router.register(r'employee', EmployeeView)


urlpatterns = [
    path('docs', schema_view),

    path('', include(router.urls)),
]

# urlpatterns = [
#     path('products/', ProductView.as_view(), name='products'),
#     path('product/create/', CreateProductView.as_view()),

#     path('parameters/', ParametersView.as_view()),
#     path('parameters/create/', CreateParametersView.as_view()),

#     path('company/', CompanyView.as_view()),
#     path('company/create/', CreateCompanyView.as_view()),

#     path('presupuesto/', PresupuestoViewSet.as_view({'get': 'list'})),
#     path('presupuesto/create/', PresupuestoView.as_view({'post':'create'})),
#     path('presupuesto/<int:pk>/',DetailsPresupuestoView.as_view()),

#     path('client/', ClientView.as_view()),
#     path('client/create/', CreateClientView.as_view()),

#     # path('get-token/', obtain_auth_token)
# ]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns