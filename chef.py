import requests
from pprint import pprint
from ikea_scraper import itemLocation

countryCode = "gb"
languageCode = "en"
storeCode = "261"
itemCode = "40248513"


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
itemAPIEndpointContent = itemAPIEndpoint.json()
pprint(itemAPIEndpointContent)

pprint(itemLocation(countryCode, languageCode, storeCode, itemCode))