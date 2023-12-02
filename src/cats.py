

class Cat:
    def __init__(self, breed_data):
        self.weight_imperial = breed_data['weight']['imperial']
        self.weight_metric = breed_data['weight']['metric']
        self.id = breed_data['id']
        self.name = breed_data['name']
        self.cfa_url = breed_data.get('cfa_url')
        self.vetstreet_url = breed_data.get('vetstreet_url') if "vetstreet_url" in breed_data else None
        self.vcahospitals_url = breed_data.get('vcahospitals_url') if "vcahospitals_url" in breed_data else None
        self.temperament = breed_data['temperament'] if "temperament" in breed_data else None
        self.origin = breed_data['origin'] if "origin" in breed_data else None
        self.description = breed_data['description'] if "description" in breed_data else None
        self.life_span = breed_data['life_span']
        self.indoor = breed_data['indoor'] if "indoor" in breed_data else None
        self.alt_names = breed_data.get('alt_names', '')
        self.affection_level = breed_data['affection_level'] if "affection_level" in breed_data else None
        self.child_friendly = breed_data['child_friendly'] if "child_friendly" in breed_data else None
        self.dog_friendly = breed_data['dog_friendly'] if "dog_friendly" in breed_data else None
        self.image_url = None
        # self.energy_level = breed_data['energy_level']
        # self.grooming = breed_data['grooming']
        # self.health_issues = breed_data['health_issues']
        # self.intelligence = breed_data['intelligence']
        # self.shedding_level = breed_data['shedding_level']
        # self.social_needs = breed_data['social_needs']
        # self.stranger_friendly = breed_data['stranger_friendly']
        # self.vocalisation = breed_data['vocalisation']
        # self.experimental = breed_data['experimental']
        # self.hairless = breed_data['hairless']
        # self.natural = breed_data['natural']
        # self.rare = breed_data['rare']
        # self.rex = breed_data['rex']
        # self.suppressed_tail = breed_data['suppressed_tail']
        # self.short_legs = breed_data['short_legs']
        # self.wikipedia_url = breed_data.get('wikipedia_url')
        # self.hypoallergenic = breed_data['hypoallergenic']
        # self.reference_image_id = breed_data['reference_image_id']
        
    def check_feature(self, input_str):
        return getattr(self, input_str, None) is not None

# def map_id_to_origin(self):
#     """Maps each cat breed's id to its origin."""
#     return {item['id']: item['origin'] for item in self.data}
    
    # def map_origin_to_id(self):
    #     """Maps each cat breed's id to its origin."""
    #     return {item['origin']:item['id'] for item in self.data}

# Example JSON data
# json_data = [
#     {"id": "abys", "origin": "Egypt"},
#     {"id": "aege", "origin": "Greece"},
#     {"id": "abob", "origin": "United States"},
#     # ... other data ...
# ]

# Creating an instance of the class
# mapper = Cat(json_data)

# # Mapping ids to origins
# id_origin_map = mapper.map_id_to_origin()
# id_origin_map