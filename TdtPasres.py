import re
import json
from datetime import datetime

KEY_TIME_STAMP = 'TIME_STAMP'

RE_LINE_NUM_PTRN = r'\d+'
# 06.02.2025 13:52:25
RE_DATE_PTRN = r'\d{2}.\d{2}.\d{4}'
RE_TIME_PTRN = r'\d{2}:\d{2}:\d{2}'
RE_DTTM_PTRN = RE_DATE_PTRN + '\s' + RE_TIME_PTRN

# ^1.1 25,4 X X 
RE_TEMP_PREFIX = r'\s\^'
RE_SNSR_NUM = r'\d+.\d+'
RE_TEMP = r'\d+,\d+'
RE_TEMP_POSTFIX = r' X X'
RE_SNSR_DATA_PTRN = RE_TEMP_PREFIX + RE_SNSR_NUM + r'\s' + RE_TEMP + RE_TEMP_POSTFIX
RE_SNSRS_DATA =  r'(' + RE_SNSR_DATA_PTRN + r')+'

# регулярка всей строки
RE_DATA_LINE = RE_LINE_NUM_PTRN + r'\s' + RE_DTTM_PTRN + RE_SNSRS_DATA

class Parser:
     
    def __init__(self):
        pass

    def RawDataParse(self, raw_data: str=''):
        lines = raw_data.split('\n')
        self.parsed_lines = []
        for line in lines:
            if not self.LineValidate(line):
                continue
            line_num = self.GetStrNumFromLine(line)
            date_time = self.GetDateTimeFromLine(line)
            date_time_str = date_time.strftime('%m.%d.%YT%H:%M:%S')
            timestamp = date_time.timestamp()
            sensors_data = self.GetSensorsData(line)
            sensors_data[KEY_TIME_STAMP] = timestamp
            sensors_data['DATE_TIME'] = date_time_str
            self.parsed_lines.append(sensors_data)
        # print(parsed_lines)

    def LineValidate(self, line: str=''):
        res = re.search(RE_DATA_LINE, line)
        if res:
            # print(res.group(0))
            return True
        return False

    def GetStrNumFromLine(self, line: str=''):
        res = re.match(RE_LINE_NUM_PTRN, line)
        if res:
            return res.group(0)
        return None

    def GetDateTimeFromLine(self, line: str=''):
        res = re.search(RE_DTTM_PTRN, line)
        date_time_str = res.group(0)
        # 06.02.2025 13:53:19
        format = '%d.%m.%Y %H:%M:%S'
        date_time = datetime.strptime(date_time_str, format)
        return date_time
    
    def GetSensorsData(self, line: str=''):
        sensors_data = re.search(RE_SNSRS_DATA, line)
        split_data_str = re.split(RE_TEMP_POSTFIX, sensors_data.group(0))
        result = {}
        for data_str in split_data_str:
            if data_str == '':
                continue
            sensor_num = re.search(RE_SNSR_NUM, data_str).group(0)
            sensor_temp = re.search(RE_TEMP, data_str).group(0)
            result[sensor_num] = sensor_temp
        return result

    def GetParsedDataAsJson(self):
        result = ''
        for parsed_line in self.parsed_lines:
            result += json.dumps(parsed_line) + '\n'
        return result

test_raw_tdt_data = '1 06.02.2025 13:52:25 ^1.1 25,0 X X ^1.2 24,9 X X ^1.3 32,1 X X ^1.4 40,3 X X ^1.5 32,7 X X ^1.6 32,6 X X ^1.7 30,6 X X ^1.8 21,6 X X ^1.9 22,3 X X ^1.10 21,5 X X ^1.11 21,9 X X ^1.12 21,0 X X ^1.13 21,5 X X ^1.14 21,9 X X ^1.15 21,4 X X ^1.16 21,5 X X \n\
2 06.02.2025 13:53:19 ^1.1 25,4 X X ^1.2 25,2 X X ^1.3 32,7 X X ^1.4 40,2 X X ^1.5 33,0 X X ^1.6 33,4 X X ^1.7 31,5 X X ^1.8 21,7 X X ^1.9 22,3 X X ^1.10 21,5 X X ^1.11 22,0 X X ^1.12 20,9 X X ^1.13 21,5 X X ^1.14 21,9 X X ^1.15 21,4 X X ^1.16 21,6 X X \n\
3 06.02.2025 13:54:23 ^1.1 25,8 X X ^1.2 25,7 X X ^1.3 33,4 X X ^1.4 40,3 X X ^1.5 33,3 X X ^1.6 34,2 X X ^1.7 32,2 X X ^1.8 21,8 X X ^1.9 22,3 X X ^1.10 21,5 X X ^1.11 21,8 X X ^1.12 20,9 X X ^1.13 21,5 X X ^1.14 21,9 X X ^1.15 21,4 X X ^1.16 21,5 X X \n\
4 06.02.2025 13:55:26 ^1.1 26,0 X X ^1.2 25,9 X X ^1.3 34,2 X X ^1.4 40,6 X X ^1.5 33,6 X X ^1.6 34,7 X X ^1.7 32,5 X X ^1.8 21,7 X X ^1.9 22,3 X X ^1.10 21,5 X X ^1.11 21,9 X X ^1.12 21,0 X X ^1.13 21,5 X X ^1.14 22,0 X X ^1.15 21,4 X X ^1.16 21,5 X X \n\
5 06.02.2025 13:56:20 ^1.1 26,2 X X ^1.2 26,1 X X ^1.3 34,7 X X ^1.4 40,8 X X ^1.5 33,9 X X ^1.6 35,4 X X ^1.7 33,0 X X ^1.8 21,7 X X ^1.9 22,4 X X ^1.10 21,4 X X ^1.11 21,9 X X ^1.12 20,9 X X ^1.13 21,6 X X ^1.14 21,9 X X ^1.15 21,4 X X ^1.16 21,6 X X \n\
6 06.02.2025 13:57:23 ^1.1 27,5 X X ^1.2 27,3 X X ^1.3 35,6 X X ^1.4 41,2 X X ^1.5 34,3 X X ^1.6 36,8 X X ^1.7 33,2 X X ^1.8 21,8 X X ^1.9 22,3 X X ^1.10 21,5 X X ^1.11 21,9 X X ^1.12 20,9 X X ^1.13 21,5 X X ^1.14 22,0 X X ^1.15 21,4 X X ^1.16 21,7 X X \n\
7 06.02.2025 13:58:26 ^1.1 29,1 X X ^1.2 29,1 X X ^1.3 36,4 X X ^1.4 41,5 X X ^1.5 34,6 X X ^1.6 37,8 X X ^1.7 34,1 X X ^1.8 21,8 X X ^1.9 22,4 X X ^1.10 21,6 X X ^1.11 21,9 X X ^1.12 21,0 X X ^1.13 21,6 X X ^1.14 22,0 X X ^1.15 21,4 X X ^1.16 21,6 X X \n\
8 06.02.2025 13:59:20 ^1.1 30,7 X X ^1.2 31,0 X X ^1.3 37,1 X X ^1.4 41,8 X X ^1.5 35,1 X X ^1.6 38,3 X X ^1.7 35,0 X X ^1.8 21,8 X X ^1.9 22,3 X X ^1.10 21,5 X X ^1.11 21,9 X X ^1.12 21,1 X X ^1.13 21,6 X X ^1.14 21,9 X X ^1.15 21,4 X X ^1.16 21,6 X X \n\
9 06.02.2025 14:00:23 ^1.1 32,0 X X ^1.2 32,6 X X ^1.3 37,4 X X ^1.4 42,3 X X ^1.5 35,5 X X ^1.6 37,5 X X ^1.7 35,4 X X ^1.8 21,8 X X ^1.9 22,4 X X ^1.10 21,5 X X ^1.11 22,0 X X ^1.12 20,9 X X ^1.13 21,6 X X ^1.14 22,0 X X ^1.15 21,3 X X ^1.16 21,5 X X \n'


def main():
    parser = Parser()

    parser.RawDataParse(test_raw_tdt_data)

if __name__ == '__main__':
    main()