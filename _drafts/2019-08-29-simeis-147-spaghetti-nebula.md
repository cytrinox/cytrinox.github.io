---
layout: deepsky
title: "Simeis 147 - Spaghetti Nebula"
deepsky_image: "SIMEIS-147_191_web.jpg"
tags: [photography,astrophotography]
category: "deepsky"
---


Simeis 147, also known as the Spaghetti Nebula, SNR G180.0-01.7 or Sharpless 2-240, is a supernova remnant (SNR) in the Milky Way, straddling the border between the constellations Auriga and Taurus. Discovered in 1952 at the Crimean Astrophysical Observatory using a 25-inch Schmidt-Cassegrain telescope, it is difficult to observe due to its extremely low brightness.

The nebulous area is fairly large with an almost spherical shell and filamentary structure. The remnant has an apparent diameter of approximately 3 degrees, an estimated distance of approximately 3000 (±350) light-years, and an age of approximately 40,000 years.

It is believed that after its stellar explosion a rapidly spinning neutron star known as pulsar PSR J0538+2817 was left behind in the nebula core, emitting a strong radio signal.
(Source: [Wikipedia](https://en.wikipedia.org/wiki/Simeis_147))


|**Right ascension**|05h 39m 06s|
|**Declination**|+27° 59′ 55″|
|**Distance**|3,000 ly|
|**Constellation**|Taurus|

### Exposure data

|Count|Exposure|Data|Filter|Nights|
|-|-|-|-|-|
|57x|720s|Hydrogen-alpha|Astronomik 6nm Hα|2019-02-24, 2019-02-25|
|18x|720s|Oxygen-III|Astronomik 6nm OIII|2019-02-26|

**Total integration:** 15 hours

### Instrument and equipment

* Canon EF 200mm f/2.8L at f/3.5
* Skywatcher H-EQ5
* Canon EOS 1300Da
* Lacerta M-Gen Autoguider
* Astronomik Hα, OIII, SII filters
* TS-Optics 60mm Guide tube

### Location

* Balcony observatory, Germany, BW
* Bortle 4

### Used software

* APT + Stellarium for camera control
* EQMod for telescope control
* PixInsight for image processing
* Photoshop for final touch

<!--
# PixInsight processing workflow:

* Calibration, Weighting (SFS), Integration
* DrizzleIntegration (2x)
* DBE for HA, OIII, SII masters
* Ha+OIII LinearFit against SII
* PixelMath for RGB (R=HA, G=SII*0.8+OIII*0.2, B=OIII*0.8+SII*0.2)
* RGBWorkingSpace
* ABE
* BackgroundNeutralization
* ColorCalibration
* TGVDenoise
* MMT
* Deconvolution
* ArcsinhStretch
* HT + CT for color and contrast improvance
* ACDNR
* MT for star shrink
* LHE for more contrast
* UnsharpMask
-->