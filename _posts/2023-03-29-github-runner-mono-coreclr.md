---
layout: post
title: "github-runner: Failed to create CoreCLR, HRESULT: 0x8007054F"
image: "/images/themes/theme_storage.jpg"
tags: [linux, debian]
category: linux
---

Recently, my LXC container running the github linux runner, failed. The error message
was really confusing:

````
Failed to create CoreCLR, HRESULT: 0x8007054F
````

I've traced the problem down to:

[pid   680] sched_getaffinity(679, 128, 0x7f21afa0ee50) = -1 EINVAL (Invalid argument)

But why should sched_getaffinity() fail? The only reason I found in the manpage is:

       EINVAL (sched_getaffinity() and, in kernels before 2.6.9, sched_setaffinity()) cpusetsize is smaller than the size of the affinity mask used by the
              kernel.

So, the root cause was the new Linux kernel 6.1 running on this machine, which
has increased the number of maximum CPUs. A recompiled kernel with lower setting
fixed the issue.


