#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import time
import json

from name import Name

def export_json(names):
    export_filename = 'src/application/app/assets/js/names.json'
    with open(export_filename, 'wb') as f:
        f.write("[\n  ")
        lines = []
        for name in names:
            lines.append("  " + json.dumps(name.to_dict()))
        f.write(",\n  ".join(lines))
        f.write("\n]")
