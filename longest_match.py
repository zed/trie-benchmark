#!/usr/bin/env python
import os
import string
import sys
import urllib
import zipfile

from itertools import islice
from timeit import default_timer as timer

def init_hosts(trim):
    global hosts

    filename = "top-1m.csv.zip"
    if not os.path.exists(filename):
        def report(*args):
            sys.stdout.write('\r'+ ' '*60 + '\r')
            sys.stdout.write(' '.join(map(str, args)))
            sys.stdout.flush()

        urllib.urlretrieve(
            "http://s3.amazonaws.com/alexa-static/top-1m.csv.zip",
            reporthook=report, filename=filename)

    with zipfile.ZipFile(filename, compression=zipfile.ZIP_DEFLATED) as z:
        with z.open(z.namelist()[0]) as f:
            hosts = [line.split(',')[1]
                     for line in islice(f, trim)
                     if ',' in line]
    print "init_hosts(%d) -> len(hosts)=%d" % (trim, len(hosts))


def longest_match_suffixtree(url_prefix):
    if longest_match_suffixtree.trie is None:
        from SuffixTree import SubstringDict
        # to install `SuffixTree`:
        #
        #   $ wget http://hkn.eecs.berkeley.edu/~dyoo/python/suffix_trees/SuffixTree-0.7.tar.gz
        #   $ pip install SuffixTree-0.7.tar.gz
        t = longest_match_suffixtree.trie = SubstringDict()
        for url in hosts:
            t['\n'+url] = url
    matches = longest_match_suffixtree.trie['\n'+url_prefix]
    return max(matches, key=len) if matches else ''
longest_match_suffixtree.trie = None


def longest_match_startswith(search):
    matches = (url for url in hosts if url.startswith(search))
    try:
        return max(matches, key=len)
    except ValueError:
        return ''


def longest_match_pytrie(search):
    if longest_match_pytrie.trie is None:
        from pytrie import StringTrie
        longest_match_pytrie.trie = StringTrie.fromkeys(hosts)
    matches = longest_match_pytrie.trie.keys(prefix=search)
    return max(matches, key=len) if matches else ''
longest_match_pytrie.trie = None


def longest_match_trie(search):
    if longest_match_trie.trie is None:
        from trie import Trie
        t = longest_match_trie.trie = Trie()
        for url in hosts:
            t[url] = url

    try: matches = (node.value
                    for node in longest_match_trie.trie._getnode(search).walk())
    except KeyError:
        return ''
    try: return max(matches, key=len)
    except ValueError:
        return ''
longest_match_trie.trie = None


def longest_match_datrie(search):
    if longest_match_datrie.trie is None:
        import datrie
        t = longest_match_datrie.trie = datrie.new(alphabet=string.printable)
        for url in hosts:
            t[url.decode('ascii')] = 1

    matches = longest_match_datrie.trie.keys(search.decode('ascii'))
    return max(matches, key=len) if matches else ''
longest_match_datrie.trie = None


def test(func, keyword):
    for f in [longest_match_startswith, longest_match_datrie,
              longest_match_pytrie, longest_match_trie]:
        for url_prefix in [keyword]+"google youtube abcdef \n  ".split(' '):
            sp = f(url_prefix)
            me = func(url_prefix)
            assert len(sp) == len(me), (url_prefix, f.__name__, sp, me)
        f.trie = None


def timef(f, keyword, N):
    init_hosts(trim=N)

    number = 1000
    r = []
    for _ in range(3): # repeat to get minimum time
        print '.',
        sys.stdout.flush()
        assert getattr(f, 'trie', None) is None # make sure trie is
                                                # not created yet
        start = timer() #NOTE: avoid using timeit.Timer() due to f.trie
        for _ in range(number): #NOTE: for small N it introduces
                                #noticable overhead
            f(keyword)
        r.append((timer()-start) * 1e6 / number)
        f.trie = None # force trie construction
    t = min(r)
    print "%s %5d microseconds, max %d" % (f.__name__, t, max(r))
    return t

def main():
    import argparse

    p = argparse.ArgumentParser()
    p.add_argument('--test', action='store_true')
    p.add_argument('--suffix', default='pytrie')
    p.add_argument('--keyword', default='abc')
    p.add_argument('--n', type=int, default=1000)
    args = p.parse_args()

    me = __import__(__name__)
    func = getattr(me, "longest_match_"+args.suffix)
    if args.test:
        init_hosts(trim=args.n)
        test(func, args.keyword)
    else:
        print me.timef(func, args.keyword, args.n)


if __name__=="__main__":
    main()
