import requests


spec_req = 'https://kudago.com/public-api/v1.4/events/{}/?fields=id,title,place,price,favorites_count,dates'
place_req = 'https://kudago.com/public-api/v1.4/places/{}/?fields=coords'
day_events_req = 'https://kudago.com/public-api/v1.4/events-of-the-day/?page_size=100&text_format=text&location={}'
events_req = 'https://kudago.com/public-api/v1.4/events/?page_size=100&fields=id,dates,price&text_format=text&location={}&' \
             'actual_since={}&lon={}&lat={}&radius={}'


def return_json(response):
    if response.status_code == 200:
        return response.json()
    return { 'error': response.status_code }

def get_specification(event_id):
    res = requests.get(spec_req.format(event_id))
    return return_json(res)

def get_coords(place_id):
    res = requests.get(place_req.format(place_id))
    return return_json(res)

def get_events_of_the_day(city):
    res = requests.get(day_events_req.format(city))
    return return_json(res)

def get_events(city, since, lon, lat, radius):
    res = requests.get(events_req.format(city, since, lon, lat, radius))
    return return_json(res)

# if there are the 'next' field, you can get next page
def get_next(next_url):
    res = requests.get(next_url)
    return return_json(res)
