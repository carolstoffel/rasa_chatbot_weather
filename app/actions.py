
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

import geocoder
import json

weather_dict = {'freezing_rain_heavy': 'Chuva forte e neve.', 'freezing_rain': 'Chuva e neve lá fora.', 'freezing_rain_light': 'Chuva leve e neve.', 'freezing_drizzle': 'Garoa e neve.', 'ice_pellets_heavy': 'Muito granizo.', 'ice_pellets': 'Está chovendo gelo.', 'ice_pellets_light': 'Um pouco de granizo caindo.', 'snow_heavy': 'Chuva forte.', 'snow': 'Está nevando.', 'snow_light': 'Um pouco de neve.', 'flurries': 'Rajadas de vento.',
                'tstorm': 'Tempestade por perto.', 'rain_heavy': 'Chuva forte.', 'rain': 'Está chovendo.', 'rain_light': 'Chuva leve.', 'drizzle': 'Garoa.', 'fog_light': 'Neblina.', 'fog': 'Névoa.', 'cloudy': 'Nublado.', 'mostly_cloudy': 'Muitas nuvens lá fora.', 'partly_cloudy': 'Parcialmente nublado.', 'mostly_clear': 'Ensolarado com poucas nuvens.', 'clear': 'O céu está limpo e o dia está ensolarado.'}
url = "https://api.climacell.co/v3/weather/realtime"


class ActionAskWeather(Action):
    def name(self) -> Text:
        return "action_ask_weather"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # print(address, (latitude, longitude)=geolocator.geocode("175 5th Avenue NYC"))
        result = ""
        local = next(tracker.get_latest_entity_values('GPE'), None)
        if local is None:
            latitude, longitude = "-24.7105133", "-53.7477903"
            result = "Não entendi o local que deseja. Vou dizer a temperatura de Toledo, Paraná, Brazil. "
        else:
            geolocation = geocoder.tomtom(
                location=local, key='thfGJoM8E7CjMZfbvf0Jw8i2Zbl3lPSF')
            geo_json = geolocation.json
            geo_json = json.dumps(geo_json)
            geo_json = json.loads(geo_json)
            latitude, longitude = str(geo_json['lat']), str(geo_json['lng'])

        querystring = {"lat": latitude, "lon": longitude, "unit_system": "si",
                       "fields": "temp,humidity,weather_code", "apikey": "rFztmQ2ZUPdyQ2G8I4pKRKpSYBps7UEk"}
        response = requests.request("GET", url, params=querystring)

        json_data = response.json()

        if(json_data['weather_code']['value'] in weather_dict):
            result += weather_dict[json_data['weather_code']['value']] + ' '
        result += 'A temperatura é de %s%s, umidade de %s%s.' % (
            json_data['temp']['value'], json_data['temp']['units'], json_data['humidity']['value'], json_data['humidity']['units'])

        dispatcher.utter_message(text=result)

        return []
