import json

from country.models import City, Country
from flight.models import Airport
from utils.cast import address_to_jingwei


def flight_once_import():
    Airport.objects.all().delete()
    with open(f'spiders/flight_code_to_city.json', 'r+', encoding='utf-8') as f:
        context = json.loads(f.read())
        code_to_city = context[0]
        city_to_country = context[1]
    with open(f'spiders/flight_code_to_airport.json', 'r+', encoding='utf-8') as f:
        code_to_airport = json.loads(f.read())
    for country in list(set(city_to_country.values())):
        Country.objects.get_or_create(name_ch=country)
    Country.objects.get_or_create(name_ch='中国')
    cities = []
    for code, city in code_to_city.items():
        if city in cities:
            continue
        cities.append(city)
        jingdu, weidu = address_to_jingwei(city)
        City.objects.get_or_create(
            name_ch=city, defaults=dict(
                name_en='', jingdu=jingdu, weidu=weidu,
                country=Country.objects.filter(name_ch=city_to_country.get(city, '中国'))
            )
        )
    for c in code_to_city.keys():
        city = City.objects.get(name_ch=code_to_city[c])
        Airport.objects.get_or_create(name=code_to_airport[c], airport_code=c, city=city)
