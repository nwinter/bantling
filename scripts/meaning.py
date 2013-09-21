#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, with_statement

def secularity(name):
    """
    Return a 0-1 score representing how secular this name is.

    We penalize anything that's clearly Biblical (or from any other religion).

    TODO: find a database of Biblical names, or one of all name meanings and
    figure out how to parse religious tags from it.
    """
    score = 1

    return score

def seriousness(name):
    """
    Return a 0-1 score depending on how much this name + 'Winter' isn't silly.

    Real words that relate to Winter would be penalized.

    I guess we can do this one just by human intuition--the phone test.
    Could pull in a dictionary and do something with the commonness of the
    name as a word, but it's not clear whether that should be penalized, so
    maybe it's not worth doing that step.
    """
    score = 1

    return score

