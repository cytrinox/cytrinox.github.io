---
layout: post
title: "ZFS: Create pool with missing devices"
image: "/images/themes/theme_storage.jpg"
tags: [linux, zfs, zfsonlinux, debian, featured]
category: linux
---

ZFS on Linux has no support for creating pools with missing **vdevs**. Thats a benefit of mdadm which
accepts a **missing** keyword in a list of devices.

But there is a workaround:

First, check the size of an existing device (all devices must have same size). In my case,
each disk has 2000398934016 bytes. I've used fdisk to check the size but you can use whatever you want.

Now create parse file(s) with the given size.

<!--more-->

> truncate -s 2000398934016 /sparse1.img

Repeat this for each missing device and increment the number.

Now you can call *zpool create* with all existing devices and append the sparse files.
After that, you should take the sparse files offline to prevent zfs from filling these up.

~~~
root@virt-master1:/var/lib/libvirt/vmimages# zpool status
  pool: vm1storage
 state: DEGRADED
status: One or more devices has been taken offline by the administrator.
        Sufficient replicas exist for the pool to continue functioning in a
        degraded state.
action: Online the device using 'zpool online' or replace the device with
        'zpool replace'.
  scan: none requested
config:

        NAME                                          STATE     READ WRITE CKSUM
        vm1storage                                    DEGRADED     0     0     0
          raidz3-0                                    DEGRADED     0     0     0
            ata-WDC_WD20EFRX-68AX9N0_WD-WMC300377714  ONLINE       0     0     0
            ata-WDC_WD20EFRX-68AX9N0_WD-WMC300443307  ONLINE       0     0     0
            ata-WDC_WD20EFRX-68EUZN0_WD-WCC4M6UR8S28  ONLINE       0     0     0
            ata-WDC_WD20EFRX-68EUZN0_WD-WCC4M7SALHVP  ONLINE       0     0     0
            ata-WDC_WD20EFRX-68EUZN0_WD-WCC4M5PJS2AA  ONLINE       0     0     0
            /sparse1.bin                              OFFLINE      0     0     0
            /sparse2.bin                              OFFLINE      0     0     0
            /sparse3.bin                              OFFLINE      0     0     0
~~~


To prevent data loss, you should as soon as possible replace the sparse files with real physical devices.

