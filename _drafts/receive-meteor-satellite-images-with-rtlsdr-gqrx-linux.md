---
layout: post
title: "Receive METEOR weather satellite images with RTLSDR and Gqrx on Linux"
image: "/images/themes/theme_sdradio.jpg"
tags: [linux, rtlsdr, gqrx, meteorsat, featured]
category: linux
---


# Requirements

You should be able to compile sourcecode from github and installing tools from your distribution.
I use Debian and except of a few special packages, everything is included in Debian Buster.

## Satellites used

There are 3 satellites in orbit:

 * METEOR-M 1 (decommissioned)
 * METEOR-M 2
 * METEOR-M 2-2

## Frequencies used

|Satellite|Frequency|Bandwidth|Data|Symbol rate|Modulation|
|----------|--------|-------|--------|---|---|
|METEOR-M N2|137.1 MHz|140 kHz|LRPT|72000|QPSK|
|METEOR-M N2-2|137.1 MHz|140 kHz|LRPT|80000|OQPSK|

Good online resource with more information (active APIDs, ...) is <http://happysat.nl/Meteor/html/Meteor_Status.html>


<!--more-->

## Hardware used

 * Notebook
 * RTLSDR v3 dongle <https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/](>
 * QFH antenna <http://www.winklerantennenbau.de/qfh_137.htm>
 * RTLSDR Wideband LNA <https://www.rtl-sdr.com/product/rtl-sdr-blog-wideband-lna-bias-tee-powered/>


## Software used

 * rtl_fm
 * gqrx
 * gpredict
 * sox
 * meteor_demod <https://github.com/dbdexter-dev/meteor_demod> (v0.2.1 for M N2 / v0.3 for M N2-2)
 * meteor_decoder <https://github.com/artlav/meteor_decoder>
   * alternative: meteor_decode <https://github.com/dbdexter-dev/meteor_decode>
 * meteor_rectify <https://github.com/dbdexter-dev/meteor_rectify>


# Antenna setup

I've bought a QFH antenna from a manufacturer, but there are lot of DIY tutorials out there.
You may get good results with the RTLSDR bundle V-dipole antenna if it's correctly aligned and
both poles have been shorten to 53.4cm, more information on <https://www.rtl-sdr.com/simple-noaameteor-weather-satellite-antenna-137-mhz-v-dipole/>.

{% include image_caption.html imageurl="/images/posts/gqrx-meteor/qfh_outdoor.jpg" title="QFH antenna" caption="QFH antenna" %}


# Using gpredict for pass prediction

With gpredict you can see at which time and elevation a satellite
pass your location. Edit settings to match your latitude/longitude. Add the METEOR-M 2 and
METEOR-M2 2 satellites to the module and look at the **sky at a glance** window.

{% include image_caption.html imageurl="/images/posts/gqrx-meteor/gpredict_meteor.png" title="Gpredict" caption="Gpredict" %}





# Capture a raw IQ file with Gqrx

The bandwith for METEOR LRPT signals is 140 kHz. Some people recommend to use decimation
to improve the signal quality. I've not tested it but my usual configuration looks like:

{% include image_caption.html imageurl="/images/posts/gqrx-meteor/gqrx_meteor_settings.png" title="Gpredict" caption="Gpredict" %}

I'm using the RTLSDR aplifier which requires Bias-T powering. This can be enabled
with *bias=1*. **Don't use it when you don't have the RTLSDR amplifier!**

Make sure the value for the **channel offset** in tab *Receiver settings* is set to zero.
If not, the IQ recording is not centered at the signal and you won't be able do decode
it.

Gqrx has a builtin IQ recorder. Just press record when you see the satellite signal in
the waterfall diagramm.

{% include image_caption.html imageurl="/images/posts/gqrx-meteor/gqrx_meteor_recording.png" title="Gpredict" caption="Gpredict" %}

## Convert the raw IQ file to a wav file

The raw IQ file format used by Gqrx is a pair of 32 bit floating point values (one for I, one for Q).
With sox, you can convert the raw file to a wav file, encoded by two 16 bit signed integers.
meteor_demod could only read 16 bit signed integer or 8 bit unsigned integer. Without conversion,
meteor_demod couldn't read the file.

~~~
sox -t raw -e floating-point -b 32 -c 2 -r 140000 \
   gqrx_20190908_085103_137100000_140000_fc.raw \
   -t wav -e signed-integer -b 16 -c 2 -r 140000 \
   gqrx_20190908_085103_137100000_140000_fc.wav
~~~


### Alternative: use rtl_fm instead of gqrx

If you don't want to use gqrx or want to automate the process without a GUI, you could
use rtl_fm to sample the data without using a frontend.
~~~
timeout 10m rtl_fm -M raw -s 140000 -f 137.9M \
    -E dc -g 12 -p 1 > gqrx_20190908_085103_137100000_140000_fc.raw
~~~
After 10 minutes, the process terminates. Convert the raw file to a wav file with:

~~~
sox -t raw -esigned-integer -b16 -r 140000 \
    -c 2 "gqrx_20190908_085103_137100000_140000_fc.raw" \
    -t wav gqrx_20190908_085103_137100000_140000_fc.wav
~~~

A use case might be a Rasperry Pi attached to a RTLSDR dongle.


# Demodulate the recording

For demodulation, I use the great tools from Davide Belloli. Get your copy
from [https://github.com/dbdexter-dev/meteor_demod]() and compile it.

~~~
~/sdradio/src/meteor_demod/src/meteor_demod gqrx_20190908_085103_137100000_140000_fc.wav
~~~

{% include image_caption.html imageurl="/images/posts/gqrx-meteor/meteor_demod.png" title="meteor_demod" caption="meteor_demod in action" %}

This command demodulate the recording and produces a symbol file with suffix \*.s This symbol file can be decoded by meteor_decode, another tool from Davide Belloli.

## Differences between M N2 and M N2-2
The current two operating satellites using different modulations (see table in first section).
Depending on the satellite, you have to choose between symbol rate *72000* vs *80000*
and mode *qpsk* vs. *oqpsk*.

The meteor_demod utility has a command line switch **-m** to change the modulation and **-r** to change
the symbol rate.


# Decode the symbol file

Checkout meteor_decoder from Github and compile it. It requires the freepascal compiler, Debian
includes a package for it.
Depending on the satellite, you need to use *differential encoding (-diff)* and *deinterleave* (-int)* for M N2-2.

~~~
~/sdradio/src/meteor_decoder/src/medet LRPT_2019_09_08-13_04.s meteor_capture
~~~
The command outputs some statistics after finished:
~~~
Reading LRPT_2019_09_08-13_04.s...
 pos=95846094 ( 99.97%) ( 3, 9762,49) sig= -253 rs=(-1,-1,-1,-1) 0FFFB813
Total:        102.968010
Processing:   6.723472
Correlation:  21.017412
Viterbi:      70.001213
ECC:          4.982072
Remainder:    0.243836
Packets:      4032 / 5383
Elapsed time: 00:08:28.460
~~~

# Final image

The resulting PNG file could be rectified with meteor_rectify.

~~~
~/sdradio/src/meteor_rectify/rectify.py meteor_capture.bmp
Opened 1568x3672 image
Spawning process  1
Spawning process  2
Spawning process  3
Spawning process  4
Spawning process  5
Spawning process  6
Spawning process  7
Spawning process  8
Writing rectified image to meteor_capture-rectified.png
~~~

{% include image_caption.html imageurl="/images/posts/gqrx-meteor/meteor-rectified.jpg" title="METEOR M2 weather image" caption="METEOR M2 wather image" %}