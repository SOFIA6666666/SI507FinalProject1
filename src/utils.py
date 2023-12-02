import requests

cuisine_to_location = {
    "American": ["North America", "Central America", "South America", "Caribbean", "United States", "Mexico", "Canada"],
    "British": ["Northern Europe", "Western Europe", "United Kingdom", "Ireland"],
    "Canadian": ["North America", "Canada"],
    "Chinese": ["Eastern Asia", "China", "Hong Kong", "Macau"],
    "Croatian": ["Southeast Europe", "Croatia"],
    "Dutch": ["Western Europe", "Netherlands"],
    "Egyptian": ["Northern Africa", "Egypt"],
    "Filipino": ["Southeast Asia", "Philippines"],
    "French": ["Western Europe", "France", "Monaco", "Réunion", "French Guiana", "French Polynesia", "French Southern and Antarctic Lands", "Martinique", "Guadeloupe", "Saint Martin"],
    "Greek": ["Southern Europe", "Greece"],
    "Indian": ["Southern Asia", "India"],
    "Irish": ["Northern Europe", "Ireland"],
    "Italian": ["Southern Europe", "Italy"],
    "Jamaican": ["Caribbean", "Jamaica"],
    "Japanese": ["Eastern Asia", "Japan"],
    "Kenyan": ["Eastern Africa", "Kenya"],
    "Malaysian": ["Southeast Asia", "Malaysia"],
    "Mexican": ["Central America", "Mexico"],
    "Moroccan": ["Northern Africa", "Morocco"],
    "Polish": ["Eastern Europe", "Poland"],
    "Portuguese": ["Southern Europe", "Portugal"],
    "Russian": ["Eastern Europe", "Northern Asia", "Russia"],
    "Spanish": ["Southern Europe", "Spain"],
    "Thai": ["Southeast Asia", "Thailand"],
    "Tunisian": ["Northern Africa", "Tunisia"],
    "Turkish": ["Western Asia", "Turkey"],
    "Unknown": [],
    "Vietnamese": ["Southeast Asia", "Vietnam"]
}


# Create mapping between country information to avaible cuisine. The mapping may not be bijective.
location_to_cuisine = {}
for food_area, countries in cuisine_to_location.items():
    for country in countries:
        if country not in location_to_cuisine:
            location_to_cuisine[country] = []
        location_to_cuisine[country].append(food_area)


origin_to_location = {
    "Egypt": ["Northern Africa", "Egypt"],
    "Greece": ["Southern Europe", "Greece"],
    "United States": ["North America", "United States"],
    "United Arab Emirates": ["Western Asia", "United Arab Emirates"],
    "Australia": ["Australia and New Zealand", "Oceania", "Australia"],
    "France": ["Western Europe", "France", "French Southern and Antarctic Lands", "French Polynesia", "French Guiana", "Martinique", "Guadeloupe", "Réunion", "Saint Martin"],
    "United Kingdom": ["Northern Europe", "Western Europe", "United Kingdom"],
    "Burma": ["Southeast Asia", "Myanmar"],
    "Canada": ["North America", "Canada"],
    "Cyprus": ["Western Asia", "Southern Europe", "Cyprus"],
    "Russia": ["Eastern Europe", "Northern Asia", "Russia"],
    "China": ["Eastern Asia", "China", "Hong Kong", "Macau"],
    "Japan": ["Eastern Asia", "Japan"],
    "Thailand": ["Southeast Asia", "Thailand"],
    "Isle of Man": ["Northern Europe", "Isle of Man"],
    "Norway": ["Northern Europe", "Norway"],
    "Iran (Persia)": ["Western Asia", "Middle East", "Iran"],
    "Singapore": ["Southeast Asia", "Singapore"],
    "Somalia": ["Eastern Africa", "Somalia"],
    "Turkey": ["Western Asia", "Southeast Europe", "Turkey"]
}


location_to_origin = {}
for origin, countries in origin_to_location.items():
    for country in countries:
        if country not in location_to_origin:
            location_to_origin[country] = []
        location_to_origin[country].append(origin)
        
def getRequest(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Request failed, url: {url}")


