import re
from datetime import datetime
from pyquery import PyQuery as pq

# Take the text from markup and convert to
# float value before we persist to database
def string_to_float(value):
    try:
        toRet = float(value)
    except:
        toRet = 0.0

    return toRet

# Dates are bit tricky because they don't
# seem to be stored in a consistent format
# also they are non-standard
def parse_date(value):

    if len(value) == 0:
        return "N/A"

    # May 12 - May 24 (Est.)
    exp = re.match(r'(\w{3}\s*\d{1,2})\s*-\s*(\w{3}\s*\d{1,2}).', value.strip(), re.I)
    if exp:
        date = exp.group(1) + " 2015"
        return datetime.strptime(date, '%b %d %Y').isoformat()

    # 12-apr-15
    exp = re.match(r'(\d{1,2}-\w{3}-\d{1,2})', value.strip(), re.I)
    if exp:
        date = exp.group(1)
        return datetime.strptime(date, '%d-%b-%y').isoformat()

    return "N/A"


def get_field(col, row):

    if len(col) < row:
        return ""

    element = pq(col[row]);
    return element.text();


def Stock(content, symbol, name):
    dom = pq(content)
    col1 = dom.find("#table1 .yfnc_tabledata1")
    col2 = dom.find("#table2 .yfnc_tabledata1")

    if len(col1) == 0 or len(col2) == 0:
        return None

    obj = {}

    obj["name"] = name.strip().replace("\n", "")
    obj["symbol"] = symbol

    # get header info
    obj["price"] = string_to_float(dom.find(".time_rtq_ticker span").text())

    # get first column
    obj["prev_close"] = string_to_float(get_field(col1, 0))
    obj["open"] = string_to_float(get_field(col1, 1))
    obj["beta"] = string_to_float(get_field(col1, 5))
    obj["earnings_date"] = parse_date(get_field(col1, 6))

    # get second column
    day_range = get_field(col2, 0).split("-")
    year_range = get_field(col2, 1).split("-")
    div_yield = get_field(col2, 7).split(" ")


    obj["day_low"] = len(day_range) > 1 and string_to_float(day_range[0]) or 0
    obj["day_high"] = len(day_range) > 1 and string_to_float(day_range[1]) or 0


    obj["year_low"] = len(year_range) > 1 and string_to_float(year_range[0]) or 0
    obj["year_high"] = len(year_range) > 1 and string_to_float(year_range[1]) or 0

    obj["market_cap"] = get_field(col2, 4)
    obj["pe"] = string_to_float(get_field(col2, 5))
    obj["eps"] = string_to_float(get_field(col2, 6))


    obj["div_yield_dollar"] = len(div_yield) > 1 and string_to_float(div_yield[0]) or 0
    obj["div_yield_percent"] = len(div_yield) > 1 and string_to_float(re.sub("[()%]", "", div_yield[1])) or 0

    obj["daily_dollar_gain"] = obj["price"] - obj["prev_close"]


    obj["daily_percentage_gain"] = obj["prev_close"] != 0 and \
                                   round(((obj["price"] - obj["prev_close"])/obj["prev_close"]) * 100, 2) or \
                                   100

    return obj
