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

# Скачивает ваканции из переданного каталога
class GetItemsFromCatalog:
    def __init__(self, urls: list, messagebox, root):
        self.root = root
        self.title = urls[0]
        self.url = urls[1]
        self.request_status = 1
        self.list_vacancies = []                         # тут хранится все ваканции
        self.error_text = "Ошибка", "Загрузка прервана\nПожалуйста проверьте подключение к интернету"

        self.get_number_of_pages()
        self.get_all_vacancies_from_page()

    def get_number_of_pages(self):
        try:
            html = get_html(self.url)
        except:
            self.messagebox.showerror(*self.error_text)
            self.root.destroy()


        if html.status_code == 200:
            soup = BeautifulSoup(html.text, "html.parser")
            bloko_button = soup.find_all("a", class_="bloko-button HH-Pager-Control")

            pages = [0]

            try:
                for page_num in bloko_button:
                    date_page = page_num.get("data-page")
                    pages.append(int(date_page))
            except:
                pass

            self.number_of_pages = max(pages)
        else:
            self.messagebox.showerror(*self.error_text)
            self.root.destroy()
            return 0

    def get_all_vacancies_from_page(self):
        if self.request_status:
            for i in range(self.number_of_pages+1):
                vacancies_from_page = self.get_items_from_one_page(i)
                if vacancies_from_page:
                    self.list_vacancies.extend(vacancies_from_page)

    def get_items_from_one_page(self, page_num):
        try:
            html = get_html(self.url, params={"page":page_num})
        except:
            self.messagebox.showerror(*self.error_text)
            self.root.destroy()


        if html.status_code == 200:
            soup = BeautifulSoup(html.text, "html.parser")
            vacancy_block = soup.find("div", class_="bloko-column bloko-column_l-13 bloko-column_m-9 bloko-column_s-8 bloko-column_xs-4")
            vacancy_items = vacancy_block.find_all("div", class_="vacancy-serp-item")

            items = []
            for item in vacancy_items:
                i = item.find("span", class_="resume-search-item__name").find("a", class_="bloko-link HH-LinkModifier")
                name = i.get_text()
                href = i.get("href")

                wage = item.find_next("div", class_="vacancy-serp-item__sidebar").get_text()

                try:
                    employer_block = item.find("a", class_="bloko-link bloko-link_secondary")
                    employer = employer_block.get_text()
                    employer_href = "https://tashkent.hh.uz"+employer_block.get("href")
                except:
                    employer = ''
                    employer_href = ''

                city = item.find("span", class_="vacancy-serp-item__meta-info").get_text()

                about_vacancy = item.find("div", class_="g-user-content").find_all("div")

                vrr = 1
                for i in about_vacancy:
                    if vrr:
                        vacancy_responsibility = i.get_text()
                        vrr = 0
                    else:
                        vacancy_requirement = i.get_text()


                date = item.find("span", class_="vacancy-serp-item__publication-date").get_text()

                items.append({"item_name": name,

                              "wage": wage,
                              "city": city,
                              "date": date,
                              "employer": employer,
                              "vacancy_responsibility": vacancy_responsibility,
                              "vacancy_requirement" : vacancy_requirement,
                              "item_href": href,
                              "employer_href": employer_href
                              })

            return items
        else:
            self.request_status = 0
            self.messagebox.showerror(*self.error_text)
            self.root.destroy()



# Вернет список работ по профессиям c ссылками
def list_jobs(root, messagebox):
    try:
        html = get_html("/catalog")
    except:
        messagebox.showerror("Ошибка", "Загрузка прервана\nПожалуйста проверьте подключение к интернету")
        root.destroy()

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
        messagebox.showerror("Ошибка", "Загрузка прервана\nПожалуйста проверьте подключение к интернету")
        root.destroy()
        return 0

















