import os
import sys
import re
from TdtPasres import ParserTdt
from TdtPasres import ParserCsv

EXT_TDT = 'tdt'
EXT_CSV = 'csv'
EXT_OUT = 'json'

KEY_TIME_STAMP = 'TIME_STAMP'

def ReadFromFile(file_name: str='') -> str:
    content = ''
    try:
        f = open(file_name, 'rt')
        content =  f.read()
        f.close()
        return content
    except:
        print(f'Невозможно открыть файл: {file_name}')
        return None

def SaveResultToFile(file_name: str='', save_data:str=''):
    ext = GetFileExt(file_name)
    out_file = file_name.replace(ext, EXT_OUT)
    f = open(out_file, 'wt')
    f.write(save_data)
    f.close()

def GetFileExt(file_name: str='') -> str:
    split_file_name = file_name.split('.')
    ext = split_file_name[len(split_file_name)-1]
    return ext

def ListDirFiles(dir:str=os.getcwd(), exts: list[str] = []) -> dict[str,str]:
    result = {}
    cnt = 0
    for file_name in os.listdir(dir):
        for ext in exts:
            if ext == GetFileExt(file_name):
                result[cnt] = file_name
                cnt += 1
    return result

def ParseTdtFile(file_name: str=''):
    content = ReadFromFile(file_name)
    if content == None:
        return

    parser = ParserTdt()
    parser.RawDataParse(content)
    json_data = parser.GetParsedDataAsJson()

    SaveResultToFile(file_name, json_data)

def ParseCsvFile(file_name: str=''):
    content = ReadFromFile(file_name)
    if content == None:
        return

    parser = ParserCsv()
    parser.RawDataParse(content)
    json_data = parser.GetParsedDataAsJson()

    SaveResultToFile(file_name, json_data)


def main():
    files = ListDirFiles(exts=[EXT_TDT, EXT_CSV])
    print(files)
    file_num = int(input('Введите номер файла для парсинга:'))
    file_name = files[file_num]
    if GetFileExt(file_name) == EXT_TDT:
        ParseTdtFile(file_name)
    if GetFileExt(file_name) == EXT_CSV:
        ParseCsvFile(file_name)


if __name__ == '__main__':
    main()