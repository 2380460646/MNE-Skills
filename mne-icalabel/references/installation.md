# Mne-Icalabel - Installation

**Pages:** 1

---

## Installation#

**URL:** https://mne.tools/mne-icalabel/stable/install.html

**Contents:**
- Installation#
- Dependencies#
- Methods#

mne-icalabel requires Python 3.9 or higher.

mne-icalabel works best with the latest stable release of MNE-Python. To ensure MNE-Python is up-to-date, see MNE installation instructions. mne-icalabel is available on Pypi and on conda-forge.

As of MNE-Python 1.0, mne-icalabel is distributed in the MNE standalone installers.

The installers create a conda environment with the entire MNE-ecosystem setup, and more!

mne-icalabel is available on PyPI and can be installed in a given environment via pip.

The ICLabel model requires either pytorch or Microsoft onnxruntime.

If you are working with MEG data and plan to use the MEGnet model, e.g. mne_icalabel.megnet.megnet_label_components(), you must install onnxruntime, and do not need to install torch.

Additional dependencies can be installed with different keywords:

Depending on your system, you may want to create a separate environment to install mne-icalabel. You can create a virtual environment with conda:

Replace myenv with the environment name you prefer. mne-icalabel can then be installed from the conda-forge channel:

If you want to install a snapshot of the current development version, run:

To check if everything worked fine, the following command should not raise any error messages:

---
