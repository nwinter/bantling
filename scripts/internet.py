#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, with_statement
import whois
import os
import cPickle as pickle

_all_names_whois = {}
_all_names_whois_cache_filename = 'names/cached_whois.pkl'
def look_up(names, use_cache=True):
    """
    Uses whois to find out whether the domain name is available.

    Later, should also figure out how many search results there are.
    """
    global _all_names_whois
    if use_cache and os.path.exists(_all_names_whois_cache_filename):
        with open(_all_names_whois_cache_filename, 'rb') as f:
            _all_names_whois = pickle.load(f)
    else:
        print
        for i, name in enumerate(names):
            if name.get_popularity(normalized=True) < 0.0001:
                continue
            print "\r%05d / %05d - testing whois for %20swinter.com"%(
                i, len(names), name.name.lower()),
            try:
                result = whois.query(name.name.lower() + 'winter.com')
            except (KeyboardInterrupt, SystemExit), e:
                print "\nStopping whois lookups due to KeyboardInterrupt."
                break
            except Exception, e:
                print "\nCouldn't fetch %s: %s"%(name.name.lower() + 'winter.com', e)
                _all_names_whois[name.name] = False
                continue
            _all_names_whois[name.name] = bool(result)
            print bool(result),
            if result:
                print
        with open(_all_names_whois_cache_filename, 'wb') as f:
            pickle.dump(_all_names_whois, f, pickle.HIGHEST_PROTOCOL)
    for name in names:
        name.whois = _all_names_whois.get(name.name)

def googlability(name):
    """
    Return a 0-1 score representing how Googlable this name is.

    We penalize more depending on how many results for "<Name> Winter".
    """
    score = 1
    #print "Googlability for", name, getattr(name, 'whois', '<no whois>')

    return score

def availability(name):
    """
    Return a 0-1 score representing whether <name>winter.com is available.

    We could also check for <name>winter available handles on various
    online services.
    """
    score = 1

    return score
