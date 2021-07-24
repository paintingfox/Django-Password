from django.http.response import HttpResponse
from django.shortcuts import render
from Login import forms
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required




# Create your views here.
def register(request):
    registered = False
    
    if request.method == 'POST':
        user_form = forms.UserForm(data = request.POST)
        profile_form = forms.UserProfileInfoForm(data = request.POST)
        print("Ok")

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            #hashing password before saving it
            user.set_password(user.password)

            user.save()

            profile = profile_form.save(commit = False)
            profile_user = user
            print("Fuck")
            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()
            print('saved')
            # Registration Successful!
            registered = True
            
        else:
                # One of the forms was invalid if this else gets called.
                print(user_form.errors,profile_form.errors)
                print("Shit")

                

    else:
            # Was not an HTTP post so we just render the forms as blank.
        user_form = forms.UserForm()
        profile_form = forms.UserProfileInfoForm()
        print("Shit")
            # This is the render and context dictionary to feed
            # back to the registration.html file page.
            
    return render(request,'basic/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse(index))
            else:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and false.")
            print("They used username: {} and password: {}", format(username,password))
            return HttpResponse("Invalid login details supptied")
    else:
        return render(request,'basic/login.html', {})

def index(request):
    return render(request,'basic/index.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

