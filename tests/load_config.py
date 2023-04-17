# -*- coding: utf-8 -*-

# coding=utf-8

import base as test_base

import logging

from logging import debug as log_debug, error as log_err

from billtack.utils import config
from billtack.utils import log


def test_load_config():
    config.init()
    config.CONF.print_usage()
    #log_debug(dir(config.CONF))
    log_debug(config.CONF.database.local_connection)
    log_debug(type(config.CONF.database.local_connection))
    log_debug(config.CONF.bill.trade_classify)
    
    if len(config.CONF.database.local_connection) == 0:
        log_err("Not have params \"local_connection\" in database group.")
    

if __name__ == '__main__':
    log.init(logging.DEBUG)
    test_load_config()