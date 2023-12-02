from flask import Flask, render_template, request, jsonify
import requests
import random
import json
from src.country import Country, organizeCountiesByLoc, getNearByCountries
from src.utils import cuisine_to_location, location_to_cuisine, \
                      origin_to_location, location_to_origin, \
                      getRequest
from src.cats import Cat
import random
import os

app = Flask(__name__)

# Get country information
if os.path.exists('data/countries.json'):
    with open('data/countries.json', 'r') as f:
        countries_data = json.load(f)
else:
    countries_data = getRequest('https://restcountries.com/v3.1/all')
    with open('data/countries.json', 'w') as f:
        json.dump(countries_data, f)
countries = [Country(cd) for cd in countries_data]
print(len(countries))
# Convert the country information to a tree structure.
countries_dict = organizeCountiesByLoc(countries)
nearby_countries = getNearByCountries(countries)

# Get breeds information
if os.path.exists('data/breeds.json'):
    with open('data/breeds.json', 'r') as f:
        breeds = json.load(f)
else:
    breeds = getRequest('https://api.thecatapi.com/v1/breeds')
    with open('data/breeds.json', 'w') as f:
        json.dump(breeds, f)
cats = [Cat(breed) for breed in breeds]
cats = [cat for cat in cats if cat.check_feature("origin")]
origin_to_id_dict = {cat.origin:cat.id for cat in cats}

# Get all avaliable languages information
languages = set()
for country in countries:
    languages.update(set(country.languages.values()))
    

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/country_info', methods=['GET', 'POST'])
def select_region():
    if request.method == 'POST':
        if 'region' in request.form:
            selected_region = request.form['region']
            return render_template('select_subregion.html', 
                                   selected_region=selected_region, 
                                   subregions=countries_dict[selected_region].keys())
        elif 'language' in request.form:
            selected_language = request.form['language']
            locations = [country.name for country in countries if (selected_language in country.languages.values())]
            return render_template('select_location.html', 
                                   selected_language = selected_language,
                                   locations=locations)
    return render_template('select_region.html', 
                           regions=sorted(list(countries_dict.keys())), 
                           languages=sorted(list(languages)))



@app.route('/country_info/subregion', methods=['POST'])
def select_subregion():
    selected_region = request.form['selected_region']
    selected_subregion = request.form['subregion']
    return render_template('select_location.html', 
                           selected_region=selected_region, 
                           selected_subregion=selected_subregion, 
                           locations=countries_dict[selected_region][selected_subregion])

@app.route('/country_info/location', methods=['POST'])
def select_location():
    selected_location = request.form['location']
    search_nearby = request.form['nearby']
    if int(search_nearby) != 0:
        target_countries = []
        target_countries += nearby_countries[selected_location]
        for _ in range(1, int(search_nearby)):
            for c in target_countries.copy():
                target_countries += nearby_countries[c]
        target_countries = set(target_countries)
        return render_template('select_location.html', 
            nearby=target_countries,
            locations=target_countries)
            
        
    country=[country for country in countries if country.name == selected_location][0]
    region = country.region
    subregion = country.subregion
    cuisines = []
    cuisine_data = None
    if selected_location in location_to_cuisine.keys(): 
        cuisines += location_to_cuisine[selected_location]
    if region in location_to_cuisine.keys(): 
        cuisines += location_to_cuisine[region]
    if subregion in location_to_cuisine.keys(): 
        cuisines += location_to_cuisine[subregion]
    if cuisines:
        cuisine_regions = random.choice(cuisines)
        cuisine_data = getRequest(f'http://www.themealdb.com/api/json/v1/1/filter.php?a={cuisine_regions}')
        meal = cuisine_data['meals'][0] if cuisine_data['meals'] else None
        meal_id = meal['idMeal']

        response = requests.get(f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}')
        data = response.json()
        meal = data['meals'][0] if data['meals'] else None
        # Prepare the data to pass to the template
        if meal:
            cuisine_data = {
                'name': meal['strMeal'],
                'category': meal['strCategory'],
                'area': meal['strArea'],
                'instructions': meal['strInstructions'],
                'image': meal['strMealThumb']
            }
            
    origin = []
    cat = None
    if selected_location in location_to_origin.keys(): 
        origin += location_to_origin[selected_location]
    if region in location_to_origin.keys(): 
        origin += location_to_origin[region]
    if subregion in location_to_origin.keys(): 
        origin += location_to_origin[subregion]
    if origin:
        wildlife_regions = random.choice(origin)
        url = f"https://api.thecatapi.com/v1/images/search?breed_ids={origin_to_id_dict[wildlife_regions]}"
        response = requests.get(url)
        breeds = response.json()
        breed = breeds[0] if breeds else None
        trys = 0
        while not breed or 'url' not in breed:
            url = f"https://api.thecatapi.com/v1/images/search?breed_ids={origin_to_id_dict[wildlife_regions]}"
            response = requests.get(url)
            breeds = response.json()
            breed = breeds[0] if breeds else None
            if trys > 10:
                print(trys)
                breed = None
                break
        if breed:
            response = requests.get(f"https://api.thecatapi.com/v1/images/{breed['id']}")
            data = response.json()
            cat = Cat(data["breeds"][0])
            cat.image_url = data["url"]

    return render_template('country_details.html', 
                           country=country, 
                           cuisine_data=cuisine_data, 
                           wildlife_data=cat)



@app.route('/cuisine_info', methods=['GET', 'POST'])
def cuisine_info():
    if request.method == 'POST':
        cuisine_regions = request.form['cuisine_regions']
        response = requests.get(f'http://www.themealdb.com/api/json/v1/1/filter.php?a={cuisine_regions}')
        data = response.json()
        
        # Assuming the API returns a list of meals, and we take the first one
        meal = data['meals'][0] if data['meals'] else None
        meal_id = meal['idMeal']

        response = requests.get(f'https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}')
        data = response.json()
        meal = data['meals'][0] if data['meals'] else None
        # Prepare the data to pass to the template
        if meal:
            cuisine_data = {
                'name': meal['strMeal'],
                'category': meal['strCategory'],
                'area': meal['strArea'],
                'instructions': meal['strInstructions'],
                'image': meal['strMealThumb']
            }
        else:
            cuisine_data = None

        return render_template('cuisine_info.html', cuisine_data=cuisine_data)
    return render_template('select_region.html', cuisine_regions=sorted(list(cuisine_to_location.keys())))


@app.route('/wildlife_info', methods=['GET', 'POST'])
def wildlife_info():
    
    if request.method == 'POST':
        wildlife_regions = request.form['wildlife_regions']
        url = f"https://api.thecatapi.com/v1/images/search?breed_ids={origin_to_id_dict[wildlife_regions]}"
        response = requests.get(url)
        breeds = response.json()
        breed = breeds[0] if breeds else None
        trys = 0
        while not breed or 'url' not in breed:
            url = f"https://api.thecatapi.com/v1/images/search?breed_ids={origin_to_id_dict[wildlife_regions]}"
            response = requests.get(url)
            breeds = response.json()
            breed = breeds[0] if breeds else None
            if trys > 10:
                print(trys)
                breed = None
                break
        if breed:
            response = requests.get(f"https://api.thecatapi.com/v1/images/{breed['id']}")
            data = response.json()
            cat = Cat(data["breeds"][0])
            cat.image_url = data["url"]
        else:
            cat = None

        return render_template('wildlife_info.html', wildlife_data=cat)
    return render_template('select_region.html', wildlife_regions=sorted([cat.origin for cat in cats]))


if __name__ == '__main__':
    app.run(debug=True)
