---
redirect_from:
  - "08-00-image-masking"
interact_link: content/08-00-Image-masking.ipynb
kernel_name: python3
has_widgets: false
title: 'Finding and dealing with bad pixels'
prev_page:
  url: /06-00-Reducing-science-images
  title: 'Calibrating science images'
next_page:
  url: /08-01-Identifying-hot-pixels
  title: 'Identifying hot pixels'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---

# Image masking

There are several reasons a particular pixel in a specific image might not be
useful:

+ The pixel could be "hot," meaning it isn't possible to remove the dark current
from the pixel.
+ The pixel could be bad in the sense that it does not respond to light the way
the other pixels do.
+ A cosmic ray can hit the pixel during the image.

The following notebooks walk through identifying each of those types of bad
pixels and how to create a mask for them.
