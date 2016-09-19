---
layout: post
title: "Rescan PCI for new virtio devices"
banner_image: theme_storage.jpg
tags: [linux, kvm]
category: linux
---

I want to extend a running KVM Linux guest system with a physical hard drive. I've connected the new disk via

> virsh attach-disk my_vm /dev/sdf vdc

to connect sdf to vdc, but inside the guest, nothing happens.

The solution is simple: attaching a new disk requires a new virtio block controller which is a PCI device. The trick is to rescan the PCI bus system to detect the new controller:

> echo 1 > /sys/bus/pci/rescan

Now lspci shows the new controller and dmesg shows the new vdc block device.

> 00:08.0 SCSI storage controller: Red Hat, Inc Virtio block device

## Update:

Simply load the both modules

>    acpiphp
>    pci_hotplug

then you don't need to rescan the PCI bus.
