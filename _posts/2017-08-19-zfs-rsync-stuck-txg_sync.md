---
layout: post
title: "ZFS: txg_sync stuck at 100% while copy large dataset with rsync"
banner_image: theme_storage.jpg
tags: [linux, zfs, zfsonlinux, debian]
category: linux
---

While transfering a large dataset (2TiB) via rsync from **ext4** to **zfs**, rsync hangs at some time
and txf_sync stuck at 100% cpu.

It was a fresh system and zfs was set up just a few minutes ago. After some research,
I found out that this problem is related to ARC.

I've changed the *zfs_arc_min parameter* while trx_sync stuck and the system immediately
responses.

> echo 1073741824 >> /sys/module/zfs/parameters/zfs_arc_min

This sets the minimum size (hard limit) for ARC to 1 GiB. 


## References

[https://github.com/zfsonlinux/zfs/issues/3409#issuecomment-283551036](https://github.com/zfsonlinux/zfs/issues/3409#issuecomment-283551036)


