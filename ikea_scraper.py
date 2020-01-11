import xmltodict
from pprint import pprint
import json
import requests
import dateutil.parser


def itemInfo(storeNum, items):
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


def itemLocation(storeNum, items):
    returnable = []
    """
    Output Item Location
    
    Prints per item and per store, will return in the future
    
    Item Types:
    
    CONTACT_STAFF
    BOX_SHELF - box, shelf
    SPECIALITY_SHOP - specialityShop
    
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
                    # print(
                    #    str(stores["stock"]["findItList"]["findIt"])
                    # )  # Example output
                    if (
                        stores["stock"]["findItList"]["findIt"]["type"]
                        == "CONTACT_STAFF"
                    ):
                        print(stores["stock"]["findItList"]["findIt"]["type"])
                        returnable.append(
                            (
                                ["store", ikeaStore],
                                ["item", item],
                                stores["stock"]["findItList"]["findIt"]["type"],
                            )
                        )

                    elif (
                        stores["stock"]["findItList"]["findIt"]["type"]
                        == "SPECIALITY_SHOP"
                    ):
                        print(
                            stores["stock"]["findItList"]["findIt"]["type"]
                            + " "
                            + stores["stock"]["findItList"]["findIt"]["specialityShop"],
                        )
                        returnable.append(
                            (
                                ["store", ikeaStore],
                                ["item", item],
                                stores["stock"]["findItList"]["findIt"]["type"],
                                stores["stock"]["findItList"]["findIt"][
                                    "specialityShop"
                                ],
                            )
                        )
                    elif stores["stock"]["findItList"]["findIt"]["type"] == "BOX_SHELF":
                        print(
                            stores["stock"]["findItList"]["findIt"]["type"]
                            + " "
                            + stores["stock"]["findItList"]["findIt"]["box"]
                            + " "
                            + stores["stock"]["findItList"]["findIt"]["shelf"]
                        )
                        returnable.append(
                            (
                                ["store", ikeaStore],
                                ["item", item],
                                stores["stock"]["findItList"]["findIt"]["type"],
                                stores["stock"]["findItList"]["findIt"]["box"],
                                stores["stock"]["findItList"]["findIt"]["shelf"],
                            )
                        )
                    else:
                        return TypeError

                else:
                    pass  # Skip to next dict as it is not what user requires
    return returnable
