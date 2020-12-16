import requests
import os
from datetime import datetime
from lxml import html

HOME_URL = 'https://www.larepublica.co/'

XPATH_LINK_TO_ARTICLE = '//text-fill/a/@href'
XPATH_NEWS_TITLE = '//div[@class="mb-auto"]/text-fill/a/text()'
XPATH_NEWS_SUMMARY = '//div[@class="lead"]/p/text()'
XPATH_NEWS_CONTENT = '//div[@class="html-content"]/p/text()'


def parse_notice(link, date):
    print(f'[!] Scraping {link[:70]}...')
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode('utf-8')
            parsed = html.fromstring(notice)
            try:
                title = parsed.xpath(XPATH_NEWS_TITLE)[0]
                title = title.replace('\"', '')
                summary = parsed.xpath(XPATH_NEWS_SUMMARY)[0]
                content = parsed.xpath(XPATH_NEWS_CONTENT)
            except IndexError:
                return

            with open(f'{date}/{title}.text', 'w', encoding='utf-8') as f:
                f.write(title)
                f.write('\n')
                f.write('--- ' * 10)
                f.write('\n')
                f.write(summary)
                f.write('\n\n')
                for p in content:
                    f.write(p)
                    f.write('\n')

        else:
            raise ValueError(f'Error: {response.status_code} to visit {link}')
    except ValueError as ve:
        print(ve)


def parse_home():
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode('utf-8')
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH_LINK_TO_ARTICLE)

            today = datetime.now().strftime('%d-%m-%Y')

            if not os.path.isdir(today):
                os.mkdir(today)

            for link in links_to_notices:
                parse_notice(link, today)

        else:
            raise ValueError(f'Error: {response.status_code}')

    except ValueError as ve:
        print(ve)


def run():
    print("""  
         _       __     __       _____                                
        | |     / /__  / /_     / ___/______________ _____  ___  _____
        | | /| / / _ \/ __ \    \__ \/ ___/ ___/ __ `/ __ \/ _ \/ ___/
        | |/ |/ /  __/ /_/ /   ___/ / /__/ /  / /_/ / /_/ /  __/ /    
        |__/|__/\___/_.___/   /____/\___/_/   \__,_/ .___/\___/_/     
                                                  /_/                 
            Web Scraper to La Republica News - @RoyerGuerreroP
          """)
    parse_home()


if __name__ == '__main__':
    run()
