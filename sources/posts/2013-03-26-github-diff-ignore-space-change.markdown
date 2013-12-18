---
layout: post
title: "githubでdiff --ignore-space-changeを見る方法"
date: 2013-03-26 15:15
comments: true
categories: github
old_post: true
---
Python書いてると、モジュールの関数をクラスに抽出するリファクタリングとかで、git diff --ignore-space-changeする機会が多いですね。

githubでdiffを見る時にも--ignore-space-change出来たらなぁと思ったら、mizzy（@gosukenator）さんから神の声が！

<blockquote class="twitter-tweet"><p>@<a href="https://twitter.com/nekoya">nekoya</a> ?w=1 とURLにつけるといいみたいですよ <a href="https://t.co/3iuAcB3Stp" title="https://github.com/blog/967-github-secrets">github.com/blog/967-githu…</a></p>&mdash; Gosuke Miyashita (@gosukenator) <a href="https://twitter.com/gosukenator/status/316431837444595713">March 26, 2013</a></blockquote>
<script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

というわけで、githubでdiff画面開いて、URLに?w=1を付ければOKでした。
