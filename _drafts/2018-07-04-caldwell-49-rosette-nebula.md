---
layout: deepsky
title: "Caldwell 49 - Rosette Nebula"
deepsky_image: "C49_ROESETTE_NEBULA_191_web.jpg"
tags: [photography,astrophotography]
category: "deepsky"
---

The Rosette Nebula (also known as Caldwell 49) is a large spherical H II region (circular in appearance) located near one end of a giant molecular cloud in the Monoceros region of the Milky Way Galaxy.
The open cluster NGC 2244 (Caldwell 50) is closely associated with the nebulosity, the stars of the cluster having been formed from the nebula's matter.

The cluster and nebula lie at a distance of some 5,000 light-years from Earth) and measure roughly 130 light years in diameter. The radiation from the young stars excites the atoms in the nebula, causing them to emit radiation themselves producing the emission nebula we see. The mass of the nebula is estimated to be around 10,000 solar masses.
(Source: [Wikipedia](https://en.wikipedia.org/wiki/Rosette_Nebula))

|**Right ascension**|06h 33m 45s|
|**Declination**|+04° 59′ 54″|
|**Distance**|5,200 ly|
|**Diameter**|130 ly|
|**Apparent magnitude (V)**|9.0|
|**Constellation**|Monoceros|


### Exposure data

|Count|Exposure|Data|Filter|Nights|
|-|-|-|-|-|
|43x|600s|Hydrogen-alpha|Astronomik 6nm Hα|2019-02-14,2019-02-15|
|35x|600s|Oxygen-III|Astronomik 6nm OIII|2019-02-19|
|26x|600s|Sulphur-II|Astronomik 6nm SII|2019-02-17|

**Total integration:** 17 hours 19 minutes

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