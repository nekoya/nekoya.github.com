---
layout: post
title: "Pythonでdatetimeにtzinfoを付与するのにreplaceを使ってはいけない"
date: 2013-07-05 12:24
comments: true
categories: python
---
Pythonでnaiveなdatetimeオブジェクトにtzinfoを付けてawareにするには、[公式](http://docs.python.jp/2/library/datetime.html#datetime.datetime.astimezone)には

>単にタイムゾーンオブジェクト tz を datetime オブジェクト dt に追加したいだけで、日付や時刻データメンバへの調整を行わないのなら、 dt.replace(tzinfo=tz) を使ってください。

こう書かれているのですが、どうもこの方法は夏時間の扱い以外にも問題があるようです。

    >>> import datetime, pytz
    >>> jst = pytz.timezone('Asia/Tokyo')
    >>> datetime.datetime.now(jst)
    datetime.datetime(2013, 7, 5, 12, 23, 1, 962735, tzinfo=<DstTzInfo 'Asia/Tokyo' JST+9:00:00 STD>)
    >>> datetime.datetime.now().replace(tzinfo=jst)
    datetime.datetime(2013, 7, 5, 12, 23, 9, 143578, tzinfo=<DstTzInfo 'Asia/Tokyo' CJT+9:00:00 STD>)

replaceでtzinfoを付与すると、JSTではなくCJTとなります。CentOS5.8 + Python2.6.5とSnowLeopard + Python2.7.1で同じ結果になりました。

- [SQLクリニック（4）：日付データ演算の達人技を伝授する 【第3話】 (3/3) - ＠IT](http://www.atmarkit.co.jp/ait/articles/0505/27/news116_3.html)

>実は、日本にも複数のタイムゾーンが存在したことが過去にあるようです。それまでJSTとされていたタイムゾーンがこのときCJTとなりました。「Central Japan Time」の略称で、日本中央時間（もしくは中央日本時間）です。

少なくとも2013年にCJTを使うことはなさそうなので、これは嬉しくないですね。

    >>> jst.localize(datetime.datetime.now())
    datetime.datetime(2013, 7, 5, 12, 23, 19, 647283, tzinfo=<DstTzInfo 'Asia/Tokyo' JST+9:00:00 STD>)

夏時間に対処した時と同じように、localizeしてやれば問題なくJSTが返ってきます。とりあえずlocalizeしておけば安心、なのかな。

## 関連エントリ
- [Pythonの日付処理とTimeZone](http://nekoya.github.io/blog/2013/06/21/python-datetime/)
- [Pythonのdatetimeで夏時間を扱う](http://nekoya.github.io/blog/2013/07/02/python-aware-datetime-dst/)
