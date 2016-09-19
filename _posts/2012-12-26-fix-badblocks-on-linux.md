---
layout: post
title: "Fix badblocks on a hard drive"
banner_image: theme_storage.jpg
tags: [linux, storage]
category: linux
---


At first, we run a read-only badblocks scan on the device to find the corrupt blocks.

```
% badblocks /dev/sda       
55575184
55575185
55575186
55575187
55575188
55575189
55575190
55575191
55575192
55575193
55575194
55575195
55575196
55575197
55575198
55575199
```

Now we know that block 55575184 - 55575199 are dead. If there are only a few blocks, it's possible to replace these.

The disk firmware may reallocate new blocks, but only if you try to write to the corrupt blocks. This can be done via

```
% badblocks -v -w /dev/sda 55575199 55575184
Checking for bad blocks in read-write mode
From block 55575184 to 55575199
Testing with pattern 0xaa: done                                                 
Reading and comparing: done                                                 
Testing with pattern 0x55: done                                                 
Reading and comparing: done                                                 
Testing with pattern 0xff: done                                                 
Reading and comparing: done                                                 
Testing with pattern 0x00: done                                                 
Reading and comparing: done                                                 
Pass completed, 0 bad blocks found. (0/0/0 errors)
```

Seems good. We can repeat the whole read-only scan to see if there are no more badblocks.

Finally, you should start a self-test with smartctl -t long /dev/sda. After finished, smartctl -a /dev/sda should return something like this:

```
SMART Self-test log structure revision number 1
Num  Test_Description    Status                  Remaining  LifeTime(hours)  LBA_of_first_error
# 1  Extended offline    Completed without error       00%       231         -
# 2  Extended offline    Completed: read failure       60%       230         111150080
# 3  Short offline       Completed without error       00%       196         -
# 4  Short offline       Completed without error       00%         9         -
1 of 1 failed self-tests are outdated by newer successful extended offline self-test # 1
```

Because we have killed some data (the bad blocks), it is recommended to recreate the filesystem or run a full repair.
Some filesystems like ZFS can repair the defect blocks, other (like ext4) can not detect errors if these are in data blocks.
