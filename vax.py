import requests
import json
import time
import math

#Enter your State Code, starting GPS coordinates and max distance in km to search for open vaccine appointments
state_code = "CO"
starting_coords = {"lat": 39.7413348, "long": -105.0692655}
distance = 80

url = "https://www.vaccinespotter.org/api/v0/states/" + state_code + ".json"

def query_appts(starting_coords, distance):
    appointments = json.loads(requests.get(url).text.encode('ascii', 'ignore'))
    for appointment in appointments['features']:
        if appointment['properties']['appointments_available'] == True:
            appointment_coords = {"lat": appointment['geometry']['coordinates'][1], "long": appointment['geometry']['coordinates'][0]}
            diff_distance = distance_calc(starting_coords, appointment_coords)
            if diff_distance < distance:
                msg1 = "Appointment found in " + appointment['properties']['city'] + " for" 
                for appt in appointment['properties']['appointments']:
                    print(msg1, appt['type'], "on", appt['time'][0:10], "at", appt['time'][11:19], appointment['properties']['name'], appointment['properties']['address'], appointment['properties']['url'])

def distance_calc(starting_coords, appointment_coords):
    #Haversine formula
    R = 6373.0
    lat1 = math.radians(starting_coords['lat'])
    long1 = math.radians(starting_coords['long'])
    lat2 = math.radians(appointment_coords['lat'])
    long2 = math.radians(appointment_coords['long'])
    diff_lon = long2 - long1
    diff_lat = lat2 - lat1
    a = math.sin(diff_lat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(diff_lon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

if __name__ == "__main__":
    while True:
        query_appts(starting_coords, distance)
        time.sleep(300)
