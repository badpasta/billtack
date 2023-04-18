# -*- coding: utf-8 -*-


import base as test_base
import logging

from logging import debug as log_debug, info as log_info

from billtack.utils import log
from billtack.utils import config
from billtack.utils.bills import read_xls, read_csv, WechatBillFactory, AlipayBillFactory
from billtack.utils.ledgers import SuishoujiBillEntry


"""测试BillFactory功能, 从xls文件中读取账单数据"""
#def test_bill_factory_from_xls():
#    file_path = 'tests/data/2019-12-01.xls'
#    bill = BillFactory(file_path).create_bill()
#    assert len(bill) == 4
#    assert str(bill) == 'Bill(4 entries)'
#


"""测试read_xls功能, 读取xls文件"""
def test_read_xls():
    file_path = '/Users/jingyu.wang/Downloads/支付账单(20230201-20230331)/微信支付账单(20230201-20230331).csv'
    data = read_xls(file_path, header_line=16)
    log_debug(data)
    
    
"""测试read_csv功能, 读取csv文件"""
def test_read_csv():
    file_path = '/Users/jingyu.wang/Downloads/支付账单(20230201-20230331)/微信支付账单(20230201-20230331).csv'
    data = read_csv(file_path, header_line=17)
    log_debug(data)

"""测试WechatBillFactory功能, 从csv文件中读取账单数据""" 
def test_wechat_bill_factory_from_csv():
    file_path = '/Users/jingyu.wang/Downloads/支付账单(20230201-20230331)/微信支付账单(20230201-20230331).csv'
    factory = WechatBillFactory(file_path)
    bill = factory.create_bill(SuishoujiBillEntry)
    
    log_info(f"Wechat 账单条目数量: {len(bill)}")
    export_path = '/Users/jingyu.wang/Downloads/支付账单(20230201-20230331)/微信支付账单(20230201-20230331)_export.xls'
    factory.to_file(export_path, bill)

"""测试AlipayBillFactory功能, 从csv文件中读取账单数据"""
def test_alipay_bill_factory_from_csv():
    file_path = '/Users/jingyu.wang/Downloads/支付账单(20230201-20230331)/alipay_record_20230413_202413.csv'
    factory = AlipayBillFactory(file_path)
    bill = factory.create_bill(SuishoujiBillEntry)
    log_info(f"Alipay 账单条目数量: {len(bill)}")
    export_path = '/Users/jingyu.wang/Downloads/支付账单(20230201-20230331)/alipay_record_20230413_202413_export.xls'
    factory.to_file(export_path, bill)


def export_alipay_and_wechat_bill_to_suishouji():
    """导出支付宝和微信账单到随手记"""
    alipay_file_path = '/Users/jingyu.wang/Downloads/支付账单(20230201-20230331)/alipay_record_20230413_202413.csv'
    alipay_factory = AlipayBillFactory(alipay_file_path)
    bill = alipay_factory.create_bill(SuishoujiBillEntry)
    

   
    
    export_path = '/Users/jingyu.wang/Downloads/支付账单(20230201-20230331)/suishouji.xls'
    
    wechat_file_path = '/Users/jingyu.wang/Downloads/支付账单(20230201-20230331)/微信支付账单(20230201-20230331).csv'
    wechat_factory = WechatBillFactory(wechat_file_path)
    wecaht_bill = wechat_factory.create_bill(SuishoujiBillEntry)
    
    log_info(f"{id(bill.entries)}")
    log_info(f"{id(wecaht_bill.entries)}")

   
    alipay_length = len(bill)
    wechat_length = len(wecaht_bill)
    #log_info(alipay_length)
    #log_debug(wechat_length)
    
    log_info(f"Alipay 账单条目数量: {alipay_length}")
    log_info(f"Wechat 账单条目数量: {wechat_length}")
    
    
    bill.extend(wecaht_bill)
    
    log_info(len(bill))
    
    alipay_factory.to_file(export_path, bill)


 
if __name__ == '__main__':
    
    config.init()
    
    from billtack.utils.config import CONF
    log.init(logging.INFO)
    
    #test_read_xls()
    #test_read_csv()
    #test_wechat_bill_factory_from_csv()
    #test_alipay_bill_factory_from_csv()
    export_alipay_and_wechat_bill_to_suishouji()
    
    
    
    