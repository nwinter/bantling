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
    (phonetics.spellability, 40),
    (phonetics.pronounceability, 10),
    (history.timelessness, 20),
    (history.relevancy, 30),
    (history.rarity, 30),
    (internet.googlability, 8),
    (internet.availability, 4),
    (meaning.secularity, 30),
    (meaning.seriousness, 3),
    (beauty.palindromicity, 5),
    (beauty.initialization, 10),
    (speed.shortness, 20),
    (speed.recitability, 4),
    (speed.nicklessness, 15),
    (culture.chineseness, 4),
    (culture.genderedness, 20),
    (speed.nicklessness, 15),
)

total_weight = sum([w for (s, w) in weights])

def judge(name):
    """
    Return some sort of score for automatically ranking names based on all the
    features we can extract so far.

    I guess we'll just add the scores * weights up for now.
    """
    score = 0
    for scorer, weight in weights:
        score += scorer(name) * weight
    name.score = score
    return score
