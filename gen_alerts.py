import sqlite3
import datetime

'''
    Get all the stocks that are trading within the 'threshold'
    parameter of the yearly low, and is in the desired sectors

'''
def get_stocks_near_low(sectors, threshold=1.3):

    str_in = "({seq})".format(seq=','.join(['?']*len(sectors)))
    sectors.insert(0, threshold)

    db = sqlite3.connect('db/stock_finder')
    cursor = db.cursor()
    cursor.execute('''

        SELECT * FROM stocks AS A
        INNER JOIN sectors_mapping AS B
        ON A.symbol = B.symbol
        WHERE A.price < A.year_low * ? AND
        B.sector IN ''' + str_in + '''
        ORDER BY A.symbol ASC

        '''
        , tuple(sectors))

    db.commit()

    for rows in cursor:
        print rows

'''
    Get all the stocks that had a drop in price exceeding
    the threshold, and is in the desired sectors

'''
def get_stocks_dropped_by_percent(sectors, threshold=7):

    str_in = "({seq})".format(seq=','.join(['?']*len(sectors)))
    sectors.insert(0, threshold)

    db = sqlite3.connect('db/stock_finder')
    cursor = db.cursor()
    cursor.execute('''

        SELECT A.symbol, A.daily_percentage_gain FROM stocks AS A
        INNER JOIN sectors_mapping AS B
        ON A.symbol = B.symbol
        WHERE A.daily_percentage_gain < -? AND
        B.sector IN ''' + str_in + '''
        ORDER BY A.daily_percentage_gain ASC

        '''
        ,tuple(sectors))

    db.commit()

    for rows in cursor:
        print rows


def get_stocks_near_low_and_near_report(sectors, days_range=7, threshold=1.2):

    # we negate value to get date into future
    t = -1 * days_range
    days_in_future = datetime.datetime.now() - datetime.timedelta(days=t)
    str_days_in_future = days_in_future.isoformat()
    str_in = "({seq})".format(seq=','.join(['?']*len(sectors)))

    sectors.insert(0, threshold)
    sectors.insert(0, str_days_in_future)

    db = sqlite3.connect('db/stock_finder')
    cursor = db.cursor()
    cursor.execute('''

        SELECT * FROM stocks AS A
        INNER JOIN sectors_mapping AS B
        ON A.symbol = B.symbol
        WHERE A.earnings_date < ? AND (A.price < A.year_low * ?) AND
        B.sector IN ''' + str_in + '''
        ORDER BY A.price ASC

    '''
    , tuple(sectors))

    db.commit()

    for rows in cursor:
        print rows



#get_stocks_near_low(["Favourites"], 1.3)

get_stocks_near_low_and_near_report(["Favourites"], 180, 1.3)


# get_stocks_dropped_by_percent(["Favourites"], 0)
#
