import re
import json
from datetime import datetime

KEY_TIME_STAMP = 'TIME_STAMP'

RE_LINE_NUM_PTRN = r'\d+'
# 06.02.2025 13:52:25
RE_DATE_PTRN = r'\d{2}.\d{2}.\d{4}'
RE_SECONDS = r':\d{2}'
RE_TDT_TIME_PTRN = r'\d{2}:\d{2}' + RE_SECONDS
RE_TDT_DTTM_PTRN = RE_DATE_PTRN + r'\s' + RE_TDT_TIME_PTRN

# ^1.1 25,4 X X 
RE_TEMP_PREFIX = r'\s\^'
RE_SNSR_NUM = r'\d+.\d+'
RE_TEMP = r'[-]?\d+,\d+'
RE_TEMP_POSTFIX = r' X X'
RE_SNSR_DATA_PTRN = RE_TEMP_PREFIX + RE_SNSR_NUM + r'\s' + RE_TEMP + RE_TEMP_POSTFIX
RE_SNSRS_DATA =  r'(' + RE_SNSR_DATA_PTRN + r')+'

# регулярка всей строки tdt формата
RE_TDT_DATA_LINE = RE_LINE_NUM_PTRN + r'\s' + RE_TDT_DTTM_PTRN + RE_SNSRS_DATA


# регулярка всей строки csv формата
# 04.02.2025 18:21;24,2;23,7;25;25,3;25,6;24,4;23
RE_CSV_SPLITTER = r';'
RE_CSV_DTTM_PTRN = RE_DATE_PTRN + r'\s' + r'\d{2}:\d{2}'
RE_CSV_TEMP_PTRN = r'[-]?\d+(,\d+)?'
RE_CSV_SNSRS_DATA = r'(' + RE_CSV_SPLITTER + RE_CSV_TEMP_PTRN + r')+'
RE_CSV_DATA_LINE = RE_CSV_DTTM_PTRN + RE_CSV_SNSRS_DATA


class ParserTdt:
     
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
        print(self.parsed_lines)

    def LineValidate(self, line: str=''):
        res = re.search(RE_TDT_DATA_LINE, line)
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
        res = re.search(RE_TDT_DTTM_PTRN, line)
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
            sensor_temp = sensor_temp.replace(',','.')
            sensor_temp = float(sensor_temp)
            result[sensor_num] = sensor_temp
        return result

    def GetParsedDataAsJson(self):
        result = ''
        for parsed_line in self.parsed_lines:
            result += json.dumps(parsed_line) + '\n'
        return result

class ParserCsv:
     
    def __init__(self):
        pass

    def RawDataParse(self, raw_data: str=''):
        lines = raw_data.split('\n')
        self.parsed_lines = []
        for line in lines:
            if not self.LineValidate(line):
                continue
            pass
            date_time = self.GetDateTimeFromLine(line)
            date_time_str = date_time.strftime('%m.%d.%YT%H:%M:%S')
            timestamp = date_time.timestamp()
            sensors_data = self.GetSensorsData(line)
            sensors_data[KEY_TIME_STAMP] = timestamp
            sensors_data['DATE_TIME'] = date_time_str
            self.parsed_lines.append(sensors_data)

    def LineValidate(self, line: str=''):
        res = re.search(RE_CSV_DATA_LINE, line)
        if res:
            # print(res.group(0))
            return True
        return False

    def GetDateTimeFromLine(self, line: str=''):
        res = re.search(RE_CSV_DTTM_PTRN, line)
        date_time_str = res.group(0)
        # 06.02.2025 13:53:19
        format = '%d.%m.%Y %H:%M'
        date_time = datetime.strptime(date_time_str, format)
        return date_time

    def GetSensorsData(self, line: str=''):
        sensors_data = re.search(RE_CSV_SNSRS_DATA, line)
        split_data_str = re.split(RE_CSV_SPLITTER, sensors_data.group(0))
        result = {}
        sensor_num = 1
        for data_str in split_data_str:
            if data_str == '':
                continue
            # sensor_num = re.search(RE_SNSR_NUM, data_str).group(0)
            sensor_temp = re.search(RE_CSV_TEMP_PTRN, data_str).group(0)
            sensor_temp = sensor_temp.replace(',','.')
            sensor_temp = float(sensor_temp)
            result[sensor_num] = sensor_temp
            sensor_num += 1
        return result

    def GetParsedDataAsJson(self): # TODO вынести в базовый класс
        result = ''
        for parsed_line in self.parsed_lines:
            result += json.dumps(parsed_line) + '\n'
        return result

test_raw_tdt_data = '1 06.02.2025 13:52:25 ^1.1 25,0 X X ^1.2 24,9 X X ^1.3 32,1 X X ^1.4 40,3 X X ^1.5 32,7 X X ^1.6 32,6 X X ^1.7 30,6 X X ^1.8 21,6 X X ^1.9 22,3 X X ^1.10 21,5 X X ^1.11 21,9 X X ^1.12 21,0 X X ^1.13 21,5 X X ^1.14 21,9 X X ^1.15 21,4 X X ^1.16 21,5 X X \n\
2 06.02.2025 13:53:19 ^1.1 25,4 X X ^1.2 25,2 X X ^1.3 32,7 X X ^1.4 40,2 X X ^1.5 33,0 X X ^1.6 33,4 X X ^1.7 31,5 X X ^1.8 21,7 X X ^1.9 22,3 X X ^1.10 21,5 X X ^1.11 22,0 X X ^1.12 20,9 X X ^1.13 21,5 X X ^1.14 21,9 X X ^1.15 21,4 X X ^1.16 21,6 X X \n\
3 06.02.2025 13:54:23 ^1.1 25,8 X X ^1.2 25,7 X X ^1.3 33,4 X X ^1.4 40,3 X X ^1.5 33,3 X X ^1.6 34,2 X X ^1.7 32,2 X X ^1.8 21,8 X X ^1.9 22,3 X X ^1.10 21,5 X X ^1.11 21,8 X X ^1.12 20,9 X X ^1.13 21,5 X X ^1.14 21,9 X X ^1.15 21,4 X X ^1.16 21,5 X X \n\
4 06.02.2025 13:55:26 ^1.1 26,0 X X ^1.2 25,9 X X ^1.3 34,2 X X ^1.4 40,6 X X ^1.5 33,6 X X ^1.6 34,7 X X ^1.7 32,5 X X ^1.8 21,7 X X ^1.9 22,3 X X ^1.10 21,5 X X ^1.11 21,9 X X ^1.12 21,0 X X ^1.13 21,5 X X ^1.14 22,0 X X ^1.15 21,4 X X ^1.16 21,5 X X \n\
5 06.02.2025 13:56:20 ^1.1 -26,2 X X ^1.2 26,1 X X ^1.3 34,7 X X ^1.4 40,8 X X ^1.5 33,9 X X ^1.6 35,4 X X ^1.7 33,0 X X ^1.8 21,7 X X ^1.9 22,4 X X ^1.10 21,4 X X ^1.11 21,9 X X ^1.12 20,9 X X ^1.13 21,6 X X ^1.14 21,9 X X ^1.15 21,4 X X ^1.16 21,6 X X \n\
6 06.02.2025 13:57:23 ^1.1 27,5 X X ^1.2 27,3 X X ^1.3 35,6 X X ^1.4 41,2 X X ^1.5 34,3 X X ^1.6 36,8 X X ^1.7 33,2 X X ^1.8 21,8 X X ^1.9 22,3 X X ^1.10 21,5 X X ^1.11 21,9 X X ^1.12 20,9 X X ^1.13 21,5 X X ^1.14 22,0 X X ^1.15 21,4 X X ^1.16 21,7 X X \n\
7 06.02.2025 13:58:26 ^1.1 29,1 X X ^1.2 29,1 X X ^1.3 -36,4 X X ^1.4 41,5 X X ^1.5 34,6 X X ^1.6 37,8 X X ^1.7 34,1 X X ^1.8 21,8 X X ^1.9 22,4 X X ^1.10 21,6 X X ^1.11 21,9 X X ^1.12 21,0 X X ^1.13 21,6 X X ^1.14 22,0 X X ^1.15 21,4 X X ^1.16 21,6 X X \n\
8 06.02.2025 13:59:20 ^1.1 30,7 X X ^1.2 31,0 X X ^1.3 37,1 X X ^1.4 41,8 X X ^1.5 35,1 X X ^1.6 38,3 X X ^1.7 35,0 X X ^1.8 21,8 X X ^1.9 22,3 X X ^1.10 21,5 X X ^1.11 21,9 X X ^1.12 21,1 X X ^1.13 21,6 X X ^1.14 21,9 X X ^1.15 21,4 X X ^1.16 21,6 X X \n\
9 06.02.2025 14:00:23 ^1.1 -32,0 X X ^1.2 32,6 X X ^1.3 37,4 X X ^1.4 42,3 X X ^1.5 35,5 X X ^1.6 37,5 X X ^1.7 35,4 X X ^1.8 21,8 X X ^1.9 22,4 X X ^1.10 21,5 X X ^1.11 22,0 X X ^1.12 20,9 X X ^1.13 21,6 X X ^1.14 22,0 X X ^1.15 21,3 X X ^1.16 21,5 X X \n'


test_raw_csv_data = '06.02.2025 14:52;26;26,4;27,8;36;29,9;29,3;28,9;21,8\n\
06.02.2025 14:53;26,3;26,3;27,8;35,9;29,8;29,4;28,9;21,8\n\
06.02.2025 14:55;26,3;26,4;27,9;36,5;30,4;29,8;29,4;21,8\n\
06.02.2025 14:57;25,5;25,7;29,1;37;30,8;31,8;36,1;21,7\n\
06.02.2025 14:59;26,1;25,8;31,3;37,4;31,5;33,9;40,7;21,8\n\
06.02.2025 15:01;29,3;30,2;33,8;38,1;32,4;36,4;44,3;21,8\n\
06.02.2025 15:03;32,6;34,2;36,1;39,2;33,8;39,1;47,5;21,8\n\
06.02.2025 15:04;34,1;35,5;37;39,6;34,4;39,9;48,7;21,8\n\
06.02.2025 15:06;36,9;38,1;39,2;40,9;35,7;42,1;51,3;21,7\n\
06.02.2025 15:08;38,9;40;41,1;42;37,1;44;53,3;21,8\n\
06.02.2025 15:10;42,9;42,6;42,6;43,4;39,8;42,4;51,9;21,7\n\
06.02.2025 15:12;44;43,7;43,1;44,6;41,6;41,4;50,8;21,6\n\
06.02.2025 15:14;43,9;43,5;43,2;45,4;42,7;41,3;55,3;21,8\n'

def main():
    tdt_parser = ParserTdt()
    tdt_parser.RawDataParse(test_raw_tdt_data)

    csv_parser = ParserCsv()
    csv_parser.RawDataParse(test_raw_csv_data)
    json_data = csv_parser.GetParsedDataAsJson()

    pass

if __name__ == '__main__':
    main()