import xmltodict
from pprint import pprint
import json
import requests
import dateutil.parser


def itemInfo(countryCode, languageCode, storeCode, itemCode):
    """
    Example Output, used for testing inputted config variables, e.g. storeCode, item, etc
    """
    itemAPIEndpoint = requests.get(
        "https://www.ikea.com/"
        + countryCode
        + "/"
        + languageCode
        + "/iows/catalog/availability/"
        + itemCode
        + "/"
    ).content

    itemDict = xmltodict.parse(itemAPIEndpoint)["ir:ikea-rest"]["availability"][
        "localStore"
    ]

    for stores in itemDict:  # Loop through all stores in the item's dict
        if (
            stores["@buCode"] == storeCode
        ):  # Check if selected store is one selected by end user
            pprint(stores)
            print(
                "Avalable "
                + itemCode
                + " at "
                + storeCode
                + " as of "
                + dateutil.parser.parse(stores["stock"]["validDate"]).strftime(
                    "%d/%m/%Y"
                )
                + " : "
                + str(stores["stock"]["availableStock"])
            )  # Example output
        else:
            pass  # Skip to next dict as it is not what user requires


def itemLocation(countryCode, languageCode, storeCode, itemCode):
    """
    Output Item Location
    
    Prints per item and per store, will return in the future
    
    Item Types:
    
    CONTACT_STAFF
    BOX_SHELF - box, shelf
    SPECIALITY_SHOP - specialityShop
    
    """

    d = dict()

    itemAPIEndpoint = requests.get(
        "https://www.ikea.com/"
        + countryCode
        + "/"
        + languageCode
        + "/iows/catalog/availability/"
        + itemCode
        + "/"
    ).content

    itemDict = xmltodict.parse(itemAPIEndpoint)["ir:ikea-rest"]["availability"][
        "localStore"
    ]

    for stores in itemDict:  # Loop through all stores in the item's dict
        if (
            stores["@buCode"] == storeCode
        ):  # Check if selected store is one selected by end user
            # print(
            #    str(stores["stock"]["findItList"]["findIt"])
            # )  # Example output
            if stores["stock"]["findItList"]["findIt"]["type"] == "CONTACT_STAFF":
                print(stores["stock"]["findItList"]["findIt"]["type"])

                d["status"] = "success"
                d["store"] = storeCode
                d["item"] = itemCode
                d["type"] = stores["stock"]["findItList"]["findIt"]["type"]

                return d

            elif stores["stock"]["findItList"]["findIt"]["type"] == "SPECIALITY_SHOP":
                print(
                    stores["stock"]["findItList"]["findIt"]["type"]
                    + " "
                    + stores["stock"]["findItList"]["findIt"]["specialityShop"],
                )

                d["status"] = "success"
                d["store"] = storeCode
                d["item"] = itemCode
                d["type"] = stores["stock"]["findItList"]["findIt"]["type"]
                d["humanReadable"] = stores["stock"]["findItList"]["findIt"][
                    "specialityShop"
                ]

                return d

            elif stores["stock"]["findItList"]["findIt"]["type"] == "BOX_SHELF":
                print(
                    stores["stock"]["findItList"]["findIt"]["type"]
                    + " "
                    + stores["stock"]["findItList"]["findIt"]["box"]
                    + " "
                    + stores["stock"]["findItList"]["findIt"]["shelf"]
                )

                d["status"] = "success"
                d["store"] = storeCode
                d["item"] = itemCode
                d["type"] = stores["stock"]["findItList"]["findIt"]["type"]
                d["box"] = stores["stock"]["findItList"]["findIt"]["box"]
                d["shelf"] = stores["stock"]["findItList"]["findIt"]["shelf"]

                return d

            else:

                d["status"] = "failure"
                return d

        else:
            pass  # Skip to next dict as it is not what user requires
