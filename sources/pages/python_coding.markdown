---
title: 逆引きPython - コーディングスタイル（社内向け）
---
## INDEX

<li>コーディングスタイル</li>
<li><a href="/pages/python_file/">ファイル操作</a></li>
<li><a href="/pages/python_date/">日付・時刻</a></li>
<li><a href="/pages/python/">その他</a></li>

## 基本方針

Pythonの公式ガイドである[PEP8](http://www.python.org/dev/peps/pep-0008/)を基本とする（[mumumu版日本語訳](https://github.com/mumumu/pep8-ja/blob/master/index.rst)）。

ただし、全てのファイルの先頭に以下のエンコーディング宣言を入れるものとする。

<pre class="prettyprint">
# -*- coding: utf-8 -*-
</pre>

これは、ソースコード内に日本語を書くことをイレギュラーとして捉えることを抑止するためである。

「日本語でコメントを入れたいけど、その前にエンコーディング宣言を入れなければ」のような事態が発生することは、現状を鑑みると好ましくないと判断した。

それ以外の細かい部分は原則として[Google Python Style Guide](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html)に従うが、絶対厳守というわけではない。

明文化しているわけではないが、なんとなくこんな感じでやってる。

1. メンバーの理解を損ねない範囲でクラスを直接importしてもよい
1. サードパーティライブラリの公式ドキュメントにあれば関数を直接importしてもよい

1はそろそろ改めることも考えていいかもしれない…

Google Python Style Guideは[rev 2.29の和訳](http://works.surgo.jp/translation/pyguide.html)があるが、2014/01/03現在の最新版はrev 2.59になっているので[差分](https://code.google.com/p/google-styleguide/source/list?path=/trunk/pyguide.html)は追いかけたい。

## 表記に関する規約

### flake8による文法チェック

プロダクトのコードは全て[flake8](https://pypi.python.org/pypi/flake8)による文法チェックを通過することとする。

vimを使っている場合は、[vim-flake8](https://github.com/nvie/vim-flake8)でファイルの保存時に随時チェックをかけることを推奨する。

インストールは適当にやればいいが、例えばプレーンなvim環境だと~/.vim/plugin/でこういう風にやる。

<pre class="prettyprint">
pip install flake8
wget --no-check-certificate https://raw.github.com/nvie/vim-flake8/master/ftplugin/python_flake8.vim
</pre>

.vimrcに以下を書いておくと保存時に自動チェックが出来る。

<pre class="prettyprint">
autocmd BufWrite *.py :call Flake8()
</pre>

任意で実行したければ以下のようにキーを割り当てれば良い。

<pre class="prettyprint">
map <F6> :!inspect_python %<CR>
" もしくは以下
autocmd FileType python map <buffer> <F6> :call Flake8()<CR>
</pre>

チェックしたくないルールは.vimrcに以下のように記述すればOK

<pre class="prettyprint">
let g:flake8_ignore="E501,E128,E124,E221"
</pre>


こういうのを書いておくと、トグルでE501の判定ON/OFFとか出来るのでご自由に。

<pre class="prettyprint">
let g:flake8_ignore = ''
function! Flake8IgnoreToggle()
    let rule = 'E501'
    if g:flake8_ignore == rule
        echo 'flake8 check E501'
        let g:flake8_ignore = ''
    else
        echo 'flake8 ignore E501'
        let g:flake8_ignore = rule
    endifendfunction
nnoremap <Space>5 :<C-u>call Flake8IgnoreToggle()<CR>
</pre>

### 一行の文字数

- [flake8 で Python のコードをチェックするときにオプションを渡すやつ - 祢占堂](http://drillbits.hatenablog.com/entry/flake8-config)

PEP8の制約がゆるくなって「チームで合意が取れるなら一行100文字でもいいんじゃねーの」という記述になったようだ。

今までチーム的には「厳しいけど他に基準がないので80文字に収める、ただしテストコードは破ってもよい」としていたが、この変更を受けて「全てのコードを一行100文字未満に収める」ことを規約とする。

プロジェクトのルートディレクトリに以下のようなsetup.cfgを置けば、あとはよしなにやってくれる。

<pre class="prettyprint">
[flake8]
max-line-length = 99
</pre>

## テストコードの書き方

### テストランナー

[nose](https://nose.readthedocs.org/en/latest/testing.html)を使う。今のトレンドは[Pytest](http://pytest.org/latest-ja/)っぽいけど、乗り換えるだけのメリットが感じられないので今までの路線を継続する。

### ok\_, eq\_の禁止

今まではこの2つを積極的に利用してきたが、これから書くコードについてはこの2つを使ってはならない。

Python2.7になってunittest.assertEqualでリストや辞書を比較して違った時の出力がPytestみたいに[親切になった](https://gist.github.com/nekoya/9522681)ので、

<pre class="prettyprint">
from nose.tools import assert_equal
</pre>

としてこれを使う。

ok\_についてはこれまでも特に取り上げなかったが、eq_とセットで扱うべきだと考えられるので（どちらもnose/tools/trivial.pyで定義されている）個別のassert系のメソッドを利用することとする。

### assert_equalのmaxDiff設定

長い項目で差異があった場合、[assert_equalが情報を省略する](https://gist.github.com/nekoya/9525030)。この挙動は[maxDiff](http://docs.python.jp/2/library/unittest.html#unittest.TestCase.maxDiff)で調整できる。

<pre class="prettyprint">
import nose.tools
nose.tools.assert_equal.__self__.maxDiff = None
</pre>

のように書くと、一切の省略をしないようになる。この値をどうするかはプロジェクトごとに判断すればよい。

現時点での推奨は、プロジェクトごとにtestutils.pyを持ち、その中でプロジェクト標準の設定値を与えることとする。


### assertionの順序

assert_equalなどの「実値」と「期待値」を比較する場合は、期待値を後に書く。

[公式ドキュメント](http://docs.python.jp/2/library/unittest.html#unittest.TestCase.assertEqual)では、

<pre class="prettyprint">
assertEqual(first, second, msg=None)
</pre>

first, secondとなっていて、順序については記載がない。

[JUnitでは期待値が先](http://junit.sourceforge.net/javadoc/org/junit/Assert.html)になっていて、Javaのバックグラウンドがある人はこちらを自然なものとして捉えている。[phpunitも同様](http://phpunit.de/manual/3.7/ja/writing-tests-for-phpunit.html#writing-tests-for-phpunit.assertions.assertEquals)である。

Perlでは[Test::More](http://search.cpan.org/~rjbs/Test-Simple-1.001002/lib/Test/More.pm)がgot, expectedの順で書くことを標準としている。

Rubyの[RSpec](http://rspec.info/)は文法そのものが違うが、実値に対して「XXであるべき」のような記述をするので期待値が後のパターンと考えられる。

unittestのドキュメントにはfirst, secondとしか書いていないが、ドキュメントのサンプルコードが全て期待値を後に書いているので、それに従うことにする。
