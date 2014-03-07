---
title: 逆引きPython
---
## INDEX

<li>コーディングスタイル</li>
<li><a href="/pages/python_file/">ファイル操作</a></li>
<li><a href="/pages/python_date/">日付・時刻</a></li>
<li><a href="/pages/python/">その他</a></li>

## コーディングスタイル（社内向け）

Pythonの公式ガイドである[PEP8](http://www.python.org/dev/peps/pep-0008/)を基本とする。

細かい部分は原則として[Google Python Style Guide](http://google-styleguide.googlecode.com/svn/trunk/pyguide.html)に従うが、絶対厳守というわけではない。

明文化しているわけではないが、なんとなくこんな感じでやってる。

1. メンバーの理解を損ねない範囲でクラスを直接importしてもよい
1. サードパーティライブラリの公式ドキュメントにあれば関数を直接importしてもよい
1. 文法チェッカーは[flake8](https://pypi.python.org/pypi/flake8)を使う

1はそろそろ改めることも考えていいかもしれない…

Google Python Style Guideは[rev 2.29の和訳](http://works.surgo.jp/translation/pyguide.html)があるが、2014/01/03現在の最新版はrev 2.59になっているので[差分](https://code.google.com/p/google-styleguide/source/list?path=/trunk/pyguide.html)は追いかけたい。

### flake8のvim連携

[vim-flake8](https://github.com/nvie/vim-flake8)を入れて、ファイルの保存時に文法チェックをかけるのを推奨する。

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

今までチーム的には「厳しいけど他に基準がないので80文字に収める、ただしテストコードは破ってもよい」としていたが、100文字に移行することを考えたい。

プロジェクトのルートディレクトリに以下のようなsetup.cfgを置けば、あとはよしなにやってくれる。

<pre class="prettyprint">
[flake8]
max-line-length = 99
</pre>
