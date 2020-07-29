# Preface


The purpose of this text is to walk through image reduction and photometry using
Python, especially Astropy and its affiliated packages. It assumes some basic
familiarity with astronomical images and with Python. The inspiration for this
work is a pair of guides written for IRAF, ["A User's Guide to CCD Reductions with IRAF" (Massey 1997)](http://www.ifa.hawaii.edu/~meech/a399/handouts/ccduser3.pdf) and
["A User's Guide to Stellar CCD Photometry with IRAF" (Massey and Davis 1992)](https://www.mn.uio.no/astro/english/services/it/help/visualization/iraf/daophot2.pdf).

The focus is on optical/IR images, not spectra.

## Credits

### Authors

This guide was written by Matt Craig and Lauren Chambers. Editing was done by
Lauren Glattly.

New contributors will be moved from the acknowledgments to the author list when
they have either written roughly the equivalent of one section or provided
detailed review of several sections. This is intended as a rough guideline, and
when in doubt we will lean towards including people as authors rather than
excluding them.

### Funding

[*Click here to comment on this section on GitHub (opens in new tab).*](https://github.com/mwcraig/ccd-reduction-and-photometry-guide/pull/198/files#diff-6b9e05c00a713108878905584fab99ceR55){:target="_blank"}

Made possible by the Astropy Project and ScienceBetter Consulting through
financial support from the Community Software Initiative at the Space Telescope
Science Institute.

### Acknowledgments

[*Click here to comment on this section on GitHub (opens in new tab).*](https://github.com/mwcraig/ccd-reduction-and-photometry-guide/pull/198/files#diff-6b9e05c00a713108878905584fab99ceR66){:target="_blank"}

The following people contributed to this work by making suggestions, testing
code, or providing feedback on drafts. We are greatful for their assistance!

+ Lia Corrales
+ Kelle Cruz
+ Richard Hendricks
+ Stuart Littlefair
+ Isobel Snellenberger
+ Kris Stern
+ Thomas Stibor

If you have provided feedback and are not listed above, we apologize -- please
[open an issue here](https://github.com/mwcraig/ccd-reduction-and-photometry-guide/issues/new) so we can fix it.

## Resources

[*Click here to comment on this section on GitHub (opens in new tab).*](https://github.com/mwcraig/ccd-reduction-and-photometry-guide/pull/198/files#diff-6b9e05c00a713108878905584fab99ceR87){:target="_blank"}

This astronomical content work was inspired by, and guided by, the excellent
resources below:

+ ["A User's Guide to CCD Reductions with IRAF" (Massey 1997)](http://www.ifa.hawaii.edu/~meech/a399/handouts/ccduser3.pdf) is very thorough, but IRAF has become more
difficult to install over time and is no longer supported.
+ ["A User's Guide to Stellar CCD Photometry with IRAF" (Massey and Davis 1992)](https://www.mn.uio.no/astro/english/services/it/help/visualization/iraf/daophot2.pdf).
+ [The Handbook of Astronomical Image Processing](https://www.amazon.com/Handbook-Astronomical-Image-Processing/dp/0943396824) by Richard Berry and James Burnell. This
provides a very detailed overview of data reduction and photometry. One virtue
is its inclusion of *real* images with defects.
+ The [AAVSO CCD Obseving Manual]() provides a complete introduction to CCD data reduction and photometry.  
+ [A Beginner's Guide to Working with Astronomical Data](https://arxiv.org/abs/1905.13189) is much broader than this guide. It
includes an introduction to Python.

## Software setup

[*Click here to comment on this section on GitHub (opens in new tab).*](https://github.com/mwcraig/ccd-reduction-and-photometry-guide/pull/198/files#diff-6b9e05c00a713108878905584fab99ceR107){:target="_blank"}

The recommended way to get set up to use this guide is to use the
[Anaconda Python distribution](https://www.anaconda.com/download/) (or the much smaller
[miniconda installer](https://conda.io/miniconda.html)). Once you have that, you can install
everything you need with:

```
conda install -c astropy ccdproc photutils ipywidgets matplotlib
```

## Data files

[*Click here to comment on this section on GitHub (opens in new tab).*](https://github.com/mwcraig/ccd-reduction-and-photometry-guide/pull/198/files#diff-6b9e05c00a713108878905584fab99ceR123){:target="_blank"}

The list of the data files, and their approximate sizes, is below. You can
either download them one by one, or use the download helper included with these
notebooks.

### Use this in a terminal to download the data

[*Click here to comment on this section on GitHub (opens in new tab).*](https://github.com/mwcraig/ccd-reduction-and-photometry-guide/pull/198/files#diff-6b9e05c00a713108878905584fab99ceR129){:target="_blank"}

```console
$ python download_data.py
```

### Use this in a notebook cell to download the data

[*Click here to comment on this section on GitHub (opens in new tab).*](https://github.com/mwcraig/ccd-reduction-and-photometry-guide/pull/198/files#diff-6b9e05c00a713108878905584fab99ceR135){:target="_blank"}

```python
%run download_data.py
```

### List of data files

[*Click here to comment on this section on GitHub (opens in new tab).*](https://github.com/mwcraig/ccd-reduction-and-photometry-guide/pull/198/files#diff-6b9e05c00a713108878905584fab99ceR141){:target="_blank"}

+ [Combination of 100 bias images (26MB)](https://zenodo.org/record/3320113/files/combined_bias_100_images.fit.bz2?download=1) (DOI: https://doi.org/10.5281/zenodo.3320113)
+ [Single dark frame, exposure time 1,000 seconds (11MB)](https://zenodo.org/record/3312535/files/dark-test-0002d1000.fit.bz2?download=1) (DOI: https://doi.org/10.5281/zenodo.3312535)
+ [Combination of several dark frames, each 1,000 exposure time (52MB)](https://zenodo.org/record/2634177/files/master_dark_exposure_1000.0.fit.bz2?download=1) (DOI: https://doi.org/10.5281/zenodo.2634177)
+ [Combination of several dark frames, each 300 sec (7MB)](https://zenodo.org/record/3332818/files/combined_dark_300.000.fits.bz2?download=1) (DOI: https://doi.org/10.5281/zenodo.3332818)
+ **"Example 1" in the reduction notebooks:** [Several images from the Palomar Large Format Camera, Chip 0 **(162MB)**](https://zenodo.org/record/3254683/files/example-cryo-LFC.tar.bz2?download=1)
(DOI: https://doi.org/10.5281/zenodo.3254683)
+ **"Example 2" in the reduction notebooks:** [Several images from an Andor Aspen CG16M **(483MB)**](https://zenodo.org/record/3245296/files/example-thermo-electric.tar.bz2?download=1)
(DOI: https://doi.org/10.5281/zenodo.3245296)