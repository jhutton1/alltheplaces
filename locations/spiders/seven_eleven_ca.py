from locations.categories import Extras, apply_yes_no, Categories, apply_category
from locations.storefinders.yext import YextSpider


class SevenElevenCASpider(YextSpider):
    name = "seven_eleven_ca"
    item_attributes = {"brand": "7-Eleven", "brand_wikidata": "Q259340"}
    api_key = "4c8292a53c2dae5082ba012bdf783295"

    def parse_item(self, item, location):
        item.pop("twitter")

        apply_yes_no(Extras.DELIVERY, item, "c_delivery" in location)
        apply_yes_no(Extras.ATM, item, "SCOTIABANK_ATM" in location["c_7ElevenServices2"])
        apply_yes_no(Extras.WIFI, item, "WIFI" in location["c_7ElevenServices2"])

        apply_category(Categories.SHOP_CONVENIENCE, item)
        yield item




