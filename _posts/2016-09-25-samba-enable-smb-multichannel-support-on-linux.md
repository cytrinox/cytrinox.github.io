---
layout: post
title: "Samba: Enable SMB multi-channel"
teaser: "Speed up your Samba server with multiple low-cost NICs"
banner_image: theme_networking.jpg
tags: [linux, samba, networking, storage, featured]
category: linux
---
Starting wie Samba 4.4.0, it comes with multi-channel support as a new experimental feature.
This is still marked as unstable in current 4.5.0 release, but if you're crazy, you can enable it easily
with a new smb.conf parameter.



Microsoft has introduced a new feature called **SMB multi-channel** into SMB 3.0 (available since Windows Server 2012).
With multi-channel, you can share a SMB connection across multiple NICs to increase throughput and implementing
fault-tolerant connections.

<!--more-->

{% include image_caption.html imageurl="/images/posts/2016-09-20-smb-multichannel-transfer-rate.png" title="SMB multi-channel in action" caption="SMB multi-channel in action" %}


The implementation supports more complex networking features like RSS and RDMA, but I will focus on low-cost
hardware and private network setups. For mor details and requirements, see [this TechNet article](https://blogs.technet.microsoft.com/josebda/2012/06/28/the-basics-of-smb-multichannel-a-feature-of-windows-server-2012-and-smb-3-0/).


# Requirements

1. At first, multi-channel ist only available if two hosts (e.g. server and client) are interconnected with more
then one NIC and all interfaces provides the same network speed. For example, to can use a server with 4x 1Gbps
NICs and a client with 2x 1Gbps NICs connected to a switch (only two NICs will be used for multi-channel), but you can't
use a 100Mbps NIC + 1Gbps NIC for the client. Windows only uses NICs with the same speed for multi-channel!

2. You need a recent Windows version, Server 2012 or Windows 10 would be fine.

3. A recent Samba build is required (min. 4.4.0, I recommend to use 4.5.0). For Debian, you have to build your
own package.

# Building Samba (smbd) on Debian Jessie

Check out the latest tarball from [samba.org](https://www.samba.org/samba/download/) and run

~~~
# ./configure
# make
# make install
~~~

Then create a systemd service file to start smbd **/etc/systemd/system/smbd.service**:

~~~
[Unit]
Description=Samba SMB/CIFS server

[Service]
ExecStart=/usr/local/samba/sbin/smbd -F
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
~~~

Enable the new service with:

~~~
systemctl enable smbd
~~~



# Enable multi-channel in smb.conf

This is really simple, just put:

~~~~
server multi channel support = yes
aio read size = 1
aio write size = 1
~~~~

in your smb.conf.

It is required to enable async I/O, because a single file transfer is handled by a single process.
A single process can't handle feeding multiple NICs without using separate threads. That's what async I/O would
do for you [see Samba ML for details](https://lists.samba.org/archive/samba/2016-September/202696.html).


Some admins want to tune their samba setup with different options. One well known is **use sendfile = yes**. With aio enabled, the usage of sendfile is disabled. So you can skip such optimizations.

> Hint: If you use ZFS, it is not recommended to use sendfile anyway, because ZFS on Linux has not implemented *sendfile()* yet.

## Start smbd daemon
You can start smbd with

~~~
service smbd start
~~~

## Test if Windows uses multi-channel

You can test for active multi-channel connections with **Get-SmbMultichannelConnection**.
Start PowerShell as administrator:

~~~
PS C:\WINDOWS\system32> Get-SmbMultichannelConnection

Server Name    Selected Client IP                           Server IP                           Client Interface Index
-----------    -------- ---------                           ---------                           ----------------------
mz4.home.local True     2a01:1e8:e172:1:d0e8:4ba2:d9b6:a7e7 2a01:1e8:e172:1:d250:99ff:fec1:867a 7
mz4.home.local True     2a01:1e8:e172:1:ade6:9cd9:6c95:d326 2a01:1e8:e172:1::cafe               6
mz4            True     2a01:1e8:e172:1:d0e8:4ba2:d9b6:a7e7 2a01:1e8:e172:1:d250:99ff:fec1:867a 7
mz4            True     2a01:1e8:e172:1:ade6:9cd9:6c95:d326 2a01:1e8:e172:1::cafe               6


PS C:\WINDOWS\system32>
~~~



# Tips

1. Make sure that your samba hostname has valid A records (and AAAA records if you use IPv6) in your DNS setup.
When running 4 NICs, you have to define a record for each IP.

2. Don't mix IPv4 and IPv6 interfaces. If eth0 has both v4 and v6 addresses and eth1 has only a v4 address, multi-channel
may not work as expected.

3. Reboot your Windows client if multi-channel works not as expected during tests (really!).


# Full smb.conf example


~~~
#
# Sample configuration file for the Samba suite for Debian GNU/Linux.
#
#
# This is the main Samba configuration file. You should read the
# smb.conf(5) manual page in order to understand the options listed
# here. Samba has a huge number of configurable options most of which
# are not shown in this example
#
# Some options that are often worth tuning have been included as
# commented-out examples in this file.
#  - When such options are commented with ";", the proposed setting
#    differs from the default Samba behaviour
#  - When commented with "#", the proposed setting is the default
#    behaviour of Samba but the option is considered important
#    enough to be mentioned here
#
# NOTE: Whenever you modify this file you should run the command
# "testparm" to check that you have not made any basic syntactic
# errors.
# A well-established practice is to name the original file
# "smb.conf.master" and create the "real" config file with
# testparm -s smb.conf.master >smb.conf
# This minimizes the size of the really used smb.conf file
# which, according to the Samba Team, impacts performance
# However, use this with caution if your smb.conf file contains nested
# "include" statements. See Debian bug #483187 for a case
# where using a master file is not a good idea.
#

#======================= Global Settings =======================

[global]

## Browsing/Identification ###

# Change this to the workgroup/NT-domain name your Samba server will part of
   workgroup = WORKGROUP

# server string is the equivalent of the NT Description field
   server string = %h server

# Windows Internet Name Serving Support Section:
# WINS Support - Tells the NMBD component of Samba to enable its WINS Server
#   wins support = no

# WINS Server - Tells the NMBD components of Samba to be a WINS Client
# Note: Samba can be either a WINS Server, or a WINS Client, but NOT both
;   wins server = w.x.y.z

# This will prevent nmbd to search for NetBIOS names through DNS.
   dns proxy = no

# What naming service and in what order should we use to resolve host names
# to IP addresses
;   name resolve order = lmhosts host wins bcast


#### Networking ####

# The specific set of interfaces / networks to bind to
# This can be either the interface name or an IP address/netmask;
# interface names are normally preferred
;   interfaces = 127.0.0.0/8 eth0

vfs objects = recycle aio_pthread

aio read size = 1
aio write size = 1

strict locking = No

use sendfile = no
# https://github.com/zfsonlinux/zfs/issues/1156

server multi channel support = yes

# Only bind to the named interfaces and/or networks; you must use the
# 'interfaces' option above to use this.
# It is recommended that you enable this feature if your Samba machine is
# not protected by a firewall or is a firewall itself.  However, this
# option cannot handle dynamic or non-broadcast interfaces correctly.
;   bind interfaces only = yes


recycle:repository = .recyclebin
recycle:keeptree = yes
recycle:versions = yes
recycle:touch = yes
recycle:touch_mtime = yes


#### Debugging/Accounting ####

# This tells Samba to use a separate log file for each machine
# that connects
   log file = /var/log/samba/log.%m

# Cap the size of the individual log files (in KiB).
#   max log size = 1000

# If you want Samba to only log through syslog then set the following
# parameter to 'yes'.
   syslog only = yes

# We want Samba to log a minimum amount of information to syslog. Everything
# should go to /var/log/samba/log.{smbd,nmbd} instead. If you want to log
# through syslog you should set the following parameter to something higher.
   syslog = 3

# Do something sensible when Samba crashes: mail the admin a backtrace
   panic action = /usr/share/samba/panic-action %d

####### Authentication #######

# "security = user" is always a good idea. This will require a Unix account
# in this server for every user accessing the server. See
# /usr/share/doc/samba-doc/htmldocs/Samba3-HOWTO/ServerType.html
# in the samba-doc package for details.
#   security = user

# You may wish to use password encryption.  See the section on
# 'encrypt passwords' in the smb.conf(5) manpage before enabling.
   encrypt passwords = true

# If you are using encrypted passwords, Samba will need to know what
# password database type you are using.
   passdb backend = tdbsam

   obey pam restrictions = yes

# This boolean parameter controls whether Samba attempts to sync the Unix
# password with the SMB password when the encrypted SMB password in the
# passdb is changed.
   unix password sync = yes

# For Unix password sync to work on a Debian GNU/Linux system, the following
# parameters must be set (thanks to Ian Kahan <<kahan@informatik.tu-muenchen.de> for
# sending the correct chat script for the passwd program in Debian Sarge).
   passwd program = /usr/bin/passwd %u
   passwd chat = *Enter\snew\s*\spassword:* %n\n *Retype\snew\s*\spassword:* %n\n *password\supdated\ssuccessfully* .

# This boolean controls whether PAM will be used for password changes
# when requested by an SMB client instead of the program listed in
# 'passwd program'. The default is 'no'.
   pam password change = yes

# This option controls how unsuccessful authentication attempts are mapped
# to anonymous connections
   map to guest = bad user

########## Domains ###########

# Is this machine able to authenticate users. Both PDC and BDC
# must have this setting enabled. If you are the BDC you must
# change the 'domain master' setting to no
#
;   domain logons = yes
#
# The following setting only takes effect if 'domain logons' is set
# It specifies the location of the user's profile directory
# from the client point of view)
# The following required a [profiles] share to be setup on the
# samba server (see below)
;   logon path = \\%N\profiles\%U
# Another common choice is storing the profile in the user's home directory
# (this is Samba's default)
#   logon path = \\%N\%U\profile

# The following setting only takes effect if 'domain logons' is set
# It specifies the location of a user's home directory (from the client
# point of view)
;   logon drive = H:
#   logon home = \\%N\%U

# The following setting only takes effect if 'domain logons' is set
# It specifies the script to run during logon. The script must be stored
# in the [netlogon] share
# NOTE: Must be store in 'DOS' file format convention
;   logon script = logon.cmd
# This allows machine accounts to be created on the domain controller via the
# SAMR RPC pipe.
# The following assumes a "machines" group exists on the system
; add machine script  = /usr/sbin/useradd -g machines -c "%u machine account" -d /var/lib/samba -s /bin/false %u

# This allows Unix groups to be created on the domain controller via the SAMR
# RPC pipe.
; add group script = /usr/sbin/addgroup --force-badname %g

########## Printing ##########

# If you want to automatically load your printer list rather
# than setting them up individually then you'll need this
#   load printers = yes

# lpr(ng) printing. You may wish to override the location of the
# printcap file
;   printing = bsd
;   printcap name = /etc/printcap

# CUPS printing.  See also the cupsaddsmb(8) manpage in the
# cupsys-client package.
;   printing = cups
;   printcap name = cups

############ Misc ############

# Using the following line enables you to customise your configuration
# on a per machine basis. The %m gets replaced with the netbios name
# of the machine that is connecting
;   include = /home/samba/etc/smb.conf.%m

# Most people will find that this option gives better performance.
# See smb.conf(5) and /usr/share/doc/samba-doc/htmldocs/Samba3-HOWTO/speed.html
# for details
# You may want to add the following on a Linux system:
#         SO_RCVBUF=8192 SO_SNDBUF=8192
#   socket options = TCP_NODELAY

# The following parameter is useful only if you have the linpopup package
# installed. The samba maintainer and the linpopup maintainer are
# working to ease installation and configuration of linpopup and samba.
;   message command = /bin/sh -c '/usr/bin/linpopup "%f" "%m" %s; rm %s' &

# Domain Master specifies Samba to be the Domain Master Browser. If this
# machine will be configured as a BDC (a secondary logon server), you
# must set this to 'no'; otherwise, the default behavior is recommended.
#   domain master = auto

# Some defaults for winbind (make sure you're not using the ranges
# for something else.)
;   idmap uid = 10000-20000
;   idmap gid = 10000-20000
;   template shell = /bin/bash

# The following was the default behaviour in sarge,
# but samba upstream reverted the default because it might induce
# performance issues in large organizations.
# See Debian bug #368251 for some of the consequences of *not*
# having this setting and smb.conf(5) for details.
;   winbind enum groups = yes
;   winbind enum users = yes

# Setup usershare options to enable non-root users to share folders
# with the net usershare command.

# Maximum number of usershare. 0 (default) means that usershare is disabled.
;   usershare max shares = 100

# Allow users who've been granted usershare privileges to create
# public shares, not just authenticated ones
   usershare allow guests = yes

#======================= Share Definitions =======================

[homes]
   comment = Home Directories
   browseable = no

# By default, the home directories are exported read-only. Change the
# next parameter to 'no' if you want to be able to write to them.
   read only = yes

# File creation mask is set to 0700 for security reasons. If you want to
# create files with group=rw permissions, set next parameter to 0775.
   create mask = 0700

# Directory creation mask is set to 0700 for security reasons. If you want to
# create dirs. with group=rw permissions, set next parameter to 0775.
   directory mask = 0700

# By default, \\server\username shares can be connected to by anyone
# with access to the samba server.
# The following parameter makes sure that only "username" can connect
# to \\server\username
# This might need tweaking when using external authentication schemes
   valid users = %S

# Un-comment the following and create the netlogon directory for Domain Logons
# (you need to configure Samba to act as a domain controller too.)
;[netlogon]
;   comment = Network Logon Service
;   path = /home/samba/netlogon
;   guest ok = yes
;   read only = yes

# Un-comment the following and create the profiles directory to store
# users profiles (see the "logon path" option above)
# (you need to configure Samba to act as a domain controller too.)
# The path below should be writable by all users so that their
# profile directory may be created the first time they log on
;[profiles]
;   comment = Users profiles
;   path = /home/samba/profiles
;   guest ok = no
;   browseable = no
;   create mask = 0600
;   directory mask = 0700


# A sample share for sharing your CD-ROM with others.
;[cdrom]
;   comment = Samba server's CD-ROM
;   read only = yes
;   locking = no
;   path = /cdrom
;   guest ok = yes

# The next two parameters show how to auto-mount a CD-ROM when the
#       cdrom share is accesed. For this to work /etc/fstab must contain
#       an entry like this:
#
#       /dev/scd0   /cdrom  iso9660 defaults,noauto,ro,user   0 0
#
# The CD-ROM gets unmounted automatically after the connection to the
#
# If you don't want to use auto-mounting/unmounting make sure the CD
#       is mounted on /cdrom
#
;   preexec = /bin/mount /cdrom
;   postexec = /bin/umount /cdrom


[storage]
        comment = Storage
        path = /storage/main/data
        writeable = yes
        public = yes
        guest ok = no
        valid users = cytrinox
        hide unreadable = yes
~~~

# References

[https://www.samba.org/samba/history/samba-4.4.0.html]()

[https://blogs.technet.microsoft.com/josebda/2012/06/28/the-basics-of-smb-multichannel-a-feature-of-windows-server-2012-and-smb-3-0/]()

[https://lists.samba.org/archive/samba/2016-September/202696.html]()
