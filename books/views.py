from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def book_list(request):
    books=Books.objects.all()
    return render(request,'book_list.html',{'books':books})

@login_required
def book_details(request):
    book=Books.objects.all()
    reviews=book.reviews.all()
    avg_rating=book.average_rating()
    return render(request,'book_detail.html',{'book':book,'reviews':reviews,'avg_rating':avg_rating})


def add_books(request):
    pass
    

def edit_book(request):
    pass

def delete_book(request):
    pass

def add_review(request):
    pass

def edit_review(request):
    pass

def delete_review(request):
    pass


def login_page(request):

    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=User.objects.filter(username=username)

        if  not user.exists():
            messages.error(request, "Invalid Username")
            return redirect('login/')
        
        user=authenticate(username=username,password=password)

        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('login/')
        
        else:
            login(request,user)
            return redirect('booklist/')

    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('login/')

def register(request):

    if request.method=="POST":

        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        user_type=request.POST.get('user_type')
        email=request.POST.get('email')

        user=User.objects.filter(username=username)

        if user.exists():
            messages.info(request, "Username already taken")
            return redirect('register/')
            

        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            user_type=user_type
        )

        user.set_password(password)
        user.save()

        messages.info(request, "Account created")

        return redirect('register/')


    return render(request,'register.html')
   
   
