---
redirect_from:
  - "08-02-creating-a-mask"
interact_link: content/08-02-Creating-a-mask.ipynb
kernel_name: python3
has_widgets: false
title: 'Identifying bad pixels with ccdmask'
prev_page:
  url: /08-01-Identifying-hot-pixels
  title: 'Identifying hot pixels'
next_page:
  url: /08-03-Cosmic-ray-removal
  title: 'Removing cosmic rays'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---

# Creating an image mask

Calibration cannot compensate for every defect in a CCD. Some examples (a
non-exhaustive list):

+ Some hot pixels are not actually linear with exposure time.
+ Some pixels in the CCD may respond less to light than others in a way that
flat frames cannot compensate for.
+ There may be defects in all or part of a row or column of the chip.
+ Cosmic rays strike the CCD during every exposure. While those are eliminated
in the combined calibrated frames with the proper choice of combination
parameters, they are not removed from science images.

The first three are discussed in this notebook. Removal of cosmic rays from
science images is discussed [in the cosmic ray notebook]()



{:.input_area}
```python
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt

from astropy import units as u
from astropy.nddata import CCDData

import ccdproc as ccdp
from photutils import detect_sources
from astrowidgets import ImageWidget

from convenience_functions import show_image, image_snippet
```




{:.input_area}
```python
# Use custom style for larger fonts and figures
plt.style.use('guide.mplstyle')
```


## Detecting bad pixels with `ccdmask`

The ccdproc function [ccdmask](https://ccdproc.readthedocs.io/en/latest/api/ccdproc.ccdmask.html#ccdproc.ccdmask) uses an method that is
based on the [IRAF task ccdmask](http://stsdas.stsci.edu/cgi-bin/gethelp.cgi?ccdmask). The method works best when the
input image used to detect flaws in the CCD is the ratio of two flat frames with
different counts. That may or may not be available depending on what images are
collected.

In the example below, which uses images from Example 2 in the reduction
notebooks, the two extreme exposure times are 1 sec and 1.2 sec, but the average
counts in the images differ by 10,000. These were twilight flats taken just
after sunset.

Even with dome flats where the illumination is supposed to be constant the
counts may actually vary. If they do not, use a single flat for identifying bad
pixels instead of a ratio.

We begin by creating an image collection and then the information for all of the
calibrated, uncombined, flat images.



{:.input_area}
```python
ex2_path = Path('example2-reduced')

ifc = ccdp.ImageFileCollection(ex2_path)

for long_values in ['history', 'comment']:
    try:
        ifc.summary.remove_column(long_values)
    except KeyError:
        # These two columns were not present, so removing them failed.
        # Just keep going.
        pass
```




{:.input_area}
```python
flats = (ifc.summary['imagetyp'] == 'FLAT') & (ifc.summary['combined'] != True)
ifc.summary[flats]
```





<div markdown="0" class="output output_html">
<i>Table masked=True length=10</i>
<table id="table81956507720" class="table-striped table-bordered table-condensed">
<thead><tr><th>file</th><th>simple</th><th>bitpix</th><th>naxis</th><th>naxis1</th><th>naxis2</th><th>date-obs</th><th>exptime</th><th>exposure</th><th>set-temp</th><th>ccd-temp</th><th>xpixsz</th><th>ypixsz</th><th>xbinning</th><th>ybinning</th><th>xorgsubf</th><th>yorgsubf</th><th>readoutm</th><th>filter</th><th>imagetyp</th><th>focallen</th><th>aptdia</th><th>aptarea</th><th>swcreate</th><th>swserial</th><th>sitelat</th><th>sitelong</th><th>telescop</th><th>instrume</th><th>notes</th><th>flipstat</th><th>swowner</th><th>date</th><th>time-obs</th><th>ut</th><th>timesys</th><th>radecsys</th><th>purged</th><th>latitude</th><th>longitud</th><th>altitude</th><th>lst</th><th>jd-obs</th><th>mjd-obs</th><th>biassec</th><th>trimsec</th><th>bunit</th><th>trim_image</th><th>trimim</th><th>subtract_dark</th><th>subdark</th><th>cstretch</th><th>cblack</th><th>cwhite</th><th>pedestal</th><th>bscale</th><th>bzero</th><th>subtract_bias</th><th>subbias</th><th>combined</th><th>hjd-obs</th><th>bjd-obs</th><th>azimuth</th><th>ha</th><th>readmode</th><th>st</th><th>lat-obs</th><th>long-obs</th><th>alt-obs</th><th>observat</th><th>ra</th><th>objctra</th><th>dec</th><th>objctdec</th><th>fwhm</th><th>zmag</th><th>_quinox</th><th>epoch</th><th>pa</th><th>_type1</th><th>_rval1</th><th>_rpix1</th><th>_delt1</th><th>_rota1</th><th>_type2</th><th>_rval2</th><th>_rpix2</th><th>_delt2</th><th>_rota2</th><th>_d1_1</th><th>_d1_2</th><th>_d2_1</th><th>_d2_2</th><th>tr1_0</th><th>tr1_1</th><th>tr1_2</th><th>tr1_3</th><th>tr1_4</th><th>tr1_5</th><th>tr1_6</th><th>tr1_7</th><th>tr1_8</th><th>tr1_9</th><th>tr1_10</th><th>tr1_11</th><th>tr1_12</th><th>tr1_13</th><th>tr1_14</th><th>tr2_0</th><th>tr2_1</th><th>tr2_2</th><th>tr2_3</th><th>tr2_4</th><th>tr2_5</th><th>tr2_6</th><th>tr2_7</th><th>tr2_8</th><th>tr2_9</th><th>tr2_10</th><th>tr2_11</th><th>tr2_12</th><th>tr2_13</th><th>tr2_14</th><th>pltsolvd</th><th>airmass</th><th>secz</th><th>alt-obj</th><th>az-obj</th><th>object</th><th>cd1_1</th><th>cd1_2</th><th>cd2_1</th><th>cd2_2</th><th>a_0_0</th><th>a_0_1</th><th>a_1_0</th><th>b_0_0</th><th>b_0_1</th><th>b_1_0</th><th>_ate</th><th>flat_correct</th><th>flatcor</th><th>wcsaxes</th><th>crpix1</th><th>crpix2</th><th>pc1_1</th><th>pc1_2</th><th>pc2_1</th><th>pc2_2</th><th>cdelt1</th><th>cdelt2</th><th>cunit1</th><th>cunit2</th><th>ctype1</th><th>ctype2</th><th>crval1</th><th>crval2</th><th>lonpole</th><th>latpole</th><th>radesys</th><th>equinox</th><th>a_order</th><th>a_0_2</th><th>a_1_1</th><th>a_2_0</th><th>b_order</th><th>b_0_2</th><th>b_1_1</th><th>b_2_0</th><th>ap_order</th><th>ap_0_0</th><th>ap_0_1</th><th>ap_0_2</th><th>ap_1_0</th><th>ap_1_1</th><th>ap_2_0</th><th>bp_order</th><th>bp_0_0</th><th>bp_0_1</th><th>bp_0_2</th><th>bp_1_0</th><th>bp_1_1</th><th>bp_2_0</th></tr></thead>
<thead><tr><th>str35</th><th>bool</th><th>int64</th><th>int64</th><th>int64</th><th>int64</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>str9</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th></tr></thead>
<tr><td>AutoFlat-PANoRot-r-Bin1-001.fit</td><td>True</td><td>-64</td><td>2</td><td>4096</td><td>4096</td><td>2018-08-23T01:25:17</td><td>1.0</td><td>1.0</td><td>-20.0</td><td>-20.0225025</td><td>9.0</td><td>9.0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>Monochrome</td><td>r</td><td>FLAT</td><td>3200.0</td><td>400.0</td><td>125663.70964050293</td><td>MaxIm DL Version 6.18 190601 00KPP</td><td>00KPP-F3HN8-9JMTJ-1CE5W-A4AX5-F3</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td></td><td>AspenCG16</td><td></td><td></td><td>Matt Craig</td><td>23/08/18</td><td>01:25:17</td><td>01:25:17</td><td>UTC</td><td>FK5</td><td>True</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td>311.7999999995668</td><td>17:04:39.2507</td><td>2458353.559224537</td><td>58353.05922453704</td><td>[4096:4109]</td><td>[1:4096, :]</td><td>adu</td><td>trimim</td><td>ccd=&lt;CCDData&gt;</td><td>subdark</td><td>ccd=&lt;CCDData&gt;, master=&lt;CCDData&gt;, exposure_time=exptime, exposure_unit=s, scale=True</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td></tr>
<tr><td>AutoFlat-PANoRot-r-Bin1-002.fit</td><td>True</td><td>-64</td><td>2</td><td>4096</td><td>4096</td><td>2018-08-23T01:25:43</td><td>1.0</td><td>1.0</td><td>-20.0</td><td>-20.041362000000003</td><td>9.0</td><td>9.0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>Monochrome</td><td>r</td><td>FLAT</td><td>3200.0</td><td>400.0</td><td>125663.70964050293</td><td>MaxIm DL Version 6.18 190601 00KPP</td><td>00KPP-F3HN8-9JMTJ-1CE5W-A4AX5-F3</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td></td><td>AspenCG16</td><td></td><td></td><td>Matt Craig</td><td>23/08/18</td><td>01:25:43</td><td>01:25:43</td><td>UTC</td><td>FK5</td><td>True</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td>311.7999999995668</td><td>17:05:05.3219</td><td>2458353.559525463</td><td>58353.05952546297</td><td>[4096:4109]</td><td>[1:4096, :]</td><td>adu</td><td>trimim</td><td>ccd=&lt;CCDData&gt;</td><td>subdark</td><td>ccd=&lt;CCDData&gt;, master=&lt;CCDData&gt;, exposure_time=exptime, exposure_unit=s, scale=True</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td></tr>
<tr><td>AutoFlat-PANoRot-r-Bin1-003.fit</td><td>True</td><td>-64</td><td>2</td><td>4096</td><td>4096</td><td>2018-08-23T01:26:08</td><td>1.0</td><td>1.0</td><td>-20.0</td><td>-20.041362000000003</td><td>9.0</td><td>9.0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>Monochrome</td><td>r</td><td>FLAT</td><td>3200.0</td><td>400.0</td><td>125663.70964050293</td><td>MaxIm DL Version 6.18 190601 00KPP</td><td>00KPP-F3HN8-9JMTJ-1CE5W-A4AX5-F3</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td></td><td>AspenCG16</td><td></td><td></td><td>Matt Craig</td><td>23/08/18</td><td>01:26:08</td><td>01:26:08</td><td>UTC</td><td>FK5</td><td>True</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td>311.7999999995668</td><td>17:05:30.3903</td><td>2458353.559814815</td><td>58353.05981481481</td><td>[4096:4109]</td><td>[1:4096, :]</td><td>adu</td><td>trimim</td><td>ccd=&lt;CCDData&gt;</td><td>subdark</td><td>ccd=&lt;CCDData&gt;, master=&lt;CCDData&gt;, exposure_time=exptime, exposure_unit=s, scale=True</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td></tr>
<tr><td>AutoFlat-PANoRot-r-Bin1-004.fit</td><td>True</td><td>-64</td><td>2</td><td>4096</td><td>4096</td><td>2018-08-23T01:26:34</td><td>1.0</td><td>1.0</td><td>-20.0</td><td>-20.06965125</td><td>9.0</td><td>9.0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>Monochrome</td><td>r</td><td>FLAT</td><td>3200.0</td><td>400.0</td><td>125663.70964050293</td><td>MaxIm DL Version 6.18 190601 00KPP</td><td>00KPP-F3HN8-9JMTJ-1CE5W-A4AX5-F3</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td></td><td>AspenCG16</td><td></td><td></td><td>Matt Craig</td><td>23/08/18</td><td>01:26:34</td><td>01:26:34</td><td>UTC</td><td>FK5</td><td>True</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td>311.7999999995668</td><td>17:05:56.4615</td><td>2458353.560115741</td><td>58353.06011574074</td><td>[4096:4109]</td><td>[1:4096, :]</td><td>adu</td><td>trimim</td><td>ccd=&lt;CCDData&gt;</td><td>subdark</td><td>ccd=&lt;CCDData&gt;, master=&lt;CCDData&gt;, exposure_time=exptime, exposure_unit=s, scale=True</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td></tr>
<tr><td>AutoFlat-PANoRot-r-Bin1-005.fit</td><td>True</td><td>-64</td><td>2</td><td>4096</td><td>4096</td><td>2018-08-23T01:27:00</td><td>1.0</td><td>1.0</td><td>-20.0</td><td>-20.0602215</td><td>9.0</td><td>9.0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>Monochrome</td><td>r</td><td>FLAT</td><td>3200.0</td><td>400.0</td><td>125663.70964050293</td><td>MaxIm DL Version 6.18 190601 00KPP</td><td>00KPP-F3HN8-9JMTJ-1CE5W-A4AX5-F3</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td></td><td>AspenCG16</td><td></td><td></td><td>Matt Craig</td><td>23/08/18</td><td>01:27:00</td><td>01:27:00</td><td>UTC</td><td>FK5</td><td>True</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td>311.7999999995668</td><td>17:06:22.5327</td><td>2458353.560416667</td><td>58353.06041666667</td><td>[4096:4109]</td><td>[1:4096, :]</td><td>adu</td><td>trimim</td><td>ccd=&lt;CCDData&gt;</td><td>subdark</td><td>ccd=&lt;CCDData&gt;, master=&lt;CCDData&gt;, exposure_time=exptime, exposure_unit=s, scale=True</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td></tr>
<tr><td>AutoFlat-PANoRot-r-Bin1-006.fit</td><td>True</td><td>-64</td><td>2</td><td>4096</td><td>4096</td><td>2018-08-23T01:27:25</td><td>1.02</td><td>1.02</td><td>-20.0</td><td>-20.066508000000002</td><td>9.0</td><td>9.0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>Monochrome</td><td>r</td><td>FLAT</td><td>3200.0</td><td>400.0</td><td>125663.70964050293</td><td>MaxIm DL Version 6.18 190601 00KPP</td><td>00KPP-F3HN8-9JMTJ-1CE5W-A4AX5-F3</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td></td><td>AspenCG16</td><td></td><td></td><td>Matt Craig</td><td>23/08/18</td><td>01:27:25</td><td>01:27:25</td><td>UTC</td><td>FK5</td><td>True</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td>311.7999999995668</td><td>17:06:47.6012</td><td>2458353.560706018</td><td>58353.06070601852</td><td>[4096:4109]</td><td>[1:4096, :]</td><td>adu</td><td>trimim</td><td>ccd=&lt;CCDData&gt;</td><td>subdark</td><td>ccd=&lt;CCDData&gt;, master=&lt;CCDData&gt;, exposure_time=exptime, exposure_unit=s, scale=True</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td></tr>
<tr><td>AutoFlat-PANoRot-r-Bin1-007.fit</td><td>True</td><td>-64</td><td>2</td><td>4096</td><td>4096</td><td>2018-08-23T01:27:51</td><td>1.06</td><td>1.06</td><td>-20.0</td><td>-20.053935000000003</td><td>9.0</td><td>9.0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>Monochrome</td><td>r</td><td>FLAT</td><td>3200.0</td><td>400.0</td><td>125663.70964050293</td><td>MaxIm DL Version 6.18 190601 00KPP</td><td>00KPP-F3HN8-9JMTJ-1CE5W-A4AX5-F3</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td></td><td>AspenCG16</td><td></td><td></td><td>Matt Craig</td><td>23/08/18</td><td>01:27:51</td><td>01:27:51</td><td>UTC</td><td>FK5</td><td>True</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td>311.7999999995668</td><td>17:07:13.6723</td><td>2458353.561006945</td><td>58353.06100694444</td><td>[4096:4109]</td><td>[1:4096, :]</td><td>adu</td><td>trimim</td><td>ccd=&lt;CCDData&gt;</td><td>subdark</td><td>ccd=&lt;CCDData&gt;, master=&lt;CCDData&gt;, exposure_time=exptime, exposure_unit=s, scale=True</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td></tr>
<tr><td>AutoFlat-PANoRot-r-Bin1-008.fit</td><td>True</td><td>-64</td><td>2</td><td>4096</td><td>4096</td><td>2018-08-23T01:28:17</td><td>1.11</td><td>1.11</td><td>-20.0</td><td>-20.050791750000002</td><td>9.0</td><td>9.0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>Monochrome</td><td>r</td><td>FLAT</td><td>3200.0</td><td>400.0</td><td>125663.70964050293</td><td>MaxIm DL Version 6.18 190601 00KPP</td><td>00KPP-F3HN8-9JMTJ-1CE5W-A4AX5-F3</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td></td><td>AspenCG16</td><td></td><td></td><td>Matt Craig</td><td>23/08/18</td><td>01:28:17</td><td>01:28:17</td><td>UTC</td><td>FK5</td><td>True</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td>311.7999999995668</td><td>17:07:39.7435</td><td>2458353.56130787</td><td>58353.06130787037</td><td>[4096:4109]</td><td>[1:4096, :]</td><td>adu</td><td>trimim</td><td>ccd=&lt;CCDData&gt;</td><td>subdark</td><td>ccd=&lt;CCDData&gt;, master=&lt;CCDData&gt;, exposure_time=exptime, exposure_unit=s, scale=True</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td></tr>
<tr><td>AutoFlat-PANoRot-r-Bin1-009.fit</td><td>True</td><td>-64</td><td>2</td><td>4096</td><td>4096</td><td>2018-08-23T01:28:42</td><td>1.16</td><td>1.16</td><td>-20.0</td><td>-20.0225025</td><td>9.0</td><td>9.0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>Monochrome</td><td>r</td><td>FLAT</td><td>3200.0</td><td>400.0</td><td>125663.70964050293</td><td>MaxIm DL Version 6.18 190601 00KPP</td><td>00KPP-F3HN8-9JMTJ-1CE5W-A4AX5-F3</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td></td><td>AspenCG16</td><td></td><td></td><td>Matt Craig</td><td>23/08/18</td><td>01:28:42</td><td>01:28:42</td><td>UTC</td><td>FK5</td><td>True</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td>311.7999999995668</td><td>17:08:04.8120</td><td>2458353.561597222</td><td>58353.06159722222</td><td>[4096:4109]</td><td>[1:4096, :]</td><td>adu</td><td>trimim</td><td>ccd=&lt;CCDData&gt;</td><td>subdark</td><td>ccd=&lt;CCDData&gt;, master=&lt;CCDData&gt;, exposure_time=exptime, exposure_unit=s, scale=True</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td></tr>
<tr><td>AutoFlat-PANoRot-r-Bin1-010.fit</td><td>True</td><td>-64</td><td>2</td><td>4096</td><td>4096</td><td>2018-08-23T01:29:08</td><td>1.21</td><td>1.21</td><td>-20.0</td><td>-20.013072750000003</td><td>9.0</td><td>9.0</td><td>1</td><td>1</td><td>0</td><td>0</td><td>Monochrome</td><td>r</td><td>FLAT</td><td>3200.0</td><td>400.0</td><td>125663.70964050293</td><td>MaxIm DL Version 6.18 190601 00KPP</td><td>00KPP-F3HN8-9JMTJ-1CE5W-A4AX5-F3</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td></td><td>AspenCG16</td><td></td><td></td><td>Matt Craig</td><td>23/08/18</td><td>01:29:08</td><td>01:29:08</td><td>UTC</td><td>FK5</td><td>True</td><td>+46:52:00.408</td><td>-96:27:11.8008</td><td>311.7999999995668</td><td>17:08:30.8832</td><td>2458353.561898148</td><td>58353.06189814815</td><td>[4096:4109]</td><td>[1:4096, :]</td><td>adu</td><td>trimim</td><td>ccd=&lt;CCDData&gt;</td><td>subdark</td><td>ccd=&lt;CCDData&gt;, master=&lt;CCDData&gt;, exposure_time=exptime, exposure_unit=s, scale=True</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td><td>--</td></tr>
</table>
</div>



The best we can do here is the ratio of the first and last of the flat images
listed above.



{:.input_area}
```python
first = ifc.summary['file'][flats][0]
last = ifc.summary['file'][flats][-1]
```




{:.input_area}
```python
ccd1 = CCDData.read(ex2_path / first)
ccd2 = CCDData.read(ex2_path / last)
```




{:.input_area}
```python
ratio = ccd2.divide(ccd1)
```


The ratio is roughly 0.85:



{:.input_area}
```python
ratio.data.mean()
```





{:.output .output_data_text}
```
0.8424684815539478
```



Running `ccdmask` takes a little time but only needs to be done once, not once
for each image.



{:.input_area}
```python
%%time
maskr = ccdp.ccdmask(ratio)
```


{:.output .output_stream}
```
CPU times: user 1min 27s, sys: 452 ms, total: 1min 28s
Wall time: 1min 28s

```

The result of `ccdmask` is one where there is a defect and zero where the chip
is good, which matches the format of the mask numpy expects.

The input image and derived mask are shown below



{:.input_area}
```python
fig, axes = plt.subplots(1, 2, figsize=(40, 20))

show_image(ratio, cmap='gray', fig=fig, ax=axes[0], show_colorbar=False)
axes[0].set_title('Ratio of two flats')

show_image(maskr, cmap='gray', fig=fig, ax=axes[1], show_colorbar=False)
axes[1].set_title('Derived mask')
```





{:.output .output_data_text}
```
Text(0.5, 1.0, 'Derived mask')
```




{:.output .output_png}
![png](images/08-02-Creating-a-mask_16_1.png)



Two comments are in order:

+ The "starfish" pattern in the first image is an artifact of the camera
shutter. Ideally, a longer exposure time would be used for the flats to avoid
this.
+ It appear at first glance that there were no pixels masked. The problem is
that the masked regions are very small and, at the scale shown, happen to not be
visible.

Two defects in this CCD are shown below. The first is a small patch of pixels
that are vastly less sensitive than the rest. The second is a column on the left
edge of the CCD. It turns out this column is not actually exposed to light.
`ccdmask` correctly identifies both patches as bad.



{:.input_area}
```python
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

width = 100
center = (3823, 2446)
plot_row = 0

image_snippet(ccd1, center, width=width, fig=fig, axis=axes[plot_row, 0])
axes[plot_row, 0].set_title('Flat, camera defect')

image_snippet(maskr, center, width=width, fig=fig, axis=axes[plot_row, 1], is_mask=True)
axes[plot_row, 1].set_title('Mask, same center')

center = (0, 2048)
plot_row = 1

image_snippet(ccd1, center, width=width, fig=fig, axis=axes[plot_row, 0], percu=99.9, percl=70)
axes[plot_row, 0].set_title('Flat, bad column')

image_snippet(maskr, center, width=width, fig=fig, axis=axes[plot_row, 1], is_mask=True)
axes[plot_row, 1].set_title('Mask, same center')
```





{:.output .output_data_text}
```
Text(0.5, 1.0, 'Mask, same center')
```




{:.output .output_png}
![png](images/08-02-Creating-a-mask_19_1.png)



### Saving the mask

[*Click here to comment on this section on GitHub (opens in new tab).*](https://github.com/mwcraig/ccd-reduction-and-photometry-guide/pull/113/files#diff-3d31a738ada4920a4a4656b218ad63efR266){:target="_blank"}

The mask can be saved in a FITS file as an image. We will see in [the summary
notebook on masking]() how to combine the mask generated here with a mask
generated from the dark current and with a cosmic ray mask for each science
image.



{:.input_area}
```python
mask_as_ccd = CCDData(data=maskr.astype('uint8'), unit=u.dimensionless_unscaled)
mask_as_ccd.header['imagetyp'] = 'flat mask'
mask_as_ccd.write(ex2_path / 'mask_from_ccdmask.fits')
```


## Making the mask with a single flat

The flats we used in Example 1, taken with the Large Format Camera at Palomar,
are dome flats taken with nearly constant illumination. In that case the best we
can do is run `ccdmask` on a single flat image. As we will see, this still
allows the identification of several clearly bad areas of the chip.

First, a look at the calibratted, but not combined, flat images.



{:.input_area}
```python
ex1_path = Path('example1-reduced')

ifc1 = ccdp.ImageFileCollection(ex1_path)

flats = (ifc1.summary['imagetyp'] == 'FLATFIELD') & (ifc1.summary['combined'] != True)
ifc1.summary[flats]
```





<div markdown="0" class="output output_html">
<i>Table masked=True length=6</i>
<table id="table82429485464" class="table-striped table-bordered table-condensed">
<thead><tr><th>file</th><th>simple</th><th>bitpix</th><th>naxis</th><th>naxis1</th><th>naxis2</th><th>date</th><th>origin</th><th>latitude</th><th>longitud</th><th>telescop</th><th>fratio</th><th>instrume</th><th>detector</th><th>frame</th><th>ccdpicno</th><th>object</th><th>imagetyp</th><th>exptime</th><th>darktime</th><th>date-obs</th><th>ut</th><th>jd</th><th>ra</th><th>dec</th><th>equinox</th><th>epoch</th><th>ha</th><th>st</th><th>airmass</th><th>filter</th><th>gain</th><th>secpix1</th><th>secpix2</th><th>ccdbin1</th><th>ccdbin2</th><th>rotangle</th><th>datasec</th><th>ccdsec</th><th>biassec</th><th>loginfo</th><th>chipid</th><th>subtract_overscan</th><th>suboscan</th><th>trim_image</th><th>trimim</th><th>bunit</th><th>subtract_dark</th><th>subdark</th><th>flat_correct</th><th>flatcor</th><th>combined</th></tr></thead>
<thead><tr><th>str27</th><th>bool</th><th>int64</th><th>int64</th><th>int64</th><th>int64</th><th>str10</th><th>str34</th><th>float64</th><th>float64</th><th>str17</th><th>float64</th><th>str3</th><th>str14</th><th>int64</th><th>int64</th><th>str7</th><th>str9</th><th>float64</th><th>float64</th><th>str10</th><th>str12</th><th>float64</th><th>str12</th><th>str12</th><th>float64</th><th>float64</th><th>str12</th><th>str12</th><th>float64</th><th>str2</th><th>float64</th><th>float64</th><th>float64</th><th>int64</th><th>int64</th><th>float64</th><th>str15</th><th>str15</th><th>str18</th><th>str18</th><th>int64</th><th>str8</th><th>str46</th><th>str6</th><th>str13</th><th>str3</th><th>object</th><th>object</th><th>object</th><th>object</th><th>object</th></tr></thead>
<tr><td>flat-ccd.014.0.fits</td><td>True</td><td>-64</td><td>2</td><td>2048</td><td>4128</td><td>2016-01-16</td><td>California Institute of Technology</td><td>33.4</td><td>-116.9</td><td>Hale 5m Telescope</td><td>7.5</td><td>LFC</td><td>SITe SI002 x 6</td><td>14</td><td>14</td><td>flat_g</td><td>FLATFIELD</td><td>70.001</td><td>70.673</td><td>2016-01-16</td><td>04:17:28.00</td><td>2457403.678796</td><td>04:08:58.50</td><td>33:25:12.69</td><td>2000.0</td><td>2000.0</td><td>00:00:04.00</td><td>04:10:04.46</td><td>1.0</td><td>g&apos;</td><td>1.1</td><td>0.182</td><td>0.182</td><td>1</td><td>1</td><td>0.0</td><td>[1:2048,1:4128]</td><td>[1:2048,1:4128]</td><td>[2049:2080,1:4127]</td><td>Status=0x00000000</td><td>0</td><td>suboscan</td><td>ccd=&lt;CCDData&gt;, overscan=&lt;CCDData&gt;, median=True</td><td>trimim</td><td>ccd=&lt;CCDData&gt;</td><td>adu</td><td>subdark</td><td>ccd=&lt;CCDData&gt;, master=&lt;CCDData&gt;, exposure_time=exptime, exposure_unit=s</td><td>--</td><td>--</td><td>--</td></tr>
<tr><td>flat-ccd.015.0.fits</td><td>True</td><td>-64</td><td>2</td><td>2048</td><td>4128</td><td>2016-01-16</td><td>California Institute of Technology</td><td>33.4</td><td>-116.9</td><td>Hale 5m Telescope</td><td>7.5</td><td>LFC</td><td>SITe SI002 x 6</td><td>15</td><td>15</td><td>flat_g</td><td>FLATFIELD</td><td>70.011</td><td>70.683</td><td>2016-01-16</td><td>04:20:35.00</td><td>2457403.680961</td><td>04:12:05.19</td><td>33:25:16.79</td><td>2000.0</td><td>2000.0</td><td>00:00:04.00</td><td>04:13:11.98</td><td>1.0</td><td>g&apos;</td><td>1.1</td><td>0.182</td><td>0.182</td><td>1</td><td>1</td><td>0.0</td><td>[1:2048,1:4128]</td><td>[1:2048,1:4128]</td><td>[2049:2080,1:4127]</td><td>Status=0x00000000</td><td>0</td><td>suboscan</td><td>ccd=&lt;CCDData&gt;, overscan=&lt;CCDData&gt;, median=True</td><td>trimim</td><td>ccd=&lt;CCDData&gt;</td><td>adu</td><td>subdark</td><td>ccd=&lt;CCDData&gt;, master=&lt;CCDData&gt;, exposure_time=exptime, exposure_unit=s</td><td>--</td><td>--</td><td>--</td></tr>
<tr><td>flat-ccd.016.0.fits</td><td>True</td><td>-64</td><td>2</td><td>2048</td><td>4128</td><td>2016-01-16</td><td>California Institute of Technology</td><td>33.4</td><td>-116.9</td><td>Hale 5m Telescope</td><td>7.5</td><td>LFC</td><td>SITe SI002 x 6</td><td>16</td><td>16</td><td>flat_g</td><td>FLATFIELD</td><td>70.001</td><td>70.684</td><td>2016-01-16</td><td>04:23:41.00</td><td>2457403.683113</td><td>04:15:12.00</td><td>33:25:20.79</td><td>2000.0</td><td>2000.0</td><td>00:00:04.00</td><td>04:16:18.49</td><td>1.0</td><td>g&apos;</td><td>1.1</td><td>0.182</td><td>0.182</td><td>1</td><td>1</td><td>0.0</td><td>[1:2048,1:4128]</td><td>[1:2048,1:4128]</td><td>[2049:2080,1:4127]</td><td>Status=0x00000000</td><td>0</td><td>suboscan</td><td>ccd=&lt;CCDData&gt;, overscan=&lt;CCDData&gt;, median=True</td><td>trimim</td><td>ccd=&lt;CCDData&gt;</td><td>adu</td><td>subdark</td><td>ccd=&lt;CCDData&gt;, master=&lt;CCDData&gt;, exposure_time=exptime, exposure_unit=s</td><td>--</td><td>--</td><td>--</td></tr>
<tr><td>flat-ccd.017.0.fits</td><td>True</td><td>-64</td><td>2</td><td>2048</td><td>4128</td><td>2016-01-16</td><td>California Institute of Technology</td><td>33.4</td><td>-116.9</td><td>Hale 5m Telescope</td><td>7.5</td><td>LFC</td><td>SITe SI002 x 6</td><td>17</td><td>17</td><td>flat_i</td><td>FLATFIELD</td><td>7.0</td><td>7.683</td><td>2016-01-16</td><td>04:27:23.00</td><td>2457403.685683</td><td>04:18:54.58</td><td>33:25:25.70</td><td>2000.0</td><td>2000.0</td><td>00:00:04.00</td><td>04:20:01.09</td><td>1.0</td><td>i&apos;</td><td>1.1</td><td>0.182</td><td>0.182</td><td>1</td><td>1</td><td>0.0</td><td>[1:2048,1:4128]</td><td>[1:2048,1:4128]</td><td>[2049:2080,1:4127]</td><td>Status=0x00000000</td><td>0</td><td>suboscan</td><td>ccd=&lt;CCDData&gt;, overscan=&lt;CCDData&gt;, median=True</td><td>trimim</td><td>ccd=&lt;CCDData&gt;</td><td>adu</td><td>subdark</td><td>ccd=&lt;CCDData&gt;, master=&lt;CCDData&gt;, exposure_time=exptime, exposure_unit=s</td><td>--</td><td>--</td><td>--</td></tr>
<tr><td>flat-ccd.018.0.fits</td><td>True</td><td>-64</td><td>2</td><td>2048</td><td>4128</td><td>2016-01-16</td><td>California Institute of Technology</td><td>33.4</td><td>-116.9</td><td>Hale 5m Telescope</td><td>7.5</td><td>LFC</td><td>SITe SI002 x 6</td><td>18</td><td>18</td><td>flat_i</td><td>FLATFIELD</td><td>7.0</td><td>7.672</td><td>2016-01-16</td><td>04:29:26.00</td><td>2457403.687106</td><td>04:20:58.15</td><td>33:25:28.39</td><td>2000.0</td><td>2000.0</td><td>00:00:04.00</td><td>04:22:04.43</td><td>1.0</td><td>i&apos;</td><td>1.1</td><td>0.182</td><td>0.182</td><td>1</td><td>1</td><td>0.0</td><td>[1:2048,1:4128]</td><td>[1:2048,1:4128]</td><td>[2049:2080,1:4127]</td><td>Status=0x00000000</td><td>0</td><td>suboscan</td><td>ccd=&lt;CCDData&gt;, overscan=&lt;CCDData&gt;, median=True</td><td>trimim</td><td>ccd=&lt;CCDData&gt;</td><td>adu</td><td>subdark</td><td>ccd=&lt;CCDData&gt;, master=&lt;CCDData&gt;, exposure_time=exptime, exposure_unit=s</td><td>--</td><td>--</td><td>--</td></tr>
<tr><td>flat-ccd.019.0.fits</td><td>True</td><td>-64</td><td>2</td><td>2048</td><td>4128</td><td>2016-01-16</td><td>California Institute of Technology</td><td>33.4</td><td>-116.9</td><td>Hale 5m Telescope</td><td>7.5</td><td>LFC</td><td>SITe SI002 x 6</td><td>19</td><td>19</td><td>flat_i</td><td>FLATFIELD</td><td>7.0</td><td>7.673</td><td>2016-01-16</td><td>04:31:30.00</td><td>2457403.688542</td><td>04:23:01.65</td><td>33:25:31.20</td><td>2000.0</td><td>2000.0</td><td>00:00:04.00</td><td>04:24:08.77</td><td>1.0</td><td>i&apos;</td><td>1.1</td><td>0.182</td><td>0.182</td><td>1</td><td>1</td><td>0.0</td><td>[1:2048,1:4128]</td><td>[1:2048,1:4128]</td><td>[2049:2080,1:4127]</td><td>Status=0x00000000</td><td>0</td><td>suboscan</td><td>ccd=&lt;CCDData&gt;, overscan=&lt;CCDData&gt;, median=True</td><td>trimim</td><td>ccd=&lt;CCDData&gt;</td><td>adu</td><td>subdark</td><td>ccd=&lt;CCDData&gt;, master=&lt;CCDData&gt;, exposure_time=exptime, exposure_unit=s</td><td>--</td><td>--</td><td>--</td></tr>
</table>
</div>



We can double check that a ratio of flats will not be useful by calculating the
mean counts in each flat image:



{:.input_area}
```python
ccs = []

for c in ifc1.ccds(imagetyp='flatfield', filter="g'"):
    if 'combined' in c.header:
        continue
    print(c.data.mean())
    ccs.append(c)
```


{:.output .output_stream}
```
19906.38951623411
19902.514437929316
19890.652615963663

```

The variation in counts is so small that the ratio of two flats will not be
useful.

Instead, we run `ccdmask` on the first flat. There is nothing special about that
one. The kind of defects that `ccdmask` tries to identify are in the CCD sensor
itself and should be the same for all filters.



{:.input_area}
```python
%%time
ccs1_mask = ccdp.ccdmask(ccs[0])
```


{:.output .output_stream}
```
CPU times: user 43.9 s, sys: 198 ms, total: 44.1 s
Wall time: 44.2 s

```

Displaying the flat we used and the mask side-by-side demonstrates that the
defects which are clear in the flat are picked up in the mask.



{:.input_area}
```python
fig, axes = plt.subplots(1, 2, figsize=(15, 10))

show_image(ccs[0], cmap='gray', fig=fig, ax=axes[0])
axes[0].set_title('Single calibrated flat')

show_image(ccs1_mask, cmap='gray', fig=fig, ax=axes[1], is_mask=False)
axes[1].set_title('Derived mask');
```



{:.output .output_png}
![png](images/08-02-Creating-a-mask_30_0.png)



A couple of cutouts are shown below illustrating some of the individual defects
identified.



{:.input_area}
```python
fig, axes = plt.subplots(2, 2, figsize=(10, 10))

width = 300
center = (512, 3976)
plot_row = 0

image_snippet(ccs[0], center, width=width, fig=fig, axis=axes[plot_row, 0])
axes[plot_row, 0].set_title('Flat, partial bad column')

image_snippet(ccs1_mask, center, width=width, fig=fig, axis=axes[plot_row, 1], is_mask=True)
axes[plot_row, 1].set_title('Mask, same center')

center = (420, 3250)
width = 100
plot_row = 1

image_snippet(ccs[0], center, width=width, fig=fig, axis=axes[plot_row, 0])
axes[plot_row, 0].set_title('Flat, bad patch')

image_snippet(ccs1_mask, center, width=width, fig=fig, axis=axes[plot_row, 1], is_mask=True)
axes[plot_row, 1].set_title('Mask, same center')
```





{:.output .output_data_text}
```
Text(0.5, 1.0, 'Mask, same center')
```




{:.output .output_png}
![png](images/08-02-Creating-a-mask_32_1.png)


