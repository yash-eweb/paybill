from django.db import models
from django.core.exceptions import ValidationError
import datetime

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
    
    '''
    class Notification(models.Model):
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        message = models.TextField()
        is_read = models.BooleanField(default=False)
        created_at = models.DateTimeField(auto_now_add=True)
        # Optionally, you could track the admin action for resending notifications
        admin_notified = models.BooleanField(default=False)  # Admin mark when notification is sent

    def __str__(self):
        return self.message
    
    '''
    
class Notification(models.Model):
    user = models.ForeignKey("auth.user",on_delete=models.CASCADE)
    message =models.TextField()
    is_read = models.BooleanField(default=False)
    created_at =models.DateTimeField(auto_now_add=True)
    admin_notified =models.BooleanField(default=False) # Admin mark when notification is sent

    def __str__(self):
        return self.message
    
class Expense(models.Model):
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Petrol', 'Petrol'),
        ('Mobile Recharge', 'Mobile Recharge'),
        ('Traveling', 'Traveling'),
        ('Office Expense', 'Office Expense'),
        ('Other', 'Other'),
        ('Shopping', 'Shopping'),
    ]

    user = models.ForeignKey("auth.user",on_delete=models.CASCADE)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Other')
    amount = models.DecimalField(max_digits=10 , decimal_places=2)
    date=models.DateField(default= datetime.date.today)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    def __str__(self):
        return f"{self.category.name} - {self.amount} ({self.user.username})"

# Group Functionalitty

class Group(models.Model):
    group_name =models.CharField(max_length=255 , unique=True)
    created_by =models.ForeignKey("auth.user",on_delete=models.CASCADE)
    created_date= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group_name
    
class GroupMember(models.Model):
    group =models.ForeignKey(Group , on_delete=models.CASCADE)
    user = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    join_date =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} in {self.group.group_name}"
    
class GroupExpense(models.Model):
    group = models.ForeignKey(Group , on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category =models.CharField(max_length=200)
    paid_by_user =models.ForeignKey("auth.user", on_delete=models.CASCADE, related_name="paid_expenses")
    date = models.DateField(default=datetime.date.today)
    description = models.TextField(blank=True, null=True)

    SHARED = 1
    INDIVIDUAL = 0
    is_shared = models.IntegerField(choices=((SHARED, 'Shared'), (INDIVIDUAL, 'Individual')), default=SHARED) 

    participating_members = models.ManyToManyField(
        "GroupMember", related_name="participating_expenses", blank=True
    ) 

    def __str__(self):
        return f"{self.category} - {self.amount} in {self.group.group_name}"

class GroupBalance(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    user = models.ForeignKey("auth.user", on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2 ,default=0.0)  # Positive if owed, negative if owes

    class Meta:
        unique_together = ('group', 'user')  # Ensure one balance per user per group


    def __str__(self):
        return f"{self.user.username} balance in {self.group.group_name}: {self.balance}"