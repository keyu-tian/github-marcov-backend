import json

from tqdm import tqdm

from flight.models import Flight, Airport
from meta_config import SPIDER_DATA_DIRNAME, BULK_CREATE_BATCH_SIZE


def flight_daily_import():
    Flight.objects.all().delete()
    with open(f'{SPIDER_DATA_DIRNAME}/flights_data.json', 'r+', encoding='utf-8') as f:
        data = json.loads(f.read())

    objs = []
    bar = tqdm(list(enumerate(data)), dynamic_ncols=True)
    for line, item in bar:
        bar.set_description(f'[line{line}]')
        bar.set_postfix_str(f'{item["dept_city"]} => {item["arri_city"]}')
        
        dept_airport = item['dept_city']
        if Airport.objects.filter(airport_code=dept_airport).count() == 0:
            dept_airport = None
        else:
            dept_airport = Airport.objects.filter(airport_code=dept_airport).get()
        arri_airport = item['arri_city']
        if Airport.objects.filter(airport_code=arri_airport).count() == 0:
            arri_airport = None
        else:
            arri_airport = Airport.objects.filter(airport_code=arri_airport).get()
        if arri_airport is None or dept_airport is None:
            continue
        kwargs = {'code': item['code'], 'dept_time': item['dept_time'], 'dept_airport': dept_airport, 'arri_time': item['arri_time'], 'arri_airport': arri_airport, 'condition': item['condition']}
        objs.append(Flight(**kwargs))
    bar.close()
    
    Flight.objects.bulk_create(objs, BULK_CREATE_BATCH_SIZE)
