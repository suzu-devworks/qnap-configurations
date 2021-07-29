# crontab

## Introduction
QNAPにおけるcronの設定をまとめる。

### Environmet

- QTS 4.5.1.1495 on TS-231K
- BusyBox v1.01 (2020.11.22-20:02+0000) multi-call binary

## Configuration

通常の ```crotab -e``` で編集しても、再起動時には初期化されてしまう。
```/etc/config/crontab``` を直接編集するのが正しいらしい。

```:/etc/config/crontab
# m h dom m dow cmd
0-59/20 3 * * * /sbin/adjust_time
0 1 * * * /etc/init.d/flush_memory.sh >/dev/null 2>&1
0 4 * * * /sbin/hwclock -s
0 3 * * * /sbin/clean_reset_pwd
0-59/15 * * * * /etc/init.d/nss2_dusg.sh
30 7 * * * /sbin/clean_upload_file
0-59/10 * * * * /etc/init.d/storage_usage.sh
30 3 * * * /sbin/notice_log_tool -v -R
*/10 * * * * /sbin/config_cache_util 0
9 9,21 * * * /sbin/notify_update --nc 1>/dev/null 2>&1
32 7 * * * /share/CACHEDEV1_DATA/.qpkg/HybridBackup/rr2/scripts/insight/insight.sh -runall >/dev/null 2>&1
#0 2 * * * /sbin/qfstrim
00 03 * * * sh /share/CACHEDEV1_DATA/.qpkg/MalwareRemover/MalwareRemover.sh scan;#_QSC_:MalwareRemover:malware_remover_schedule:None:d::
00 02 * * * sh /share/CACHEDEV1_DATA/.qpkg/MalwareRemover/Upgrade.sh;#_QSC_:MalwareRemover:malware_remover_upgrade:None:d::
30 6 * * 1 /sbin/storage_util --disk_sequential_read_speed_test 1>/dev/null 2>&1
10 15 * * * /usr/bin/power_clean -c 2>/dev/null
0 3 * * 0 /etc/init.d/idmap.sh dump
12 3 * * * /bin/sh /etc/init.d/disk_data_collection.sh
* * * * * /var/cache/netmgr/lock_timer.sh
50 7 * * * /sbin/qpkg_cli --check_license 0 > /dev/null 2>/dev/null
0 4 * * * /etc/init.d/wsd.sh restart
0 3 * * * /sbin/vs_refresh
4 3 * * 3 /etc/init.d/backup_conf.sh
* 4 * * * /usr/sbin/logrotate /etc/config/mc_logr.conf
0 2 * * 0 /usr/local/medialibrary/bin/mymediadbcmd checkRepairDB  >/dev/null 2>&1
10 9 * * 1 /etc/init.d/antivirus.sh scan 1
0 0 * * * /etc/init.d/antivirus.sh scan 2
0 0 * * * /etc/init.d/antivirus.sh archive_log
45 0 */1 * * /etc/init.d/antivirus.sh update_db
0 12 * * * /mnt/ext/opt/LicenseCenter/bin/qlicense_tool local_check
0 0 * * * /usr/local/sbin/qsh nc.archive >/dev/null 2>&1
07 08 * * * /mnt/ext/opt/QcloudSSLCertificate/bin/ssl_agent_cli
50 23 * * 1 /etc/init.d/poweroff
0 7 * * 2 /etc/init.d/startup
2 10,16 * * * /share/homes/admin/qnap-configurations/bin/cron_exec_local.sh 1>/dev/null 2>&1
```

コマンドで再起動。

```console
# /etc/init.d/crond.sh restart
Stopping periodic command scheduler: crond.
Starting periodic command scheduler: crond.
```

コマンドで確認

```shell
crontab -l
```

## References
* [qnapのcronの設定](https://ymraintree.hatenadiary.org/entry/20120919/1348035056)
