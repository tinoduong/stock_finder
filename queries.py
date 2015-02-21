from pymongo import MongoClient
from bson.code import Code

client = MongoClient('localhost', 27017)
db = client.stock_finder
stocks = db.stocks
import re
# All stocks trading within 20% of yearly low
# def near_fifty_two_week_low(filters=[], low_percent_range=1.3):
#
#     sectors = {} if len(filters) == 0 else {"sector": {"$all": filters}}
#
#     mapper = Code("""
#                 function () {
#                     var price = this.price,
#                         low = this.year_low,
#                 """
#                 "        high = this.year_low * " + str(low_percent_range) + ";"
#                 """
#                     if (price <= high) {
#                         emit(this._id, this);
#                     }
#                 }
#                """)
#
#     # no need for reduce because we are only emitting once (on the unique _id)
#     reducer = Code("")
#
#     return stocks.map_reduce(mapper, reducer, "myresults", query=sectors)

def near_fifty_two_week_low(filters=[], low_percent_range=1.3):

    mapper = Code("""
                  function () {
                    return this;
                  }
                  """)

    dir(stocks.find({}))
    stocks.find({}).each(mapper)


# All stocks trading near 52 week low, and just dropped in the last day
def drop_in_last_day_and_near_low(filters, low_percent_range=1.3, drop_percentage_range=-7):

    sectors = {} if len(filters) == 0 else {"sector": {"$all": filters}}

    mapper = Code("""
                function () {
                    var price = this.price,
                        daily_percentage_gain = this.daily_percentage_gain,
                        low = this.year_low,
                """
                "       high = this.year_low * " +  str(low_percent_range) + ","
                "       threshold = " + str(drop_percentage_range) + ";"
                """
                    if ((daily_percentage_gain <= threshold) && (price <= high)) {
                        emit(this._id, this);
                    }
                }
               """)

    # no need for reduce because we are only emitting once (on the unique _id)
    reducer = Code("")

    return stocks.map_reduce(mapper, reducer, "myresults", query=sectors)


# All the stocks that dropped at least 7 percent or more today
def biggest_drop_in_last_day(filters=[], drop_percentage_range=-7):
    sectors = {} if len(filters) == 0 else {"$all": filters}
    return stocks.find({"$query": {"daily_percentage_gain": {"$lte": drop_percentage_range}, "sector": sectors},
                        "$orderby":  {"daily_percentage_gain": 1}})


def biggest_gain_in_last_day(filters=[], gain_percentage_range=7):
    sectors = {} if len(filters) == 0 else {"$all": filters}
    return stocks.find({"$query": {"daily_percentage_gain": {"$gte": gain_percentage_range}, "sector": sectors},
                        "$orderby":{"daily_percentage_gain":-1}})
