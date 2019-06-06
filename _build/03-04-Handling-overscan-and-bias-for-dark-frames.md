---
redirect_from:
  - "03-04-handling-overscan-and-bias-for-dark-frames"
interact_link: content/03-04-Handling-overscan-and-bias-for-dark-frames.ipynb
kernel_name: python3
has_widgets: false
title: 'Handling overscan and bias for dark frames'
prev_page:
  url: /03-02-Real-dark-current-noise-and-other-artifacts
  title: 'Real dark current: noise and other artifacts'
next_page:
  url: /03-05-Calibrate-dark-images
  title: 'Calibrate dark images'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---

# Handling overscan and bias for dark frames

## The options for reducing dark frames

The next steps to take depend on two things:

1. Are you subtracting overscan? If so, you should subtract overscan for the dark frames.
1. Will you need to scale these darks to a different exposure time? If so, you need to subtract bias from the darks. If not, leave the bias in.

### 1. Do you need to subtract overscan?

If you decide to subtract the overscan from *any* of the images used in your data reduction then you must subtract overscan from *all* of the images. This includes the darks, and is independent of whether you intend to scale the dark frames to other exposure times.

Use [`ccdproc.subtract_overscan`](https://ccdproc.readthedocs.io/en/latest/ccdproc/reduction_toolbox.html#overscan-subtraction) to remove the overscan. See the notebook XX for a discussion of overscan, and see YY for a worked example in which overscan is subtracted.

### 2. Do you need to scale the darks?

It depends on the exposure times of the other images you need to reduce. If the other images have exposure times that match your dark frames then you do not need to scale the darks. If any other images (except bias frames, which are always zero exposure) have exposure time that do not match the exposure times of the darks, then you will need to scale the darks by exposure time. 

If you do need to scale the dark frames, then you should subtract the bias from them using [`ccdproc.subtract_bias`](https://ccdproc.readthedocs.io/en/latest/ccdproc/reduction_toolbox.html#subtract-bias-and-dark). Examples of using [`ccdproc.subtract_bias`](https://ccdproc.readthedocs.io/en/latest/ccdproc/reduction_toolbox.html#subtract-bias-and-dark) are in the next notebook.

If you do not need to scale the dark frames to a different exposure time then do not subtract the bias from the darks. The dark frames will serve to remove both the bias and the dark current your images.


As a reminder, you should try very hard to avoid scaling dark frames up to a longer exposure time because you will primarily be scaling up noise rather than dark current.


