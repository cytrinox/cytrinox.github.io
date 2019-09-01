---
layout: post
title: "Rename network interface"
image: "/images/themes/theme_networking.jpg"
tags: [linux, featured]
category: linux
---

# Using udev

Change the interface name in `/etc/udev/rules.d/75-persistent-net-generator.rules`

# Using ip utility

~~~
ip link set eth1 down
ip link set eth1 name wan0
ip link set wan0 up
~~~
