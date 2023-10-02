from scrapy.spiders import SitemapSpider

from locations.categories import Categories
from locations.structured_data_spider import StructuredDataSpider


class MacysBackstageSpider(SitemapSpider, StructuredDataSpider):
    name = "macys_backstage"
    item_attributes = {"brand": "Macy's Backstage", "brand_wikidata": "Q122914589", "extras": Categories.SHOP_DEPARTMENT_STORE.value}
    sitemap_urls = ["https://stores.macysbackstage.com/sitemap.xml"]
    wanted_types = ["DepartmentStore"]
