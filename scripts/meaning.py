#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, with_statement
import os
import csv
import re

def imbue(names):
    meanings_filename = 'names/meanings.csv'
    with open(meanings_filename, 'rb') as f:
        reader = csv.DictReader(f)
        found = 0
        total = 0
        for row in reader:
            total += 1
            text = row['name.text'].decode('utf-8').title()
            text = re.sub(r' \(\d+\)$', '', text)
            name = names.get(text)
            if not name:
                text = text.encode('ascii', 'ignore')
                name = names.get(text)
            if not name: continue
            meaning = row['meaning.text'].decode('utf-8')
            if hasattr(name, 'meaning'):
                meaning += name.meaning + ' | ' + meaning
            name.meaning = meaning
            #print name.name, 'assigned meaning', name.meaning
            found += 1
            find_nicknames(name, names)
        print "Matched", found, "name meanings of", total, "meanings and", len(names), "names."
        print "Total nicknames matched:", total_nicks_found

total_nicks_found = 0
def find_nicknames(name, names):
    global total_nicks_found
    full_name_lists = re.findall(r'(?:diminutive|short form) of ([^().]+)', name.meaning, re.IGNORECASE + re.UNICODE)
    full_names = []
    for full_name_list in full_name_lists:
        full_names = full_names + re.split(r'(?:,| or | and )', full_name_list)
    full_names = list(set(full_names))
    for full_name in full_names:
        full_name = names.get(full_name.strip().title())
        if full_name:
            total_nicks_found += full_name.add_nickname(name)
        
def secularity(name):
    """
    Return a 0-1 score representing how secular this name is.

    We penalize anything that's clearly Biblical (or from any other religion).

    TODO: come up with more religious triggers based on looking at other names.
    """
    score = 1
    for religion in ['Biblical', 'Hebrew', 'Christian', 'Testament']:
        if hasattr(name, 'meaning') and religion in name.meaning:
            score /= 2
    return score
