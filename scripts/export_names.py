#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time
import json

from name import Name

def export_json(names):
    export_filename = 'src/application/static/js/names.json'
    with open(export_filename, 'wb') as f:
        f.write("[\n")
        for name in names:
           f.write("  " + json.dumps(name.to_dict()) + "\n")
        f.write("]")
