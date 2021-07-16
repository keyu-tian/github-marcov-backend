import json

from flight.models import Airport


def flight_once_import():
    Airport.objects.all().delete()
    with open(f'spiders/flight_code_to_city.json', 'r+', encoding='utf-8') as f:
        context = json.loads(f.read())
        code_to_city = context[0]
        city_to_country = context[1]
    with open(f'spiders/flight_code_to_airport.json', 'r+', encoding='utf-8') as f:
        code_to_airport = json.loads(f.read())
    with open(f'spiders/flight_airport_to_jingwei.json', 'r+', encoding='utf-8') as f:
        airport_to_jingwei = json.loads(f.read())
    for code in set(code_to_city.keys()):
        if airport_to_jingwei.get(code_to_airport[code], None) is None:
            continue
        Airport.objects.create(
            airport_name=code_to_airport[code],
            airport_code=code,
            city_name=code_to_city[code],
            jingdu=airport_to_jingwei[code_to_airport[code]][0],
            weidu=airport_to_jingwei[code_to_airport[code]][1],
            country_name=city_to_country.get(code_to_city[code], '中国')
        )
