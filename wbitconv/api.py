from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

def convertir(monedaFrom, monedaTo, cantidad):
    
    url = 'https://pro-api.coinmarketcap.com/v1/tools/price-conversion'
    parameters = {
    'symbol': monedaFrom,
    'amount': cantidad,
    'convert': monedaTo
    
    }
    
    headers = {
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': '7be0ed35-dc84-4ccd-8eb4-5875ae66cb93',
    }
    
    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    return round(data['data']['quote'][monedaTo]['price'], 5)
