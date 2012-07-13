#!/usr/bin/env python
import sys
from itertools import product
from subprocess import Popen, PIPE

prefix = sys.argv[sys.argv.index("--prefix")+1]
ndots = 7
exponents = range(ndots)
maxn = 10**max(exponents)
function_suffixes = ["pytrie", "suffixtree", "datrie", "startswith",
"trie",
]

input_dict = dict(nonexistent_key="\n",
                  rare_key="freeezinearticles.com",
                  frequent_key="x")

for suff, input_type in product(function_suffixes, input_dict.keys()):
    filename = "%s%s-%s-%d-%d.xy" % (prefix, suff, input_type, ndots, maxn)
    print '*'*60
    print filename
    with open(filename, 'w') as file:
        for exp in exponents:
            n = 10**exp
            # run .timef() in a separate process for isolation
            p = Popen([sys.executable, '-u', 'longest_match.py',
                         '--suffix', suff,
                         '--keyword', input_dict[input_type],
                         '--n', str(n)],
                      stdout=PIPE, close_fds=True)
            for line in iter(p.stdout.readline, b''):
                print line,
            print >>file, n, line,
            file.flush()
