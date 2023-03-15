"""
Master Admin
"""
# pylint: disable=E0401
from django.contrib import admin
from .models import DmsSetting, Company, Country, State,Designation, CustomerUser, Project, Plan, Checklist, ProductType, Category, Product,Customer,DroneAllocation,DashboardData,LogTemplate, DroneConfiguraion, ConsumptionLog

admin.site.register(DmsSetting)
admin.site.register(Company)
admin.site.register(Country)
admin.site.register(State)
admin.site.register(Designation)
admin.site.register(CustomerUser)
admin.site.register(Project)
admin.site.register(Plan)
admin.site.register(DashboardData)
admin.site.register(Checklist)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(ProductType)
admin.site.register(Customer)
admin.site.register(DroneAllocation)
admin.site.register(LogTemplate)
admin.site.register(DroneConfiguraion)
admin.site.register(ConsumptionLog)


# Register your models here.
