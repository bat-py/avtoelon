import xlsxwriter
import csv


class ExcelWriter:
    def __init__(self, parsed_data):
        self.parsed_data = parsed_data
