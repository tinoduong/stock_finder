import sqlite3



def create_db():

    print "Creating database ..."
    db = sqlite3.connect('db/stock_finder')
    cursor = db.cursor();
    cursor.execute('''

        CREATE TABLE IF NOT EXISTS stocks
        (id INTEGER PRIMARY KEY,
         ticker TEXT unique,
         name TEXT,
         price REAL,
         prev_close REAL,
         open REAL,
         beta REAL,
         earnings_date TEXT,
         day_low REAL,
         day_high REAL,
         year_low REAL,
         year_high REAL,
         market_cap TEXT,
         pe REAL,
         eps REAL,
         div_yield_dollar REAL,
         div_yield_percent REAL,
         daily_dollar_gain REAL,
         daily_percentage_gain REAL)

    ''')

    cursor.execute('''

        CREATE TABLE IF NOT EXISTS sectors
        (id INTEGER PRIMARY KEY,
         sector TEXT unique
        )

    ''')

    cursor.execute('''

        CREATE TABLE IF NOT EXISTS sectors_mapping
        (ticker TEXT,
         sector TEXT,
         PRIMARY KEY(ticker, sector)
         FOREIGN KEY(ticker) REFERENCES stocks(ticker),
         FOREIGN KEY(sector) REFERENCES sectors(sector)
        )

    ''')

    db.commit()
    db.close();


def insert_sectors(sector):

    db = sqlite3.connect('db/stock_finder')
    cursor = db.cursor();
    cursor.execute('''INSERT OR IGNORE INTO sectors(sector) VALUES(?)''', [sector,])
    db.commit()
    db.close()


def insert_row(symbol, sector, db):

    cursor = db.cursor();
    print "Inserting " + symbol["ticker"]

    cursor.execute("DELETE FROM stocks where ticker = ?", (symbol["ticker"],))

    cursor.execute('''

                INSERT INTO
                stocks( ticker,
                        name,
                        price,
                        prev_close,
                        open,
                        beta,
                        earnings_date,
                        day_low,
                        day_high,
                        year_low,
                        year_high,
                        market_cap,
                        pe,
                        eps,
                        div_yield_dollar,
                        div_yield_percent,
                        daily_dollar_gain,
                        daily_percentage_gain)
                VALUES( :ticker,
                        :name,
                        :price,
                        :prev_close,
                        :open,
                        :beta,
                        :earnings_date,
                        :day_low,
                        :day_high,
                        :year_low,
                        :year_high,
                        :market_cap,
                        :pe,
                        :eps,
                        :div_yield_dollar,
                        :div_yield_percent,
                        :daily_dollar_gain,
                        :daily_percentage_gain)

                ''', symbol)

    cursor.execute("INSERT OR IGNORE INTO sectors_mapping (ticker, sector) VALUES(?,?)", (symbol["ticker"], sector))

    db.commit()
