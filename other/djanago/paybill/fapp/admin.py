from django.contrib import admin
from . models import Bill

# Register your models here.
class BillAdmin(admin.ModelAdmin):
    list_display =('user','bill_name','amount','warranty_status','expiry_date','remember_expiry_date','uploaded_date','file_path')

def get_readonly_fields(self, request, obj=None):
        if obj and obj.warranty_status == 'expired':
            return ['expiry_date']
        return []

admin.site.register(Bill, BillAdmin)