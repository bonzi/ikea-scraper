import requests
from pprint import pprint

countryCode = "gb"
languageCode = "en"
storeCode = "267"
itemCode = "00346407"


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
