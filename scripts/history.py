#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, with_statement

import math
import random

test_names = ["Dwight", "Michael", "Joseph", "Kent", "Abigail",
              "Gertrude", "Nicholas", "Jennifer", "Jason",
              "Ashley", "Shirley", "Sophia", "Emma",
              "Phillip", "Keith", "Scott", "Brett", "Mitchell",
              "Marc", "Dustin", "Larry", "Terry", "Douglas",
              "Randall", "Corey", "Curtis", "Lindsay",
              "Caitlin", "Erica", "Dana", "Brittany",
              "Tiffany", "Kelly", "Bethany", "Tara",
              "Whitney", "Heather", "Shannon", "Courtney",
              "John", "James", "William", "David", "Mary",
              "Sarah", "Elizabeth", "Woodrow", "Calvin",
              "Lynn", "Aubrey", "Adolph", "Caroline",
              "Elizabeth", "Julia", "Victoria", "Iris",
              "Andrew", "Peter", "Benjamin"]

def timelessness(name):
    """
    Return a 0-1 score representing how timeless this name is.

    We penalize anything that's extra old-fashioned or extra trendy now.
    """
    smoothing_addend = 0.0001
    total_normed_popularity = 0
    for i, year in enumerate(name.years):
        p = name.get_popularity(year=year, normalized=True)
        p += smoothing_addend
        total_normed_popularity += p
    average_normed_popularity = total_normed_popularity / len(name.years)
    total_deviation = 0
    recent_deviation = 0
    for i, year in enumerate(name.years):
        p = name.get_popularity(year=year, normalized=True)
        p += smoothing_addend
        deviation = p / average_normed_popularity
        if deviation < 1:
            deviation = 1 / deviation
        total_deviation += deviation
        if i >= len(name.years) - 10:
            recent_deviation += deviation
    deviation_per_year = total_deviation / len(name.years)
    recent_deviation_per_year = recent_deviation / 10

    score = 1
    score -= max(0, min(1, (deviation_per_year - 1.1) / 2)) * 0.67
    score -= max(0, min(1, (recent_deviation_per_year - 1.1) / 2)) * 0.33
    score = max(0, score)
    test = False
    if test and name.name in test_names:
        print "\n", name.name, "deviation per year", deviation_per_year, "recent", recent_deviation_per_year, "score", score
    return score

target_popularity_min = 1E5
target_popularity_max = 1E6

def relevancy(name):
    """
    Return a 0-1 score representing whether the name is an actual name,
    as opposed to some crazy typo gibberish with like five occurrences.
    """
    score = min(1, math.log(1 + name.get_popularity(), target_popularity_min))
    return score

def rarity(name):
    """
    Return a 0-1 score representing whether the name isn't too popular.
    """
    pop_ratio = name.get_popularity() / target_popularity_max
    if pop_ratio < 1:
        return 1
    else:
        return 1 - (1 / pop_ratio) ** 0.5
