import json
from datetime import datetime

class ItemManager:
    def __init__(self, price_scraper):
        self.price_scraper = price_scraper
        self.today = self.get_today()
        self.tracked_items = self.get_items_from_json()

    def check_items_price(self):  # Updates the current value for each item
        self.today = self.get_today()
        for (key, value) in self.tracked_items.items():
            current_price = self.price_scraper.price_scrape(value["url"])
            value["current_price"] = current_price
            value["price_history"][self.today] = current_price

        with open("tracked_items.json", "w") as item_json:
            json.dump(self.tracked_items, item_json, indent=4)

    def get_items_from_json(self):
        try:  # Attempts to open a pre-existing json file
            with open("tracked_items.json", "r") as item_json:
               return json.load(item_json)  # Reading old JSON
        except FileNotFoundError:  # If a file not found, creates an empty one
            with open("tracked_items.json", "w") as item_json:
                json.dump({}, item_json, indent=4)
                return {}

    def return_current_prices(self):
        # This line of code creates a list of all items along with their prices and returns them as a formatted string.
        self.today = self.get_today()
        prices_list = []
        for (key, value) in self.tracked_items.items():
            # Starts by getting the value for the previous entry using a try statement in case there isn't any price history yet
            try:
                previous_price = list(value["price_history"].values())[-2]
                previous_day = list(value["price_history"].keys())[-2]
            except IndexError:
                previous_price = value["current_price"]
                previous_day = self.today

            # Calculating the percentage change on last entry
            difference = value["current_price"]-previous_price
            percentage_difference = round((difference / abs(previous_price)) * 100, 2)
            if difference >= 0:
                change_on_date = f"+{percentage_difference}% from {previous_day}"
            else:
                change_on_date = f"-{percentage_difference}% from {previous_day}"

            entry = f"{key}: £{value["current_price"]}    {change_on_date}"
            prices_list.append(entry)
        return '\n'.join(prices_list)

    def return_price_history(self, item):
        return '\n'.join(f"{key} - £{value}" for (key, value) in self.tracked_items[item]["price_history"].items())

    def update_item(self, new_item, old_item, url, cutoff):
        # If the key has changed, this copies the data from the old key, and pastes it in the new one,
        # before deleting and adding
        if new_item not in self.tracked_items.keys():
            self.tracked_items[new_item] = self.tracked_items.pop(old_item)

        # Updating the URL and Cutoff with what's in the remaining fields
        self.tracked_items[new_item]["url"] = url
        self.tracked_items[new_item]["cutoff"] = cutoff

    def add_items(self, item, url, cutoff):  # Adds new items
        if item not in self.tracked_items.keys():  # Will only trigger if the new item isn't in the dictionary
            item_price = self.price_scraper.price_scrape(url)  # Automatically scrapes the current price to add to json
            new_item = {
                item: {
                    "url": url,
                    "cutoff": cutoff,
                    "current_price": item_price,
                    "price_history": {
                        self.today: item_price}
                }
            }
            self.tracked_items.update(new_item)  # Updating old data with new data
            self.update_json()

    def delete_item(self, item):
        if item: # Returns true if it's not empty
            del self.tracked_items[item]

    def update_json(self):
        with open("tracked_items.json", "w") as item_json:
            json.dump(self.tracked_items, item_json, indent=4)

    def get_today(self):
        return datetime.today().date().strftime("%d/%m/%y")
