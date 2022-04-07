from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import sqlalchemy
import os

key=os.environ.get('COINMARKETCAP_API_KEY')
db_password=os.environ.get('DB_PASSWORD')
db_publicip=os.environ.get('PUBLIC_IP')

engine = sqlalchemy.create_engine(f'mysql+pymysql://root:{db_password}@{db_publicip}/coinmarket')


url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
parameters = {
    'start': '1',
    'limit': '20',
    'convert': 'GBP'
}
headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': key,
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    df = pd.json_normalize(data['data'])
    df = df[['id', 'name', 'symbol', 'slug', 'num_market_pairs', 'date_added', 'cmc_rank',  'last_updated', 'quote.GBP.price', 'quote.GBP.volume_24h', 'quote.GBP.volume_change_24h', 'quote.GBP.percent_change_1h', 'quote.GBP.percent_change_24h',  ]]
    df.to_sql(con=engine, name='coinmarket', if_exists='replace')

except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(e)