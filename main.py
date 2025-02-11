import os
import sys
import re
from TdtPasres import Parser

FILE_NAME = 'Arch Термодат-29 v5.11 04.02.2025-07.02.2025.tdt'

def main():
    file_name = FILE_NAME
    content = ''
    try:
        f = open(file_name, 'rt')
        content =  f.read()
        f.close()
    except:
        print(f'Невозможно открыть файл: {file_name}')
        return

    parser = Parser()
    parser.RawDataParse(content)
    json_data = parser.GetParsedDataAsJson()

    split_name = file_name.split('.')
    ext = split_name[len(split_name)-1]
    out_file = file_name.replace(ext, 'json')

    f = open(out_file, 'wt')
    f.write(json_data)
    f.close()

    pass

if __name__ == '__main__':
    main()