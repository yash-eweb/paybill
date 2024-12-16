from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Bill(models.Model):
    user = models.ForeignKey("auth.user",on_delete=models.CASCADE)
    bill_name = models.CharField(max_length=500)
    amount = models.DecimalField(max_digits=10 , decimal_places=2)
    # due_date=models.DateField()
    warranty_status =models.CharField(
        max_length=50 ,
        choices=[('under_warranty', 'Under Warranty'),('expired', 'Expired')],
        default='expired'
    )
    expiry_date = models.DateField(null=True, blank=True)
    remember_expiry_date = models.BooleanField(default=False)  # Whether the user remembers the expiry date
    uploaded_date = models.DateTimeField(auto_now_add=True)
    file_path = models.FileField(upload_to="bills/")
    
    
    def __str__(self):
        return self.bill_name
    

