import requests
import json
from .models import CarMake,CarModel
from requests.auth import HTTPBasicAuth
from .models import CarDealer,DealerReview
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features,SentimentOptions
# import time

# Create a `get_request` to make HTTP GET requests
def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

# Create a get_dealers_from_cf method to get dealers from a cloud function

def get_dealers_from_cf(url, **kwargs):
    results = []
    state = kwargs.get("state")
    if state:
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)
    # print(json_result)    
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["body"]["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # print(dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],state=dealer_doc["state"],
                                    st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results





# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    json_obj = json_payload["review"]
    print(kwargs)
    try:
        response = requests.post(url, json=json_obj, params=kwargs)
    except:
        print("Something went wrong")
    print (response)
    return response




# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_by_id_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result["body"]["rows"]
        for review in reviews:
            review_doc = review["doc"]
            review_obj = DealerReview(id=review_doc["id"],name=review_doc["name"],dealership = review_doc["dealership"], review = review_doc["review"], purchase=review_doc["purchase"],
                                    purchase_date = review_doc["purchase_date"], car_make = review_doc['car_make'],
                                    car_model = review_doc['car_model'], car_year= review_doc['car_year'], sentiment= "none")
            
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            print(review_obj.sentiment)
                    
            results.append(review_obj)

    return results




# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):

    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/1e4de4a8-d09f-4a38-9308-313ec974f75d" 

    api_key = "zobNkm1knBgIl38HiTHZH-inPDJRd0L31s2Zda80WiRt" 

    authenticator = IAMAuthenticator(api_key) 

    natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator) 

    natural_language_understanding.set_service_url(url) 

    response = natural_language_understanding.analyze( text=text,features=Features(sentiment=SentimentOptions(targets=[text]))).get_result() 

    label=json.dumps(response, indent=2) 

    label = response['sentiment']['document']['label'] 

    return(label) 















# def analyze_review_sentiments(text):
#     api_key = "zobNkm1knBgIl38HiTHZH-inPDJRd0L31s2Zda80WiRt"
#     url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/1e4de4a8-d09f-4a38-9308-313ec974f75d"
#     texttoanalyze= text
#     version = '2020-08-01'
#     authenticator = IAMAuthenticator(api_key)
#     natural_language_understanding = NaturalLanguageUnderstandingV1(
#     version='2020-08-01',
#     authenticator=authenticator
#     )
#     natural_language_understanding.set_service_url(url)
#     response = natural_language_understanding.analyze(
#         text=text,
#         features= Features(sentiment= SentimentOptions())
#     ).get_result()
#     print(json.dumps(response))
#     sentiment_score = str(response["sentiment"]["document"]["score"])
#     sentiment_label = response["sentiment"]["document"]["label"]
#     print(sentiment_score)
#     print(sentiment_label)
#     sentimentresult = sentiment_label
    
#     return sentimentresult










# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
# import requests
# import json
# from .models import CarDealer
# from requests.auth import HTTPBasicAuth


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_reviews_by_id_from_cf(url, dealerId):
#     results = []
#     json_result = get_request(url, dealerId=dealerId)
#     if json_result:
#         reviews = json_result['entries']
#         for review in reviews:
#             review_doc = review["doc"]

            
#                 review_obj = DealerReview(name=review_doc["name"],
#                 dealership = review_doc["dealership"], review = review_doc["review"], purchase=review_doc["purchase"],
#                 purchase_date = review_doc["purchase_date"], car_make = review_doc['car_make'],
#                 car_model = review_obj['car_model'], car_year= review_obj['car_year'], sentiment= "none")
#             except:
#                 review_obj = DealerReview(name = review["name"],
#                 dealership = review["dealership"], review = review["review"], purchase=review["purchase"],
#                 purchase_date = 'none', car_make = 'none',
#                 car_model = 'none', car_year= 'none', sentiment= "none")
                
#             review_obj.sentiment = analyze_review_sentiments(review_obj.review)
#             print(review_obj.sentiment)
                    
#             results.append(review_obj)

#     return results

