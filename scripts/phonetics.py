#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, with_statement

# We're using this Double Metaphone implementation
# http://www.atomodo.com/code/double-metaphone/metaphone.py

# There's a Metaphone 3 implementation in Java here, but we'll just use Double
# until I can figure out how to call the Java version.
# (Metaphone 3 is more accurate than Double Metaphone (Metaphone 2).)

import metaphone2
import subprocess
import collections
from levenshtein import levenshtein
import math
import os
import cPickle as pickle

_all_names_metaphones = {}
_all_names_metaphones_cache_filename = 'names/cached_metaphones.pkl'
def phoneticize(names, method='java', use_cache=True, test=False):
    global _all_names_metaphones
    if method == 'python':
        for name in names:
            primary, secondary = metaphone2.dm(name.name)
            name.add_metaphones(primary, secondary)
    else:
        if use_cache and os.path.exists(_all_names_metaphones_cache_filename):
            with open(_all_names_metaphones_cache_filename, 'rb') as f:
                _all_names_metaphones = pickle.load(f)
        else:
            N = 20000  # can't pass a string with 30K+ names in it, too long
            names_to_process = names[:]
            while names_to_process:
                names_batch = names_to_process[:N]
                names_to_process = names_to_process[N:]
                args = ['java', '-classpath', 'scripts', 'Metaphone3', "_".join(
                    [name.name for name in names_batch])]
                metaphones = subprocess.check_output(args).strip().split("\n")
                for i, (name, line) in enumerate(zip(names_batch, metaphones)):
                    try:
                        primary, secondary = line.split('_')
                    except ValueError, e:
                        print "Hmm; no luck on", i, name, line, e
                    _all_names_metaphones[name.name] = [primary, secondary]
            with open(_all_names_metaphones_cache_filename, 'wb') as f:
                pickle.dump(_all_names_metaphones, f, pickle.HIGHEST_PROTOCOL)
        for name in names:
            [primary, secondary] = _all_names_metaphones[name.name]
            name.add_metaphones(primary, secondary)
            
_metaphone_index = collections.defaultdict(list)
def build_metaphone_index(all_names):
    for name in all_names:
        for metaphone in name.metaphones:
            _metaphone_index[metaphone].append(name)

def spellability(name, test=False):
    """
    Return a 0-1 score representing how spellable this name is. 0 is bad.
    
    How? To start off, we look at all the names with the same Metaphone key,
    then assign a penalty depending on collisions with any common names.
    The size of the penalty will depend on how common the other name is relative
    to this name (so this is also somewhat of a popularity weighting), and
    the Levenshtein distance to any names with Metaphone collisions, since
    Metaphone ignores vowels and we do care about actual vowel and letter
    differences here.

    There might be more we could do here, but I can't think of it now.
    """
    score = 1
    for metaphone in name.metaphones:
        for other in _metaphone_index[metaphone]:
            if other is name: continue
            pop_ratio = (other.get_popularity(emphasize_recent=True) /
                         (name.get_popularity(emphasize_recent=True) or 0.000001))
            if pop_ratio < 0.01: continue  # levenshtein is expensive
            distance = levenshtein(other.name, name.name)
            penalty = math.log(1 + pop_ratio) / (distance ** 2)
            if test and name.name == "Eliza" and penalty > 0.1:
                print (name.name, "took a hit of", penalty, "from",
                       other.name, pop_ratio, distance)
            score *= max(0.5, (1 - penalty))
            if test: print "%s vs. %s: pop_ratio %.5f"%(other, name, pop_ratio)
    if test: print "%s got spellability score %.3f"%(name, score)
    return score

def pronounceability(name):
    """
    Return a 0-1 score representing how pronounceable this name is.

    We assign a slight penalty to anything with two Metaphone keys.

    We also penalize things with R's, since Chloe can't say R's very well.

    Other than that, we got nothing, so this ranker isn't very strong.
    """
    score = 1 if len(name.metaphones) == 1 else 0.5
    score -= 0.5 * name.name.lower().count('r')
    return max(0, score)

def similar_names(name, all_names, limit=90019001):
    """
    Given a name, returns names that would be pronounced similarly, sorted
    by popularity.
    """
    cousins = []
    for metaphone in name.metaphones:
        cousins.extend(_metaphone_index[metaphone])
    cousins.sort(key = lambda n: n.get_popularity(emphasize_recent=True))
    cousins.reverse()
    return cousins[:limit]
