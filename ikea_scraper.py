import xmltodict
from pprint import pprint
import json
import requests
import dateutil.parser


def itemInfo(countryCode: str, languageCode: str, storeCode: str, itemCode: str):
    d = dict()
    """
    itemInfo
    --------
    Example Output, used for testing inputted config variables, e.g. storeCode, item, etc
    
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
    """
    itemAPIEndpoint = requests.get(
        "https://www.ikea.com/"
        + countryCode
        + "/"
        + languageCode
        + "/iows/catalog/availability/"
        + itemCode
        + "/"
    )

    if itemAPIEndpoint.headers["Content-Type"] != "text/xml;charset=UTF-8":
        print(
            "Error: Status " + str(itemAPIEndpoint.status_code) + ", Invalid Item Code"
        )
        d["status"] = "failure"
        d["code"] = "404"
        d["message"] = "Invalid Item Code"
        return d

    else:

        itemAPIEndpointContent = itemAPIEndpoint.content

        itemDict = xmltodict.parse(itemAPIEndpointContent)["ir:ikea-rest"][
            "availability"
        ]["localStore"]

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


def itemLocation(countryCode: str, languageCode: str, storeCode: str, itemCode: str):
    """
    itemLocation
    ------------
    Output Item Location
    
    Prints per item and per store.
    Returns JSON Dictionary for use
    
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
        JSON Array/Dictionary of formatted API Data
        
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
        "https://www.ikea.com/"
        + countryCode
        + "/"
        + languageCode
        + "/iows/catalog/availability/"
        + itemCode
        + "/"
    )
    if itemAPIEndpoint.headers["Content-Type"] != "text/xml;charset=UTF-8":
        print(
            "Error: Status " + str(itemAPIEndpoint.status_code) + ", Invalid Item Code"
        )
        d["status"] = "failure"
        d["code"] = "404"
        d["message"] = "Invalid Item Code"
        return d

    else:
        itemAPIEndpointContent = itemAPIEndpoint.content

        itemDict = xmltodict.parse(itemAPIEndpointContent)["ir:ikea-rest"][
            "availability"
        ]["localStore"]

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

                elif (
                    stores["stock"]["findItList"]["findIt"]["type"] == "SPECIALITY_SHOP"
                ):
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
                pass  # Skip to next dict as it is not what user requires
