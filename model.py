from flask import Flask, render_template, request, jsonify
import requests
app = Flask(__name__)


app.secret_key = "ABC"




@app.route("/",methods=["GET","POST"])
def show_all_doctors():
    """Display all doctors of a specific location to user"""
    if request.method == "GET":
        location_docs = "San francisco"
        category = "familydr"
        
    else:
        args = request.form
        location_docs = args["location"]
        category = args["speciality"]

    key ="k9VGFeAw2G7hlaSzDbt2bM9corS2Yvll4zQyATsUTvo9PmUfM3HzJ6EKV1fA5k83hBwZkXU04Il0qTh4PO64LsPqPLL5KsNGnIy0bs0jyE1KS2PDKGYItIGcMxhdXHYx"

    headers = {"Authorization": 'Bearer ' + key}
    payload = {"term": "doctors", "location": location_docs, "sort_by": "rating", "categories":category}
    r = requests.get("https://api.yelp.com/v3/businesses/search",
                     headers=headers, params=payload)
    doctors_info = r.json()
    list_doctors_info = doctors_info["businesses"]
    location = set()
    speciality=set()
    rating = set()
    for doc in list_doctors_info:
        x = doc["categories"][0]["alias"]
        y = "/n".join(doc["location"]["display_address"])
        z = doc["rating"]
        speciality.add(x)
        location.add(y)
        rating.add(z)

    doc_speciality = list(speciality)
    location = ["San Franciso, CA", "Los Angeles, CA", "New York City, NY"]
    rating = list(rating)
    return render_template("index.html",
        list_doctors_info=list_doctors_info,
        doc_speciality=doc_speciality,
        selected_location=location_docs, 
        location=location,
        rating=rating)    


@app.route("/doctor/<id>")
def doc_details(id):
    key ="k9VGFeAw2G7hlaSzDbt2bM9corS2Yvll4zQyATsUTvo9PmUfM3HzJ6EKV1fA5k83hBwZkXU04Il0qTh4PO64LsPqPLL5KsNGnIy0bs0jyE1KS2PDKGYItIGcMxhdXHYx"
    location_docs = "San francisco"
    headers = {"Authorization": 'Bearer ' + key}
    r = requests.get(f"https://api.yelp.com/v3/businesses/{id}",
                     headers=headers)
    doctor = r.json()


    location_docs = "San francisco"
    headers = {"Authorization": 'Bearer ' + key}
    category = doctor["categories"][0]["alias"]
    category_name = doctor["categories"][0]["title"]
    payload = {"categories": category, "location": location_docs, "sort_by": "rating"}
    r = requests.get("https://api.yelp.com/v3/businesses/search",
                     headers=headers, params=payload)
    doctors_info = r.json()
    list_doctors_info = doctors_info["businesses"]
    return render_template("about.html",doctor=doctor, category=category, category_name=category_name, list_doctors_info=list_doctors_info)




if __name__ == "__main__":

    app.debug = True



    # DebugToolbarExtension(app)
    app.run(host="0.0.0.0", port=6001)
