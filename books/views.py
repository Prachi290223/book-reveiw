from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from .forms import *

# Create your views here.

def book_list(request):
    books=Books.objects.all()
    return render(request,'book_list.html',{'books':books})

@login_required
def book_details(request,id):
    book=Books.objects.get(id=id)
    reviews=book.reviews.all()
    avg_rating=book.average_rating()
    return render(request,'book_detail.html',{'book':book,'reviews':reviews,'avg_rating':avg_rating})

@login_required
def add_book(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden('ONLY ADMIN CAN ADD BOOKS')
    
    if request.method=="POST":
        form=BookForm(request.POST,request.FILES)
        if form.is_valid():
            books=form.save()
            books.author=request.user
            return redirect("/")
    else:
        form=BookForm()

    return render(request,'add_book.html',context={'form':form})

@login_required
def edit_book(request,id):
    book=Books.objects.get(id=id)
    if request.user.user_type != 'admin':
        return HttpResponseForbidden('ONLY ADMIN CAN EDIT THIS BOOKS')

    if request.method=="POST": 
        form=BookForm(request.POST,request.FILES,instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_detail/")
    else:
        form=BookForm(instance=book)

    return render(request,'edit_book.html',{'form':form,'book':book})

    
@login_required
def delete_book(request,id):
    book=Books.objects.get(id=id)
    if request.user.user_type != 'admin':
        return HttpResponseForbidden('ONLY ADMIN CAN DELETE THIS BOOKS')

    if request.method=="POST":
        book.delete()
        return redirect("book_list/")


@login_required
def add_review(request,id):
    book=Books.objects.get(id=id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            review.user = request.user
            review.book = book
            review.save()
            return redirect('book_detail', id=id)
    else:
        form = ReviewForm()
    return render(request, 'review_page.html', {'form': form, 'book': book})

@login_required
def edit_review(request,id):
    review=Review.objects.get(id=id)
    if request.user != review.user:
        return HttpResponseForbidden("You can only edit your own reviews.")
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('book_detail', id=review.id)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'edit_review.html', {'form': form, 'review': review})


@login_required
def delete_review(request,id):
    review=Review.objects.get(id=id)
    if request.user != review.user and request.user.user_type != 'admin':
        return HttpResponseForbidden("You are not allowed to delete this review.")
    id = review.id
    if request.method == 'POST':
        review.delete()
        return redirect('book_detail', id=id)
    


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
            return redirect('/')

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
   
   
