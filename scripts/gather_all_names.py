#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import glob
import time
import cPickle as pickle

from name import Name
import phonetics
import meaning
import internet

_all_names = {}
_all_names_cache_filename = 'names/cached.pkl'
def gather(yob_years, use_cache=True, test=False):
    global _all_names
    if _all_names: return _all_names
    t0 = time.time()
    if use_cache and os.path.exists(_all_names_cache_filename):
        with open(_all_names_cache_filename, 'rb') as f:
            _all_names = pickle.load(f)
    else:
        if not os.path.exists('names'):
            print '"names" dir not found; quitting.'
            print 'Unzip http://www.ssa.gov/OACT/babynames/names.zip into "names".'
            exit()
        yobs = glob.glob("names/yob*.txt")
        yearly_totals = []
        for yob in yobs:
            year = int(yob[9:13])
            if year < yob_years[0]: continue
            print "\rGathering names from", yob,
            sys.stdout.flush()
            total_popularity = 0
            with open(yob, 'r') as f:
                for line in f:
                    n, gender, count = line.strip().split(',')
                    count = int(count)
                    name = _all_names.get(n, Name(n, yob_years))
                    _all_names[n] = name
                    name.add_popularity(year, gender, count)
                    total_popularity += count
            yearly_totals.append(total_popularity)
        for name in _all_names.values():
            name.normalize_popularities(yearly_totals)
        #internet.look_up(_all_names.values(), use_cache)
        meaning.imbue(_all_names)
        phonetics.phoneticize(_all_names.values(), 'java', use_cache, test)
        with open(_all_names_cache_filename, 'wb') as f:
            pickle.dump(_all_names, f, pickle.HIGHEST_PROTOCOL)
    t1 = time.time()
    print "\rGathered %d names from %d - %d in %.3f seconds."%(
        len(_all_names),
        yob_years[0],
        yob_years[-1],
        t1 - t0)
    all_names = list(reversed(sorted(_all_names.values(),
                                     key=lambda name: name.get_popularity())))
    phonetics.build_metaphone_index(all_names)
    return all_names
