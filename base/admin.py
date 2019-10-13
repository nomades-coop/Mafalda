from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Company, Parameters, Product, Client, Presupuesto, Employee, Item

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False


class EmployeeAdmin(admin.ModelAdmin):
    model = Employee
admin.site.register(Employee, EmployeeAdmin)


# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ParametersAdmin(admin.ModelAdmin):
    model = Parameters
admin.site.register(Parameters, ParametersAdmin)


class ItemAdmin(admin.ModelAdmin):
    model = Item
admin.site.register(Item, ItemAdmin)


class ItemInline(admin.TabularInline):
    model = Item
    extra = 1


class PresupuestoAdmin(admin.ModelAdmin):
    inlines = [ItemInline]
admin.site.register(Presupuesto, PresupuestoAdmin)


class ProductAdmin(admin.ModelAdmin):
    model = Product
admin.site.register(Product,ProductAdmin)


class ClientAdmin(admin.ModelAdmin):
    model = Client
admin.site.register(Client,ClientAdmin)


class CompanyAdmin(admin.ModelAdmin):
    model = Company
admin.site.register(Company,CompanyAdmin)
