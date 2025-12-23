# Autoreject - Preprocessing

**Pages:** 1

---

## autoreject.get_rejection_threshold#

**URL:** https://autoreject.github.io/stable/generated/autoreject.get_rejection_threshold.html

**Contents:**
- autoreject.get_rejection_threshold#
- Examples using autoreject.get_rejection_threshold#

Compute global rejection thresholds.

The epochs from which to estimate the epochs dictionary

The decimation factor: Increment for selecting every nth time slice.

The seed of the pseudo random number generator to use. Defaults to None.

The channel types for which to find the rejection dictionary. e.g., [‘mag’, ‘grad’]. If None, the rejection dictionary will have keys [‘mag’, ‘grad’, ‘eeg’, ‘eog’, ‘hbo’, ‘hbr’, ‘ecog’, ‘seeg’].

The verbosity of progress messages. If False, suppress all output messages.

The rejection dictionary with keys as specified by ch_types.

Sensors marked as bad by user will be excluded when estimating the rejection dictionary.

Find global rejection threshold

Plotting the cross-validation curve

autoreject.compute_thresholds

autoreject.read_auto_reject

---
