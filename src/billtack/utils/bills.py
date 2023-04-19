# -*- coding: utf-8 -*-

from typing import Optional, Self, TypeVar
from logging import debug as log_debug

from .ledgers import BillEntry, Ledger
from .file import read_csv, read_xls, write_xls

    
Entry = TypeVar('Entry', bound=BillEntry)
L = TypeVar('L', bound=Ledger)
   
    
class BillFactory(object):
    """账单工厂类"""
    file_path: str
    file_type: str
    file_encode: str = 'utf-8'
    header_line: int = 0
    entry_cls: Entry
    
    def __init__(self, file_path: str, cls: Optional[Entry] =None) -> None:
        self.file_path = file_path
        self.file_type = self.file_path.split('.')[-1]
        self.entry_cls = cls
    
    def create_bill(self, cls: Optional[Entry] = None) -> L:
        
        log_debug(f"create_bill: {self.file_path}")
        assert self.file_type in ['xls', 'csv'], f'不支持的文件类型：{self.file_type}'

        if cls is not None:
            self.entry_cls = cls
            
        if self.entry_cls is None:
            raise Exception("entry_cls is None")
        
        
        entries = getattr(self, f'_from_{self.file_type}')()

        bill = Ledger()        
        for _entry in entries:
            entry = self._parse_meta_bill(_entry)
            
            log_debug(f"entry: {entry}")
            bill.append(entry)
           
        return bill 

    
    def _from_xls(self) -> list[dict]:
        return read_xls(self.file_path)
    
    def _from_csv(self) -> list[dict]:
        return read_csv(self.file_path, self.header_line, encode=self.file_encode)
    
    def _parse_meta_bill(self, meta_bill: dict) -> Entry: ...


    def to_file(self, file_path: str, bills: L) -> None: 
      
        assert isinstance(bills, Ledger), "bills is not Ledger"
        assert len(bills) > 0, "bills is empty"
        
        file_type = bills[0].file_type
        
        headers = bills[0].headers
        
        if file_type == 'csv':
            self.to_csv(file_path, headers, bills.values())
        elif file_type == 'xls':
            self.to_xls(file_path, headers, bills.values())
    
    """TODO: 实现输出账单为csv文件, 用于导入记账软件"""
    def to_csv(self, file_path: str, headers: list[str], values: list[list]) -> None: 
       
        raise NotImplementedError("to_csv")
    
    
    def to_xls(self, file_path: str, headers: list[str], values: list[list]) -> None: 
        
        write_xls(headers, values, file_path)
   

class WechatBillFactory(BillFactory):
    """微信账单工厂类"""
    header_line = 17
    
    def _parse_meta_bill(self, meta_bill: dict) -> Entry:
        """解析原始账单, 格式化为标准账单"""
       
        log_debug(meta_bill.keys())
        meta_bill["source"] = "wechat"

        return self.entry_cls.parse_wechat_bill(meta_bill)
        
    
    
class AlipayBillFactory(BillFactory):
    """支付宝账单工厂类"""
    header_line = 25
    file_encode = 'gbk'
    
    def _parse_meta_bill(self, meta_bill: list[dict]) -> list[dict]:
        """解析原始账单, 格式化为标准账单"""
        
       
        log_debug(meta_bill.keys())

        def _replace(value):

            value = value.replace('\t', '')
            """去掉value末尾的空格"""
            value = value.rstrip()

            return value

        _bill = {}            

        for k, v in meta_bill.items():
            _bill[_replace(k)] = _replace(v)

        log_debug(f"_bill: {_bill}")
        _bill["source"] = "alipay"

        return self.entry_cls.parse_alipay_bill(_bill)


