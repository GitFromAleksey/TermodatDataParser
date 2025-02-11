import os
import sys
import re
from TdtPasres import ParserTdt
from TdtPasres import ParserCsv


FILE_NAME_TDT = 'Arch Термодат-29 v5.11 04.02.2025-07.02.2025.tdt'
FILE_NAME_CSV = '06-07.02.2025.csv'

def ParseTdtFile(file_name: str=''):
    content = ''
    try:
        f = open(file_name, 'rt')
        content =  f.read()
        f.close()
    except:
        print(f'Невозможно открыть файл: {file_name}')
        return

    parser = ParserTdt()
    parser.RawDataParse(content)
    json_data = parser.GetParsedDataAsJson()

    split_name = file_name.split('.')
    ext = split_name[len(split_name)-1]
    out_file = file_name.replace(ext, 'json')

    f = open(out_file, 'wt')
    f.write(json_data)
    f.close()

def ParseCsvFile(file_name: str=''):
    content = ''
    try:
        f = open(file_name, 'rt')
        content =  f.read()
        f.close()
    except:
        print(f'Невозможно открыть файл: {file_name}')
        return

    parser = ParserCsv()
    parser.RawDataParse(content)
    json_data = parser.GetParsedDataAsJson()

    split_name = file_name.split('.')
    ext = split_name[len(split_name)-1]
    out_file = file_name.replace(ext, 'json')

    f = open(out_file, 'wt')
    f.write(json_data)
    f.close()

def main():
    ParseTdtFile(FILE_NAME_TDT)
    ParseCsvFile(FILE_NAME_CSV)
    pass

if __name__ == '__main__':
    main()