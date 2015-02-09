#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, with_statement
import re

def chineseness(name):
    """
    Return a 0-1 score representing how easy this name would be to say
    for a Chinese speaker.

    Could write something that figures out how hard the name is to say
    for a Chinese speaker... but we can perhaps figure out a Chinese name
    based on the English name that will work instead?
    """
    score = 1
    test = False
    sound_groups = {
        "impossible": {
            "penalty": 0.75,
            "sounds": ['l$', 'le$', 'er', 'st', 'ts', 'ld', 'lt', 'rl', 'x']
        },
        "tough": {
            "penalty": 0.3,
            "sounds": ['th', 'r', 'mb', 'rl', 'oo', 'v']
        },
        "okay": {
            "penalty": 0.15,
            "sounds": ['b$', 'c$', 'd$', 'de$', 'f$', 'g$', 'j$', 'k$', 'ke$',
                       'm$', 'me$', 'n$', 'ne$', 'p$', 'pe$', 'q$',
                       'r$', 're$', 's$', 'se$', 't$', 'te$']
        }
    }
    for sound_group in sound_groups.values():
        for sound in sound_group['sounds']:
            score -= sound_group['penalty'] * len(re.findall(sound, name.name.lower()))
    score = max(0, score)
    if test:
        print "%s got chineseness score %.3f"%(name, score)
    return score

def genderedness(name):
    """
    Return a 0-1 score representing how unambiguous the gender of this
    name is.
    
    As much as this helps in the initial don't-genderify-my-baby phase, we
    can come up with some other appellation for use then. It's just
    inconvenient later to have a gender-ambiguous name.
    """
    male_pop = name.get_popularity("M", normalized=True, emphasize_recent=True)
    female_pop = name.get_popularity("F", normalized=True, emphasize_recent=True)
    pop_ratio = male_pop / (male_pop + female_pop)
    pop_ratio = max(pop_ratio, 1 - pop_ratio)
    score = 2 * (pop_ratio - 0.5)
    return score
