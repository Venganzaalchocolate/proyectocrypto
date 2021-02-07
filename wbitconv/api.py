from wbitconv import app
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

APIKEY=app.config['APIKEY']

def convertir(monedaFrom, monedaTo, cantidad):
    
    url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
    parameters = {
    'symbol': monedaFrom,
    'amount': cantidad,
    'convert': monedaTo
    
    }
    
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '{}'.format(APIKEY),
    }
    
    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    return round(data['data']['quote'][monedaTo]['price'], 5)
