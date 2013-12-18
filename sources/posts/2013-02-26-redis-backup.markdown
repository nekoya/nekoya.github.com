---
layout: post
title: "redisのバックアップは慎重に"
date: 2013-02-26 23:06
comments: true
categories: redis
old_post: true
fb_url_raw: true
---
<iframe src="http://rcm-jp.amazon.co.jp/e/cm?lt1=_top&bc1=000000&IS2=1&nou=1&bg1=FFFFFF&fc1=000000&lc1=0000FF&t=studiomweblog-22&o=9&p=8&l=as4&m=amazon&f=ifr&ref=ss_til&asins=4774155071" style="float:left;width:120px;height:240px;margin:0 1em 1em 0" scrolling="no" marginwidth="0" marginheight="0" frameborder="0"></iframe>

皆様におかれましては、WEB+DB PRESSの最新号のRedis特集は既にご覧頂いたかと存じます。

弊社では1年ほど前から広告配信に関する様々な部分でRedisを使っています。まだ2.4系なので、2.6の新機能とか新鮮でした。

本番環境でRedisを運用する上で、強く訴えたい注意点は「RDBが壊れることがある」ということです。

「RDBがあるからインスタンスが落ちても平気だぜ」とか思ってると、RDBが壊れてリストア失敗→データ消失ということになりかねません。ファイルにdumpされるからと安心していると痛い目に遭うかも知れません。

（2013/02/27追記）今のところ壊れたのはハード障害が怪しい場面のみです。「RDB壊れるとかRedis使えねー」とかそういう話ではまったくありません。誤解無きよう。壊れる時はRedisじゃなくても壊れます。自分のユースケースではTokyo Cabinet/Tyrantからの乗り換えだったので「RDBの修復自体がサポートされていない」というのが一番の注意点でした（AOFは育ちすぎるのと、I/O発生しすぎで見送り）。

Redisにはredis-check-dump, redis-check-aofというファイルのチェックツールが同梱されています。

redis-check-aofには--fixオプションがあり、ディスクに保存されたAOFログの復旧を試みることが出来ますが、redis-check-dumpにはそういったオプションはありません。ちゃんと準備しておかないと、RDBが壊れていることは確認できても、それを修復することはかなわず途方に暮れることになります。

ふつうに使っていてRDBが壊れることはそうそうないのは確かですが、メモリ故障などのハード障害のあおりを受けてクラッシュすることはあります。ハード障害に対してはレプリケーションは有効な対策ですが、RDB自体のバックアップもきっちり取っておきたいもの。

なので、ごくごく単純ですがRedisサーバでのRDBのバックアップは

1. RDBファイルの待避
2. redis-check-dumpで検査
3. bzip2で固める
4. バックアップキューに突っ込む

という手順で取っています。

キューに登録しておくと、バックアップサーバが後でrsyncしてくれるような簡単なジョブキューの仕組みをRedisのSortedSetを使って作っています。

なお、アプリケーションレベルでのRedisの使い方については[Redis in Action](http://www.manning.com/carlson/)が実例豊富でお勧めです。データ型の解説などもじっくりたっぷり解説してあるので、これからRedisを始めようという人はWEB+DBの特集を見た上で、この本を読むのがよいと思います。
