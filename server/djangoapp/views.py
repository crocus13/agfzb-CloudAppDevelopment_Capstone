from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel, CarMake, CarDealer, DealerReview, ReviewPost
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json






# Get an instance of a logger
logger = logging.getLogger(__name__)
# logger = logging.getLogger(name)



# Create your views here.



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
            user.is_superuser = True
            user.is_staff=True
            user.save()                               
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/user_registration.html', context)



# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://8aa95a23.us-south.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)


     

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, id):
    # context = {}

    if request.method == "GET":
        context = {}
        dealer_url = "https://8aa95a23.us-south.apigw.appdomain.cloud/api/dealership"
        dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
        # print(dealer)
        context["dealer"] = dealer

        review_url = "https://8aa95a23.us-south.apigw.appdomain.cloud/api/get-review"

        reviews = get_dealer_reviews_from_cf(review_url, id=id)
        print(reviews)
        context["reviews"] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)



# Create a `add_review` view to submit a review

def add_review(request, id):
    context = {}
    dealer_url = "https://8aa95a23.us-south.apigw.appdomain.cloud/api/dealership"
    dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
    context["dealer"] = dealer
    if request.method == 'GET':
    # Get cars for the dealer
        cars = CarModel.objects.all()
        print(cars)
        context["cars"] = cars
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            payload = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = id
            payload["id"] = id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchasedate"]
            payload["car_make"] = car.make.name
            payload["car_model"] = car.name
            payload["car_year"] = int(car.year.strftime("%Y"))

            new_payload = {}
            new_payload["review"] = payload
            review_post_url = "https://8aa95a23.us-south.apigw.appdomain.cloud/api/post-review"
            post_request(review_post_url, new_payload, id=id)
            # return redirect("djangoapp:dealer_details", id=id)
    return redirect('djangoapp/dealer_details.html', id=id)













# def add_review(request, id): 
#     context = {} # If it is a GET request, just render the add_review page 
#     if request.method == 'GET': 
#         url = "https://8aa95a23.us-south.apigw.appdomain.cloud/api/dealership" # Get dealers from the URL c
#         context = { "id": id, "dealer_name": get_dealers_from_cf(url)[id-1].full_name, "cars": CarModel.objects.all() } 
#         print(context) 
#         return render(request, 'djangoapp/add_review.html', context) 
#     elif request.method == 'POST': 
#         if (request.user.is_authenticated):
#             review = dict() 
        
#             review["id"]=0#placeholder
#             review["name"]=request.POST["name"]
#             review["dealership"]= id 
#             review["review"]=request.POST["content"] 
#             if ("purchasecheck" in request.POST): 
#                 review["purchase"]=True
#             else:
#                 review["purchase"]=False 
#                 print(request.POST["car"]) 
#             if review["purchase"] == True:
#                 car_parts=request.POST["car"].split("|") 
#                 review["purchase_date"]=request.POST["purchase_date"] 
#                 review["car_make"]=car_parts[0] 
#                 review["car_model"]=car_parts[1] 
#                 review["car_year"]=car_parts[2]

#             else:
#                 review["purchase_date"]=None
#                 review["car_make"]=None
#                 review["car_model"]=None
#                 review["car_year"]=None
#                 json_result = post_request("https://8aa95a23.us-south.apigw.appdomain.cloud/api/post-review", review, id=id)
#                 print(json_result)
#             if "error" in json_result:
#                 context["message"] = "ERROR: Review was not submitted."
#             else:
#                 context["message"] = "Review was submited"
#             return redirect("djangoapp:dealer_details", id=id)
