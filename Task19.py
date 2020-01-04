import requests
from bs4 import BeautifulSoup
import csv
from time import time


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find('ul', class_='pagn').find_all('a')[-1].get('href')

    total_pages = pages.split('=')[1]
    return int(total_pages)


def write_csv(data):
    with open('lalafo.csv', 'a') as file_:
        writer = csv.writer(file_)
        writer.writerow( (data['title'],
                          data['price'],
                          data['photo'],
                          data['url'],) )


def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    goods = soup.find('div', id='main-listing-block').find_all(
                            'article', class_='listing-item')

    for good in goods:
               
        try:
            title = good.find('div', class_='listing-item-main'
                                    ).find('a').text.strip()
        except:
            title = ''
        
        try:
            price = good.find('p', class_='listing-item-title').text.strip()
        except:
            price = ''

        try:
            photo = good.find('img', class_=
                            'listing-item-photo link-image').get('src')
        except:
            photo = ''

        try:
            url = 'https://lalafo.kg' + good.find('div', class_=
                            'listing-item-main').find('a').get('href')
        except:
            url = ''
        
        data = {'title': title,
                'price': price,
                'photo': photo,
                'url': url,}

        write_csv(data)
        

def main():
    time_start = time()
    
    url = ('https://lalafo.kg/kyrgyzstan'
            '/mobilnye-telefony-i-aksessuary/mobilnyetelefony')

    part1_url = ('https://lalafo.kg/kyrgyzstan'
            '/mobilnye-telefony-i-aksessuary/mobilnyetelefony?')

    part2_url = 'page='

    total_pages = get_total_pages(get_html(url))
    
    for i in range(1, total_pages+1):
        url_counter = part1_url + part2_url + str(i)
        print(url_counter)
        html = get_html(url_counter)
        get_page_data(html)
    time_stop = time()
    print("Time: " + str(round(time_stop - time_start, 2)) + " seconds")


if __name__ == '__main__':
    main()
