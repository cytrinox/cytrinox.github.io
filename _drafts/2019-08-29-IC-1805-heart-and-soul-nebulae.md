---
layout: deepsky
title: "IC 1805 - Heart and Soul Nebulae"
image: "/images/deepsky/IC1805_HEART_AND_SOUL_NEBULAE_181_web.jpg"
tags: [photography,astrophotography]
category: "deepsky"
---

The Heart Nebula, IC 1805, Sharpless 2-190, lies some 7500 light years away from Earth and is located in the Perseus Arm of the Galaxy in the constellation Cassiopeia. It was discovered by William Herschel on 3 November 1787. This is an emission nebula showing glowing ionized hydrogen gas and darker dust lanes.

The very brightest part of this nebula (the knot at the western edge) is separately classified as NGC 896, because it was the first part of this nebula to be discovered.

Westerhout 5 (Sharpless 2-199, LBN 667, Soul Nebula) is an emission nebula and the
 eastern neighbor of IC1805 (Heart Nebula) and the two are often mentioned together as the "Heart and Soul".
(Source: [Wikipedia](https://en.wikipedia.org/wiki/Heart_Nebula))


|**Right ascension**|02h 33m 22s|
|**Declination**|+61° 26′ 36″|
|**Distance**|7,500 ly|
|**Diameter**|330 ly|
|**Apparent magnitude (V)**|18.3|
|**Constellation**|Cassiopeia|




### Exposure data

|Count|Exposure|Data|Filter|Nights|
|-|-|-|-|-|
|80x|600s|Hydrogen-alpha|Astronomik 6nm Hα|2018-11-16, 2018-11-17|
|42x|600s|Oxygen-III|Astronomik 6nm OIII|2019-02-13|
|42x|600s|Sulphur-II|Astronomik 6nm SII|2019-02-05, 2019-02-06|

**Total integration:** 27 hours 19 minutes

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