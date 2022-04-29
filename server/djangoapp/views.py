from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake,CarModel,CarDealer, DealerReview
from .restapis import get_dealers_from_cf,get_dealer_reviews_from_cf,get_dealer_by_id_from_cf,post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
# from . import restapis
# from . import models

# Get an instance of a logger
logger = logging.getLogger(__name__)


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

def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        dealer_url = "https://8aa95a23.us-south.apigw.appdomain.cloud/api/dealership"
        # dealer = get_dealer_by_id_from_cf(dealer_url, id=id)
        dealer = get_dealer_by_id_from_cf(dealer_url, dealer_id=dealer_id)

        # dealer = get_request(url, id=id)
        context["dealer"] = dealer
        review_url = "https://8aa95a23.us-south.apigw.appdomain.cloud/api/get-review"
        # reviews = get_dealer_reviews_from_cf(review_url, id=id)
        reviews = get_dealer_reviews_from_cf(review_url, dealer_id=dealer_id)
        print(reviews)
        context["reviews"] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)




# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "GET":
        dealer_id = dealerId
        url = "https://8aa95a23.us-south.apigw.appdomain.cloud/api/get-review?id={0}".format(dealersId)
        # Get dealers from the URL
        context = {
            "cars": models.CarModel.objects.all(),
            "dealers": restapis.get_dealers_from_cf(url),
        }
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        if request.user.is_authenticated:
            form = request.POST
            review = {
                "name": "{request.user.first_name} {request.user.last_name}",
                # "dealership": dealer_id,
                "dealership": id,

                "review": form["content"],
                "purchase": form.get("purchasecheck"),
                }
            if form.get("purchasecheck"):
                review["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%m/%d/%Y").isoformat()
                car = models.CarModel.objects.get(pk=form["car"])
                review["car_make"] = car.carmake.name
                review["car_model"] = car.name
                review["car_year"]= car.year.strftime("%Y")
            json_payload["review"] = review
            print (json_payload)
            url = "https://8aa95a23.us-south.apigw.appdomain.cloud/api/post-review"
            restapis.post_request(url, json_payload, dealerId=dealer_id)
            # restapis.post_request(url, json_payload, id=id)
            return redirect("djangoapp:dealer_details.html", dealerId=dealer_id)
        else:
            return redirect("/djangoapp/user_login.html")

