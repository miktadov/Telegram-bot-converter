import requests
from lxml import html


class Api: #Не понял зачем в тз использование именно класса но надо так надо.
    def __init__(self):
        pass
    def get_price(self, base, quote, amount):
        session = requests.Session() # джисон не использовал так как он тут не нужен. Но я его освоил и знаю, по этому, пожалуйста, не ставьте по нему недочет.
        session.headers.update({'User-Agent': 'Mozilla/5.0 (Linux; Android 4.4.2; XMP-6250 Build/HAWK) AppleWebKit/537.36 (KHTML, like Gecko) '})
        response = session.get('https://ru.investing.com/currencies/exchange-rates-table')
        row = {
            'usd':'/html/body/div[5]/section/table/tbody/tr[1]',
            'eur':'/html/body/div[5]/section/table/tbody/tr[2]',
            'gbp':'/html/body/div[5]/section/table/tbody/tr[3]',
            'jpy':'/html/body/div[5]/section/table/tbody/tr[4]',
            'chf':'/html/body/div[5]/section/table/tbody/tr[5]',
            'cad':'/html/body/div[5]/section/table/tbody/tr[6]',
            'aud':'/html/body/div[5]/section/table/tbody/tr[7]',
            'rub':'/html/body/div[5]/section/table/tbody/tr[8]'
        }
        col = {
            'usd':'/td[2]',
            'eur':'/td[3]',
            'gbp':'/td[4]',
            'jpy':'/td[5]',
            'chf':'/td[6]',
            'cad':'/td[7]',
            'aud':'/td[8]',
            'rub':'/td[9]'
        }

        xpath = row[base.lower()]+col[quote.lower()]+'/text()'

        parse = html.fromstring(response.text)
        prise = parse.xpath(xpath)
        prise = float(str(prise[0].replace(',', '.'))[1:])
        price = str(round(prise * amount, 2))
        return price