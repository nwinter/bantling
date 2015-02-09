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
        self.scores = {}
        self.yearly_popularity = {"M": [0] * len(self.years),
                                  "F": [0] * len(self.years)}
        self.normed_popularity = {"M": [0] * len(self.years),
                                  "F": [0] * len(self.years)}
        self.nicknames = {}
        self.full_names = {}

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

    def to_dict(self):
        o = {"name": self.name, "scores": self.scores, "genders": self.get_genders()}
        if hasattr(self, "meaning"):
            o['meaning'] = self.meaning
        return o

    def get_genders(self):
        male_pop = self.get_popularity("M", normalized=True, emphasize_recent=True)
        female_pop = self.get_popularity("F", normalized=True, emphasize_recent=True)
        genders = []
        if male_pop > 10 * female_pop:
            genders = ["M"]
        elif female_pop > 10 * male_pop:
            genders = ["F"]
        else:
            genders = ["F", "M"]
        return genders

    def add_nickname(self, nick):
        if nick.name in self.nicknames: return 0
        if nick.name is self.name: return 0
        #print "Found nickname", nick.name, "for", self.name, "from", nick.meaning
        self.nicknames[nick.name] = nick
        return 1 + nick.add_full_name(self)

    def add_full_name(self, full):
        if full.name in self.full_names: return 0
        if full.name is self.name: return 0
        self.full_names[full.name] = full
        return 1 + full.add_nickname(self)
