---
redirect_from:
  - "03-00-dark-current-and-hot-pixels"
interact_link: content/03-00-Dark-current-and-hot-pixels.ipynb
kernel_name: python3
has_widgets: false
title: 'Dark current and dark frames'
prev_page:
  url: /02-04-Combine-bias-images-to-make-master
  title: 'Combinge bias images to make master bias'
next_page:
  url: /03-01-Dark-current-The-ideal-case
  title: 'Dark current: the ideal case'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---

# Dark current and hot pixels

Every image from a CCD contains *dark current*, which are counts in a raw image caused by thermal effects in the CCD. 
the dark current is modern CCDs is extremely small if the camera is cooled in some way. Cameras cooled with liquid nitrogen have nearly zero dark current while thermo-electrically cooled CCDs have a somewhat larger dark current. The dark current in a CCD operating at room temperature will typically be very large.

Even a camera in which the dark current is *typically* very small will have a small fraction of pixels, called hot pixels, in which the dark current is much higher.

The next notebook walks through how to identify those pixels and how to decide the right way to remove dark current from your data. 
