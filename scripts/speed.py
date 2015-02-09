#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, with_statement
import math

def shortness(name):
    """
    Return a 0-1 score representing how short this name is.

    We penalize anything that has many letters or many syllables.
    """
    score = 1
    syllables = name.metaphones[0].count('A')
    letters = len(name.name)
    test = False
    if syllables > 1:
        score *= 1 - min(1, max(0, 0.1 * (syllables - 1) ** 2))
    if letters > 4:
        score *= 1 - min(1, max(0, 0.1 * (letters - 4)))
    if test:
        print "%s got shortness score %.3f with %d syllables and %d letters"%(
            name.name, score, syllables, letters)
    return score

def recitability(name):
    """
    Return a 0-1 score representing how easy this name is to spell aloud.

    We penalize anything that has W's in it, and assign slight penalties for
    unclearly pronounced letters.
    """
    score = 1
    test = False
    name = name.name.lower()
    for bad_letter in ['w', 'y', 'm', 'n', 'r']:
        # W is three syllables.
        # Y will get miswritten as W because of the initial sound.
        # M and N sound the same.
        # Chloe can't say R's very well.
        score *= 1 - 0.2 * name.count(bad_letter)
    for not_great_letter in ['g', 'j']:
        # G will get misread as J because of the initial sound.
        # Presumably J sometimes gets confused as G, too?
        score *= 1 - 0.05 * name.count(not_great_letter)
    for okay_letter in ['b', 'c', 'd', 'e', 't', 'p', 'v', 'z', 'f', 's']:
        # *ee sound similar.
        # f and s sound similar.
        score *= 1 - 0.025 * name.count(okay_letter)
    for letter in set(name):
        # Double letters are tough!
        score /= (name.count(letter + letter) + 1)
    if test:
        print "%s got recitability score %.3f"%(name, score)
    return score

def nicklessness(name):
    """
    Return a 0-1 score representing how little this name needs a nickname.

    We penalize anything that has a nickname. The more and more popular the
    nicknames, the more the penalty.
    """
    score = 1
    test = False
    for nick in name.nicknames.values():
        pop_ratio = (nick.get_popularity(emphasize_recent=True) /
                     name.get_popularity(emphasize_recent=True))
        penalty = 20 * pop_ratio
        if test and name.name == "Abigail":
            print (name.name, "took a hit of", penalty, "from",
                   nick.name, pop_ratio)
        score *= max(0.25, (1 - penalty))
    if test: print "%s got nicklessness score %.3f"%(name, score)
    return score

def nickedness(name):
    """
    Return a 0-1 score representing how much we think this name is a nickname.

    We penalize anything that is a nickname of another, longer name.
    The more (and the more popular) the full names the more the penalty.
    """
    score = 1
    test = False
    for full in name.full_names.values():
        pop_ratio = (full.get_popularity(emphasize_recent=True) /
                     name.get_popularity(emphasize_recent=True))
        penalty = math.log(1 + pop_ratio / 5)
        if test and name.name == "Terri":
            print (name.name, "took a hit of", penalty, "from",
                   full.name, pop_ratio)
        score *= min(0.8, max(0.25, (1 - penalty)))
    if test: print "%s got nickedness score %.3f"%(name, score)
    return score
