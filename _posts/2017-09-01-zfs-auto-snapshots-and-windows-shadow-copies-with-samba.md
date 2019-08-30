---
layout: post
title: "ZFS: auto-snapshots and Windows shadow copies with Samba"
banner_image: theme_storage.jpg
tags: [linux, zfs, zfsonlinux, debian, samba]
category: linux
---

With ZFS snapshots and Samba's **shadow_copy2** module, 
you can expose snapshots to Windows clients as shadow copies.

First, install *zfs-auto-snapshot* on Debian:

> apt-get install zfs-auto-snapshot

Default configuration for **zfs-auto-snapshot** uses specific labels like _daily_, _weekly_ etc.
This is incompatible to samba's expected snapshot format. As a good workaround, instead of using
text labels, I've changed the labels to numbers:


|**31**: for daily snapshots|
|**05**: for 5 minute interval snapshots|
|**24**: for hourly snapshots|
|**12**: for monthly snapshots|
|**52**: for weekly snapshots|

<!--more-->

This generates snapshot names like:

> storage/datapool/support@zfs-auto-snap_05-2017-09-01-1045

Now it is possible to use the label as input for the shadow copy timestamp:

>  shadow: format = zfs-auto-snap_%S-%Y-%m-%d-%H%M

The "label" which is always an integer, is now used as second (%S) part which is (mostly) negligible
for shadow copies.

The required changes for **smb.conf** are:

~~~
[global]
    vfs objects = shadow_copy2
    shadow: snapdir = .zfs/snapshot
    shadow: sort = desc
    shadow: format = zfs-auto-snap_%S-%Y-%m-%d-%H%M
    shadow:localtime = no
~~~


I've modified the installed cronjob files for numeric labels:

~~~
# tail -vn +1 /etc/cron.*/zfs-auto-snapshot
==> /etc/cron.daily/zfs-auto-snapshot <==
#!/bin/sh
exec zfs-auto-snapshot --quiet --syslog --label=31 --keep=7 //

==> /etc/cron.d/zfs-auto-snapshot <==
PATH="/usr/bin:/bin:/usr/sbin:/sbin"

*/5 7-21 * * * root zfs-auto-snapshot -q -g --label=05 --keep=12  //

==> /etc/cron.hourly/zfs-auto-snapshot <==
#!/bin/sh
exec zfs-auto-snapshot --quiet --syslog --label=24 --keep=24 //

==> /etc/cron.monthly/zfs-auto-snapshot <==
#!/bin/sh
exec zfs-auto-snapshot --quiet --syslog --label=12 --keep=3 //

==> /etc/cron.weekly/zfs-auto-snapshot <==
#!/bin/sh
exec zfs-auto-snapshot --quiet --syslog --label=52 --keep=4 //
~~~

