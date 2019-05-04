---
redirect_from:
  - "00-00-preface"
interact_link: content/00-00-Preface.ipynb
kernel_name: python3
title: 'Home'
prev_page:
  url: 
  title: ''
next_page:
  url: /01-00-Understanding-an-astronomical-CCD-image
  title: 'Understanding astronomical images'
comment: "***PROGRAMMATICALLY GENERATED, DO NOT EDIT. SEE ORIGINAL FILES IN /content***"
---

# Preface


The purpose of this text is to walk through image reduction and photometry using Python, especially Astropy and its affiliated packages. It assumes some basic familiarity with astronomical images and with Python. The inspiration for this work is a pair of guides written for IRAF, ["A User's Guide to CCD Reductions with IRAF" (Massey 1997)](http://www.ifa.hawaii.edu/~meech/a399/handouts/ccduser3.pdf) and ["A User's Guide to Stellar CCD Photometry with IRAF" (Massey and Davis 1992)](https://www.mn.uio.no/astro/english/services/it/help/visualization/iraf/daophot2.pdf).

The focus is on optical/IR images, not spectra.

## Software setup

The recommended way to get set up to use this guide is to use the [Anaconda Python distribution](https://www.anaconda.com/download/) (or the much smaller [miniconda installer](https://conda.io/miniconda.html)). Once you have that, you can install everything you need with:

```
conda install -c astropy ccdproc photutils ipywidgets matplotlib
```
