# -*- coding: utf-8 -*-

from typing import Optional, Self, TypeVar

from logging import debug as log_debug
from json import loads as json_loads

from .config import CONF
from .file import load_file


class BillEntry(object):
    """账单条目类"""
    trade_type: str # 交易类型, 例如: 支出, 收入, 转账
    date: str    # 交易日期
    classify: str # 交易分类, 例如: 休闲娱乐, 运动健身, Match to TODO
    l2_classify: str
    bank_type: str # 银行类型, 例如: 现金, 储蓄卡, 信用卡
    bank_account: str # 银行账户, 例如: 中国招商银行(0237), 支付宝(2088)
    payout: float     # 支出金额
    #pay_owner: str  # 支付人
    merchant: str   # 商户, 例如: 京东, 淘宝, 微信支付
    comment: str    # 备注
    currency: str
    source: str # 来源, 例如: wechat, alipay, bank, cash
    
    def __init__(self, **kwargs) -> None:
        self.currency = 'CNY'
        
        assert 'merchant' in kwargs, 'merchant is None'
        
        classify_dict = self.trade_classify(kwargs['merchant'])
        
        kwargs.update(classify_dict)
        
        kwargs.update(self.bank_type(kwargs))
        
        log_debug(f"kwargs: {kwargs}")
        
        for key, value in kwargs.items():
            if key in self.__annotations__:
                setattr(self, key, value)

        # 通过__annotations__属性，获取类的所有自定义属性，然后遍历，如果属性值为None，则报错
        for  key, value in self.__annotations__.items():
            if getattr(self, key) is None:
                raise ValueError(f'{key} is None')

    def trade_classify(self, merchant: str) -> dict:
        """交易分类"""
        
        
        _classify = load_file(CONF.bill.trade_classify)
      
        log_debug(f"merchant: {merchant}") 
        log_debug(f"_classify: {_classify}")
        classify: dict[dict[str,list[str]]] = json_loads(_classify)
        log_debug(f"classify: {classify}")
        
        classify_result = {
            'classify': '其他',
            'l2_classify': '未知',
        }
        
        """
        classify是一个二级字典, 二级字典的value值是list, list的每个元素是一个字符串, 遍历list中的每个字符串, 
        如果字符串在merchant中, 则返回二级字典的key值, 其中一级字典的key值为classify, 二级字典的key值为l2_classify
        """
        for key, value in classify.items():
            for k, v in value.items():
                for value in v:
                    log_debug(f"value: {value}")
                    if value in merchant:
                        classify_result['classify'] = key
                        classify_result['l2_classify'] = k
        
        return classify_result
        
    def bank_type(self, entry: dict) -> dict:
        account_mapping = {
            '现金': ['现金'],
            '信用卡': ['浦发银行(0895)', '浦发银行信用卡(0895)', '招商银行信用卡(9632)'],
            '储蓄卡': ['招商银行(5237)', '招商银行储蓄卡(5237)'],
            '微信': ['零钱', '/', '零钱通'],
            '支付宝': ['余额宝', '余额']
        }
        
        bank_account = entry['bank_account']
        
        for key, value in account_mapping.items():
            if bank_account in value:
                return {'bank_type': key}  
        
        log_debug(f"entry: {entry}")   
        raise ValueError(f'bank_account: {bank_account} is not in account_mapping')      
        
        
            
    @classmethod        
    def parse_wechat_bill(cls, entry: dict) -> Self: ...
    
    @classmethod        
    def parse_alipay_bill(cls, entry: dict) -> Self: ...
    
    @classmethod
    def parse_bill(cls, entry: dict, key_mapping: dict) -> Self:
       
        keywords = dict()
        for key, value in entry.items():
            if key in key_mapping:
                keywords.update({key_mapping[key]: value})
                
        return cls(**keywords)
    
    def __str__(self) -> str:
        """输出带着类名的字符串, value从self.__anonations__中获取"""
        return f"{self.__class__.__name__}: {self.__dict__}"
    
    __repr__ = __str__
    
    def to_dict(self) -> dict:
        return self.__dict__
    
    def values(self) -> list:
        return list(self.__dict__.values())
    
    def headers(self) -> list: ...


class SuishoujiBillEntry(BillEntry): 
    
    @classmethod
    def parse_wechat_bill(cls, entry: dict) -> Self:
        key_mapping = {
            '交易时间': 'date',
            '收/支': 'trade_type',
            '交易对方': 'merchant',
            '备注': 'comment',
            '金额(元)': 'payout',
            '支付方式': 'bank_account',
            'source': 'source'
        }
        
        log_debug(f"key_mapping: {key_mapping}")
        log_debug(f"entry: {entry}")
        
        """将entry中金额(元)的值转换为float类型"""
        entry['金额(元)'] = float(entry['金额(元)'].replace('¥', ''))
        
        return cls.parse_bill(entry, key_mapping)

    @classmethod
    def parse_alipay_bill(cls, entry: dict) -> Self:
        key_mapping = {
            '交易时间': 'date',
            '收/支': 'trade_type',
            '交易对方': 'merchant',
            '备注': 'comment',
            '金额': 'payout',
            '收/付款方式': 'bank_account',
            'source': 'source'
        }
        
        log_debug(f"key_mapping: {key_mapping}")
        log_debug(f"entry: {entry}")
        
        """将entry中金额(元)的值转换为float类型"""
        entry['金额'] = float(entry['金额'])
        
        return cls.parse_bill(entry, key_mapping)

   
    @property 
    def file_type(self) -> str:
        return 'xls'
   
    @property 
    def headers(self) -> list:
        return ['币种', '日期', '商家', '交易类型', '金额', '账户2', '备注', 'source', '分类', '子分类', '账户1']

        
class Ledger(object):
    """账单类"""
    entries: list
    def __init__(self, entries: Optional[list] = None) -> None:
        self.entries = list()
        if entries is not None:
            self.entries = entries
            
    def append(self, entry: BillEntry) -> None:
        
        if not isinstance(entry, BillEntry):
            raise TypeError(f'entry must be BillEntry, not {type(entry)}')
        
        self.entries.append(entry)           
        
    def extend(self, entries: Self) -> None:
                            
        self.entries.extend(entries.entries)
        
    def values(self) -> list:
        return list(map(lambda e: e.values(), self.entries))
    
    def __iter__(self) -> iter:
        return iter(self.entries)
    
    def __len__(self) -> int:
        return len(self.entries)
    
    def __getitem__(self, index) -> BillEntry:
        return self.entries[index]
        
    def __str__(self) -> str:
        return f'Bill({len(self.entries)} entries)'
    
    __repr__ = __str__       
    
    
    