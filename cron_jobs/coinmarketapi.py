#!/usr/bin/env python3

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
import sqlalchemy
import os
from decouple import Config, RepositoryEnv

DOTENV_FILE = '../.env'
env_config = Config(RepositoryEnv(DOTENV_FILE))


def get_data():
    """Getting data from coinmarketcap API
    Authentication values will be stored in .env file that ignored by git for security reason
    """
    # Authentication configuration
    KEY = env_config('COINMARKETCAP_API_KEY')
    PASSWORD = env_config.get("PASSWORD")
    PUBLIC_IP_ADDRESS = env_config.get("PUBLIC_IP_ADDRESS")
    DBNAME = env_config.get("DBNAME")
    PROJECT_ID = env_config.get("PROJECT_ID")
    INSTANCE_NAME = env_config.get("INSTANCE_NAME")

    engine = sqlalchemy.create_engine(2
        f'mysql+mysqldb://root:{PASSWORD}@{PUBLIC_IP_ADDRESS}/{DBNAME}?unix_socket=/cloudsql/{PROJECT_ID}:{INSTANCE_NAME}'
    )

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {'start': '1', 'limit': '20', 'convert': 'GBP'}
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': key,
    }

    session = Session()
    session.headers.update(headers)

    # Get data from coinmarketcap api
    try:
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        df = pd.json_normalize(data['data'])
        df = df[[
            'id',
            'name',
            'symbol',
            'slug',
            'num_market_pairs',
            'date_added',
            'cmc_rank',
            'last_updated',
            'quote_GBP_price',
            'quote_GBP_volume_24h',
            'quote_GBP_volume_change_24h',
            'quote_GBP_percent_change_1h',
            'quote_GBP_percent_change_24h',
        ]]
        df.to_sql(con=engine, name='coinmarket', if_exists='replace')

    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)


if __name__ == '__main__':
    get_data()