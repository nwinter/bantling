#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, with_statement

def shortness(name):
    """
    Return a 0-1 score representing how short this name is.

    We penalize anything that has many letters or many syllables.
    """
    score = 1

    return score

def recitability(name):
    """
    Return a 0-1 score representing how easy this name is to spell aloud.

    We penalize anything that has W's in it, and assign slight penalties for
    unclearly pronounced letters.
    """
    score = 1

    return score

def nicklessness(name):
    """
    Return a 0-1 score representing how little this name needs a nickname.

    We penalize anything that has a nickname. The more nicknames, the more
    the penalty. The more full name the nickname maps to, the worse.

    TODO: find a database of nicknames.
    """
    score = 1

    return score
