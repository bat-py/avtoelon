import xlsxwriter
import csv


class ExcelWriter:
    def __init__(self, selected_place, parsed_data, stop):
        self.selected_place = selected_place
        self.parsed_data = parsed_data
        self.stop = stop
        self.row = 0

        self.writer()

    def writer(self):
        workbook = xlsxwriter.Workbook(self.selected_place)
        worksheet = workbook.add_worksheet()

        bold = workbook.add_format({'bold':True, "align":'center'})


        worksheet.set_column('A:A', 38)
        worksheet.set_column('B:B', 20)
        worksheet.set_column('D:D', 13)
        worksheet.set_column('E:G', 25)
        worksheet.set_column('H:I', 38)

        field = ['Заголовок', 'Зарплата', 'Город', 'Дата', 'Работодатель',  'Обязанность', 'Требования', 'Ссылка на объявление', 'Ссылка работодателя']
        # Записываем на первую строку имена столбцов
        for column_num, i in enumerate(field):
            worksheet.write(self.row, column_num, i, bold)
        self.row += 1

        first_line = 1
        # Повторится столько раз, сколько было выбрано каталоги
        for i in self.parsed_data:
            if first_line:
                first_line = 0
            else:
                self.row += 1

            # Записываем название каталога
            _format = workbook.add_format({'bg_color' : '#5eba7d', 'bold':True, "align":'center'})
            worksheet.set_row(self.row, cell_format=_format)
            worksheet.write(self.row, 0, "Категория: "+i.title, _format)
            self.row += 1

            # Тут записываем все обявления по соотвествующим столбцам
            for columns in i.list_vacancies:                         # Каждый повтор создает новую строку
                for column_num, column in enumerate(columns.items()):        # Каждый повтор создает новый столбец
                    worksheet.write(self.row, column_num, column[1])
                self.row +=1

        workbook.close()
        self.stop()




class CsvWriter:
    def __init__(self, selected_place, parsed_data, stop):
        self.selected_place = selected_place
        self.parsed_data = parsed_data
        self.stop = stop
        self.writer()

    def writer(self):
        fieldnames_ru = {'item_name':'Заголовок',
                         'wage' : 'Зарплата',
                         'city' : 'Город',
                         'date' : 'Дата',
                         'employer' : 'Работодатель',
                         'vacancy_responsibility' : 'Обязанность',
                         'vacancy_requirement' : 'Требования',
                         'item_href' : 'Ссылка на объявление',
                         'employer_href' : 'Ссылка работодателя'}

        fieldnames_en = []
        first_line = 1
        for i in self.parsed_data[0].list_vacancies[0].items():
            fieldnames_en.append(i[0])

        with open(self.selected_place, 'w', encoding='utf-16', newline='') as w:
            for i in self.parsed_data:
                if not first_line:
                    w.write('\n')
                first_line = 0

                w.write(i.title+'\n')
                cursor = csv.DictWriter(w, fieldnames=fieldnames_en)
                cursor.writerow(fieldnames_ru)
                cursor.writerows(i.list_vacancies)

        self.stop()





