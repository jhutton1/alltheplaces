from locations.geo import extract_geojson_point_geometry
from locations.items import Feature


class DictParser:
    # Variations can't handle capitalised acronyms such as "ID" so
    # the common variants of case including such acronyms need to
    # all be listed below.
    ref_keys = [
        # EN
        "ref",
        "id",
        "identifier",
        "store-id",
        "StoreID",
        "storeID",
        "storeId",
        "store-number",
        "shop-number",
        "location-id",
        "LocationID",
        "locationID",
        "location-number",
        "slug",
        "store-code",
        "item-id",
        "ItemID",
        "itemID",
        "branch-id",
        "BranchID",
        "branchID",
        "branch-code",
        # ES
        "id-tienda",
        "ID-tienda",
    ]

    name_keys = [
        # EN
        "name",
        "store-name",
        "display-name",
        "title",
        "business-name",
        "item-name",
        "location-name",
        "loc-name",
        "branch-name",
        # ES
        "nombre",
        # IT
        "nome",
    ]

    house_number_keys = [
        # EN
        "house-number",
        "house-no",
        "street-number",
        "street-no",
        "address-street-no",
    ]

    full_address_keys = [
        # EN
        "address",
        "addr",
        "store-address",
        "physical-address",
        "full-address",
        "formattedAddress",
        # ES
        "direccion",  # "address"
    ]

    street_keys = [
        # EN
        "street",
        "street-name",
        # DE
        "strasse",
    ]

    street_address_keys = [
        # EN
        "street-address",
        "address1",
        "address-line",
        "address-line1",
        "line1",
        "address-line-one",
        "address-street",
        # JP
        "町域以下住所",  # "address below town limits"
        # IT
        "indirizzo",
    ]

    city_keys = [
        # EN
        "address-locality",
        "city",
        "address-city",
        "physical-city",
        "town",
        "locality",
        "suburb",
        "physical-suburb",
        "city-name",
        "store-city",
        # JP
        "市区町村",  # "municipality"
        # PL
        "miasto",
        # ES
        "ciudad",  # "city"
        # IT
        "comune",  # "comune",
        "citta",
        # DE
        "ort",  # location
    ]

    region_keys = [
        # EN
        "address-region",
        "region",
        "state",
        "state-province",
        "province",
        "state-code",
        "county",
        "state-name",
        "store-state",
        "store-province",
        "storeProvince",
        "prefecture",
        # JP
        "都道府県",  # "prefecture"
        # IT
        "regione",  # "region"
    ]

    country_keys = [
        # EN
        "country-code",
        "address-country",
        "country",
        "country-name",
        "store-country",
    ]

    isocode_keys = [
        "iso-code",
    ]

    postcode_keys = [
        # EN
        "postal-code",
        "post-code",
        "postcode",
        "zip",
        "zipcode",
        "address-post-code",
        "postal",
        "zip-code",
        "address-postal-code",
        "store-postcode",
        "store-post-code",
        "store-postal-code",
        "store-zip",
        "store-zip-code",
        "store-zipcode",
        "address-zip",
        # JP
        "郵便番号",  # "post code"
        # DE
        "plz",
        "postleitzahl",
        # IT
        "cap",
    ]

    email_keys = [
        # EN
        "email",
        "contact-email",
        "email-address",
        "email1",
        "store-email",
    ]

    phone_keys = [
        # EN
        "phone-number",
        "phone",
        "telephone",
        "tel",
        "tel-no",
        "telephone-number",
        "telephone1",
        "contact-number",
        "phone-no",
        "contact-phone",
        "store-phone",
        "primary-phone",
        "primaryNumber",
        "main-phone",
        "branch-phone",
        "branch-telephone",
        # ES
        "telefono",  # "phone"
    ]

    lat_keys = [
        # EN
        "latitude",
        "lat",
        "store-latitude",
        "storeLatitude",
        "display-lat",
        "yext-display-lat",
        "map-latitude",
        "geo-lat",
        "GPSLat",
        "geographicCoordinatesLatitude",
        # ES
        "coordenaday",  # "Coordinate Y"
        "latitud",
    ]

    lon_keys = [
        # EN
        "longitude",
        "lon",
        "long",
        "lng",
        "store-longitude",
        "storeLongitude",
        "display-lng",
        "yext-display-lng",
        "map-longitude",
        "geo-lng",
        "geo-long",
        "GPSLong",
        "geographicCoordinatesLongitude",
        # ES
        "coordenadax",  # "Coordinate X"
        "longitud",
    ]

    website_keys = [
        # EN
        "url",
        "website",
        "permalink",
        "store-url",
        "storeURL",
        "website-url",
        "websiteURL",
        "location-url",
        "web-address",
        "WebSiteURL",
    ]

    hours_keys = [
        "hours",
        "opening-hours",
        "open-hours",
        "store-opening-hours",
        "store-hours",
        # IT
        "orario",
        "orari",
    ]

    twitter_keys = [
        "twitter",
        "twitter-link",
        "twitter-url",
    ]

    facebook_keys = [
        "facebook",
        "facebook-link",
        "facebook-url",
    ]

    @staticmethod
    def parse(obj: dict) -> Feature:
        item = Feature()

        item["ref"] = DictParser.get_first_key(obj, DictParser.ref_keys)
        item["name"] = DictParser.get_first_key(obj, DictParser.name_keys)

        if obj.get("geometry") and obj["geometry"].get("type") in [
            "Point",
            "MultiPoint",
            "LineString",
            "MultiLineString",
            "Polygon",
            "MultiPolygon",
        ]:
            if rfc7946_point_geometry := extract_geojson_point_geometry(obj["geometry"]):
                item["geometry"] = rfc7946_point_geometry
            elif obj["geometry"]["type"] != "Point":
                # Source geometry is supplied as a non-Point geometry type
                # (such as Polygon) and should be returned as-is. There are no
                # further checks done to ensure this geometry is valid RFC7946
                # GeoJSON or GJ2008 geometry.
                item["geometry"] = obj["geometry"]
        else:
            location = DictParser.get_first_key(
                obj,
                [
                    "location",
                    "geo-location",
                    "geo",
                    "geo-point",
                    "geocoded-coordinate",
                    "coordinates",
                    "coords",
                    "geo-position",
                    "position",
                    "positions",
                    "display-coordinate",
                    "yextDisplayCoordinate",
                ],
            )
            if location and isinstance(location, dict):
                # Latitude/longitude are wrapped inside a "coordinates" /
                # "location" style of named dictionary.
                item["lat"] = DictParser.get_first_key(location, DictParser.lat_keys)
                item["lon"] = DictParser.get_first_key(location, DictParser.lon_keys)
            else:
                # Latitude/longitude are properties of the root dictionary or
                # any other nested dictionary of any name.
                item["lat"] = DictParser.get_first_key(obj, DictParser.lat_keys)
                item["lon"] = DictParser.get_first_key(obj, DictParser.lon_keys)

        address = DictParser.get_first_key(obj, DictParser.full_address_keys)

        if address and isinstance(address, str):
            item["addr_full"] = address

        if not address or not isinstance(address, dict):
            address = obj

        item["housenumber"] = DictParser.get_first_key(address, DictParser.house_number_keys)
        item["street"] = DictParser.get_first_key(address, DictParser.street_keys)
        item["street_address"] = DictParser.get_first_key(address, DictParser.street_address_keys)
        item["city"] = DictParser.get_first_key(address, DictParser.city_keys)
        item["state"] = DictParser.get_first_key(address, DictParser.region_keys)
        item["postcode"] = DictParser.get_first_key(address, DictParser.postcode_keys)

        country = DictParser.get_first_key(address, DictParser.country_keys)
        if country and isinstance(country, dict):
            isocode = DictParser.get_first_key(country, DictParser.isocode_keys)
            if isocode and isinstance(isocode, str):
                item["country"] = isocode
            # TODO: Handle other potential country fields inside the dict?
        else:
            item["country"] = country

        contact = DictParser.get_first_key(obj, ["contact"])
        if not contact or not isinstance(contact, dict):
            contact = obj

        item["email"] = DictParser.get_first_key(contact, DictParser.email_keys)
        item["phone"] = DictParser.get_first_key(contact, DictParser.phone_keys)
        item["website"] = DictParser.get_first_key(contact, DictParser.website_keys)
        item["twitter"] = DictParser.get_first_key(contact, DictParser.twitter_keys)
        item["facebook"] = DictParser.get_first_key(contact, DictParser.facebook_keys)

        return item

    @staticmethod
    def get_first_key(obj, keys):
        for key in keys:
            variations = DictParser.get_variations(key)
            for variation in variations:
                if obj.get(variation):
                    return obj[variation]

    @staticmethod
    def get_variations(key):
        results = set()
        results.add(key)

        lower = key.lower()
        results.add(lower)

        upper = key.upper()
        results.add(upper)

        title = key.title()
        results.add(title)

        # example: flatcase
        flatcase = key.lower().replace("-", "")
        results.add(flatcase)

        # example: FLATCASEUPPER
        flatcase_upper = flatcase.upper()
        results.add(flatcase_upper)

        # example: camelCase
        camel_case = key[0].lower()
        i = 1
        while i < len(key):
            if key[i] == "-":
                i += 1
                camel_case += key[i].upper()
            else:
                camel_case += key[i]
            i += 1

        results.add(camel_case)

        # example: PascalCase
        pascal_case = camel_case[0].upper() + camel_case[1:]

        results.add(pascal_case)

        # example: snake_case
        snake_case = key.lower().replace("-", "_")
        results.add(snake_case)

        # example: SCREAMING_SNAKE_CASE
        screaming_snake_case = key.upper().replace("-", "_")
        results.add(screaming_snake_case)

        # example: camel_Snake_Case
        camel_snake_case = key[0].lower()
        i = 1
        while i < len(key):
            if key[i] == "-":
                i += 1
                camel_snake_case += "_"
                camel_snake_case += key[i].upper()
            else:
                camel_snake_case += key[i]
            i += 1

        results.add(camel_snake_case)

        # example: Pascal_Snake_Case
        pascal_snake_case = camel_snake_case[0].upper() + camel_snake_case[1:]

        results.add(pascal_snake_case)

        return results

    @staticmethod
    def get_nested_key(obj, key):
        """
        Return value for first matching key in an object, traversing lists and dicts.
        :param obj: the object to traverse
        :param key: the key to match
        :return: the first matching value, or None
        """
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == key:
                    return v
                if val := DictParser.get_nested_key(v, key):
                    return val
        elif isinstance(obj, list):
            for x in obj:
                if val := DictParser.get_nested_key(x, key):
                    return val
        return None

    @staticmethod
    def iter_matching_keys(obj, key):
        """
        An iterator for values for all matching keys in an object, traversing lists and dicts.
        :param obj: the object to traverse
        :param key: the key to match
        :return: value iterator for all matching keys
        """
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == key:
                    yield v
                else:
                    yield from DictParser.iter_matching_keys(v, key)
        elif isinstance(obj, list):
            for x in obj:
                yield from DictParser.iter_matching_keys(x, key)
