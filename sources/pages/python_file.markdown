---
title: 逆引きPython
---
## INDEX

<li><a href="/pages/python_coding/">コーディングスタイル</a></li>
<li>ファイル操作</li>
<li><a href="/pages/python_date/">日付・時刻</a></li>
<li><a href="/pages/python/">その他</a></li>

## ファイル操作

### bzip2で圧縮されたファイルの処理

Python2.7からは[with構文で処理できるようになった](http://docs.python.jp/2/library/bz2.html#id1)ので、ふつうに書ける。

<pre class="prettyprint">
with bz2.BZ2File('hoge.pl.bz2') as f:
    for line in f:
        yield line
</pre>


### コマンドライン引数でファイルを処理する

標準モジュールの[fileinput](http://docs.python.jp/2.7/library/fileinput.html)が便利。

ファイルを複数指定しても処理してくれるし、引数がなければ標準入力を受けてくれる。

openhookにhook\_compressedを指定しておけばgzipやbzip2で圧縮したデータもよしなにやってくれる。

<pre class="prettyprint">
import fileinput

for line in fileinput.input(openhook=fileinput.hook_compressed):
    yield line
</pre>


### テンポラリファイルを扱う

ファイルシステム上で認識可能なテンポラリファイルを作る場合は、[tempfile.NamedTemporaryFile](http://docs.python.jp/2/library/tempfile.html#tempfile.TemporaryFile)を使う。

これで作ったファイルは確かにopenできるが、ファイルに何か書き込もうとするともう一工夫が必要になる。

write()しただけではその書き込み内容が反映されず、close()するとファイルが消えてしまう。delete=Falseで作れば自主的に消さない限り消えないが、今度は消しそこねのリスクが発生する。

<pre class="prettyprint">
>>> import tempfile
>>> import os.path
>>> with tempfile.NamedTemporaryFile() as f:
...     _f = open(f.name, 'w')
...     _f.write('abcde')
...     _f.close()
...     os.path.getsize(f.name)
...
5
</pre>

with文で開いて、中で別途書き込みすれば好きな内容を書き込んだ上で自動削除も利用できる。
