---
interact_link: content/01-09-reading-images.ipynb
kernel_name: python3
has_widgets: false
title: 'Reading images'
prev_page:
  url: /01-08-Overscan
  title: 'Overscan'
next_page:
  url: /02-00-Handling-overscan,-trimming,-and-bias-subtraction
  title: 'Overscan and bias images'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---

# Reading images

Astropy provides a few ways to read in FITS images, some in the core package and others in affiliated packages.

Before exploring those, we'll create a set of (fake) images to work with.



{:.input_area}
```python
from pathlib import Path
from astropy.nddata import CCDData
from astropy.io import fits
```


## Working with directories

The cell below contains the path to the images. In this notebook we'll use it both to store the fake images we generate and to read images. In normal use, you wouldn't start by writing images there, however. 

If the images are in the same directory as the notebook you can omit this, or set it to an empty string `''`. Having images in the same directory as the notebook is less complicated, but it's not at all uncommon to need to work with images in a different directory.

Later, we'll look at how to generate the full path to an image (directory plus file name) in a way that will work on any platform. One of the approaches to loading images (using `ccdproc.ImageFileCollection`) lets you mostly forget about this.



{:.input_area}
```python
data_directory = 'path/to/my/images'
```


## Generate some fake images

The cells below generate some fake images to use later in the notebook.



{:.input_area}
```python
from pathlib import Path
from itertools import cycle

import numpy as np

image_path = Path(data_directory)

image_path.mkdir(parents=True, exist_ok=True)

images_to_generate = {
    'BIAS': 5,
    'DARK': 10,
    'FLAT': 3,
    'LIGHT': 10
}

exposure_times = {
    'BIAS': [0.0],
    'DARK': [5.0, 30.0],
    'FLAT': [5.0, 6.1, 7.3],
    'LIGHT': [30.0],
}

filters = {
    'FLAT': 'V',
    'LIGHT': 'V'
}

objects = {
    'LIGHT': ['m82', 'xx cyg']
}

image_size = [300, 200]

image_number = 0
for image_type, num in images_to_generate.items():
    exposures = cycle(exposure_times[image_type])
    try:
        filts = cycle(filters[image_type])
    except KeyError:
        filts = []
    
    try:
        objs = cycle(objects[image_type])
    except KeyError:
        objs = []
    for _ in range(num):
        img = CCDData(data=np.random.randn(*image_size), unit='adu')
        img.meta['IMAGETYP'] = image_type
        img.meta['EXPOSURE'] = next(exposures)
        if filts:
            img.meta['FILTER'] = next(filts)
        if objs:
            img.meta['OBJECT'] = next(objs)
        image_name = str(image_path / f'img-{image_number:04d}.fits')
        img.write(image_name)
        print(image_name)
        image_number += 1
```


{:.output .output_stream}
```
path/to/my/images/img-0000.fits
path/to/my/images/img-0001.fits
path/to/my/images/img-0002.fits
path/to/my/images/img-0003.fits
path/to/my/images/img-0004.fits
path/to/my/images/img-0005.fits
path/to/my/images/img-0006.fits
path/to/my/images/img-0007.fits
path/to/my/images/img-0008.fits
path/to/my/images/img-0009.fits
path/to/my/images/img-0010.fits
path/to/my/images/img-0011.fits
path/to/my/images/img-0012.fits
path/to/my/images/img-0013.fits
path/to/my/images/img-0014.fits
path/to/my/images/img-0015.fits
path/to/my/images/img-0016.fits
path/to/my/images/img-0017.fits
path/to/my/images/img-0018.fits
path/to/my/images/img-0019.fits
path/to/my/images/img-0020.fits
path/to/my/images/img-0021.fits
path/to/my/images/img-0022.fits
path/to/my/images/img-0023.fits
path/to/my/images/img-0024.fits
path/to/my/images/img-0025.fits
path/to/my/images/img-0026.fits
path/to/my/images/img-0027.fits

```

## Option 1: Reading a single image with `astropy.io.fits`

This option gives you the most flexibility but is the least adapted to CCD images specifically. What you read in is a list of FITS extensions; you must first select the one you want then access the data or header as desired. 

We'll open up the first of the fake images, `img-0001.fits`. To combine that with the directory name we'll use Python 3's `pathlib`, which ensures that the path combination will work on Windows too.



{:.input_area}
```python
image_name = 'img-0001.fits'

image_path = Path(data_directory) / image_name

hdu_list = fits.open(image_path)
hdu_list
```





{:.output .output_data_text}
```
[<astropy.io.fits.hdu.image.PrimaryHDU object at 0x821006438>]
```



The `hdu_list` is a list of FITS Header-Data Units. In this case there is just one, containing both the image header and data, which can be accessed as shown below.



{:.input_area}
```python
hdu = hdu_list[0]
hdu.header
```





{:.output .output_data_text}
```
SIMPLE  =                    T / conforms to FITS standard                      
BITPIX  =                  -64 / array data type                                
NAXIS   =                    2 / number of array dimensions                     
NAXIS1  =                  200                                                  
NAXIS2  =                  300                                                  
IMAGETYP= 'BIAS    '                                                            
EXPOSURE=                  0.0                                                  
BUNIT   = 'adu     '                                                            
```





{:.input_area}
```python
hdu.data
```





{:.output .output_data_text}
```
array([[ 1.40681538,  1.21485825,  0.58203361, ...,  2.05846497,
         2.01841455, -0.08320567],
       [-1.20997896, -1.6118031 , -0.66081119, ..., -0.86253335,
        -1.20258606, -0.20025521],
       [ 0.25188371, -0.1317854 , -1.3605608 , ...,  0.49013659,
         0.25824718, -0.85209647],
       ...,
       [-1.44412851, -0.25505099, -0.41099761, ..., -0.66918224,
        -0.24640291, -1.30810838],
       [-1.0567436 ,  0.34563845,  0.41963767, ...,  1.33837704,
        -0.65504702, -0.58744726],
       [ 2.26466001, -0.35858374,  0.70337786, ..., -1.56865442,
         0.75968878, -0.2766397 ]])
```



The [documentation for io.fits](https://astropy.readthedocs.io/en/stable/io/fits/index.html) describes more of its capabilities.

## Option 2:  Use `CCDData` to read in a single image

Astropy contains a `CCDData` object for representing a single image. It's not as flexible as using `astrop.io.fits` directly (for example, it assumes there is only one FITS extension and that it contains image data) but it sets up several properties that make the data easier to work with. 

We'll read in the same single image we did in the example above, `img-0001.fits`.



{:.input_area}
```python
ccd = CCDData.read(image_path)
```


The data and header are accessed similarly to how you access it in an HDU returned by `astropy.io.fits`:



{:.input_area}
```python
ccd.header
```





{:.output .output_data_text}
```
SIMPLE  =                    T / conforms to FITS standard                      
BITPIX  =                  -64 / array data type                                
NAXIS   =                    2 / number of array dimensions                     
NAXIS1  =                  200                                                  
NAXIS2  =                  300                                                  
IMAGETYP= 'BIAS    '                                                            
EXPOSURE=                  0.0                                                  
BUNIT   = 'adu     '                                                            
```





{:.input_area}
```python
ccd.data
```





{:.output .output_data_text}
```
array([[ 1.40681538,  1.21485825,  0.58203361, ...,  2.05846497,
         2.01841455, -0.08320567],
       [-1.20997896, -1.6118031 , -0.66081119, ..., -0.86253335,
        -1.20258606, -0.20025521],
       [ 0.25188371, -0.1317854 , -1.3605608 , ...,  0.49013659,
         0.25824718, -0.85209647],
       ...,
       [-1.44412851, -0.25505099, -0.41099761, ..., -0.66918224,
        -0.24640291, -1.30810838],
       [-1.0567436 ,  0.34563845,  0.41963767, ...,  1.33837704,
        -0.65504702, -0.58744726],
       [ 2.26466001, -0.35858374,  0.70337786, ..., -1.56865442,
         0.75968878, -0.2766397 ]])
```



There are a [number of features of `CCDData`](https://astropy.readthedocs.io/en/stable/nddata/ccddata.html) that make it convenient for working with WCS, slicing, and more. Some of those features will be discussed in more detail in the notebooks that follow.

## Option 3: Working with a directory of images using `ImageFileCollection`

The affiliated package [cdcproc](https://ccdproc.readthedocs.io/) provides an easier way to work with collections of images in a directory: an `ImageFileCollection`. The `ImageFileCollection` is initialized with the name of the directory containing the images.



{:.input_area}
```python
from ccdproc import ImageFileCollection
im_collection = ImageFileCollection(data_directory)
```


Note that we didn't need to worry about using `pathlib` to combine the directory and file name, instead we give the collection the name of the directory.

### Summary of directory contents

The `summary` property provides an overview of the files in the directory: it's an astropy `Table`, so you can access columns in the usual way.



{:.input_area}
```python
im_collection.summary
```





<div markdown="0" class="output output_html">
<i>Table masked=True length=28</i>
<table id="table47815864952" class="table-striped table-bordered table-condensed">
<thead><tr><th>file</th><th>simple</th><th>bitpix</th><th>naxis</th><th>naxis1</th><th>naxis2</th><th>imagetyp</th><th>exposure</th><th>bunit</th><th>filter</th><th>object</th></tr></thead>
<thead><tr><th>str13</th><th>bool</th><th>int64</th><th>int64</th><th>int64</th><th>int64</th><th>str5</th><th>float64</th><th>str3</th><th>object</th><th>object</th></tr></thead>
<tr><td>img-0000.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>BIAS</td><td>0.0</td><td>adu</td><td>--</td><td>--</td></tr>
<tr><td>img-0001.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>BIAS</td><td>0.0</td><td>adu</td><td>--</td><td>--</td></tr>
<tr><td>img-0002.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>BIAS</td><td>0.0</td><td>adu</td><td>--</td><td>--</td></tr>
<tr><td>img-0003.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>BIAS</td><td>0.0</td><td>adu</td><td>--</td><td>--</td></tr>
<tr><td>img-0004.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>BIAS</td><td>0.0</td><td>adu</td><td>--</td><td>--</td></tr>
<tr><td>img-0005.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>DARK</td><td>5.0</td><td>adu</td><td>--</td><td>--</td></tr>
<tr><td>img-0006.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>DARK</td><td>30.0</td><td>adu</td><td>--</td><td>--</td></tr>
<tr><td>img-0007.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>DARK</td><td>5.0</td><td>adu</td><td>--</td><td>--</td></tr>
<tr><td>img-0008.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>DARK</td><td>30.0</td><td>adu</td><td>--</td><td>--</td></tr>
<tr><td>img-0009.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>DARK</td><td>5.0</td><td>adu</td><td>--</td><td>--</td></tr>
<tr><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td><td>...</td></tr>
<tr><td>img-0018.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>LIGHT</td><td>30.0</td><td>adu</td><td>V</td><td>m82</td></tr>
<tr><td>img-0019.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>LIGHT</td><td>30.0</td><td>adu</td><td>V</td><td>xx cyg</td></tr>
<tr><td>img-0020.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>LIGHT</td><td>30.0</td><td>adu</td><td>V</td><td>m82</td></tr>
<tr><td>img-0021.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>LIGHT</td><td>30.0</td><td>adu</td><td>V</td><td>xx cyg</td></tr>
<tr><td>img-0022.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>LIGHT</td><td>30.0</td><td>adu</td><td>V</td><td>m82</td></tr>
<tr><td>img-0023.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>LIGHT</td><td>30.0</td><td>adu</td><td>V</td><td>xx cyg</td></tr>
<tr><td>img-0024.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>LIGHT</td><td>30.0</td><td>adu</td><td>V</td><td>m82</td></tr>
<tr><td>img-0025.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>LIGHT</td><td>30.0</td><td>adu</td><td>V</td><td>xx cyg</td></tr>
<tr><td>img-0026.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>LIGHT</td><td>30.0</td><td>adu</td><td>V</td><td>m82</td></tr>
<tr><td>img-0027.fits</td><td>True</td><td>-64</td><td>2</td><td>200</td><td>300</td><td>LIGHT</td><td>30.0</td><td>adu</td><td>V</td><td>xx cyg</td></tr>
</table>
</div>



### Filtering and iterating over images

The convenient thing about `ImageFileCollection` is that it provides easy ways to filter or loop over files via FITS header keyword values. 

For example, looping over just the flat files is one line of code:



{:.input_area}
```python
for a_flat in im_collection.hdus(imagetyp='FLAT'):
    print(a_flat.header['EXPOSURE'])
```


{:.output .output_stream}
```
5.0
6.1
7.3

```

Instead of iterating over HDUs, as in the example above, you can iterate over just the headers (with `.headers`) or just the data (with `.data`). You can use any FITS keyword from the header as a keyword for selecting the images you want. In addition, you can return the file name while also iterating.



{:.input_area}
```python
for a_flat, fname in im_collection.hdus(imagetyp='LIGHT', object='m82', return_fname=True):
    print(f'In file {fname} the exposure is:', a_flat.header['EXPOSURE'], 'with standard deviation ', a_flat.data.std())
```


{:.output .output_stream}
```
In file img-0018.fits the exposure is: 30.0 with standard deviation  0.9965693117641756
In file img-0020.fits the exposure is: 30.0 with standard deviation  0.9966905082434526
In file img-0022.fits the exposure is: 30.0 with standard deviation  0.9969161457344193
In file img-0024.fits the exposure is: 30.0 with standard deviation  0.9961830977757162
In file img-0026.fits the exposure is: 30.0 with standard deviation  0.9949013719116523

```

The [documentation for `ImageFileCollection`](https://ccdproc.readthedocs.io/en/latest/ccdproc/image_management.html) describes more of its capabilities. `ImageFileCollection` can automatically save a copy of each image as you iterate over them, for example.



{:.input_area}
```python
for a_flat, fname in im_collection.ccds(bunit='ADU', return_fname=True):
    print(a_flat.unit)
```


{:.output .output_stream}
```
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu
adu

```



{:.input_area}
```python
a_flat.header
```





{:.output .output_data_text}
```
SIMPLE  =                    T / conforms to FITS standard                      
BITPIX  =                  -64 / array data type                                
NAXIS   =                    2 / number of array dimensions                     
NAXIS1  =                  200                                                  
NAXIS2  =                  300                                                  
IMAGETYP= 'LIGHT   '                                                            
EXPOSURE=                 30.0                                                  
FILTER  = 'V       '                                                            
OBJECT  = 'xx cyg  '                                                            
BUNIT   = 'adu     '                                                            
```


