from rasa_core import utils
from rasa_core.actions import Action
from rasa_core.agent import Agent
from rasa_core.events import SlotSet
from rasa_core.interpreter import RasaNLUInterpreter

class RestaurantAPI(object):
    def search(self, info):
        return "papi's pizza place"

class ActionSearchRestaurants(Action):
    def name(self):
        return 'action_ricerca_ristoranti'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Loocking for restaurants")
        restaurant_api = RestaurantAPI()
        restaurants = restaurant_api.search(tracker.get_slot("cucina"))
        return [SlotSet("matches", restaurants)]
