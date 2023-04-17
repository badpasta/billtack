#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Jingyu Wang <badpasta@gmail.com>
#
# Environment:
# Python by version 3.9.


import logging


def init(level):
    logging.basicConfig( \
        format='%(asctime)s|%(levelname)s|%(funcName)s|%(message)s', level=level, force=True)

