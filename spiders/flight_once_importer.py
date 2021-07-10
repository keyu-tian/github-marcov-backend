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
    
    # todo wz：删除下面的三行：不允许在这里新建Country
    for country in list(set(city_to_country.values())):
        Country.objects.get_or_create(name_ch=country)
    Country.objects.get_or_create(name_ch='中国')
    
    cities = []
    for code, city in code_to_city.items():
        if city in cities:
            continue
        cities.append(city)
        jingdu, weidu = address_to_jingwei(city)
        # todo wz：删除这里；因为城市是一次性导入的，在这里不要再用get_or_create
        City.objects.get_or_create(
            name_ch=city, defaults=dict(
                name_en='', jingdu=jingdu, weidu=weidu,
                country=Country.objects.get(name_ch=city_to_country.get(city, '中国'))
            )
        )
    for c in set(code_to_city.keys()):
        city = City.objects.get(name_ch=code_to_city[c])
        Airport.objects.create(name=code_to_airport[c], airport_code=c, city=city)
