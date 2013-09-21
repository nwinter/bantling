#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, with_statement

def initialization(name):
    """
    Return a 0-1 score representing how cool this name's initials could be.

    Without picking a middle name first, this will rely on 676 possibilities
    for first and middle. I guess we could fill out a table...
    """
    score = 1

    return score

def palindromicity(name):
    """
    Return a 0-1 score representing whether this name is a palindrome.
    """
    n = name.name
    score = 1 if n == n[len(n) - 1 : -1 : -1] else 0

    return score
    
