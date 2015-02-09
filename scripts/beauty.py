#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, with_statement

def initialization(name):
    """
    Return a 0-1 score representing how cool this name's initials could be.

    Without picking a middle name first, this will rely on 676 possibilities
    for first and middle. I just went through and found all the ones I thought
    could be cool that had a final W.
    """
    cool = [
        'BOW',
        'DEW',
        'HEW',
        'HOW',
        'JAW',
        'MAW',
        'NEW',
        'NOW',
        'PAW',
        'POW',
        'RAW',
        'ROW',
        'UVW',
        'VAW',
        'VOW',
        'WOW',
        'YEW',
        'YOW',
        'ZOW'
    ]
    cool_letters = [s[0] for s in cool]
    if name.name[0] in cool_letters:
        return 1
    else:
        return 0

def palindromicity(name):
    """
    Return a 0-1 score representing whether this name is a palindrome.
    """
    n = name.name
    if n == ''.join(reversed(n)):
        return 1
    else:
        return 0
