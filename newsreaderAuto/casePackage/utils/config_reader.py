# -*- coding: utf-8 -*-
import json
import os

def read(file):
    if file.find('.json') < 0:
        file = file + '.json'
    file = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")), file)
    if os.path.exists(file):
        config = json.load(open(file))
        return config