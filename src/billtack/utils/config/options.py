# -*- coding: utf-8 -*-

import sys

from oslo_config import cfg


default_opts = [
    cfg.BoolOpt('debug', default=False),
    cfg.BoolOpt('verbose', default=True),
    cfg.StrOpt('default_log_levels'),
    cfg.StrOpt('log_level', default=5),
    cfg.StrOpt('log_dir', default=''),
]


database_opts = [
    cfg.StrOpt('local_connection', default=''),
    cfg.IntOpt('pool_size', default=5),
]

bill_opts = [
    cfg.StrOpt('trade_classify', default=''),
    cfg.StrOpt('bank_account', default=''),
]

groups = {
    "default": default_opts,
    "database": database_opts,
    "bill": bill_opts,
}