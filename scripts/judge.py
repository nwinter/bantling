#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, with_statement

import phonetics
import history
import culture
import speed
import beauty
import internet
import meaning

weights = (
    ("phonetics.spellability", phonetics.spellability, 40),
    ("phonetics.pronounceability", phonetics.pronounceability, 10),
    ("history.timelessness", history.timelessness, 20),
    ("history.relevancy", history.relevancy, 30),
    ("history.rarity", history.rarity, 30),
    ("internet.googlability", internet.googlability, 8),
    ("internet.availability", internet.availability, 4),
    ("meaning.secularity", meaning.secularity, 30),
    ("meaning.seriousness", meaning.seriousness, 3),
    ("beauty.palindromicity", beauty.palindromicity, 5),
    ("beauty.initialization", beauty.initialization, 10),
    ("speed.shortness", speed.shortness, 20),
    ("speed.recitability", speed.recitability, 4),
    ("speed.nicklessness", speed.nicklessness, 15),
    ("culture.chineseness", culture.chineseness, 4),
    ("culture.genderedness", culture.genderedness, 20),
    ("speed.nicklessness", speed.nicklessness, 15),
)

total_weight = sum([w for (id, s, w) in weights])

def judge(name):
    """
    Return some sort of score for automatically ranking names based on all the
    features we can extract so far.

    I guess we'll just add the scores * weights up for now.
    """
    score = 0
    for scoreID, scorer, weight in weights:
        subscore = scorer(name)
        score += subscore * weight
        name.scores[scoreID] = subscore
    name.score = score
    return score
