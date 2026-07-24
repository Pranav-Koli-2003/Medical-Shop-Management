from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Purchase_Company)
admin.site.register(Purchase_Medicine_data)
admin.site.register(Purchase_Medicine_bill_details)
admin.site.register(sell_medicine_details)
admin.site.register(sell_medicine_bills)