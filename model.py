from flask import Flask, render_template, request, jsonify
import requests
import logging
app = Flask(__name__)


app.secret_key = "ABC"
base_url = "https://api.yelp.com/v3/"
api_key ="k9VGFeAw2G7hlaSzDbt2bM9corS2Yvll4zQyATsUTvo9PmUfM3HzJ6EKV1fA5k83hBwZkXU04Il0qTh4PO64LsPqPLL5KsNGnIy0bs0jyE1KS2PDKGYItIGcMxhdXHYx"
logger = logging.getLogger(__name__)


def get_doctor_detail(id):
    """
    Make request to Yelp API to get doctor detail object
    """
    headers = {"Authorization": 'Bearer ' + api_key}
    return requests.get(
        f"{base_url}businesses/{id}",
        headers=headers).json()

def get_doctors(term, location, category=""):
    """
    Make request to YELP API to get all doctors.
    """
    headers = {
        "Authorization": 'Bearer ' + api_key
    }

    payload = {
        "term": "doctors", 
        "location": location, 
        "sort_by": "rating", 
        "categories":category
    }

    r = requests.get(
        f"{base_url}businesses/search",
        headers=headers, 
        params=payload
    ).json()
    
    return r["businesses"]


def unique_elements(elements):
    result = set()
    for elem in elements:
        result.add(elem)
    return list(result)

@app.route("/",methods=["GET","POST"])
def show_all_doctors():
    """Display all doctors of a specific location to user"""
    if request.method == "GET":
        location = "San Francisco, CA"
        category=""
    else:
        args = request.form
        location = args["location"]
        category = args["speciality"]

    doctors = get_doctors("doctors", location, category)
    specialities = unique_elements([doc["categories"][0]["alias"] for doc in doctors])
    locations = ["San Franciso, CA", "Los Angeles, CA", "New York City, NY"]
    
    return render_template("index.html",
        list_doctors_info=doctors,
        doc_speciality=specialities,
        selected_location=location, 
        location=locations)    

    
@app.route("/doctor/<id>")
def doc_details(id):    
    """
    See Doctor details with similar doctors based on 
    current doctor's categories
    """
    doctor = get_doctor_detail(id)

    location = doctor["location"]["city"]
    print(f"getting similar doctors in {location}")
    category = doctor["categories"][0]["alias"]
    category_name = doctor["categories"][0]["title"]
    similar_doctors = get_doctors("doctors", location=location, category=category)
    return render_template("about.html",
        doctor=doctor, 
        category=category, 
        category_name=category_name, 
        list_doctors_info=similar_doctors,
        location=location
    )

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=6001)
