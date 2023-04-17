#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: Jingyu Wang <badpasta@gmail.com>
#
# Environment:
# Python by version 3.9.


import sys

def import_program_path():
    root_path = "/".join(sys.path[0].split("/")[:-1])
    program_path = f"{root_path}/src/"
    #print(program_path)
    sys.path.append(program_path)


import_program_path()