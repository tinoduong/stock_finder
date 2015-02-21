import json
import queries

from pymongo import MongoClient
from bson import json_util
from jinja2 import Template


client = MongoClient('localhost', 27017)
db = client.stock_finder
stocks = db.stocks

def print_mr_results(records):
    for record in records.find():
        print record

def print_query_results(records):
    for record in records:
        print json.dumps(record, default=json_util.default, indent=4, sort_keys=True)


DROP_RANGE = -7
GAIN_RANGE = 5
LOW_RANGE = 1.2

template = Template('Hello {{ name }}!')
template.render(name='woah')

print 'done'

# low = queries.near_fifty_two_week_low(["Technology", "Favourites"], LOW_RANGE)
# print_query_results(low)
#
# drop = queries.biggest_drop_in_last_day(["Technology"], DROP_RANGE)
# print_query_results(drop)
#
gain = queries.biggest_gain_in_last_day(["Favourites"], GAIN_RANGE)
print_query_results(gain)
#
# low_and_drop = queries.drop_in_last_day_and_near_low(["Technology"], LOW_RANGE, DROP_RANGE)
# print_mr_results(low_and_drop)