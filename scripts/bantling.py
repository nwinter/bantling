#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division, with_statement

# Here's some more info
# https://docs.google.com/document/d/17Cw5-2XJ6yPbz5Y6H3bQpeMeSvUwo9XJTHrkUzvyseI/edit#heading=h.bruwyu647l8e
# http://stackoverflow.com/questions/164831/how-to-rank-a-million-images-with-a-crowdsourced-sort

import sys
import random

import gather_all_names
import phonetics
import judge
import export_names

yob_years = range(1880, 2014)

def main(use_cache=True, test=False, test_name=None, exhaustive=False):
    print "Let's label this bantling!"
    all_names = gather_all_names.gather(yob_years, use_cache, test)
    print "Some example names:\n", '\n'.join(
        [str(n) for n in random.sample(all_names, 3)])
    print "Popular names:\n", '\n'.join(
        [str(name) for name in all_names[:3]])
    print "Spellability scores:"
    for name in random.sample(all_names, 3):
        print name, phonetics.spellability(name, test)
    if test_name:
        test_name = [n for n in all_names if n.name.lower() == test_name.lower()][0]
        print "Ways to spell %s:"%test_name.name
        print '\n'.join(
            ["%.6f\t%s"%(phonetics.spellability(name), name)
             for name in phonetics.similar_names(test_name, all_names, 10)])

    if not exhaustive:
        all_names = [name for name in all_names
                     if name.get_popularity(normalized=True) > 0.01]
                     #if random.random() < 0.01]
	# Later we can lower the threshold or run the exhaustive version.
        print "Scoring only most popular %d names." % len(all_names)

    # Rank all the names!
    for i, name in enumerate(all_names):
        try:
            score = judge.judge(name)
        except KeyboardInterrupt:
            break
        if i % 100 == 0:
            print '\r%d\t%03.1f\t%s                          '%(i, score, name),
            sys.stdout.flush()
    print
    scored = [n for n in all_names if hasattr(n, "score")]
    scored.sort(key=lambda n: n.score)
    scored.reverse()
    print "Top names:\n", '\n'.join(
        ["%s\t%.3f"%(name, name.score) for name in scored[:10]])
    print "Worst names:\n", '\n'.join(
        ["%s\t%.3f"%(name, name.score) for name in scored[-10:]])
    export_names.export_json(all_names)


if __name__ == "__main__":
    use_cache = True
    if len(sys.argv) >= 2 and sys.argv[1] == 'false':
        use_cache = False
    test = False
    if len(sys.argv) >= 3 and sys.argv[2] == 'true':
        test = True
        yob_years = range(2011, 2014)
    test_name = None
    if len(sys.argv) >= 4:
        test_name = sys.argv[3]
    exhaustive = False
    if len(sys.argv) >= 5 and sys.argv[4] == 'true':
        exhaustive = sys.argv[4]
    main(use_cache, test, test_name, exhaustive)
