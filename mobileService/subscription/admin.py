from django.contrib import admin
from .models import Number, Plan, Company, UserSubscription


admin.site.register(Number)
admin.site.register(Plan)
admin.site.register(Company)
admin.site.register(UserSubscription)
