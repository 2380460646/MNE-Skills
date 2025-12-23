# Autoreject - Api

**Pages:** 9

---

## autoreject.AutoReject#

**URL:** https://autoreject.github.io/stable/generated/autoreject.AutoReject.html

**Contents:**
- autoreject.AutoReject#
- Examples using autoreject.AutoReject#

Efficiently find n_interpolate and consensus.

AutoReject by design supports multiple channels. If no picks are passed, separate solutions will be computed for each channel type and internally combined. This then readily supports cleaning unseen epochs from the different channel types used during fit.

The values to try for the number of channels for which to interpolate. This is \(\\rho\). If None, defaults to np.array([1, 4, 32])

The values to try for percentage of channels that must agree as a fraction of the total number of channels. This sets \(\\kappa/Q\). If None, defaults to np.linspace(0, 1.0, 11)

Channels to include. Slices and lists of integers will be interpreted as channel indices. In lists, channel type strings (e.g., ['meg', 'eeg']) will pick channels of those types, channel name strings (e.g., ['MEG0111', 'MEG2623'] will pick the given channels. Can also be the string values 'all' to pick all channels, or 'data' to pick data channels. None (default) will pick data channels {‘meg’, ‘eeg’}, which will lead fitting and combining autoreject solutions across these channel types. Note that channels in info['bads'] will be included if their names or indices are explicitly provided.

‘bayesian_optimization’ or ‘random_search’

The seed of the pseudo random number generator to use. Defaults to None.

The verbosity of progress messages. If False, suppress all output messages.

The instances of _AutoReject for each channel type.

The sensor-level thresholds with channel names as keys and the peak-to-peak thresholds as the values.

The cross validation error for different parameter values.

The estimated consensus per channel type.

The estimated n_interpolate per channel type.

The data channels considered by autoreject. By default only data channels, not already marked as bads are considered.

Fit the epochs on the AutoReject object.

The epochs object to be fit.

Estimate the rejection params and finds bad epochs.

The epochs object which must be cleaned.

If true the rejection log is also returned.

The rejection log. Returned only of return_log is True.

Get rejection logs of epochs.

If multiple channel types are present, reject_log[‘bad_epochs_idx’] reflects the union of bad trials across channel types.

The epoched data for which the reject log is computed.

Channels to include. Slices and lists of integers will be interpreted as channel indices. In lists, channel type strings (e.g., ['meg', 'eeg']) will pick channels of those types, channel name strings (e.g., ['MEG0111', 'MEG2623'] will pick the given channels. Can also be the string values 'all' to pick all channels, or 'data' to pick data channels. None (default) will use the .picks attribute. Note that channels in info['bads'] will be included if their names or indices are explicitly provided.

Save autoreject object with the HDF5 format.

The filename to save to. The filename must end in ‘.h5’ or ‘.hdf5’.

If True, overwrite file if it already exists. Defaults to False.

Remove bad epochs, repairs sensors and returns clean epochs.

The epochs object which must be cleaned.

If true the rejection log is also returned.

The reject log to use. If None, the default reject log is used.

The rejection log. Returned only if return_log is True.

Preprocessing workflow with autoreject and ICA

Visualize bad sensors per trial

---

## autoreject.compute_thresholds#

**URL:** https://autoreject.github.io/stable/generated/autoreject.compute_thresholds.html

**Contents:**
- autoreject.compute_thresholds#
- Examples using autoreject.compute_thresholds#

Compute thresholds for each channel.

The epochs objects whose thresholds must be computed.

‘bayesian_optimization’ or ‘random_search’

The seed of the pseudo random number generator to use. Defaults to None.

Channels to include. Slices and lists of integers will be interpreted as channel indices. In lists, channel type strings (e.g., ['meg', 'eeg']) will pick channels of those types, channel name strings (e.g., ['MEG0111', 'MEG2623'] will pick the given channels. Can also be the string values 'all' to pick all channels, or 'data' to pick data channels. None (default) will pick data channels {‘meg’, ‘eeg’}. Note that channels in info['bads'] will be included if their names or indices are explicitly provided.

Whether to augment the data or not. By default it is True, but set it to False, if the channel locations are not available.

The verbosity of progress messages. If False, suppress all output messages.

Number of jobs to run in parallel

The channel-level rejection thresholds

For example, we can compute the channel-level thresholds for all the EEG sensors this way:

Plot channel-level thresholds

Automatically repair epochs

autoreject.get_rejection_threshold

---

## autoreject.Ransac#

**URL:** https://autoreject.github.io/stable/generated/autoreject.Ransac.html

**Contents:**
- autoreject.Ransac#
- Examples using autoreject.Ransac#

RANSAC algorithm to find bad sensors and repair them.

Implements RAndom SAmple Consensus (RANSAC) method to detect bad sensors.

Number of times the sensors are resampled.

Fraction of sensors for robust reconstruction.

Cut-off correlation for abnormal wrt neighbours.

Cut-off fraction of time sensor can have poor RANSAC predictability.

Number of parallel jobs.

The seed of the pseudo random number generator to use. Defaults to 435656.

Channels to include. Slices and lists of integers will be interpreted as channel indices. In lists, channel name strings (e.g., ['MEG0111', 'MEG2623']) will pick the given channels. None (default) will pick data channels {‘meg’, ‘eeg’}. Note that channels in info['bads'] will be included if their names or indices are explicitly provided.

The verbosity of progress messages. If False, suppress all output messages.

The window_size is automatically set to the epoch length.

“The PREP pipeline: standardized preprocessing for large-scale EEG analysis.” Frontiers in neuroinformatics 9 (2015).

Alexandre Gramfort, “Autoreject: Automated artifact rejection for MEG and EEG.” arXiv preprint arXiv:1612.08194, 2016.

Perform RANSAC on the given epochs.

Interpolate all channels from a subset of channels (fraction denoted as min_channels), repeat n_resample times.

See if correlation of interpolated channels to original channel is above 75% per epoch (min_corr)

If more than unbroken_time fraction of epochs have a lower correlation than that, add channel to self.bad_chs_

An Epochs object with data to perform RANSAC on

The updated instance with the list of bad channels accessible by self.bad_chs_

Detect bad sensors using RANSAC

autoreject.compute_thresholds

---

## autoreject.read_auto_reject#

**URL:** https://autoreject.github.io/stable/generated/autoreject.read_auto_reject.html

**Contents:**
- autoreject.read_auto_reject#

Read AutoReject object.

The filename where the AutoReject object is saved.

autoreject.get_rejection_threshold

autoreject.read_reject_log

---

## autoreject.read_reject_log#

**URL:** https://autoreject.github.io/stable/generated/autoreject.read_reject_log.html

**Contents:**
- autoreject.read_reject_log#

The filename where the reject log is saved.

autoreject.read_auto_reject

autoreject.validation_curve

---

## autoreject.RejectLog#

**URL:** https://autoreject.github.io/stable/generated/autoreject.RejectLog.html

**Contents:**
- autoreject.RejectLog#
- Examples using autoreject.RejectLog#

The boolean array with entries True for epochs that are marked as bad.

It contains integers that encode if a channel in a given epoch is good (value 0), bad (1), or bad and interpolated (2).

The list of channels corresponding to the rows of the labels.

Plot an image of good, bad and interpolated channels for each epoch.

If ‘vertical’ (default), will plot sensors on x-axis and epochs on y-axis. If ‘horizontal’, will plot epochs on x-axis and sensors on y-axis.

If ‘auto’ (default), show all channel names if fewer than 25 entries. Otherwise it shows every 5 entries. If int, show every show_names entries.

If ‘equal’, the pixels are square. If ‘auto’, the axis is fixed and the aspect ratio is adjusted for data to fit. See documentation of plt.imshow() for more details.

If True (default), display the figure immediately.

The axes to plot to. In None (default), create a new figure and axes.

The figure object containing the plot.

Plot interpolated and dropped epochs.

Scaling factors for the traces. If None, defaults to:

The title to display.

The filename to save to. The filename must end in ‘.npz’.

If True, overwrite file if it already exists. Defaults to False.

Preprocessing workflow with autoreject and ICA

Visualize bad sensors per trial

autoreject.AutoReject

---

## autoreject.utils.set_matplotlib_defaults#

**URL:** https://autoreject.github.io/stable/generated/autoreject.utils.set_matplotlib_defaults.html

**Contents:**
- autoreject.utils.set_matplotlib_defaults#

Set publication quality defaults for matplotlib.

autoreject.validation_curve

---

## autoreject.validation_curve#

**URL:** https://autoreject.github.io/stable/generated/autoreject.validation_curve.html

**Contents:**
- autoreject.validation_curve#
- Examples using autoreject.validation_curve#

Validation curve on epochs for global autoreject.

Name of the parameter that will be varied. Defaults to ‘thresh’.

The values of the parameter that will be evaluated. If None, 15 values between the min and the max threshold will be tested.

Determines the cross-validation strategy. Defaults to None.

If True the used param_range is returned. Defaults to False.

The number of thresholds to compute in parallel.

The scores in the training set

The scores in the test set

The thresholds used to build the validation curve. Only returned if return_param_range is True.

Plotting the cross-validation curve

autoreject.read_reject_log

autoreject.utils.set_matplotlib_defaults

---

## autoreject#

**URL:** https://autoreject.github.io/stable/

**Contents:**
- autoreject#
- Installation#
- Quickstart#
- Bug reports#
- Cite#

This is a library to automatically reject bad trials and repair bad sensors in magneto-/electroencephalography (M/EEG) data.

We recommend the Anaconda Python distribution and a Python version >= 3.8. To obtain the stable release of autoreject, you can use pip:

If you want the latest (development) version of autoreject, use:

If you do not have admin privileges on the computer, use the --user flag with pip.

To check if everything worked fine, you can do:

and it should not give any error messages.

Below, we list the dependencies for autoreject. All required dependencies are installed automatically when you install autoreject.

scikit-learn (>=0.24.2)

Optional dependencies are:

openneuro-py (>= 2021.10.1, for fetching data from OpenNeuro.org)

The easiest way to get started is to copy the following three lines of code in your script:

This will automatically clean an epochs object read in using MNE-Python. To get the rejection dictionary, simply do:

We also implement RANSAC from the PREP pipeline (see PyPREP for a full implementation of the PREP pipeline). The API is the same:

For more details check out the example to automatically detect and repair bad epochs.

Please use the GitHub issue tracker to report bugs.

[1] Mainak Jas, Denis Engemann, Federico Raimondo, Yousra Bekhti, and Alexandre Gramfort, “Automated rejection and repair of bad trials in MEG/EEG.” In 6th International Workshop on Pattern Recognition in Neuroimaging (PRNI), 2016.

[2] Mainak Jas, Denis Engemann, Yousra Bekhti, Federico Raimondo, and Alexandre Gramfort. 2017. “Autoreject: Automated artifact rejection for MEG and EEG data”. NeuroImage, 159, 417-429.

---
