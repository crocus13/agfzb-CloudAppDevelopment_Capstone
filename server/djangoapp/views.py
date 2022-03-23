from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake,CarModel
from .restapis import get_dealers_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# def get_dealerships(request):
#     if request.method == "GET":
#         context = {}
#         url = "https://8aa95a23.us-south.apigw.appdomain.cloud/api/dealership"
#         dealerships = get_dealers_from_cf(url)
#         context["dealership_list"] = dealerships
#         return render(request, 'djangoapp/index.html', context)















# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# def index(request):
#     return render(request, 'index.html')


# Create an `about` view to render a static about page

def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)



# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)


# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            # return redirect('djangoapp:index')
            return HttpResponseRedirect('/djangoapp/') 
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)
      
      
# Create a `logout_request` view to handle sign in request

def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    # return redirect('djangoapp:index')
    return HttpResponseRedirect('/djangoapp/') 


# Create a `registration_request` view to handle sign up request

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/user_registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug("{} is new user".format(username))
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/user_registration.html', context)
            

# Update the `get_dealerships` view to render the index page with a list of dealerships
# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         return render(request, 'djangoapp/index.html', context)

        # url = "rev.us-south.cf.appdomain.cloud/dealerships/dealer-get"
        # # Get dealers from the URL
        # dealerships = get_dealers_from_cf(url)
        # # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # # Return a list of dealer short name
        # return HttpResponse(dealer_names)
        # return render(request, 'djangoapp/index.html', context)

# def get_dealerships(request):
#     context = {}
#     if request.method == "GET":
#         url = "https://8aa95a23.us-south.apigw.appdomain.cloud/api/dealership"
#         # Get dealers from the URL
#         dealerships = get_dealers_from_cf(url)
#         # Concat all dealer's short name
#         context["dealer_names"] = ' '.join([dealer.short_name for dealer in dealerships])
#         # Return a list of dealer short name
#         return HttpResponse(dealer_names)
#         return render(request, 'djangoapp/index.html', context)



def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://8aa95a23.us-south.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)


     
# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
#     context = {}
#     if request.method == "GET":
#         url = "https://8aa95a23.us-south.apigw.appdomain.cloud/api/reviews"
#         # Get dealers from the URL
#         dealerships = get_dealers_from_cf(url)
#         # Concat all dealer's short name
#         context["dealer_names"] = ' '.join([dealer.short_name for dealer in dealerships])
#         # Return a list of dealer short name
#         return HttpResponse(dealer_names)
#         return render(request, 'djangoapp/index.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
#     context = {}
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['pwd']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                   # Redirect to index page.
#                 return redirect("djangoapp:add_review")
#             else:
#                 return HttpResponse("User is not authenticated.")
#         else:    
#             return render(request, 'djangoapp/user_login.html', context)
#     else:
#         return render(request, 'djangoapp/user_login.html', context)

#         review["id"] = id
#         review["dealership"] = dealership
#         review["name"] = name
#         review["purchase"] = purchase
#         review["review"] = review
#         review["purchase_date"] = datetime.utcnow().isoformat()
#         review["car_make"] = car_make
#         review["car_model"] = car_model
#         review["car_year"] = car_year
        
#         json_payload["review"] = review
#     results.append(review)


# def get_dealerships(request):
#     if request.method == "GET":
#         context = {}
#         return render(request, 'djangoapp/index.html', context)
