from django.core.management.base import BaseCommand
import requests
import time
from time import sleep
from bs4 import BeautifulSoup
import re
from parserav.models import Job

proxy_counter = 0
class Command(BaseCommand):
    help = "collect jobs"

    # определяем логику команд
    def handle(self, *args, **options):



        url = ['https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg']
        url1 = 'https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?p={page}'
        for i in range(2, 101):
            urlishe = url1.format(page=i)
            url.append(urlishe)

        # proxies1=['steppenwolf09_yandex:970269e665@45.135.15.218:30001','steppenwolf09_yandex:970269e665@45.135.15.94:30001',
        #          'steppenwolf09_yandex:970269e665@91.188.237.241:30001', 'steppenwolf09_yandex:970269e665@91.188.239.158:30001',
        #          ]
        #
        # proxies2=['steppenwolf09_yandex:970269e665@91.188.238.47:30001','steppenwolf09_yandex:970269e665@45.135.15.227:30001',
        #          'steppenwolf09_yandex:970269e665@45.135.12.68:30001', 'steppenwolf09_yandex:970269e665@91.188.239.49:30001',
        #           'steppenwolf09_yandex:970269e665@91.188.237.170:30001']
        #
        # proxies=[proxies1,proxies2]

        proxies = ['steppenwolf09_yandex:970269e665@91.188.237.241:30001',
                   'steppenwolf09_yandex:970269e665@91.188.239.158:30001',
                   'steppenwolf09_yandex:970269e665@91.188.238.47:30001',
                   'steppenwolf09_yandex:970269e665@45.135.15.227:30001',
                   'steppenwolf09_yandex:970269e665@45.135.12.68:30001',
                   'steppenwolf09_yandex:970269e665@91.188.239.49:30001',
                   'steppenwolf09_yandex:970269e665@91.188.237.170:30001',
                   'steppenwolf09_yandex:970269e665@2.59.176.81:30001',
                   'steppenwolf09_yandex:970269e665@2.59.179.128:30001',
                   'steppenwolf09_yandex:970269e665@2.59.176.61:30001',
                   'steppenwolf09_yandex:970269e665@2.59.176.186:30001',
                   'steppenwolf09_yandex:970269e665@2.59.179.95:30001',
                   'steppenwolf09_yandex:970269e665@45.135.13.72:30001',
                   'steppenwolf09_yandex:970269e665@45.135.14.239:30001']

        # proxies=['steppenwolf09_yandex:970269e665@91.188.237.170:30001']
        def get_phone(href, counter):
            url = 'https://m.avito.ru' + href
            id = href.split('_')[-1]
            session = requests.Session()
            session.headers.update({
                'authority': 'https://www.avito.ru',
                'method': 'GET',
                'host': 'm.avito.ru',
                'path': href,
                'scheme': 'https',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache - control': 'max - age = 0',
                'referer': url,
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Linux; Android 7.1.2; Redmi Note 5A Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36'
            })

            global proxy_counter
            global proxy
            if proxy_counter == len(proxies):
                proxy_counter = 0
            else:

                proxy = proxies[proxy_counter]
                proxy_counter += 1
            # print(proxy)
            session.proxies = {"http": proxy, "https": proxy}
            url = 'https://m.avito.ru/api/1/items/' + id + '/phone?key=af0deccbgcgidddjgnvljitntccdduijhdinfgjgfjir'
            try:
                global r
                r = session.get(url)
                session.close()
            except Exception as e:
                proxies.remove(proxy)
                session.close()
                print("Ошибка при get в функции get_phone(): " + str(e))
            # Срезом берем телефон из ответа вида
            # {"status":"ok","result":{"action":{"title":"Позвонить","uri":"ru.avito://1/phone/call?number=%2B79584885658"}}}
            # print(r.text)
            if r.text[-16:-10] == 'k/show':
                proxies.remove(proxy)
                print("Увы! -1 Прокси")
            else:

                return '+' + r.text[-16:-5]

        def pars(url):
            global proxy
            global proxy_counter
            # print(proxy_counter)
            if proxy_counter == len(proxies):
                proxy_counter = 0
            else:

                proxy = proxies[proxy_counter]
                proxy_counter += 1
            # print(proxy)
            prox = {"http": proxy, "https": proxy}
            html = requests.get(url, proxies=prox)
            # if coun % 2:
            #     proxy=proxies1
            # else:
            #     proxy=proxies2
            counter = 0
            big_data = []
            page = html.text
            soup = BeautifulSoup(page)
            spis = soup.find_all("h3", {
                "class": "title-root-395AQ iva-item-title-1Rmmj title-listRedesign-3RaU2 title-root_maxHeight-3obWc text-text-1PdBw text-size-s-1PUdo text-bold-3R9dt"})
            if spis:
                for s in spis:
                    counter += 1
                    parent = s.parent.parent.next_sibling
                    price = parent.find("span", {"price-text-1HrJ_ text-text-1PdBw text-size-s-1PUdo"}).text
                    price = price.replace(u'\xa0', u' ')
                    parent_ad = parent.parent.parent.parent
                    try:
                        address_par = parent_ad.find("span",
                                                     {"geo-address-9QndR text-text-1PdBw text-size-s-1PUdo"}).span.text
                    except:
                        address_par = parent_ad.find("div", {
                            "geo-georeferences-3or5Q text-text-1PdBw text-size-s-1PUdo"}).span.text



                    par_nedv = s.parent.parent
                    url_nedv = 'https://www.avito.ru/' + par_nedv.a['href']

                    phone = get_phone(url_nedv, counter)

                    s = str(s.text)
                    # print(s, price, address_par, phone)
                    data = [s, price, address_par, phone]

                    try:
                        Job.objects.create(
                            url=url_nedv,
                            title=s,
                            location=address_par,
                            price=price,
                            telephone=phone
                        )
                        #
                    except:
                        print('%s added' % (s))

                    if s:
                        big_data.append(data)
            return big_data

        def req():
            full_data = []
            iterable = [0, 1]
            i = 0
            time1 = time.time()

            # with ThreadPoolExecutor(2) as executor:
            #     results = executor.map(pars, url)
            for u in url:
                print(u)
                data = pars(u)
                full_data.append(data)

            time2 = time1 - time.time()
            print(time2)

            return full_data

        req()






