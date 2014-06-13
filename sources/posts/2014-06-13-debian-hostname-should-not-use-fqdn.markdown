---
title: debian/Ubuntuの/etc/hostnameにはFQDNではなくshort nameを書く
date: 2014-06-13 08:23
---
Ubuntuのインストール時にFQDNを書いても/etc/hostnameにはshort nameが入るし、Vagrantのconfig.vm.hostnameにFQDNを書いても[ドメイン部分落とされる](https://github.com/mitchellh/vagrant/blob/f0cd8511ed3784415df14aa17b7e4b4935733b63/plugins/guests/debian/cap/change_host_name.rb#L44)し、どういうことなんだろうと思ったら[debianマニュアルのホスト名の項](http://www.debian.org/doc/manuals/debian-reference/ch03.en.html#_the_hostname)に書いてありました。

<pre>
3.2.5. The hostname

The kernel maintains the system hostname. The init script in runlevel S which is symlinked to "/etc/init.d/hostname.sh" sets the system hostname at boot time (using the hostname command) to the name stored in "/etc/hostname". This file should contain only the system hostname, not a fully qualified domain name.
</pre>

「only」を太字にするレベルで守られるべきルールのようです。

serverfaultに[Setting the hostname: FQDN or short name?](http://serverfault.com/questions/331936/setting-the-hostname-fqdn-or-short-name)として、CentOS, RHEL, debianの違いがまとまっていました。

自分もCentOSを使ってた時は/etc/sysconfig/networkにFQDNを書いていたのですが、debian系では

- /etc/hostnameにshort nameを書く
- /etc/hostsに書くなど名前解決のレイヤでFQDNを補完する

といったルールが敷かれているようです。「hostnameだからドメインは関係ないだろ！」ってことなんでしょうか。一理ある。

Ubuntuの[hostnameコマンドのman](http://manpages.ubuntu.com/manpages/precise/man1/hostname.1.html)にも、

<pre>
You can't change the FQDN (as returned by hostname --fqdn) or  the  DNS domain  name (as returned by dnsdomainname) with this command.
</pre>

という記述がありますね。
