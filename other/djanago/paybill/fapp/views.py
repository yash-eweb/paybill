from django.shortcuts import render , redirect ,HttpResponse ,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from . models import Bill , Notification , Expense ,Group ,GroupBalance ,GroupExpense,GroupMember
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from decimal import Decimal

# for Admin Notification 
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.decorators import user_passes_test
from . models import Bill , Notification
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from datetime import timedelta
from django.utils import timezone
from .models import Bill, Notification
from django.contrib.auth.models import User

# https://www.uvicorn.org/

'''

<!--
-> pythonanywhere.com
-> paybill
-> file_paybill

mysql
file_mysql

-->

'''

@login_required
def allop(request):
    return render(request ,'allop.html')


# Create your views here.
def register(request):

    if request.user.is_authenticated:
        messages.info(request ,'You are already logged in!')

        return redirect('allop')

    if request.method == 'POST':
        username =  request.POST['username']
        password =  request.POST['password']
        confirm_password  = request.POST['password_confirm']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')
      
      # Create a new user
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('login')
    return render(request,'register.html')


def login_view(request):

    if request.user.is_authenticated:
        messages.info(request ,'You are already logged in!')

        return redirect('allop')


    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request , username =username , password=password)
        if user is not None:
            login(request , user)

            return redirect('allop')
        else:
            me = messages.error(request, 'Invalid Username or Password')
            print(me)
            return redirect('login')
    return render(request , 'login.html')

@login_required
def home(request):
    bill = Bill.objects.filter(user =request.user)
    if not request.user.is_authenticated:
        return redirect('login')  # If not authenticated, redirect to login
    return render(request, 'home.html' ,{'bill':bill})  # Home page for logged-in users

@login_required
def addbill(request):
    if request.method =='POST':
        user =request.user
        bill_name =request.POST.get('bill_name')
        amount = request.POST.get('amount')
        warranty_status = request.POST.get('warranty_status')
        expiry_date = request.POST.get('expiry_date') or None  # None if empty
        remember_expiry_date = request.POST.get('remember_expiry_date') == 'on'
        file_path = request.FILES.get('file_path')

        # Validation: Ensure proper handling based on warranty_status and expiry_date
        if warranty_status == "under_warranty" and not expiry_date:
            return HttpResponse("Expiry date is required for bills under warranty.")

        if warranty_status == "expired" and not remember_expiry_date and not expiry_date:
            return HttpResponse("Please provide an expiry date or select 'I don’t remember the expiry date.'")

        if warranty_status == "expired" and remember_expiry_date and expiry_date:
            return HttpResponse("Expiry date should not be provided if you don’t remember it.")
        

        Bill.objects.create(
            user =user,
            bill_name=bill_name,
            amount=amount,
            warranty_status=warranty_status,
            expiry_date=expiry_date,
            remember_expiry_date=remember_expiry_date,
            file_path=file_path
        )
        messages.success(request ,'Bill added successfully') 
        return redirect('home')
    

    return render(request, 'billform.html')

@login_required
def update(request ,pk):
    bill_data =get_object_or_404(Bill ,pk=pk)
    print(bill_data)

    if request.method == 'POST':
        bill_name =request.POST.get('bill_name')
        amount = request.POST.get('amount')
        warranty_status =request.POST.get('warranty_status')
        expiry_date=request.POST.get('expiry_date') or None
        remember_expiry_date =request.POST.get('remember_expiry_date')== 'on'
        # uploaded_date=request.POST.get('uploaded_date')
        file_path=request.FILES.get('file_path')

        bill_data.bill_name= bill_name
        bill_data.amount=amount
        bill_data.warranty_status = warranty_status
        bill_data.expiry_date = expiry_date 
        bill_data.remember_expiry_date = remember_expiry_date
        # bill_data.uploaded_date =uploaded_date
        
        if file_path:
            bill_data.file_path = file_path
        
        bill_data.save()
        messages.success(request ,'Bill updated successfully')
        return redirect('home')
    
    return render(request ,'update.html', {'bill':bill_data})

@login_required
def exupdate(request, pk):
    exp=get_object_or_404(Expense ,pk=pk )

    if request.method == 'POST':
        category =request.POST.get('category')
        amount =request.POST.get('amount')
        date =request.POST.get('date')
        description =request.POST.get('description')

        exp.category =category 
        exp.amount = amount 
        exp.date = date 
        exp.description = description

        exp.save()

        messages.success(request , 'Expense updated successfully.')
        return redirect('allexpense')

    return render(request ,'exupdate.html', {'ex':exp})

@login_required
def exdelete(request, pk):
    ex =get_object_or_404(Expense ,pk=pk)

    ex.delete()

    messages.success(request,  'Expense deleted successfully.')

    return redirect('allexpense')
    
    # return render(request ,'exdelete.html' ,{'data':ex})



@login_required
def delete(request,pk):
    data = get_object_or_404(Bill , pk=pk)
    
    data.delete()

    messages.success(request ,"Bill deleted successfully.")
    
    return redirect('home')

    

@login_required
def user_notifications(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'notifications.html', {'notifications': notifications})

# Mark notification as read
@login_required
def mark_notification_as_read(request,id):
    notification = get_object_or_404(Notification, id=id, user=request.user)
    # notification = Notification.objects.get(id=id, user=request.user)
    notification.is_read = True
    notification.save()
        
    # return render(request ,'notifications.html')
    return redirect(    'notifications')

@login_required
def allexpense(request):
    # today = date.today()
    # print(today)

    expense = Expense.objects.filter(user = request.user)
                                 
    return render(request,'all_expense.html' , {'expense':expense})

@login_required
def addexpense(request):
    if request.method =='POST':
        category=request.POST.get('category')
        amount = request.POST.get('amount')
        date = request.POST.get('date')
        description = request.POST.get('description')

        expense = Expense(
                user=request.user,  # Assuming the user is logged in
                category=category,
                amount=amount,
                date=date,
                description=description,
            )
        expense.save()
        return redirect('allexpense')
    return render(request ,'addexpense.html')

# _______________Group Functionality_______________

@login_required
def create_group(request) :
    if request.method =='POST':

        group_name =request.POST['group_name']

        if Group.objects.filter(group_name=group_name).exists():
            messages.error(request, 'Group Already Exists')
            return redirect('create_group')
        group = Group.objects.create(group_name = group_name , created_by=request.user)
        GroupMember.objects.create(group =group, user =request.user)

        # return redirect('group_detail', group_id=group.id)
        return redirect('allgroup')
    
    return render(request,'Group/create_group.html')

@login_required
def add_member(request, id):
    if request.method == "POST":
        username = request.POST['username']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, f"member '{username}' does not exist.")
            return redirect('add_member', id=id)

       
        group = get_object_or_404(Group, id=id)
        if GroupMember.objects.filter(group=group , user=user).exists():
            messages.warning(request, f"{username} is already  a member  of this group.")
        else:
            GroupMember.objects.create(group=group, user=user)
            messages.success(request, f"{username} has been added to the group.")
            return redirect('group_detail',id=id)

    return render(request, 'Group/add_member.html', {'group_id': id})

@login_required
def add_group_expense(request, id):
    if request.method == "POST":
        # amount = float(request.POST['amount'])
        amount = Decimal(request.POST['amount'])  # Use Decimal instead of float
        # amount = Decimal(request.POST.get('amount'))  # Convert from string/float to Decimal
        category = request.POST['category']
        paid_by_user_id = request.POST['paid_by_user']
        description = request.POST['description']
        date = request.POST['date']

        group = Group.objects.get(id=id)
        paid_by_user = User.objects.get(id=paid_by_user_id)
        members = GroupMember.objects.filter(group=group)

        # Add expense to GroupExpense
        GroupExpense.objects.create(
            group=group, 
            amount=amount, 
            category=category, 
            paid_by_user=paid_by_user, 
            description=description, 
            date=date
        )

        # Calculate balances
        per_person_share = Decimal(amount) / Decimal(len(members))
        for member in members:
            balance_entry, created = GroupBalance.objects.get_or_create(group=group, user=member.user)

            # Ensure balance is explicitly converted to Decimal
            balance_entry.balance = Decimal(balance_entry.balance)  # If not already a Decimal


            if member.user == paid_by_user:
                balance_entry.balance += Decimal(amount) - Decimal(per_person_share)  # Explicitly convert to Decimal
            else:
                balance_entry.balance -= per_person_share  # Explicitly convert to Decimal
            
            balance_entry.save()

        return redirect('group_detail', id=id)
        

    group = Group.objects.get(id=id)
    members = GroupMember.objects.filter(group=group)
    return render(request, 'Group/add_group_expense.html', {'group': group, 'members': members})
  

'''# @login_required
def group_detail(request, id):
    group = get_object_or_404(Group, id=id)
    members = GroupMember.objects.all()
    expenses = GroupExpense.objects.filter(group=group)
    balances = GroupBalance.objects.filter(group=group)

    # Check if the current user is the creator/admin of the group
    is_admin = group.created_by == request.user

    # Calculate the total expense
    total_expense = sum(expense.amount for expense in expenses)
    share_per_person = Decimal(total_expense) / Decimal(len(members)) if members else Decimal(0)

    # Check if the user is a member of the group
    is_member = GroupMember.objects.filter(group=group, user=request.user).exists()
    
    if not is_member:
        return HttpResponseForbidden("You are not a member of this group.")


    # Calculate each member's balance
    balances = []
    for member in members:
        paid_by_member = sum(expense.amount for expense in expenses if expense.paid_by_user == member)
        balance = Decimal(paid_by_member) - share_per_person
        balances.append({'user': member, 'balance': balance})

    # Separate payers (owe money) and receivers (are owed money)
    payers = [b for b in balances if b['balance'] < 0]
    receivers = [b for b in balances if b['balance'] > 0]

    # Create transactions to settle balances
    transactions = []

    for payer in payers:
        while payer['balance'] < 0 and receivers:
            receiver = receivers[0]
            amount_to_pay = min(abs(payer['balance']), receiver['balance'])

            transactions.append({
                'from': payer['user'].username,
                'to': receiver['user'].username,
                'amount': round(amount_to_pay, 2),
            })

            # Update balances
            payer['balance'] += amount_to_pay
            receiver['balance'] -= amount_to_pay

            # Remove settled receivers
            if receiver['balance'] == 0:
                receivers.pop(0)
    context = {
        'g': group,
        'members': members,
        'expenses': expenses,
        'transactions': transactions,  # Pass the transactions to the template
        'is_admin': is_admin,  # Pass whether the user is admin or not
        'balances': balances
    }
    return render(request, 'Group/group_detail.html', context)
'''
        


from django.shortcuts import render, get_object_or_404
from .models import Group, GroupMember, GroupExpense
from decimal import Decimal
import networkx as nx
import logging

logger = logging.getLogger(__name__) 


@login_required
def group_detail(request, id):
    group = get_object_or_404(Group, id=id)
    members = GroupMember.objects.filter(group=group)
    expenses = GroupExpense.objects.filter(group=group)

    # Calculate total expense and per-member share
    total_expense = sum(Decimal(expense.amount) for expense in expenses)
    num_members = members.count()
    per_member_share = total_expense / Decimal(num_members) if num_members > 0 else Decimal(0)

    # Track payments by each member
    payments = {member.user: Decimal(0) for member in members}
    for expense in expenses:
        payments[expense.paid_by_user] += Decimal(expense.amount)

    # Calculate balances (how much each member owes or is owed)
    balances = {}
    for member in members:
        balances[member.user] = payments[member.user] - per_member_share


    # Create a settlement plan (simplified for this specific scenario)
    settlement_plan = []
    for member in members:
        if balances[member.user] < 0:# Only consider members who owe money
            # Find creditors (members with positive balances)
             for creditor, balance in balances.items():
                if balance > 0:
                    amount = min(abs(balances[member.user]), balance)
                    settlement_plan.append({
                        'debtor': member.user,
                        'creditor': creditor,
                        'amount': amount,
                    })
                    # Update balances after settlement
                    balances[member.user] += amount
                    balances[creditor] -= amount
                    if balances[member.user] >= 0:
                        break


    # change the last 
    # Create a settlement plan (simplified for this specific scenario)
    '''settlement_plan = []
    for member in members:
        if member.user != expense.paid_by_user and balances[member.user] < 0:

            #  if balances[member.user] < 0: in production

            settlement_plan.append({
                'debtor': member.user,
                'creditor': expense.paid_by_user,
                'amount': abs(balances[member.user])
            })'''
    # change the last 
            
    # Render the template with the settlement plan
    return render(request, 'Group/group_detail.html', {
        
        'g': group,
        # 'members': members,
        'members': len(members) if isinstance(members, list) else members,
        'expenses': expenses,
        'balances': balances.items(),
        'settlement_plan': settlement_plan,
        'per_member_share': per_member_share,
        'total_expense': total_expense,
    })




@login_required
def allgroup(request):

    user_group=GroupMember.objects.filter(user=request.user).values_list('group' , flat=True)

    # group = Group.objects.all()
    group = Group.objects.filter(id__in=user_group)

    return render(request,'Group/allgroup.html', {'group':group})

@login_required
def update_group_name(request,id):
    group = get_object_or_404(Group , id=id)

    if request.user  == group.created_by:
        new_group_name= request.POST.get('group_name')
        if new_group_name:
            group.group_name = new_group_name
            group.save()
            return redirect('group_detail', id =group.id)
    else:
        return redirect('allgroup')
    #     # If the user is not the admin, return a message or redirect
    #     return render(request, 'error.html', {'message': 'You do not have permission to change the group name.'})


# -------------------------   Admin Side  -------------------------------------------------------------
@user_passes_test(lambda u:u.is_superuser)
def admin_send_notification(request):
    today = timezone.now().date()
    five_days_from_now = today + timedelta(days=5)

    bills =Bill.objects.filter(expiry_date_lte = five_days_from_now ,expiry_date_gte = today)
    
    for bill in bills:
        if not Notification.objects.filter(user=bill.user, message_contains=bill.bill_name).exists():
            message =f"Reminder: Your bill for {bill.bill_name} is expiring soon on {bill.expiry_date}. "
            notification =Notification.objects.create(user=bill.user , message =message)

            # Mark admin has sent notification
            notification.admin_notified =True
            notification.save()

    return redirect('admin_dashboard')

@user_passes_test(lambda u:u.is_superuser)
def admin_notification(request):
    notification= Notification.objects.all()

    return render(request ,'admin/notification_status.html' ,{'notifications':notification})


@user_passes_test(lambda u: u.is_superuser)
def resend_notification(request, notification_id):
    notification = Notification.objects.get(id=notification_id)
    if not notification.is_read:
        # Create a new notification for the same user
        new_message = f"Reminder: Your bill for {notification.message} is expiring soon."
        Notification.objects.create(user=notification.user, message=new_message)
    return redirect('admin_notification_status')

# Automatic message send
'''
from celery import shared_task

@shared_task
def check_and_resend_unread_notifications():
    today = timezone.now().date()
    # Check for unread notifications
    notifications = Notification.objects.filter(is_read=False, created_at__lte=today - timedelta(days=2))
    for notification in notifications:
        # Resend the notification
        new_message = f"Reminder: Your bill for {notification.message} is expiring soon."
        Notification.objects.create(user=notification.user, message=new_message)

'''