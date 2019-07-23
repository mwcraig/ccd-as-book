---
redirect_from:
  - "03-05-calibrate-dark-images"
interact_link: content/03-05-Calibrate-dark-images.ipynb
kernel_name: python3
has_widgets: false
title: 'Calibrate dark images'
prev_page:
  url: /03-04-Handling-overscan-and-bias-for-dark-frames
  title: 'Handling overscan and bias for dark frames'
next_page:
  url: /03-06-Combine-darks-for-use-in-later-calibration-steps
  title: 'Combine calibrated dark images for use in later reduction steps'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---

# Calibrate dark images

Dark images, like any other images, need to be calibrated. Depending on the data
you have and the choices you have made in reducing your data the steps to
reducing your images may include:

1. Subtracting overscan (only if you decide to subtract overscan from all
images)
2. Trim the image (if it has overscan, whether you are using the overscan or
not)
3. Subtract bias (if you need to scale the calibrated dark frames to a different
exposure time).



{:.input_area}
```python
from pathlib import Path

from astropy.nddata import CCDData
from ccdproc import ImageFileCollection
import ccdproc as ccdp
```


## Example 1: Overscan subtracted, bias not removed

### Take a look at what images you have

[*Click here to comment on this section on GitHub (opens in new tab).*](https://github.com/mwcraig/ccd-reduction-and-photometry-guide/pull/128/files#diff-fc0aaef3c8ddfc5f7a8566af66d54320R45){:target="_blank"}

First we gather up some information about the raw images and the reduced images
up to this point. These examples have darks stored in a subdirectory of the
folder with the rest of the images, so we create an `ImageFileCollection` for
each.



{:.input_area}
```python
ex1_path_raw = Path('example-cryo-LFC')

ex1_images_raw = ImageFileCollection(ex1_path_raw)
ex1_darks_raw = ImageFileCollection(ex1_path_raw / 'darks')

ex1_path_reduced = Path('example1-reduced')
ex1_images_reduced = ImageFileCollection(ex1_path_reduced)
```


#### Raw images, everything except the darks



{:.input_area}
```python
ex1_images_raw.summary['file', 'imagetyp', 'exptime', 'filter']
```





<div markdown="0" class="output output_html">
<i>Table masked=True length=14</i>
<table id="table47808855176" class="table-striped table-bordered table-condensed">
<thead><tr><th>file</th><th>imagetyp</th><th>exptime</th><th>filter</th></tr></thead>
<thead><tr><th>str14</th><th>str9</th><th>float64</th><th>str2</th></tr></thead>
<tr><td>ccd.001.0.fits</td><td>BIAS</td><td>0.0</td><td>i&apos;</td></tr>
<tr><td>ccd.002.0.fits</td><td>BIAS</td><td>0.0</td><td>i&apos;</td></tr>
<tr><td>ccd.003.0.fits</td><td>BIAS</td><td>0.0</td><td>i&apos;</td></tr>
<tr><td>ccd.004.0.fits</td><td>BIAS</td><td>0.0</td><td>i&apos;</td></tr>
<tr><td>ccd.005.0.fits</td><td>BIAS</td><td>0.0</td><td>i&apos;</td></tr>
<tr><td>ccd.006.0.fits</td><td>BIAS</td><td>0.0</td><td>i&apos;</td></tr>
<tr><td>ccd.014.0.fits</td><td>FLATFIELD</td><td>70.001</td><td>g&apos;</td></tr>
<tr><td>ccd.015.0.fits</td><td>FLATFIELD</td><td>70.011</td><td>g&apos;</td></tr>
<tr><td>ccd.016.0.fits</td><td>FLATFIELD</td><td>70.001</td><td>g&apos;</td></tr>
<tr><td>ccd.017.0.fits</td><td>FLATFIELD</td><td>7.0</td><td>i&apos;</td></tr>
<tr><td>ccd.018.0.fits</td><td>FLATFIELD</td><td>7.0</td><td>i&apos;</td></tr>
<tr><td>ccd.019.0.fits</td><td>FLATFIELD</td><td>7.0</td><td>i&apos;</td></tr>
<tr><td>ccd.037.0.fits</td><td>OBJECT</td><td>300.062</td><td>g&apos;</td></tr>
<tr><td>ccd.043.0.fits</td><td>OBJECT</td><td>300.014</td><td>i&apos;</td></tr>
</table>
</div>



#### Raw dark frames



{:.input_area}
```python
ex1_darks_raw.summary['file', 'imagetyp', 'exptime', 'filter']
```





<div markdown="0" class="output output_html">
<i>Table masked=True length=10</i>
<table id="table47809056328" class="table-striped table-bordered table-condensed">
<thead><tr><th>file</th><th>imagetyp</th><th>exptime</th><th>filter</th></tr></thead>
<thead><tr><th>str14</th><th>str4</th><th>float64</th><th>str2</th></tr></thead>
<tr><td>ccd.002.0.fits</td><td>BIAS</td><td>0.0</td><td>r&apos;</td></tr>
<tr><td>ccd.013.0.fits</td><td>DARK</td><td>300.0</td><td>r&apos;</td></tr>
<tr><td>ccd.014.0.fits</td><td>DARK</td><td>300.0</td><td>r&apos;</td></tr>
<tr><td>ccd.015.0.fits</td><td>DARK</td><td>300.0</td><td>r&apos;</td></tr>
<tr><td>ccd.017.0.fits</td><td>DARK</td><td>70.0</td><td>r&apos;</td></tr>
<tr><td>ccd.018.0.fits</td><td>DARK</td><td>70.0</td><td>r&apos;</td></tr>
<tr><td>ccd.019.0.fits</td><td>DARK</td><td>70.0</td><td>r&apos;</td></tr>
<tr><td>ccd.023.0.fits</td><td>DARK</td><td>7.0</td><td>r&apos;</td></tr>
<tr><td>ccd.024.0.fits</td><td>DARK</td><td>7.0</td><td>r&apos;</td></tr>
<tr><td>ccd.025.0.fits</td><td>DARK</td><td>7.0</td><td>r&apos;</td></tr>
</table>
</div>



### Decide which calibration  steps to take

[*Click here to comment on this section on GitHub (opens in new tab).*](https://github.com/mwcraig/ccd-reduction-and-photometry-guide/pull/128/files#diff-fc0aaef3c8ddfc5f7a8566af66d54320R104){:target="_blank"}

This example is, again, one of the chips of the LFC camera at Palomar. In
earlier notebooks we have seen that the chip has a useful overscan region
(LINK), has little dark current except for some hot pixels and sensor glow in
one corner of the chip.

Looking at the list of non-dark images (i.e. the flat and light images) shows
that for each exposure time in the non-dark images there is a set of dark
exposures that has a matching, or very close to matching, exposure time.

To be more explicit, there are flats with exposure times of 7.0 sec and 70.011
sec and darks with exposure time of 7.0 and 70.0 sec. The dark and flat exposure
times are close enough that there is no need to scale them.  The two images of
an object are each roughly 300 sec, matching the darks with exposure time 300
sec. The very small difference in exposure time, under 0.1 sec, does not need to
be compensated for.

Given this, we will:

1. Subtract overscan from each of the darks. The useful overscan region is XXX
(see LINK).
2. Trim the overscan out of the dark images

We will *not* subtract bias from these images because we will *not* need to
rescale them to a different exposure time.

### Calibrate the individual dark frames



{:.input_area}
```python
for ccd, file_name in ex1_darks_raw.ccds(imagetyp='DARK',            # Just get the bias frames
                                         ccd_kwargs={'unit': 'adu'}, # CCDData requires a unit for the image if 
                                                                     # it is not in the header
                                         return_fname=True           # Provide the file name too.
                                        ):    
    # Subtract the overscan
    ccd = ccdp.subtract_overscan(ccd, overscan=ccd[:, 2055:], median=True)
    
    # Trim the overscan
    ccd = ccdp.trim_image(ccd[:, :2048])
    
    # Save the result
    ccd.write(ex1_path_reduced / file_name)
```


#### Reduced images (so far)



{:.input_area}
```python
ex1_images_reduced.refresh()
ex1_images_reduced.summary['file', 'imagetyp', 'exptime', 'filter', 'combined']
```





<div markdown="0" class="output output_html">
<i>Table masked=True length=16</i>
<table id="table47808855848" class="table-striped table-bordered table-condensed">
<thead><tr><th>file</th><th>imagetyp</th><th>exptime</th><th>filter</th><th>combined</th></tr></thead>
<thead><tr><th>str17</th><th>str4</th><th>float64</th><th>str2</th><th>object</th></tr></thead>
<tr><td>ccd.001.0.fits</td><td>BIAS</td><td>0.0</td><td>i&apos;</td><td>--</td></tr>
<tr><td>ccd.002.0.fits</td><td>BIAS</td><td>0.0</td><td>i&apos;</td><td>--</td></tr>
<tr><td>ccd.003.0.fits</td><td>BIAS</td><td>0.0</td><td>i&apos;</td><td>--</td></tr>
<tr><td>ccd.004.0.fits</td><td>BIAS</td><td>0.0</td><td>i&apos;</td><td>--</td></tr>
<tr><td>ccd.005.0.fits</td><td>BIAS</td><td>0.0</td><td>i&apos;</td><td>--</td></tr>
<tr><td>ccd.006.0.fits</td><td>BIAS</td><td>0.0</td><td>i&apos;</td><td>--</td></tr>
<tr><td>ccd.013.0.fits</td><td>DARK</td><td>300.0</td><td>r&apos;</td><td>--</td></tr>
<tr><td>ccd.014.0.fits</td><td>DARK</td><td>300.0</td><td>r&apos;</td><td>--</td></tr>
<tr><td>ccd.015.0.fits</td><td>DARK</td><td>300.0</td><td>r&apos;</td><td>--</td></tr>
<tr><td>ccd.017.0.fits</td><td>DARK</td><td>70.0</td><td>r&apos;</td><td>--</td></tr>
<tr><td>ccd.018.0.fits</td><td>DARK</td><td>70.0</td><td>r&apos;</td><td>--</td></tr>
<tr><td>ccd.019.0.fits</td><td>DARK</td><td>70.0</td><td>r&apos;</td><td>--</td></tr>
<tr><td>ccd.023.0.fits</td><td>DARK</td><td>7.0</td><td>r&apos;</td><td>--</td></tr>
<tr><td>ccd.024.0.fits</td><td>DARK</td><td>7.0</td><td>r&apos;</td><td>--</td></tr>
<tr><td>ccd.025.0.fits</td><td>DARK</td><td>7.0</td><td>r&apos;</td><td>--</td></tr>
<tr><td>combined_bias.fit</td><td>BIAS</td><td>0.0</td><td>i&apos;</td><td>True</td></tr>
</table>
</div>



## Example 2: Overscan not subtracted, bias is removed



{:.input_area}
```python
ex2_path_raw = Path('example-thermo-electric')

ex2_images_raw = ImageFileCollection(ex2_path_raw)

ex2_path_reduced = Path('example2-reduced')
ex2_images_reduced = ImageFileCollection(ex2_path_reduced)
```


We begin by looking at what exposure times we have in this data.



{:.input_area}
```python
ex2_images_raw.summary['file', 'imagetyp', 'exposure'].show_in_notebook()
```





<div markdown="0" class="output output_html">
<i>Table masked=True length=33</i>
<table id="table47808855904-127184" class="table-striped table-bordered table-condensed">
<thead><tr><th>idx</th><th>file</th><th>imagetyp</th><th>exposure</th></tr></thead>
<tr><td>0</td><td>AutoFlat-PANoRot-r-Bin1-001.fit</td><td>FLAT</td><td>1.0</td></tr>
<tr><td>1</td><td>AutoFlat-PANoRot-r-Bin1-002.fit</td><td>FLAT</td><td>1.0</td></tr>
<tr><td>2</td><td>AutoFlat-PANoRot-r-Bin1-003.fit</td><td>FLAT</td><td>1.0</td></tr>
<tr><td>3</td><td>AutoFlat-PANoRot-r-Bin1-004.fit</td><td>FLAT</td><td>1.0</td></tr>
<tr><td>4</td><td>AutoFlat-PANoRot-r-Bin1-005.fit</td><td>FLAT</td><td>1.0</td></tr>
<tr><td>5</td><td>AutoFlat-PANoRot-r-Bin1-006.fit</td><td>FLAT</td><td>1.02</td></tr>
<tr><td>6</td><td>AutoFlat-PANoRot-r-Bin1-007.fit</td><td>FLAT</td><td>1.06</td></tr>
<tr><td>7</td><td>AutoFlat-PANoRot-r-Bin1-008.fit</td><td>FLAT</td><td>1.11</td></tr>
<tr><td>8</td><td>AutoFlat-PANoRot-r-Bin1-009.fit</td><td>FLAT</td><td>1.16</td></tr>
<tr><td>9</td><td>AutoFlat-PANoRot-r-Bin1-010.fit</td><td>FLAT</td><td>1.21</td></tr>
<tr><td>10</td><td>Bias-S001-R001-C001-NoFilt.fit</td><td>BIAS</td><td>0.0</td></tr>
<tr><td>11</td><td>Bias-S001-R001-C002-NoFilt.fit</td><td>BIAS</td><td>0.0</td></tr>
<tr><td>12</td><td>Bias-S001-R001-C003-NoFilt.fit</td><td>BIAS</td><td>0.0</td></tr>
<tr><td>13</td><td>Bias-S001-R001-C004-NoFilt.fit</td><td>BIAS</td><td>0.0</td></tr>
<tr><td>14</td><td>Bias-S001-R001-C005-NoFilt.fit</td><td>BIAS</td><td>0.0</td></tr>
<tr><td>15</td><td>Bias-S001-R001-C006-NoFilt.fit</td><td>BIAS</td><td>0.0</td></tr>
<tr><td>16</td><td>Bias-S001-R001-C007-NoFilt.fit</td><td>BIAS</td><td>0.0</td></tr>
<tr><td>17</td><td>Bias-S001-R001-C008-NoFilt.fit</td><td>BIAS</td><td>0.0</td></tr>
<tr><td>18</td><td>Bias-S001-R001-C009-NoFilt.fit</td><td>BIAS</td><td>0.0</td></tr>
<tr><td>19</td><td>Bias-S001-R001-C020-NoFilt.fit</td><td>BIAS</td><td>0.0</td></tr>
<tr><td>20</td><td>Dark-S001-R001-C001-NoFilt.fit</td><td>DARK</td><td>90.0</td></tr>
<tr><td>21</td><td>Dark-S001-R001-C002-NoFilt.fit</td><td>DARK</td><td>90.0</td></tr>
<tr><td>22</td><td>Dark-S001-R001-C003-NoFilt.fit</td><td>DARK</td><td>90.0</td></tr>
<tr><td>23</td><td>Dark-S001-R001-C004-NoFilt.fit</td><td>DARK</td><td>90.0</td></tr>
<tr><td>24</td><td>Dark-S001-R001-C005-NoFilt.fit</td><td>DARK</td><td>90.0</td></tr>
<tr><td>25</td><td>Dark-S001-R001-C006-NoFilt.fit</td><td>DARK</td><td>90.0</td></tr>
<tr><td>26</td><td>Dark-S001-R001-C007-NoFilt.fit</td><td>DARK</td><td>90.0</td></tr>
<tr><td>27</td><td>Dark-S001-R001-C008-NoFilt.fit</td><td>DARK</td><td>90.0</td></tr>
<tr><td>28</td><td>Dark-S001-R001-C009-NoFilt copy.fit</td><td>DARK</td><td>90.0</td></tr>
<tr><td>29</td><td>Dark-S001-R001-C009-NoFilt.fit</td><td>DARK</td><td>90.0</td></tr>
<tr><td>30</td><td>Dark-S001-R001-C020-NoFilt.fit</td><td>DARK</td><td>90.0</td></tr>
<tr><td>31</td><td>kelt-16-b-S001-R001-C084-r.fit</td><td>LIGHT</td><td>90.0</td></tr>
<tr><td>32</td><td>kelt-16-b-S001-R001-C125-r.fit</td><td>LIGHT</td><td>90.0</td></tr>
</table><style>table.dataTable {clear: both; width: auto !important; margin: 0 !important;}
.dataTables_info, .dataTables_length, .dataTables_filter, .dataTables_paginate{
display: inline-block; margin-right: 1em; }
.paginate_button { margin-right: 5px; }
</style>
<script>

var astropy_sort_num = function(a, b) {
    var a_num = parseFloat(a);
    var b_num = parseFloat(b);

    if (isNaN(a_num) && isNaN(b_num))
        return ((a < b) ? -1 : ((a > b) ? 1 : 0));
    else if (!isNaN(a_num) && !isNaN(b_num))
        return ((a_num < b_num) ? -1 : ((a_num > b_num) ? 1 : 0));
    else
        return isNaN(a_num) ? -1 : 1;
}

require.config({paths: {
    datatables: 'https://cdn.datatables.net/1.10.12/js/jquery.dataTables.min'
}});
require(["datatables"], function(){
    console.log("$('#table47808855904-127184').dataTable()");
    
jQuery.extend( jQuery.fn.dataTableExt.oSort, {
    "optionalnum-asc": astropy_sort_num,
    "optionalnum-desc": function (a,b) { return -astropy_sort_num(a, b); }
});

    $('#table47808855904-127184').dataTable({
        order: [],
        pageLength: 50,
        lengthMenu: [[10, 25, 50, 100, 500, 1000, -1], [10, 25, 50, 100, 500, 1000, 'All']],
        pagingType: "full_numbers",
        columnDefs: [{targets: [0, 3], type: "optionalnum"}]
    });
});
</script>

</div>



### Decide what steps to take next

[*Click here to comment on this section on GitHub (opens in new tab).*](https://github.com/mwcraig/ccd-reduction-and-photometry-guide/pull/128/files#diff-fc0aaef3c8ddfc5f7a8566af66d54320R218){:target="_blank"}

In this case the only dark frames have exposure time 90 sec. Though that matches
the exposure time of the science images, the flat field images are much shorter
exposure time, ranging from 1 sec to 1.21 sec. That type range of exposure is
typical when twilights flats are taken. Since these are a much different
exposure time than the darks, the dark frames will need to be scaled.

Recall that for this camera the overscan is not useful and should simply be
trimmed off.

Given this, we will:

1. Trim the overscan from each of the dark frames.
2. Subtract calibration bias from the dark frames so that we can scale the darks
to a different exposure time.

### Calibration the individual dark frames

First, we read the combined bias image created in the previous notebook. Though
we could do this based on the file name, using a systematic set of header
keywords to keep track of which images have been combined is less likely to lead
to errors.



{:.input_area}
```python
combined_bias = CCDData.read(ex2_images_reduced.files_filtered(imagetyp='bias', 
                                                               combined=True, 
                                                               include_path=True)[0])
```




{:.input_area}
```python
for ccd, file_name in ex2_images_raw.ccds(imagetyp='DARK',            # Just get the bias frames
                                          return_fname=True           # Provide the file name too.
                                         ):
        
    # Trim the overscan
    ccd = ccdp.trim_image(ccd[:, :4096])
    
    # Subtract bias
    ccd = ccdp.subtract_bias(ccd, combined_bias)
    # Save the result
    ccd.write(ex2_path_reduced / file_name)
```

