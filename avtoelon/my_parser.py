from bs4 import BeautifulSoup 
import requests

def get_html(url, params=None):
    HEADERS = {
        'user-agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0',
        'accept' : '*/*'
    }
    
    main_url = "https://tashkent.hh.uz"
    page = requests.get(main_url+url, headers=HEADERS, params=params)
    return page


# Вернет список работ по профессиям c ссылками
def list_jobs():
    html = get_html("/catalog")

    if html.status_code == 200:
        soup = BeautifulSoup(html.text, "html.parser")
        catalog_item = soup.find_all('a', class_="catalog__item-link")
        
        dic_item = {}

        for item in catalog_item:
            item_link = item.get('href')
            item_text = item.get_text()
            dic_item[item_text] =  item_link
    
        return dic_item 
    else:
        return 0





def list_vacancies(urls):
    htmls = []
    for url in urls:


















