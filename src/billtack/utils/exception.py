#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Jingyu Wang <badpasta@gmail.com>
#
# Environment:
# Python by version 3.9.


class Error(Exception):
    """ Base class for exceptions in this module. """
    message = str()
    key = dict()
    def __init__(self, key):
        self.key = key
    
    def __str__(self):
        return self.message.format(self.key)


class ObjectKeyNotFoundException(Error):
    message = "Object key \"{}\" not found."

    
class HttpParamsException(Error):
    message = "Http Params error, msg: \"{}\""

    
class HttpParamsException(Exception):
    message = "Http response parse error, msg: \"{}\""
 
    
class HttpRequestException(Exception):
    message = "Http request failed, msg: \"{}\""
    
    