---
layout: post
title: "Passtrough GMC Z216C USB IR Adapter into Linux Wine for MetraWin"
image: "/images/themes/theme_storage.jpg"
tags: [linux, debian]
category: linux
---

To read out my Gossen Metrawatt Energy multimeter, I've bought the Z216C adapter cable.
Unfortunatly, this adapter is not yet supported by Linux kernel (see patch).
After adding support to Linux, I found out that GMC MetraWin was not able to discover
the COM adapter. There are more then 11 ways to discover COM ports in Windows by APIs, so I
had to isolate which one MetraWin uses.

The API is called SetupAPI and is implemented in Wine, but requires some registry keys that
are not automatically added by Wine:

````
[Software\\Wine\\Ports] 1707756530
#time=1da5dd35ae216cc
"COM1"="/dev/ttyUSB0"

[System\\CurrentControlSet\\Enum\\SERIAL\\COM1\\COM1] 1707757101
#time=1da5dd4af67ff44
"Class"="Ports"
"ClassGUID"="{4D36E978-E325-11CE-BFC1-08002BE10318}"
"DeviceDesc"="Serial Ports"
"FriendlyName"="Serial Port (COM1)"

[System\\CurrentControlSet\\Enum\\SERIAL\\COM1\\COM1\\Device Parameters] 1707757101
#time=1da5dd4af67fd6e
"PortName"="COM1"

````

Usually this is automatically added by Wine:
````
[Hardware\\Devicemap\\Serialcomm] 1708101636
#time=1da60f6de5e729a
"\\Device\\Serial0"="COM1"
"\\Device\\Serial1"="COM2"
"\\Device\\Serial2"="COM3"
"\\Device\\Serial3"="COM4"
"\\Device\\Serial4"="COM5"
"\\Device\\Serial5"="COM6"
"\\Device\\Serial6"="COM7"
````

Once this keys and values are added, MetraWin was able to discover the USB COM port as device.


## Linux kernel patch


You need the patch for Linux kernel I've submitted to [linux-usb mailing list](https://marc.info/?l=linux-usb&m=170766296905559&w=2).

````
---
 drivers/usb/serial/ftdi_sio.c     | 2 ++
 drivers/usb/serial/ftdi_sio_ids.h | 6 ++++++
 2 files changed, 8 insertions(+)

diff --git a/drivers/usb/serial/ftdi_sio.c b/drivers/usb/serial/ftdi_sio.c
index 13a56783830d..22d01a0f10fb 100644
--- a/drivers/usb/serial/ftdi_sio.c
+++ b/drivers/usb/serial/ftdi_sio.c
@@ -1077,6 +1077,8 @@ static const struct usb_device_id id_table_combined[] = {
 		.driver_info = (kernel_ulong_t)&ftdi_jtag_quirk },
 	{ USB_DEVICE(FTDI_VID, FTDI_FALCONIA_JTAG_UNBUF_PID),
 		.driver_info = (kernel_ulong_t)&ftdi_jtag_quirk },
+	/* GMC devices */
+	{ USB_DEVICE(GMC_VID, GMC_Z216C_PID) },
 	{ }					/* Terminating entry */
 };

diff --git a/drivers/usb/serial/ftdi_sio_ids.h b/drivers/usb/serial/ftdi_sio_ids.h
index 21a2b5a25fc0..5ee60ba2a73c 100644
--- a/drivers/usb/serial/ftdi_sio_ids.h
+++ b/drivers/usb/serial/ftdi_sio_ids.h
@@ -1606,3 +1606,9 @@
 #define UBLOX_VID			0x1546
 #define UBLOX_C099F9P_ZED_PID		0x0502
 #define UBLOX_C099F9P_ODIN_PID		0x0503
+
+/*
+ * GMC devices
+ */
+#define GMC_VID				0x1cd7
+#define GMC_Z216C_PID			0x0217 /* GMC Z216C Adapter IR-USB */
--
2.39.2
````