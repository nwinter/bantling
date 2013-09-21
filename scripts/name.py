#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, with_statement

import functools

# http://wiki.python.org/moin/PythonDecoratorLibrary#Memoize
def memoized(obj):
    cache = obj.cache = {}

    @functools.wraps(obj)
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = obj(*args, **kwargs)
        return cache[key]
    return memoizer

class Name:
    def __init__(self, name, years):
        self.name = name
        self.years = years
        self.score = 0  # until scored
        self.yearly_popularity = {"M": [0] * len(self.years),
                                  "F": [0] * len(self.years)}
        self.normed_popularity = {"M": [0] * len(self.years),
                                  "F": [0] * len(self.years)}

    def add_popularity(self, year, gender, count):
        self.yearly_popularity[gender][year - self.years[0]] = count

    def normalize_popularities(self, yearly_totals):
        for g in ["M", "F"]:
            for i, total in enumerate(yearly_totals):
                self.normed_popularity[g][i] = (
                    self.yearly_popularity[g][i] / total)

    @memoized
    def get_popularity(self, gender=None, year=None, emphasize_recent=False,
                       normalized=False):
        popularity = 0
        pops = self.normed_popularity if normalized else self.yearly_popularity
        for g in ["M", "F"]:
            if gender and gender != g: continue
            if year:
                popularity += pops[g][year - self.years[0]]
            else:
                if emphasize_recent:
                    for i, pop in enumerate(pops[g]):
                        popularity += pop * 2 * i / len(self.years)
                else:
                    popularity += sum(pops[g])
        return popularity

    def add_metaphones(self, primary, secondary):
        if secondary:
            self.metaphones = [primary, secondary]
        else:
            self.metaphones = [primary]

    def __str__(self):
        return "<%s, F: %d, M: %d | %s>"%(
            self.name, self.get_popularity('F'), self.get_popularity('M'),
            ', '.join(self.metaphones))

