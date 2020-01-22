from prometheus_client import CollectorRegistry, Gauge, ProcessCollector

from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app

from ikea_scraper import itemStock
from pprint import pprint

# Create my app
app = Flask(__name__)

# ikea_leeds_blahaj_currentStockDict = itemStock("gb", "en", "261", "30373588")
# ikea_cardiff_blahaj_currentStockDict = itemStock("gb", "en", "267", "30373588")


registry = CollectorRegistry()


ikea_leeds_blahaj_currentStockGague = Gauge(
    "IKEA_Leeds_BLAHAJ_currentStock",
    str(
        "Current stock level of "
        + itemStock("gb", "en", "261", "30373588")["item"]
        + " at "
        + itemStock("gb", "en", "261", "30373588")["storeName"]
    ),
    registry=registry,
)
ikea_leeds_blahaj_currentStockGague.set_function(
    lambda: int(itemStock("gb", "en", "261", "30373588")["currentStock"])
)

ikea_cardiff_blahaj_currentStockGague = Gauge(
    "IKEA_Cardiff_BLAHAJ_currentStock",
    str(
        "Current stock level of "
        + itemStock("gb", "en", "267", "30373588")["item"]
        + " at "
        + itemStock("gb", "en", "267", "30373588")["storeName"]
    ),
    registry=registry,
)
ikea_cardiff_blahaj_currentStockGague.set_function(
    lambda: int(itemStock("gb", "en", "267", "30373588")["currentStock"])
)

# ikea_cardiff_blahaj_forcastedStockGague = Gauge(
#     "IKEA_Cardiff_BLAHAJ_forcastedStock",
#     str(
#         "Forcasted stock level of "
#         + itemStock("gb", "en", "267", "30373588")["item"]
#         + " at "
#         + itemStock("gb", "en", "267", "30373588")["storeName"]
#     ),
#     registry=registry,
# )
# ikea_cardiff_blahaj_forcastedStockGague.set_function(
#     lambda: int(
#         itemStock("gb", "en", "267", "30373588")["forcastedStock"][0]["availableStock"]
#     )
# )
# Add prometheus wsgi middleware to route /metrics requests
app_dispatch = DispatcherMiddleware(app, {"/metrics": make_wsgi_app(registry=registry)})


@app.route("/")
def index():
    return "Welcome"
