---
layout: post
title: "Fan control on C2750D4I/C2550D4I Asrock boards"
banner_image: theme_fan2.jpg
tags: [linux, hacking, debian]
category: linux
---

The Asrock **C2750D4I** and **C2550D4I** boards provides multiple 4-pin PWM connectors. PWM configuration is available in the BIOS hardware monitoring
section, but you can not change any parameters through the hwmon interface in `/sys/class/hwmon`. Asrock uses a Nuvoton chip (nct6776 compatible) for monitoring
hardware sensors but the fans are not connected to this chip. Instead, they are handled by the onboard BMC.

You can get the current state of the sensors with `impi-sensors`:

<!--more-->

```
root@mz4:~# ipmi-sensors
ID | Name            | Type        | Reading    | Units | Event
3  | ATX+5VSB        | Voltage     | 5.07       | V     | 'OK'
4  | +3VSB           | Voltage     | 3.48       | V     | 'OK'
5  | Vcore           | Voltage     | 0.91       | V     | 'OK'
6  | VCCM            | Voltage     | 1.35       | V     | 'OK'
7  | +1.1            | Voltage     | 1.08       | V     | 'OK'
8  | +1.0            | Voltage     | 1.02       | V     | 'OK'
9  | BAT             | Voltage     | 3.28       | V     | 'OK'
10 | +3V             | Voltage     | 3.36       | V     | 'OK'
11 | +5V             | Voltage     | 5.01       | V     | 'OK'
12 | +12V            | Voltage     | 12.30      | V     | 'OK'
13 | CPU_FAN1        | Fan         | 1100.00    | RPM   | 'OK'
14 | REAR_FAN1       | Fan         | 1100.00    | RPM   | 'OK'
15 | FRNT_FAN1       | Fan         | N/A        | RPM   | N/A
16 | FRNT_FAN2       | Fan         | N/A        | RPM   | N/A
17 | REAR_FAN2       | Fan         | 1300.00    | RPM   | 'OK'
18 | CPU_FAN2        | Fan         | N/A        | RPM   | N/A
19 | MB Temperature  | Temperature | 44.00      | C     | 'OK'
20 | CPU Temperature | Temperature | 29.00      | C     | 'OK'
```

The 4-pin connectors on these two board models can't handle a 3-pin fan. A 3-pin fan would always run with full-speed.
But if a 4-pin PWM fan is connected, you can control the fan speed with a **ipmi raw** command.

> ipmitool raw 0x3a 0x01 AA BB CC DD EE FF 0x00 0x00

Each block must be replaced with the requested fan control value.

| AA: | CPU_FAN1        |
| BB: | CPU_FAN2        |
| CC: | REAR_FAN1       |
| DD: | REAR_FAN2       |
| EE: | FRNT_FAN1       |
| FF: | FRNT_FAN2       |

The control value is one of the following:

| 0x00 | Smart fan (Duty cycle setting from BIOS) |
| 0x04 | min. RPM value                           |
| .... | increase RPM value                       |
| 0x64 | max. RPM value                           |

# Example

To set *CPU Fan 1* to full speed, *Rear 1* and *Front 1* to average speed and *Rear 2* and *Front 2* to low speed:

> ipmitool raw 0x3a 0x01 0x64 0x00 0x32 0x0A 0x32 0x0A 0x00 0x00

# Permanent configuration

After a reboot, the BIOS configuration is restored. To make these changes permanent, add the ipmitool command
in `/etc/rc.local`.

# Fan performance

I've replaced my old three 3-pin fans with three 4-pin PWM fans at 5 pm and the Netdata monitoring reveals an overall temperature decrease of approximately 7°C.

{% include image_caption.html imageurl="/images/posts/2016-09-19-sc-temperature.png" title="Netdata sensors" caption="Netdata sensors" %}
