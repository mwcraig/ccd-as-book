---
redirect_from:
  - "03-04-make-a-choice-about-next-steps-for-darks"
interact_link: content/03-04-Make-a-choice-about-next-steps-for-darks.ipynb
kernel_name: python3
has_widgets: false
title: 'Make a choice about next steps for darks'
prev_page:
  url: /03-02-Reality-of-dark-currrent--most-of-your-dark-frame-is-noise-and-not-all-of-the-time-dependent-artifacts-are-dark-current
  title: 'Reality: most of your dark frame is noise and not all of the time dependent artifacts are dark current'
next_page:
  url: /03-05-Calibrate-dark-images
  title: 'Calibrate dark images'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---

# Make a choice about next steps for darks


## The options for reducing dark frames

The next steps to take depend on two things:

1. Are you subtracting overscan? If so, you should subtract overscan for the dark frames.
1. Will you need to scale these darks to a different exposure time? If so, you need to subtract bias from the darks. If not, leave the bias in.

### 1. Do you need to subtract overscan?

If you decide to subtract from *any* of the images used in your data reduction then you must subtract overscan from *all* of the images. This includes the darks, and is independent of whether you intend to scale the dark frames to other exposure times.

Use [`ccdproc.subtract_overscan`](https://ccdproc.readthedocs.io/en/latest/ccdproc/reduction_toolbox.html#overscan-subtraction) to remove the overscan. See the notebook XX for a discussion of overscan, and see YY for a worked example in which overscan is subtracted.

### 2. Do you need to scale the darks?

It depends on the exposure times of the other images you need to reduce. If the other images have exposure times that match your dark frames then you do not need to scale the darks. If any other images (except bias frames, which are always zero exposure) have exposure time that do not match the exposure times of the darks, then you will need to scale the darks by exposure time. 

If you do need to scale the dark frames, then you should subtract the bias from them using [`ccdproc.subtract_bias`](https://ccdproc.readthedocs.io/en/latest/ccdproc/reduction_toolbox.html#subtract-bias-and-dark). Examples of using [`ccdproc.subtract_bias`](https://ccdproc.readthedocs.io/en/latest/ccdproc/reduction_toolbox.html#subtract-bias-and-dark) are in the next notebook.

If you do not need to scale the dark frames to a different exposure time then do not subtract the bias from the darks. The dark frames will serve to remove both the bias and the dark current your images.


As a reminder, you should try very hard to avoid scaling dark frames up to a longer exposure time because you will primarily be scaling up noise rather than dark current.


