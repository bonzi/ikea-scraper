import xmltodict
from pprint import pprint
import json
import requests
import dateutil.parser

storeNum = ["186", "150"]
# IKEA Leeds, IKEA Cardiff
items = ["30373588", "50455234"]
# BLÅHAJ Large, BLÅHAJ Small


def itemInfo():
    """
    Example Output, used for testing inputted config variables, e.g. storeNum, items, etc
    """
    for item in items:

        itemAPIEndpoint = requests.get(
            "https://www.ikea.com/gb/en/iows/catalog/availability/" + item + "/"
        ).content

        itemDict = xmltodict.parse(itemAPIEndpoint)["ir:ikea-rest"]["availability"][
            "localStore"
        ]

        for ikeaStore in storeNum:  # Loop through store ID's in the store arrays
            for stores in itemDict:  # Loop through all stores in the item's dict
                if (
                    stores["@buCode"] == ikeaStore
                ):  # Check if selected store is one selected by end user
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
                    )  # Example output
                else:
                    pass  # Skip to next dict as it is not what user requires


itemInfo()
