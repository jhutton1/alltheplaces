from scrapy.spiders import SitemapSpider

from locations.categories import Categories
from locations.structured_data_spider import StructuredDataSpider


class WelcomeGB(SitemapSpider, StructuredDataSpider):
    name = "welcome"
    item_attributes = {"brand": "Welcome", "brand_wikidata": "Q123004215", "extras": Categories.SHOP_CONVENIENCE.value}
    sitemap_urls = ["https://stores.welcome-stores.co.uk/sitemap.xml"]
    sitemap_rules = [
        (
            r"https:\/\/stores\.welcome-stores\.co\.uk\/[-\w]+\/[-\w]+\/[-\w]+\.html$",
            "parse_sd",
        )
    ]
    wanted_types = ["GroceryStore"]
