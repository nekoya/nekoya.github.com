---
title: 逆引きPython
---
## INDEX

<li><a href="/pages/python_coding/">コーディングスタイル</a></li>
<li><a href="/pages/python_file/">ファイル操作</a></li>
<li><a href="/pages/python_date/">日付・時刻</a></li>
<li>その他</li>

## その他

### 辞書（dict）のソート

キー（key）の順に取り出す

<pre class="prettyprint">
>>> score = {'Jack':300, 'Mike':200, 'Jane':100}
>>> for (k, v) in sorted(score.items()):
...     k, v
...
('Jack', 300)
('Jane', 100)
('Mike', 200)
</pre>

値（value）の順に取り出す

<pre class="prettyprint">
>>> for (k, v) in sorted(score.items(), key=lambda x:x[1]):
...     k, v
...
('Jane', 100)
('Mike', 200)
('Jack', 300)
</pre>

reverse=Trueで降順になる。

<pre class="prettyprint">
>>> for (k, v) in sorted(score.items(), key=lambda x:x[1], reverse=True):
...     k, v
...
('Jack', 300)
('Mike', 200)
('Jane', 100)
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


### cached_propertyの励行

werkzeug.utilsにある[cached_property](http://werkzeug.pocoo.org/docs/utils/#werkzeug.utils.cached_property)の使用を推奨する。

社内でコードを書く場合は、ポートしたものがkauli.utilsにいるので以下のようにimportする。

<pre class="prettyprint">
from kauli.utils import cached_property
</pre>

通常のpropertyと比較して、キャッシュによるパフォーマンスの向上以外にも、

<pre class="prettyprint">
class Hoge(object):
    @cached_property
    def foo(self):
        return 'FOO'

hoge = Hoge()
hoge.foo = 'BAR'
</pre>

このように外部から値を注入できるのでテストを書く際にも便利である。

cached_propertyはキャッシュ可能なプロパティというよりも、遅延評価されるインスタンス変数と表現した方が適切なようにも思われる。通常のpropertyと適宜使い分けたい。
