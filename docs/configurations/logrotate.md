# logrotate

## Introduction
python command の場合、logging でローテートするより、コンソールに出力しておいたほうが使い勝手良さそう。

### Environmet
- QTS 4.5.1.1495 on TS-231K
- logrotate (3.17.0-1) 

## Installation

```console
[~] # opkg update
Downloading http://bin.entware.net/armv5sf-k3.2/Packages.gz
Updated list of available packages in /opt/var/opkg-lists/entware

[~] # opkg install logrotate
Installing logrotate (3.15.0-2) to root...
Downloading http://bin.entware.net/armv5sf-k3.2/logrotate_3.15.0-2_armv5-3.2.ipk
Installing libpopt (1.16-2) to root...
Downloading http://bin.entware.net/armv5sf-k3.2/libpopt_1.16-2_armv5-3.2.ipk
Configuring libpopt.
Configuring logrotate.
```

### /opt/etc/logrotate.conf
結果デフォルトでなにも指定していないが・・・

```:/opt/etc/logrotate.conf
# see "man logrotate" for details
# rotate log files weekly
weekly

# keep 4 weeks worth of backlogs
rotate 4

# create new (empty) log files after rotating old ones
create

# use date as a suffix of the rotated file
dateext

# uncomment this if you want your log files compressed
#compress

# packages drop log rotation information into this directory
include /opt/etc/logrotate.d

# system-specific logs may be also be configured here.
```



cron setup
/etc/config/crontab
# m h dom m dow cmd
...
50 13 * * * /opt/sbin/logrotate /opt/etc/logrotate.conf




[~] # crontab /etc/config/crontab

[~] # crontab -l
...

[~] # /etc/init.d/crond.sh restart
Stopping periodic command scheduler: crond.
Starting periodic command scheduler: crond.





Custom Configuration
Local script rotation
/opt/etc/logrotate.d/move-photo-files.conf
/share/Multimedia/logs/move-photo-files.log {
        missingok
        rotate 2
        maxsize 100M
        noolddir
        compress
}




logrotate.conf に記載のある次は省略
weekly
create

## dry-run
[~] # logrotate -dv /opt/etc/logrotate.conf
WARNING: logrotate in debug mode does nothing except printing debug messages!  Consider using verbose mode (-v) instead if this is not what you want.

reading config file /opt/etc/logrotate.conf
including /opt/etc/logrotate.d
reading config file move-photo-files.conf
Reading state from file: /var/lib/logrotate.status
error: error opening state file /var/lib/logrotate.status: No such file or directory
Allocating hash table for state file, size 64 entries

Handling 1 logs

rotating pattern: /share/Multimedia/logs/move-photo-files.log  weekly (2 rotations)
empty log files are rotated, log files >= 104857600 are rotated earlier, old logs are removed
considering log /share/Multimedia/logs/move-photo-files.log
Creating new state
  Now: 2021-01-04 18:54
  Last rotated at 2021-01-04 18:00
  log does not need rotating (log has already been rotated)


## force-run
[~] # logrotate -f /opt/etc/logrotate.conf





## Reference
QNAP TS-109II への syslog-ng の導入メモ — さめたすたすのお家
logrotate入門
任意のログをlogrotateを使って管理する
logrotateの設定 | ゆるっとエンジニアブログ
