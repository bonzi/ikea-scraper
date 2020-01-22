from ikea_scraper import itemLocation, itemInfo, itemStock
from pprint import pprint

testStores = [
    "261",
    "267",
    "150",
]  # IKEA Leeds, IKEA Cardiff, IKEA Coventry. See stores.json for list of most IKEA Store Codes by Country
testItems = [
    "00276862",
    "40248513",
    "80227797",
    "70435160",
    "60435207",
    "90406878",
    "80424255",
    "10277366",
    "40415012",
    "30286416",
    "00432872",
    "00436295",
    "80388361",
    "70440618",
    "90432231",
    "00346407",
    "00286267",
    "30373588",
    "50455234",
]  # Random Items

countryCode = "gb"

languageCode = "en"

# itemInfo("186", "00276862")

for store in testStores:
    for item in testItems:
        a = itemStock(countryCode, languageCode, store, item)
        pprint(a)
