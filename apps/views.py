from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import pyrebase

config = {
    "apiKey": "AIzaSyBVnaGc9eE0bwmNDqpm6ZV_AiwAVF04f_E",
    "authDomain": "test-e4176.firebaseapp.com",
    "databaseURL": "https://test-e4176-default-rtdb.firebaseio.com",
    "projectId": "test-e4176",
    "storageBucket": "test-e4176.appspot.com",
    "messagingSenderId": "12768005612",
    "appId": "1:12768005612:web:ddef3260c82c7f9d2884c9",
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


# Create your views here.
def index(request):
    return render(request, 'index.html')


def sign(request):
    return render(request, 'sign.html')


def logins(request):
    if request.user.is_authenticated:
        return render(request, 'main.html')
    else:
        if request.method == "POST":
            username = request.POST.get('username', '')
            email = request.POST.get('email', '')
            password = request.POST.get('repass', '')
            repass = request.POST.get('repass', '')
            if password == repass:
                try:
                    x = User.objects.create_user(email, username, password)
                    if x is not None:
                        x.save()
                        messages.success(request, "Successfully Signed In")
                        return render(request, 'login.html')
                    else:
                        messages.success(request, "! Please try again")
                        return render(request, 'sign.html')
                except:
                    messages.error(request, "Invalid credentials! Please try another")
            return render(request, 'sign.html')
    return render(request, 'login.html')


def main(request):
    if request.user.is_authenticated:
        return render(request, 'main.html')
    else:
        if request.method == "POST":
            email = request.POST.get('email', '')
            password = request.POST.get('pass', '')
            user = authenticate(username=email, password=password)
            if user is None:
                messages.error(request, "Invalid credentials! Please try again")
                return render(request, 'login.html')
            else:
                login(request, user)
                messages.success(request, "Successfully Logged In")
                return render(request, 'main.html')
    return render(request, 'login.html')



def logouts(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return render(request, 'index.html')

def test(request):
    if request.method == "POST":
        text = request.POST.getlist('text', '')
        in1 = request.POST.getlist('in1', '')
        in2 = request.POST.getlist('in2', '')
        in3 = request.POST.getlist('in3', '')
        in4 = request.POST.getlist('in4', '')
        key = request.POST.getlist('key', '')
        for i, keys in enumerate(key):
            database.child('Test').child(keys).child('question').update({'0': text[i]})
            database.child('Test').child(keys).child('option').update({'0': [in1[i], in2[i], in3[i], in4[i]]})
    if request.user.is_authenticated and request.user.username == 'pradeepskr723@gmail.com':
        name = database.child('Test').get()
        return render(request, 'test.html', {'name': name})
    return redirect(admin)

def add(request):
    if request.method == "POST":
        text = request.POST.getlist('text', '')
        in1 = request.POST.getlist('in', '')
        in2 = request.POST.getlist('in1', '')
        in3 = request.POST.getlist('in2', '')
        in4 = request.POST.getlist('in3', '')
        database.child('Test').push({'question': text, 'option': [in1, in2, in3, in4]})
        name = database.child('Test').get()
        return render(request, 'test.html', {'name': name})
    return redirect(test)


def admin(request):
    return render(request, 'admin.html')



def email(request):
    if request.method == "POST":
        email = request.POST.get('email', '')
        database.child('email').push({'email': email})
        name = database.child('email').get()
        return render(request, 'email.html', {'name': name})
    if request.user.is_authenticated and request.user.username == 'pradeepskr723@gmail.com':
        name = database.child('email').get()
        return render(request, 'email.html', {'name': name})
    return redirect(admin)


def saveemail(request):
    if request.method == "POST":
        text = request.POST.getlist('email', '')
        key = request.POST.getlist('key', '')
        for i, keys in enumerate(key):
            database.child('email').child(keys).update({'email': text[i]})
        name = database.child('email').get()
        return redirect(email)
    return redirect(admin)

def atmtest(request):
    if request.user.is_authenticated:
        name = database.child('email').get()
        tr = database.child('Test').get()
        try:
            for names in name.each():
                if names.val()['email'] == request.user.username:
                    access = 'true'
                    return render(request, 'atmtest.html', {'name': tr, 'access': access})
        except:
            messages.error(request, "You have not any test right now :)")
            return redirect(main)
    messages.error(request, "You have not any test right now :)")
    return redirect(main)

def savetest(request):
    if request.method=="POST":
        key = request.POST.getlist('key','')
        text = request.POST.getlist('text','')
        for i, keys in enumerate(key):
            inp=request.POST.get(keys,'')
            database.child('solution').push({'name': request.user.username, 'question': text[i],'answer': inp})

    return render(request, 'sucess.html')
def about(request):
    return render(request, 'about.html')
def solution(request):
    if request.user.is_authenticated and request.user.username == 'pradeepskr723@gmail.com':
        name = database.child('solution').get()
        return render(request, 'solution.html', {'name': name})
    return redirect(admin)