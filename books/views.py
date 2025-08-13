from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden, HttpResponsePermanentRedirect, HttpResponseRedirect
from .forms import *

# Create your views here.

def book_list(request):
    books=Books.objects.all()
    return render(request,'book_list.html',{'books':books})


@login_required
def add_book(request):
    if request.user.user_type != 'admin':
        return HttpResponseForbidden('ONLY ADMIN CAN ADD BOOKS')
    
    if request.method=="POST":
        form=BookForm(request.POST,request.FILES)
        if form.is_valid():
            books=form.save(commit=False)
            books.author=request.user
            books.save()
            return redirect("/book_list/")
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
            return redirect("book_detail/",id=book.id)
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
        return redirect("/book_list/")
    
    return render(request,'confirm_delete_book.html',{'book':book})



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
            return redirect('/login/')
        
        else:
            login(request,user)
            return redirect('/book_list/')

    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

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

        return redirect('/register/')

    return render(request,'register.html')

def home_page(request):
    return render(request,'home.html')



def book_detail(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    return render(request, 'book_detail.html', {'book': book})

@login_required
def add_review(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    
    if request.method == 'POST':
        rating = int(request.POST.get('rating'))
        comment = request.POST.get('comment')

        Review.objects.create(
            book=book,
            user=request.user,
            rating=rating,
            comment=comment
        )
        
        return redirect('book_detail', book_id=book.id)

@login_required
def edit_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    if request.user != review.user:
        return HttpResponseForbidden("You are not allowed to edit this review.")

    if request.method == 'POST':
        review.rating = int(request.POST.get('rating'))
        review.comment = request.POST.get('comment')
        review.save()
        
        return redirect('book_detail', book_id=review.book.id)

    return render(request, 'edit_review.html', {'review': review})

@login_required
def delete_review(request, review_id) :
    review = get_object_or_404(Review, id=review_id)

    if request.user != review.user:
        return HttpResponseForbidden("You are not allowed to delete this review.")

    book_id = review.book.id
    review.delete()

    return redirect('book_detail', book_id=book_id)









   
   
