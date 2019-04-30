---
redirect_from:
  - "01-00-understanding-an-astronomical-ccd-image"
interact_link: content/01-00-Understanding-an-astronomical-CCD-image.ipynb
kernel_name: python3
has_widgets: false
title: 'Understanding astronomical images'
prev_page:
  url: /https://github.com/mwcraig/ccd-reduction-and-photometry-guide
  title: 'GitHub repository'
next_page:
  url: /01-03-Construction-of-an-artificial-but-realistic-image
  title: 'An artificial, but realistic, image'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---

# Understanding an astronomical CCD image


An astronomical image like the one shown below is essentually a two-dimensional array of values. In an ideal world, the value of each pixel (a pixel being one element of the array) would be directly proportional to the amount of light that fell on the pixel during the time the camera's shutter was open. 

But the ideal scenario does not in fact hold true. A solid understanding of *why* pixel values are not directly proportional to light is useful before diving into the details of image reduction.

## Counts, photons, and electrons

The number stored in a raw astronomical image straight off a telescope is called an Analog Digital Unit (ADU) or count, because internally the camera converts the analog voltage in each pixel to a numerical count. The counts of interest to an astronomer are the ones generated via the photoelectric effect when a photon hits the detector. The number of photons (or equivalently, electrons) that reach the pixel is related to the counts in the pixel by the gain.

The gain is typically provided by the manufacturer of the camera and can be measured from a combination of bias and flat images (Howell 2002; p. 71).

**Take note** that trying to convert a raw image count to photons/electrons by multiplying by the gain will not be meaningful because the raw counts include contributions from sources other than light.

## Not all counts are (interesting) light

There are several contributions to the counts in a pixel. Image reduction is essentially the process of removing all of these except those due to light from an astronomical object:

+ An offset voltage called **bias** is applied to the CCD chip to ensure there are no negative counts during readout. There are small variations in the value of the bias across the chip, and there can be small variations in the bias level over time.
+ Counts can be generated in a pixel due to thermal motion of electrons in CCD; cooling a CCD reduces, but may not fully eliminate, this **dark current**. In modern CCDs the dark current is often ignorable exept for a small fraction of pixels. Dark current is typically reported in electrons/second/pixel, and depends strongly on temperature.
+ There is **read noise** intrinsic to the electronics of the CCD. It is impossible to eliminate this noise (it's present in every image taken by the camera) but there are approaches to minimizing it. Read noise is typically reported in electrons as it can depend on temperature.
+ Some light received by the telescope is scattered light coming from the night sky. The amount of **sky background** depends on the filter passband, the atmospheric conditions, and the local light sources.
+ Though a CCD chip is fairly small, it's not unsual for **cosmic rays** to hit the chip, releasing charge that is then converted to counts.

Whatever remains after taking all of those things away is, in principle, light from astronomical sources.

In practice, there are additional complications.

## CCDs are not perfect

There are a number of issues that affect the sensitivity of the CCD to light, some of which can be corrected for and some of which cannot.

+ Vignetting, a darkening of the images in the corners, is common and correctable.
+ Dust in the optical path, which causes "donuts" or "worms" on the image, is also common and correctable.
+ Variations in the sensitivity of individual pixels are also common and correctable.
+ Dead pixels, which are pixels that don't respond to light, cannot be corrected for.

**Flat** corrections attempt to remove many of these effects. The idea is to image something which is uniformly illuminated as a way to measure variations in sensitivity (regardless of cause) and compensate for them.

## References

Howell, S., *Handbook of CCD Astronomy*, Second Ed, Cambridge University Press 2006 
