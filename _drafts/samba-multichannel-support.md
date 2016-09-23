---
layout: post
title: "Samba: SMB Multichannel configuration"
teaser: "Speed up your Samba server with multiple low-cost NICs"
banner_image: theme_networking.jpg
tags: [linux, samba, networking]
category: linux
---
Starting wie Samba 4.4.0, it comes with Multi-Channel support as a new experimental features.
This is still marked as unstable in current 4.5.0 release, but if you're crazy, you can enable it easily
with a new smb.conf parameter.


<!--more-->


Microsoft has introduced a new feature called **SMB Multi-Channel** into SMB 3.0 (available since Windows Server 2012).
With Multi-Channel, you can share a SMB connection across multiplce NICs to increase throughput and implementing
fault-tolerant connection.

The implementation supports more complex networking features like RSS and RDMA, but I will focus on low-cost
hardware and private network setups. For mor details and requirements, see [this TechNet article](https://blogs.technet.microsoft.com/josebda/2012/06/28/the-basics-of-smb-multichannel-a-feature-of-windows-server-2012-and-smb-3-0/).


# Requirements

1. At first, Multi-Channel ist only available if two hosts (e.g. server and client) are interconnected with more
then one NIC and all interfaces provides the same network speed. For example, to can use a server with 4x 1Gbps
NICs and a client with 2x 1Gbps NICs connected to a switch (only two NICs will be used for Multi-Channel), but you can't
use a 100Mbps NIC + 1Gbps NIC for the client. Windows only uses NICs with the same speed for Multi-Channel!

2. You need a recent Windows version, Server 2012 or Windows 10 would be fine.

3. A recent Samba build is required (min. 4.4.0, I recommend to use 4.5.0). For Debian, you have to build your
own package.

# Building Samba (smbd) on Debian Jessie

Check out the latest tarball from [url](official Samba page) and run make.

# Enable Multi-Channel in smb.conf

This is really simple, just put:

{% highlight javascript %}
"server multi channel support" = yes
{% endhighlight %}

in your smb.conf.

It is required to enable async I/O, because a single file transfer is handled by a single process.
A single process can't handle feeding multiple NICs without using separate threads. That's what async I/O would
do for you [see Samba ML for details](link).

Omit any *optimizations* you found on the internet. Many of these parameters like *sendfile* are not required
anymore.

> Hint: If you use ZFS, it is not recommended to use sendfile anyway, because the ZoL implementation has a bug.





https://www.samba.org/samba/history/samba-4.4.0.html

https://blogs.technet.microsoft.com/josebda/2012/06/28/the-basics-of-smb-multichannel-a-feature-of-windows-server-2012-and-smb-3-0/


