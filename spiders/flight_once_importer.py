import json

from country.models import City
from flight.models import Airport


def flight_once_import():
    Airport.objects.all().delete()
    with open(f'spiders/flight_code_to_city.json', 'r+', encoding='utf-8') as f:
        code_to_city = json.loads(f.read())[0]
    with open(f'spiders/flight_code_to_airport.json', 'r+', encoding='utf-8') as f:
        code_to_airport = json.loads(f.read())
    
    for c in set(code_to_city.keys()):
        city = City.get_via_name(code_to_city[c])
        if city is not None:
            Airport.objects.create(name=code_to_airport[c], airport_code=c, city=city)
