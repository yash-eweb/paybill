from django.shortcuts import render , redirect ,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from . models import Bill


# Create your views here.
def register(request):
    if request.method == 'POST':
        username =  request.POST['username']
        password =  request.POST['password']
        confirm_password  = request.POST['password_confirm']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        if password == confirm_password:
            user = User.objects.create_user(username=username , password=password)
            user.save()
            messages.success(request ,'Registration Successful')
            return redirect('login')
        else:
            messages.error(request , "Password do not match")
            return redirect('register')
    return render(request,'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request , username =username , password=password)
        if user is not None:
            login(request , user)
            return redirect('home')
        else:
            messages.error(request,'Invalid Username or Password')
            return redirect('login')
    return render(request , 'login.html')

def home(request):
    bill = Bill.objects.all()
    if not request.user.is_authenticated:
        return redirect('login')  # If not authenticated, redirect to login
    return render(request, 'home.html' ,{'bill':bill})  # Home page for logged-in users


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
        return redirect('home')  # Redirect to a success page or another view

    return render(request, 'billform.html')



        