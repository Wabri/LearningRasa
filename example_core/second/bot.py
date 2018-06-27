class ActionSearchRestaurants(Action):
    def name(self):
        return 'action_ricerca_ristoranti'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message("Loocking for restaurants")
        restaurant_api = RestaurantAPI()
        restaurants = restaurant_api.search(tracker.get_slot("cucina"))
        return [SlotSet("matches", restaurants)]
