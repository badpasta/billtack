# -*- coding: utf-8 -*-

# coding=utf-8


import sys

from oslo_config import cfg
from oslo_utils import importutils
from logging import debug as log_debug

from billtack.utils.exception import Error


CONF = cfg.CONF


class ImportConfigurationError(Error):
    message = "Configuration for {} import failed."
    

def _register_fn(option_uri, register_fn):
    option_module = importutils.try_import(option_uri)
    if option_module is None:
        raise ImportConfigurationError(key=option_uri)
    try:
        groups = getattr(option_module, 'groups')
        for group_name, opts in groups.items():
            register_fn(opts, group_name)
    except AttributeError:
        raise ImportConfigurationError(key=option_uri)


def register_conf_opts(option_uri):
    _register_fn(option_uri, CONF.register_opts)


def register_cli_opts(option_uri):
    _register_fn(option_uri, CONF.register_cli_opts)


def register_all_opts(option_uri):
    register_conf_opts(option_uri)
    register_cli_opts(option_uri)
    
    
def init():
    register_all_opts("billtack.utils.config.options")
    global CONF
    config_path = sys.argv[1:]
    log_debug(config_path)
    CONF(config_path)
