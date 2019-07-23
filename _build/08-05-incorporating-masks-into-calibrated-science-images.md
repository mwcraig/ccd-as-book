---
interact_link: content/08-05-incorporating-masks-into-calibrated-science-images.ipynb
kernel_name: python3
has_widgets: false
title: 'Incorporating masks in science images'
prev_page:
  url: /08-03-Cosmic-ray-removal
  title: 'Removing cosmic rays'
next_page:
  url: https://github.com/mwcraig/ccd-reduction-and-photometry-guide
  title: 'GitHub repository'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---

# Incorporating masks into calibrated science images

There are three ways of determining which pixels in a CCD image may need to be
masked (this is in addition to whatever mask or bit fields the observatory at
which you are taking images may provide).

Two of them are the same for all of the science images:

+ Hot pixels unlikely to be properly calibrated by subtracting dark current,
discussed in [Identifying hot pixels](08-01-Identifying-hot-pixels.html).
+ Bad pixels identified by `ccdproc.ccdmask` from flat field images, discussed
in [Creating a mask with `ccdmask`](08-02-Creating-a-mask.html).

The third, identifying cosmic rays, discussed in
[Cosmic ray removal](08-03-Cosmic-ray-removal.html), will by its nature be different for each
science image.

The first two masks could be added to science images at the time the science
images are calibrated, if desired. They are added to the science images here, as
a separate step, because in many situations it is fine to omit masking entirely
and there is no particular advantage to introducing it earlier.

We begin, as usual, with a couple of imports.



{:.input_area}
```python
from pathlib import Path

from astropy import units as u
from astropy.nddata import CCDData

import ccdproc as ccdp
```


## Read masks that are the same for all of the science images

[*Click here to comment on this section on GitHub (opens in new tab).*](https://github.com/mwcraig/ccd-reduction-and-photometry-guide/pull/108/files#diff-8ef287f1d9f06a3732bd30c19146ef93R60){:target="_blank"}

In previous notebooks we constructed a mask based on the dark current and a mask
created by ccdmask from a flat image. Displaying the summary of the the
information about the reduced images is a handy way to determine which files are
the masks.



{:.input_area}
```python
ex2_path = Path('example2-reduced')

ifc = ccdp.ImageFileCollection(ex2_path)
ifc.summary['file', 'imagetyp']
```





<div markdown="0" class="output output_html">
<i>Table masked=True length=38</i>
<table id="table47640105480" class="table-striped table-bordered table-condensed">
<thead><tr><th>file</th><th>imagetyp</th></tr></thead>
<thead><tr><th>str35</th><th>str9</th></tr></thead>
<tr><td>AutoFlat-PANoRot-r-Bin1-001.fit</td><td>FLAT</td></tr>
<tr><td>AutoFlat-PANoRot-r-Bin1-002.fit</td><td>FLAT</td></tr>
<tr><td>AutoFlat-PANoRot-r-Bin1-003.fit</td><td>FLAT</td></tr>
<tr><td>AutoFlat-PANoRot-r-Bin1-004.fit</td><td>FLAT</td></tr>
<tr><td>AutoFlat-PANoRot-r-Bin1-005.fit</td><td>FLAT</td></tr>
<tr><td>AutoFlat-PANoRot-r-Bin1-006.fit</td><td>FLAT</td></tr>
<tr><td>AutoFlat-PANoRot-r-Bin1-007.fit</td><td>FLAT</td></tr>
<tr><td>AutoFlat-PANoRot-r-Bin1-008.fit</td><td>FLAT</td></tr>
<tr><td>AutoFlat-PANoRot-r-Bin1-009.fit</td><td>FLAT</td></tr>
<tr><td>AutoFlat-PANoRot-r-Bin1-010.fit</td><td>FLAT</td></tr>
<tr><td>...</td><td>...</td></tr>
<tr><td>Dark-S001-R001-C009-NoFilt copy.fit</td><td>DARK</td></tr>
<tr><td>Dark-S001-R001-C009-NoFilt.fit</td><td>DARK</td></tr>
<tr><td>Dark-S001-R001-C020-NoFilt.fit</td><td>DARK</td></tr>
<tr><td>combined_bias.fit</td><td>BIAS</td></tr>
<tr><td>combined_dark_90.000.fit</td><td>DARK</td></tr>
<tr><td>combined_flat_filter_r.fit</td><td>FLAT</td></tr>
<tr><td>kelt-16-b-S001-R001-C084-r.fit</td><td>LIGHT</td></tr>
<tr><td>kelt-16-b-S001-R001-C125-r.fit</td><td>LIGHT</td></tr>
<tr><td>mask_from_ccdmask.fits</td><td>flat mask</td></tr>
<tr><td>mask_from_dark_current.fits</td><td>dark mask</td></tr>
</table>
</div>



We read each of those in below, converting the mask to boolean after we read it.



{:.input_area}
```python
mask_ccdmask = CCDData.read(ex2_path / 'mask_from_ccdmask.fits', unit=u.dimensionless_unscaled)
mask_ccdmask.data = mask_ccdmask.data.astype('bool')

mask_hot_pix = CCDData.read(ex2_path / 'mask_from_dark_current.fits', unit=u.dimensionless_unscaled)
mask_hot_pix.data = mask_hot_pix.data.astype('bool')
```


### Combining the masks

[*Click here to comment on this section on GitHub (opens in new tab).*](https://github.com/mwcraig/ccd-reduction-and-photometry-guide/pull/108/files#diff-8ef287f1d9f06a3732bd30c19146ef93R104){:target="_blank"}

We combine the masks using a logical "or" since we want to mask out pixels that
unit=u.dimensionless_unscaled bad for any reason.



{:.input_area}
```python
combined_mask = mask_ccdmask.data | mask_hot_pix.data
```


It turns out we are masking roughly 0.056% of the pixels so far.



{:.input_area}
```python
combined_mask.sum()
```





{:.output .output_data_text}
```
9422
```



## Detect cosmic rays

[*Click here to comment on this section on GitHub (opens in new tab).*](https://github.com/mwcraig/ccd-reduction-and-photometry-guide/pull/108/files#diff-8ef287f1d9f06a3732bd30c19146ef93R139){:target="_blank"}

Cosmic ray detection was discussed in detail in an
[earlier section](08-03-Cosmic-ray-removal.html). Here we loop over all of the calibrated
science images and:

+ detect cosmic rays in them,
+ combine the cosmic ray mask with the mask that applies to all images,
+ set the mask of the image to the overall mask, and
+ save the image, overwriting the calibrated science image without the mask.

Since the cosmic ray detection takes a while, a status message is displayed
before each image is processed.



{:.input_area}
```python
ifc.files_filtered()
for ccd, file_name in ifc.ccds(imagetyp='light', return_fname=True):
    print('Working on file {}'.format(file_name))
    new_ccd = ccdp.cosmicray_lacosmic(ccd, readnoise=10, sigclip=8, verbose=True)
    overall_mask = new_ccd.mask | combined_mask
    # If there was already a mask, keep it.
    if ccd.mask is not None:
        ccd.mask = ccd.mask | overall_mask
    else:
        ccd.mask = overall_mask
    # Files can be overwritten only with an explicit option
    ccd.write(ifc.location / file_name, overwrite=True)
```


{:.output .output_stream}
```
Working on file kelt-16-b-S001-R001-C084-r.fit
Starting 4 L.A.Cosmic iterations
Iteration 1:
211 cosmic pixels this iteration
Iteration 2:
111 cosmic pixels this iteration
Iteration 3:
112 cosmic pixels this iteration
Iteration 4:
86 cosmic pixels this iteration
Working on file kelt-16-b-S001-R001-C125-r.fit
Starting 4 L.A.Cosmic iterations
Iteration 1:
98 cosmic pixels this iteration
Iteration 2:
62 cosmic pixels this iteration
Iteration 3:
59 cosmic pixels this iteration
Iteration 4:
67 cosmic pixels this iteration

```
