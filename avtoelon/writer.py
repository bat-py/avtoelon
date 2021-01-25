import xlsxwriter
import csv


class ExcelWriter:
    def __init__(self, w, parsed_data):
        self.w = w
        self.parsed_data = parsed_data

    def writer(self):
        pass



class CsvWriter:
    def __init__(self, w, parsed_data):
        self.w = w
        self.parsed_data = parsed_data

    def writer(self):
        fieldnames = []

        for i in self.parsed_data.list_vacancies[0].items():
            fieldnames.append(i[0])
        
        for i in self.parsed_data:
            w.write("\n" + i.title + "\n")
            cursor = csv.DictWriter(self.w, fieldnames=fieldnames)
            cursor.writeheader()
            cursor.writerows(i.list_vacancies)







