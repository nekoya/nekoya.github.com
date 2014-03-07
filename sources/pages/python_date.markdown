---
title: 逆引きPython
---
## INDEX

<li><a href="/pages/python_coding/">コーディングスタイル</a></li>
<li><a href="/pages/python_file/">ファイル操作</a></li>
<li>日付・時刻</li>
<li><a href="/pages/python/">その他</a></li>

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
