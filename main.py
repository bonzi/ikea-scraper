import xmltodict
from pprint import pprint
import json
import requests

my_xml = requests.get("https://www.ikea.com/gb/en/iows/catalog/availability/30373588/").content # IKEA Shark

my_dict = xmltodict.parse(my_xml)['ir:ikea-rest']["availability"]["localStore"]

store_id = 186 # IKEA Leeds

for store in my_dict:
	if store['@buCode'] == 186:
		pprint(store)
	else:
		pass
