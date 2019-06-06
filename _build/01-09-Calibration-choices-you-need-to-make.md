---
redirect_from:
  - "01-09-calibration-choices-you-need-to-make"
interact_link: content/01-09-Calibration-choices-you-need-to-make.ipynb
kernel_name: python3
has_widgets: false
title: 'Calibration choices to make'
prev_page:
  url: /01-08-Overscan
  title: 'Overscan'
next_page:
  url: /01-11-reading-images
  title: 'Reading images'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---

# Calibration choices you need to make

There are a few choices you need to make about how you will calibrate your data. Sometimes the decision will be made for you by the data you have.

## Subtract bias and dark as separate steps or in one step?

Every dark image contains bias when it comes off of the camera, so in principle you can take care of both bias and dark by constructing a master dark image that leaves the bias already present in the dark images in place.

This only works if for every image from which you need to remove dark currrent you have a master dark of exactly the same exposure length.

If not, you need to produce master dark images with the bias removed so that they can be scaled by exposure time. 

## Subtract overscan or not?

This is only applicable if your images have an overscan region. Subtracting overscan can be useful for removing small (typically a few counts) variations from image-to-image over the course of a night. 
