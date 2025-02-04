import requests
import time
import random

def make_requestions(number: int, sleep: int):
    for i in range(number):
        kitchen_area = random.uniform(5, 25)
        living_area = random.uniform(45, 300)
        params = {'id': 92300+i, 'building_id': 10448+i, 'floor': random.randint(1, 20), 
                    'kitchen_area': kitchen_area, 'living_area': living_area,
                    'rooms': random.randint(1, 5), 
                    'is_apartment': 'false', 'studio': 'false', 
                    'total_area': kitchen_area+living_area+random.uniform(10, 30), 'build_year': random.randint(1970, 2024),
                    'building_type_int': 4, 'latitude': 55.71713638305664, 
                    'longitude': 37.46078109741211, 
                    'ceiling_height': 2.4800000190734863, 'flats_count': 143,
                    'floors_total': random.randint(1, 20),
                    'has_elevator': 'true'}
        response = requests.post(f'http://localhost:1702/predict/{i}', json=params)
        time.sleep(sleep)

if __name__ == "__main__":
    make_requestions(5, 10)