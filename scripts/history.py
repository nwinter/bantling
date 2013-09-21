#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, with_statement

import math

def timelessness(name):
    """
    Return a 0-1 score representing how timeless this name is.

    We penalize anything that's extra old-fashioned or extra trendy now.
    """
    balance = 0
    fulcrum = 1960
    total_normed_popularity = 0
    for i, year in enumerate(name.years):
        p = name.get_popularity(year=year, normalized=True)
        total_normed_popularity += p
        interval = (fulcrum - name.years[0] if year < fulcrum else
                    name.years[-1] - fulcrum)
        balance += p * (year - fulcrum) / interval
    balance /= total_normed_popularity  # TODO: spread out over time?
    score = max(0, 1 - math.fabs(balance))
    #print name, "got score", score, "from balance", balance
    #if name.name == "Robert":
    #    print name.normed_popularity
    return score

target_popularity = 10000

def relevancy(name):
    """
    Return a 0-1 score representing whether the name is an actual name,
    as opposed to some crazy typo gibberish with like five occurrences.
    """
    score = min(1, math.log(1 + name.get_popularity(), target_popularity))
    return score

def rarity(name):
    """
    Return a 0-1 score representing whether the name isn't too popular.
    """
    score = max(0, 1 - (name.get_popularity() - target_popularity) / 5000000)
    return score
