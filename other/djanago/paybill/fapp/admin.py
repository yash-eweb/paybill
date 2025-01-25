from django.contrib import admin
from . models import Bill , Notification , Expense, Group ,GroupMember,GroupBalance,GroupExpense
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from datetime import timedelta
from django.utils import timezone



# @admin.register(Bill)
class BillAdmin(admin.ModelAdmin):

    #for all understanding how work https://chatgpt.com/c/67625971-ec24-8001-bd11-ba797c7beab2

    list_display =('user','bill_name','amount','warranty_status','expiry_date','remember_expiry_date','uploaded_date','file_path')

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.warranty_status == 'expired':
            return ['expiry_date']
        return []
    
    actions = ['send_expiry_notifications']

    def send_expiry_notifications(self, request, queryset):
        # today = timezone.now().date()
        today = timezone.now().date()
        five_days_from_now = today + timedelta(days=5)

        bills = queryset.filter(expiry_date__lte=five_days_from_now, expiry_date__gte=today)
        
        for bill in bills:
            if not Notification.objects.filter(user=bill.user, message__contains=bill.bill_name).exists():
                message = f"Reminder: Your bill for {bill.bill_name} is expiring soon on {bill.expiry_date}."
                notification = Notification.objects.create(user=bill.user, message=message)

                # Mark admin as notified
                notification.admin_notified = True
                notification.save()
                self.message_user(request, "Notifications sent successfully.")
            else:
                self.message_user(request , "Notification Already Send")

        # self.message_user(request, "Notifications sent successfully.")
    send_expiry_notifications.short_description = "Send notification for expiring bills"

admin.site.register(Bill, BillAdmin )

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'admin_notified', 'created_at')
    list_filter = ('is_read', 'admin_notified')
    search_fields = ('user__username', 'message')

    # Add custom actions, if needed
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected notifications as read"
    
    actions = [mark_as_read]

admin.site.register(Notification, NotificationAdmin)

@admin.register(Expense)
class ExpeseAdmin(admin.ModelAdmin):
    list_display= ('user','category', 'amount', 'date', 'description')
    search_fields =('user__username', 'category', 'description')

# Group Functionality
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(GroupExpense)
admin.site.register(GroupBalance)