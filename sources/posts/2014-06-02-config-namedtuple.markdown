---
title: Pythonのdictをnamedtupleに変換してベンチ取ってみた
date: 2014-06-02 09:06
---
[namedtuple](http://docs.python.jp/2/library/collections.html#collections.namedtuple)をもっと積極的に使っていきたいと思いながらも、今ひとつやれてないので軽くベンチ取ってみた。

ユースケースとして、アプリケーションのconfigをdict, namedtuple, objectそれぞれで持った場合を想定する。

<pre class="prettyprint">
from collections import namedtuple

from benchmarker import Benchmarker


def convert(v):
    if isinstance(v, dict):
        return namedtuple('_', v.keys())(**{x: convert(y) for x, y in v.items()})
    if isinstance(v, (list, tuple)):
        return [convert(x) for x in v]
    return v

conf = {
    'home': '/home/nekoya',
    'list': ['foo', 'bar', {'hoge': 'fuga'}],
    'databases': {
        'master': {
            'host': 'localhost',
            'db': 'myapp',
        },
        'slave': {
            'host': 'localhost',
            'db': 'myapp',
        },
    },
}
immutable_conf = convert(conf)


class C(object):
    def __init__(self, **kw):
        self.__dict__.update(**kw)

obj = C(databases=C(master=C(host='localhost')))

with Benchmarker(width=40, loop=1000) as bm:
    for _ in bm('convert'):
        convert(conf)

with Benchmarker(width=40, loop=1000*1000) as bm:
    for _ in bm('dict'):
        _ = conf['databases']['master']['host']
    for _ in bm('namedtuple'):
        _ = immutable_conf.databases.master.host
    for _ in bm('object'):
        _ = obj.databases.master.host
</pre>

手元のMacBookAirだとこんなもん。

<pre class="prettyprint">
## benchmarker:       release 3.0.1 (for python)
## python platform:   darwin [GCC 4.2.1 Compatible Apple LLVM 5.0 (clang-500.2.79)]
## python version:    2.7.6
## python executable: /Users/nekoya/.pyenv/versions/py27/bin/python

##                                           user       sys     total      real
convert                                    2.2300    0.0100    2.2400    2.2400

## Ranking                                   real
convert                                    2.2400 (100.0%) *************************

## Ratio Matrix                              real    [01]
[01] convert                               2.2400  100.0%
## benchmarker:       release 3.0.1 (for python)
## python platform:   darwin [GCC 4.2.1 Compatible Apple LLVM 5.0 (clang-500.2.79)]
## python version:    2.7.6
## python executable: /Users/nekoya/.pyenv/versions/py27/bin/python

##                                           user       sys     total      real
dict                                       0.2300    0.0000    0.2300    0.2269
namedtuple                                 0.6300    0.0000    0.6300    0.6369
object                                     0.2800    0.0000    0.2800    0.2786

## Ranking                                   real
dict                                       0.2269 (100.0%) *************************
object                                     0.2786 ( 81.5%) ********************
namedtuple                                 0.6369 ( 35.6%) *********

## Ratio Matrix                              real    [01]    [02]    [03]
[01] dict                                  0.2269  100.0%  122.8%  280.7%
[02] object                                0.2786   81.5%  100.0%  228.6%
[03] namedtuple                            0.6369   35.6%   43.7%  100.0%
</pre>

アクセサとしては生のdictや、オブジェクトの__dict__を参照するよりも重いようだ。

パフォーマンス的に問題になるようなレベルではないが、「高速だからnamedtupleを使うべき」というわけでもない。

indexではなくドットシンタックスでアクセスできるのは書いていて気持ちいいので、あとはimmutableであることの利点を開発プロセスの中でどれぐらい活かせるかというところか。

DDDでいうところのValueObjectを明示的に宣言するにはちょうどよさそうではある。不変なデータと関連する操作という考え方で、通常のクラスのベースに適用していくこともできるが、実際にメリットがあるかはまだ見えない。

なお、frozendictが[PEP416](http://legacy.python.org/dev/peps/pep-0416/)として上がって却下されているので、今のところdictがimmutableになることはなさそう。
