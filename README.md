trie-benchmark
==============

trie benchmark for the "longest prefix match" problem.

To generate time performance data (install pytrie, trie, datrie,
SuffixTree or remove them from comparison):

    $ ./benchmark.py --prefix nosw3_

To plot the data (install numpy/matplotlib):

    $ make-figures.py --plot-only --prefix nosw3_

see [make-figures.py](https://gist.github.com/235404)

See results [Performance comparison suffixtree vs. pytrie vs. trie vs. datrie vs. startswith -functions](http://stackoverflow.com/a/5479374/).

<!-- To edit enable orgtbl-mode

#title: rss memory for len(hosts)=1000000
| function    | memory, | ratio |
|             |     GiB |       |
|-------------+---------+-------|
| suffix_tree |   0.853 |   1.0 |
| pytrie      |   3.383 |   4.0 |
| trie        |   3.803 |   4.5 |
| datrie      |   0.194 |   0.2 |
| startswith  |   0.077 |   0.1 |
#+TBLFM: $3=$2/@3$2;%.1f

Type C-c C-c on TBLFM line to update `ratio` column
-->

### License

The code for `longest_match*` functions in `longest_match.py` is taken
from [the SO question and its
answers](http://stackoverflow.com/q/5434813/).  The rest is also [CC
BY-SA 3.0](http://creativecommons.org/licenses/by-sa/3.0/)