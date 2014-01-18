---
title: 逆引きPython
---
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


## 日付・時刻

### TimeZoneの罠

Pythonの[datetime.datetime](http://docs.python.jp/2/library/datetime.html#datetime-datetime)にはTimeZone関連のややこしい問題がある。

- コンストラクタにtzinfoを渡すと夏時間を正しく認識できない
 - 時刻が確定する前にTimeZone情報を付与すると問題が起きる
- naiveなdatetimeオブジェクトにreplaceでtzinfoを付与すると、日本時間がJSTでなくCJTになる

詳細は以下のエントリを参照のこと。

- [Pythonの日付処理とTimeZone](http://nekoya.github.io/blog/2013/06/21/python-datetime/)
- [Pythonのdatetimeで夏時間を扱う](http://nekoya.github.io/blog/2013/07/02/python-aware-datetime-dst/)
- [Pythonでdatetimeにtzinfoを付与するのにreplaceを使ってはいけない](http://nekoya.github.io/blog/2013/07/05/python-datetime-with-jst/)


### 現時刻を取得する

上記の問題を回避しつつawareなdatetimeオブジェクトを取得する。

<pre class="prettyprint">
def now(with_microsecond=False, tzinfo=None):
    """Better datetime.datetime.now()

    - avoid DST problem (datetime constructor)
    - avoid JST/CJT problem (replace naive datetime)

    Args:
        <bool> with_microsecond
        <tzinfo> timezone object (optional, default UTC)
    Returns:
        <datetime> aware datetime object
    """
    dt = datetime.datetime.now(pytz.utc)
    if not with_microsecond:
        dt = dt.replace(microsecond=0)
    return dt.astimezone(tzinfo) if tzinfo else dt
</pre>


### UNIX timeを扱う

#### 現時刻をUNIX timeとして取得する

<pre class="prettyprint">
>>> import calendar
>>> import datetime
>>> calendar.timegm(datetime.datetime.utcnow().timetuple())
1388738304
</pre>

- time.mktimeはlocaltimeを扱い、caldner.timegmはUTCを扱う
- calender.timegmの方が速い。

#### datetimeオブジェクトとUNIX timeの変換

awareなdatetimeオブジェクトdtをUNIX timeに変換する。

<pre class="prettyprint">
>>> import calendar
>>> calendar.timegm(dt.astimezone(pytz.utc).timetuple())
1388738381
</pre>

UNIX timeをawareなdatetimeに変換する。

<pre class="prettyprint">
>>> import datetime
>>> import pytz
>>> datetime.datetime.fromtimestamp(1388738381, pytz.utc)
datetime.datetime(2014, 1, 3, 8, 39, 41, tzinfo=<UTC>)
</pre>

上の例ではUTCだが、TimeZone情報を後から付与するので、夏時間のある地域でも問題ない。


### 月の末日を求める

[calendar.monthrange()](http://docs.python.jp/2.7/library/calendar.html#calendar.monthrange)を使う。

<pre class="prettyprint">
>>> import calendar
>>> calendar.monthrange(2014, 2)[1]
28
</pre>

monthrange()が指定月の1日の曜日と、月の日数をtupleで返すので後者を取ればよい。


## その他

### メールを送信する

<pre class="prettyprint">
import smtplib
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import formatdate

def send(from_addr, to_addr, subject, body=None, encoding='utf-8'):
    if isinstance(body, unicode):
        body = body.encode(encoding)
    msg = MIMEText(body, 'plain', encoding)
    msg['Subject'] = Header(subject, encoding)
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()

    s = smtplib.SMTP('localhost:25')
    s.sendmail(msg['From'], msg['To'].split(','), msg.as_string())
    s.close()
</pre>


### 文字列からクラス名を決める

クラス名を動的に決定する場合は[globals()](http://docs.python.jp/2/library/functions.html#globals)からクラスを取得する。

<pre class="prettyprint">
>>> class Hoge(object):
...     pass
...
>>> globals()['Hoge']()
<__main__.Hoge object at 0x10d62e390>
</pre>

正直ちょっと無理矢理感があるが、実際のアプリケーションではこのような操作の対象は特定のモジュールにまとまっているはずで、その場合はもっとスマートに書ける。

myapp.commandsモジュールから動的にクラスを決定してインスタンスを得る。

<pre class="prettyprint">
import myapp.commands
obj = getattr(myapp.commands, 'Hoge')()
</pre>


### スクリプトを終了する

exit()ではなく[sys.exit()](http://docs.python.jp/2/library/sys.html#sys.exit)を使う。

<pre class="prettyprint">
import sys
sys.exit(exit_code)
</pre>

- [The difference between exit() and sys.exit() in python?](http://stackoverflow.com/questions/6501121/the-difference-between-exit-and-sys-exit-in-python)

exit()はインタラクティブを終了するためのショートカット（^D相当）であって、実行の停止ではない。


### decimal.Decimalを指定の桁で丸める

Pythonで浮動小数点演算をおこなう場合は、誤差を避けるためにfloatではなく[decimal](http://docs.python.jp/2/library/decimal.html)を用いる。

指定の桁で数値を丸めるには、[quantize](http://docs.python.jp/2/library/decimal.html#decimal.Decimal.quantize)メソッドを使う。

<pre class="prettyprint">
>>> import decimal
>>> decimal.Decimal('1.05').quantize(decimal.Decimal('0.0'), rounding=decimal.ROUND_HALF_UP)
Decimal('1.1')
</pre>

roundingの種別は[decimal.Context](http://docs.python.jp/2/library/decimal.html#decimal.Context)に詳しいが、基本はこの3つ。

- 切り捨て : ROUND\_DOWN
- 切り上げ : ROUND\_UP
- 四捨五入 : ROUND\_HALF\_UP

decimal.Decimalといちいち書くのは面倒なので、今のところチームのルールとして以下を設定している。

- from decimal import Decimalで直接クラスをimportしてよい
- テストコードのみfrom decimal import Decimal as Dで省略してよい
