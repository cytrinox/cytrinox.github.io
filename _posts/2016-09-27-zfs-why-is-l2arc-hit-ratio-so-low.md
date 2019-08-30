---
layout: post
title: "ZFS: Why is L2ARC hit ratio so low?"
banner_image: theme_ram1.jpg
tags: [linux, zfs, zfsonlinux, debian, featured]
category: linux
---

Using an additional SSD disk as a second level cache for ARC - called L2ARC - can
speed up your ZFS pool. But if you analyze how often the cache is used you find a very low
hit ratio. To understand why the hit ratio is low you should know how the L2ARC works.

ZFS uses a primary cache - the ARC - which takes some space of your available RAM.
Until the ARC is really full, no noteworthy data is written to the L2ARC. Thus,
until the ARC cache is *warm*, the L2ARC cache isn't used.
But even it is not used, a read request triggers a lookup in ARC and then in L2ARC.
Because both caches are *cold* after a reboot, you can see a lot of cache misses.

<!--more-->

# Calculate the hit ratio

To calculate the hit ratio, the formula ```hit_ratio = (hits+misses)/hits``` is used.

~~~
root@mz4:~# arc_summary.py
...
L2 ARC Breakdown:                               2.25m
        Hit Ratio:                      12.80%  288.37k
        Miss Ratio:                     87.20%  1.97m
        Feeds:                                  795.95k
~~~

Now it's easy to understand why the hit ratio is low. If you have a lot of RAM (say 32 GiB),
it takes hours or days until the ARC cache is *warm*. And then it takes hours or days again until the L2ARC
is *warm*. But during this time, every cache lookup is counted as *cache-miss*: after 2 days you
may have 29837872 cache misses on L2ARC but it's still filled up with just a few bytes.
After both caches are *warm*, the L2ARC-hits will slowly increase.

A better approach to calculate the hit ratio is to wait until the L2ARC cache is *warm*. Then
write down the current count of L2ARC cache misses.

> real_hit_ratio = ((hits-hits_before_warm)+(misses-misses_before_warm))/(hits-hits_before_warm)

With this formula, you ignore all the cache misses until the cache is warm.

# Determine if L2ARC cache is cold or warm

As a rule of thumb, I assume the cache is *warm* if:

1. The difference between arc_max_size and arc_size is lower than 10% of arc_max_size.
2. The difference between l2arc_size and l2arc_usage is lower than 50% of l2arc_size.
3. The hit count of l2arc is greater than 1000

# Final thoughts

Keep in mind that if you have a lot of RAM available for ARC, it may take days until the L2ARC is
filled with data. The L2ARC is lost after a reboot (see issue [#925](https://github.com/zfsonlinux/zfs/issues/925) for persistent L2ARC) and
if you shut down your system every night, your L2ARC cache is never used.





