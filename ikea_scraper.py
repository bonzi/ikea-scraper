from pprint import pprint
import json
import requests
import dateutil.parser

with open("stores.json", "r", encoding="utf-8") as storesJSONFile:
    storesJSON = json.load(storesJSONFile)


def itemLocation(countryCode: str, languageCode: str, storeCode: str, itemCode: str):
    """
    itemLocation
    ------------
    Return Item Location Dictionary
    
    Parameters
    ----------
    countryCode: str
        User's country code - e.g. gb, us, de, fr, etc
    languageCode: str
        User's language code, e.g. en, de, fr, etc
    storeCode: str
        User's store code, Some UK ones can be found here: http://curlybrackets.co/blog/2016/04/05/scraping-ikea-api-php/
    itemCode: str
        User's item code, usually denoted xxx.xxx.xx - Provide to library without the full stop/period's
    
    Returns
    -------
    d : dict of str
        Dictionary of formatted API Data
        
    Item Types
    ----------
    CONTACT_STAFF: str
        No Child Data
    BOX_SHELF: str
        box: str, shelf: str
    SPECIALITY_SHOP
        specialityShop: str    
    """

    d = dict()

    itemAPIEndpoint = requests.get(
        "https://iows.ikea.com/retail/iows/"
        + countryCode
        + "/"
        + languageCode
        + "/stores/"
        + storeCode
        + "/availability/ART/"
        + itemCode,
        headers={
            "Accept": "application/vnd.ikea.iows+json;version=1.0",
            "Contract": "37249",
            "Consumer": "MAMMUT",
        },
    )

    if itemAPIEndpoint.headers["Content-Type"] != "application/json":
        print(
            "Error: Status " + str(itemAPIEndpoint.status_code) + ", Invalid Item Code"
        )
        d["status"] = "failure"
        d["code"] = str(itemAPIEndpoint.status_code)
        d["message"] = "Invalid Item Code"
        return d

    else:
        itemAPIEndpointContent = itemAPIEndpoint.json()["StockAvailability"]

        if (
            itemAPIEndpointContent["RetailItemAvailability"]["SalesMethodCode"]["$"]
            == "0"
        ):  # Speciality Shop, e.g. Children's IKEA. Known to break with IKEA Food, which lacks a stock number, and sales location, but has the 0 code
            if (
                len(
                    itemAPIEndpointContent["RetailItemAvailability"][
                        "RecommendedSalesLocation"
                    ].keys()
                )
                == 0
            ):
                d["status"] = "failure"
                d["code"] = "404"
                d[
                    "message"
                ] = "Invalid Item Code, this item may be an IKEA Food item, and as such has no real values on the API"
                d["item"] = itemCode

                return d

            else:
                d["status"] = "success"
                d["store"] = storeCode
                d["storeName"] = storesJSON[countryCode][storeCode]
                d["item"] = itemCode
                # d["type"] = stores["stock"]["findItList"]["findIt"]["type"] # Type no longer works on new API
                d["humanReadable"] = itemAPIEndpointContent["RetailItemAvailability"][
                    "RecommendedSalesLocation"
                ]["$"]

                return d

        elif (
            itemAPIEndpointContent["RetailItemAvailability"]["SalesMethodCode"]["$"]
            == "1"
        ):  # Aisle/Shelve
            d["status"] = "success"
            d["store"] = storeCode
            d["storeName"] = storesJSON[countryCode][storeCode]
            d["item"] = itemCode
            #            d["type"] = stores["stock"]["findItList"]["findIt"]["type"]
            d["aisle"] = str(
                itemAPIEndpointContent["RetailItemAvailability"][
                    "RecommendedSalesLocation"
                ]["$"]
            )[:2]
            d["shelf"] = str(
                itemAPIEndpointContent["RetailItemAvailability"][
                    "RecommendedSalesLocation"
                ]["$"]
            )[2:4]
            d["subShelf"] = str(
                itemAPIEndpointContent["RetailItemAvailability"][
                    "RecommendedSalesLocation"
                ]["$"]
            )[4:6]
            return d

        elif (
            itemAPIEndpointContent["RetailItemAvailability"]["SalesMethodCode"]["$"]
            == "2"
            or "3"
        ):  # Contact Staff
            d["status"] = "success"
            d["store"] = storeCode
            d["storeName"] = storesJSON[countryCode][storeCode]
            d["item"] = itemCode
            d["type"] = "Contact Staff"

            return d


def itemStock(countryCode: str, languageCode: str, storeCode: str, itemCode: str):
    """
    itemStock
    ------------
    Return Item Stock as a Dictionary
    
    
    Parameters
    ----------
    countryCode: str
        User's country code - e.g. gb, us, de, fr, etc
    languageCode: str
        User's language code, e.g. en, de, fr, etc
    storeCode: str
        User's store code, Some UK ones can be found here: http://curlybrackets.co/blog/2016/04/05/scraping-ikea-api-php/
    itemCode: str
        User's item code, usually denoted xxx.xxx.xx - Provide to library without the full stop/period's
    
    Returns
    -------
    d : dict of str
        Dictionary of formatted API Data
    """

    d = dict()

    itemAPIEndpoint = requests.get(
        "https://iows.ikea.com/retail/iows/"
        + countryCode
        + "/"
        + languageCode
        + "/stores/"
        + storeCode
        + "/availability/ART/"
        + itemCode,
        headers={
            "Accept": "application/vnd.ikea.iows+json;version=1.0",
            "Contract": "37249",
            "Consumer": "MAMMUT",
        },
    )

    if itemAPIEndpoint.headers["Content-Type"] != "application/json":
        print(
            "Error: Status " + str(itemAPIEndpoint.status_code) + ", Invalid Item Code"
        )
        d["status"] = "failure"
        d["code"] = str(itemAPIEndpoint.status_code)
        d["message"] = "Invalid Item Code"
        return d

    else:
        itemAPIEndpointContent = itemAPIEndpoint.json()["StockAvailability"]

        d["status"] = "success"
        d["store"] = storeCode
        d["storeName"] = storesJSON[countryCode][storeCode]
        d["item"] = itemCode
        d["currentStock"] = itemAPIEndpointContent["RetailItemAvailability"][
            "AvailableStock"
        ]["$"]
        d["forcastedStock"] = itemAPIEndpointContent["AvailableStockForecastList"][
            "AvailableStockForecast"
        ]

        return d
