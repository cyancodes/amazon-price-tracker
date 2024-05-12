from scraper import PriceScraper
from item_manager import ItemManager
from gui import GUI

price_scraper = PriceScraper()
item_manager = ItemManager(price_scraper)
gui = GUI(item_manager)

# Future Updates - email alerts, input validation, ordered dictionary, scrolling


