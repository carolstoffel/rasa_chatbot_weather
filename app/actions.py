
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

import geocoder
import json

openweathermap_KEY = 'Digite sua api do openweathermap aqui'
tomtom_KEY = 'Digite sua api do tomtom aqui'


class ActionAskWeather(Action):
    def name(self) -> Text:
        return "action_ask_weather"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        result = ""
        local = next(tracker.get_latest_entity_values('GPE'), None)
        if local is None:
            latitude, longitude = "-24.7105133", "-53.7477903"
            result = "Não entendi o local que deseja. Vou dizer a temperatura de Toledo, Paraná, Brazil. "
        else:
            geolocation = geocoder.tomtom(
                location=local, key=tomtom_KEY)
            geo_json = geolocation.json
            geo_json = json.dumps(geo_json)
            geo_json = json.loads(geo_json)
            latitude, longitude = str(geo_json['lat']), str(geo_json['lng'])

        url = "http://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}&units=metric&lang=pt_br".format(
            latitude, longitude, openweathermap_KEY)

        response = requests.request("GET", url)
        json_data = response.json()
        description = json_data['weather'][0]['description'].capitalize()
        temperatura = json_data['main']['temp']
        umidade = json_data['main']['humidity']
        result += '{}. A temperatura no momento é de {}°C e umidade do ar é de {}%.'.format(
            description, temperatura, umidade)

        dispatcher.utter_message(text=result)

        return []
