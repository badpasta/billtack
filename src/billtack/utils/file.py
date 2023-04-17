import xlrd, xlwt
import csv

from json import loads as json_loads
from logging import debug as log_debug


def load_file(file_path: str) -> dict:
    """从文件中加载json数据"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        
        return f.read()
    
    
"""输入headers, values, file_path, 输出一个xls文件"""
def write_xls(headers: list, values: list[list], file_path: str) -> None:
    
    def _length_check(headers, values):
        for value in values:
            if len(headers) != len(value):
                raise Exception(f"headers: {headers}, value: {value}")
            
    _length_check(headers, values)
    
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Sheet1')
    
    for col, header in enumerate(headers):
        sheet.write(0, col, header)
        
    for row, value in enumerate(values):
        for col, header in enumerate(headers):
            sheet.write(row+1, col, value[col])  
            
    workbook.save(file_path)
    

def read_xls(file_path: str, header_line: int=0, encode: str='utf-8') -> list:
    """读取xls文件, 返回一个列表, 列表的每个元素为一行数据, 每行数据是一个字典, 字典的key为表头, value为单元格的值"""
    data = []
    workbook = xlrd.open_workbook(file_path)
    sheet = workbook.sheet_by_index(0)
    headers = sheet.row_values(header_line)
    
    for row in range(header_line, sheet.nrows):
        row_data = dict(zip(headers, sheet.row_values(row)))

        data.append(row_data)
        
    return data    


def read_csv(file_path: str, header_line: int=0, encode: str='utf-8') -> list:
    """读取csv文件, 返回一个列表, 列表的每个元素为一行数据, 每行数据是一个字典, 字典的key为表头, value为单元格的值"""
    data = []
    
    with open(file_path, 'r', encoding=encode) as f:
        reader = csv.reader(f)
        log_debug(f"reader: {dir(reader)}")
        log_debug(f"reader.line_num: {reader.line_num}")

        log_debug(f"reader[0] chardet: {reader}")
        log_debug(f"reader[0]: {next(reader)}")

        headers = [] 
        for row in reader:
            if reader.line_num < header_line:
                continue
            elif reader.line_num == header_line:

                headers = row
                continue
            
            row_data = dict(zip(headers, row))
            data.append(row_data)
            
    return data