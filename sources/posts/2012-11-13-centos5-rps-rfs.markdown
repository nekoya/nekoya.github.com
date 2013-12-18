---
layout: post
title: "CentOS5でもRPS/RFSでNICが捗る話"
date: 2012-11-13 15:52
comments: true
categories: network
old_post: true
---
[kazeburo](http://twitter.com/kazeburo)さんが[CentOS6.2での事例](http://blog.nomadscafe.jp/2012/08/centos-62-rpsrfs.html)を紹介されていますが、CentOS5系でもkernelを上げればRPS/RFSが使えるようになって、NICの負荷状況が劇的に改善します。

やり方は意外に簡単で、[ELRepo](http://elrepo.org/tiki/tiki-index.php)から[kernel-ml-2.6.35-14.2.el5.elrepo.x86_64.rpm](http://elrepo.org/linux/kernel/el5/x86_64/RPMS/kernel-ml-2.6.35-14.2.el5.elrepo.x86_64.rpm)を落としてきてインストール。

あとは、/boot/grub/menu.lstの設定をdefault=0にしてrebootすればOK。

    $ uname -r
    2.6.35-14.2.el5.elrepo

ELRepoはNICのドライバなんかもいろいろ提供してくれるし、古いバージョンのRPMを[archive](http://mirror.ventraip.net.au/elrepo/archive/)で提供してくれて非常にいいですね（kernelの過去RPMはないのかな）。

RPS/RFSを有効にする設定はCentOS6と同様です。

    # echo "f" > /sys/class/net/eth0/queues/rx-0/rps_cpus
    # echo 4096 > /sys/class/net/eth0/queues/rx-0/rps_flow_cnt
    # echo 32768 > /proc/sys/net/core/rps_sock_flow_entries
    
    # cat /sys/class/net/eth0/queues/rx-0/rps_cpus
    0f

それまで特定のコアだけが他よりも30〜50%ぐらい負荷が高かったのが、各コアにいい具合に分散するようになって、1台で捌けるトラフィックがぐっと多くなりました。


## ip_conntrack_maxと監視系の変更

kernel 2.6.35を入れることで、それまでの/proc/sys/net/ipv4/ip_conntrack_maxが/proc/sys/net/nf_conntrack_maxに移動します。

この値を見るNagiosプラグインを書いて、NRPE経由で監視してたのが動かなくなったので、プラグインを更新しました。

- [https://github.com/nekoya/nagios-plugins-ip_conntrack_max](https://github.com/nekoya/nagios-plugins-ip_conntrack_max)

/etc/sysctl.confの設定も変わるのですが、既存のサーバと統一するために

    net.ipv4.ip_conntrack_max = 524288
    net.nf_conntrack_max = 524288

と両方書いてしまうことにしました。

sysctl -pすると

    error: "net.ipv4.ip_conntrack_max" is an unknown key

って怒られるけど、実際のところは無視されるだけで特に実害無さそう…

Puppetのテンプレートで真面目に判定すればいいんだろうけど、ひとまずこれで。

[弊社](http://kau.li/jp)ではLVSをUbuntu、GWをVyattaにして自作サーバでNIC叩き回してがんばっていますが、appサーバはこれでまだ戦えそうです。
