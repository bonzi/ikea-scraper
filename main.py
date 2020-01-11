import xmltodict
from pprint import pprint
import json
import requests
import dateutil.parser

storeNum = ["186", "150"]
# IKEA Leeds, IKEA Cardiff
items = ["30373588", "50455234"]
# BLÅHAJ Large, BLÅHAJ Small

for item in items:

    itemAPIEndpoint = requests.get(
        "https://www.ikea.com/gb/en/iows/catalog/availability/" + item + "/"
    ).content

    itemDict = xmltodict.parse(itemAPIEndpoint)["ir:ikea-rest"]["availability"][
        "localStore"
    ]

    for ikeaStore in storeNum:
        for stores in itemDict:
            if stores["@buCode"] == ikeaStore:
                pprint(stores)
                print(
                    "Avalable "
                    + item
                    + " at "
                    + ikeaStore
                    + " as of "
                    + dateutil.parser.parse(stores["stock"]["validDate"]).strftime(
                        "%d/%m/%Y"
                    )
                    + " : "
                    + str(stores["stock"]["availableStock"])
                )
            else:
                pass
