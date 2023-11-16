import json

import scrapy

from locations.hours import OpeningHours
from locations.categories import Categories, apply_category, apply_yes_no, Fuel
from locations.dict_parser import DictParser


class KumAndGoSpider(scrapy.Spider):
    name = "kum_and_go"
    item_attributes = {"brand": "Kum & Go", "brand_wikidata": "Q6443340"}
    allowed_domains = ["kumandgo.com"]

    def start_requests(self):
        states_list = ["ia","ar","co","mn","mo","mt","ne","nd","ok","sd","wy",]
        for state in states_list:
            yield scrapy.Request(f'https://app.kumandgo.com/api/stores/nearest?q={state}')


    def parse(self, response):
        result = json.loads(response.text)
        for store in result.get("data"):
            item = DictParser.parse(store)
            apply_category(Categories.SHOP_CONVENIENCE, item)

            fuels = store["features"].get("fuelProducts")
            if fuels:
                apply_category(Categories.FUEL_STATION, item)
                apply_yes_no(Fuel.E85, item, "E85" in fuels)
                apply_yes_no(Fuel.E15, item, "E15" in fuels)
                apply_yes_no(Fuel.KEROSENE, item, "Kerosene" in fuels)
                apply_yes_no(Fuel.ETHANOL_FREE, item, "Premium - Ethanol Free" or "Midgrade - Ethanol Free" in fuels)
                apply_yes_no(Fuel.OCTANE_93, item, "Premium Plus (93 octane)" in fuels)
                apply_yes_no(Fuel.DIESEL, item, "Diesel" or "Xtreme Diesel" in fuels)
            
            oh = OpeningHours()
            for hours in store["storeHours"].get("hours"):
                if hours.get("displayText") is not None:
                    oh.add_ranges_from_string(hours.get("day") + " " + hours.get("displayText")) 
            item["opening_hours"] = oh.as_opening_hours()

            yield item


