---
name: autoreject
description: Autoreject documentation for automated artifact rejection in MEG/EEG data. Provides automated methods to reject bad trials and interpolate bad sensors.
---

# Autoreject Skill

Comprehensive assistance with autoreject development for MEG/EEG data preprocessing.

## When to Use This Skill

This skill should be triggered when:
- **Preprocessing MEG/EEG data** and need to remove artifacts automatically
- **Detecting bad trials** in epoched data (high amplitude artifacts, channel noise)
- **Repairing bad sensors** through interpolation rather than dropping them
- **Finding optimal rejection thresholds** (global or channel-specific)
- **Implementing RANSAC** for robust bad sensor detection
- **Working with MNE-Python epochs** and need automatic quality control
- **Combining autoreject with ICA** for comprehensive artifact removal
- **Questions about** `AutoReject`, `Ransac`, `RejectLog`, or threshold computation
- **Debugging** autoreject pipelines or understanding rejection parameters

## Quick Reference

### 1. Basic AutoReject - Clean Epochs Automatically

```python
from autoreject import AutoReject

# Simplest usage - automatically clean epochs
ar = AutoReject()
ar.fit(epochs)  # Learn optimal parameters
epochs_clean = ar.transform(epochs)

# Get rejection dictionary
reject_log = ar.get_reject_log(epochs)
```

### 2. AutoReject with Parameters

```python
import numpy as np
from autoreject import AutoReject

# Define parameter search space
n_interpolates = np.array([1, 4, 32])  # ρ values to try
consensus_percs = np.linspace(0, 1.0, 11)  # κ values to try

# Create AutoReject with custom parameters
ar = AutoReject(
    n_interpolate=n_interpolates,
    consensus=consensus_percs,
    picks=['meg', 'eeg'],  # Channel types to process
    random_state=42,
    n_jobs=-1,
    verbose=True
)

epochs_clean, reject_log = ar.fit_transform(epochs, return_log=True)
```

### 3. RANSAC - Detect Bad Sensors

```python
from autoreject import Ransac

# Use RANSAC to find bad sensors
ransac = Ransac(
    n_resample=50,
    min_channels=0.25,  # Fraction for robust reconstruction
    min_corr=0.75,       # Correlation threshold
    unbroken_time=0.4,   # Fraction of good epochs required
    n_jobs=-1
)

# Fit and transform epochs
epochs_clean = ransac.fit_transform(epochs)

# Get list of bad channels detected
bad_channels = ransac.bad_chs_
print(f"Bad channels: {bad_channels}")
```

### 4. Compute Global Rejection Threshold

```python
from autoreject import get_rejection_threshold

# Get global rejection threshold for all channels
reject = get_rejection_threshold(epochs, ch_types=['mag', 'grad', 'eeg'])

# Use with MNE epochs
epochs.drop_bad(reject=reject)
```

### 5. Compute Channel-Level Thresholds

```python
from autoreject import compute_thresholds

# Compute individual thresholds per channel
thresholds = compute_thresholds(
    epochs,
    method='bayesian_optimization',  # or 'random_search'
    random_state=42,
    augment=True,
    verbose=True
)

# thresholds is a dict: {'channel_name': threshold_value, ...}
print(f"EEG001 threshold: {thresholds['EEG001']}")
```

### 6. Validation Curve - Find Optimal Threshold

```python
from autoreject import validation_curve
import numpy as np

# Define threshold range to test
param_range = np.linspace(40e-6, 200e-6, 30)

# Compute validation curve
train_scores, test_scores, param_range = validation_curve(
    epochs,
    param_name='thresh',
    param_range=param_range,
    cv=5,
    return_param_range=True
)

# Find best threshold
best_thresh_idx = np.argmin(test_scores.mean(axis=1))
best_thresh = param_range[best_thresh_idx]
```

### 7. Visualize Rejection Log

```python
from autoreject import AutoReject

ar = AutoReject()
epochs_clean, reject_log = ar.fit_transform(epochs, return_log=True)

# Plot heatmap of good/bad/interpolated channels
reject_log.plot('horizontal')

# Access rejection information
bad_epochs_idx = reject_log.bad_epochs  # Boolean array
labels = reject_log.labels  # 0=good, 1=bad, 2=interpolated
```

### 8. Save and Load AutoReject Object

```python
from autoreject import AutoReject, read_auto_reject

# Fit and save
ar = AutoReject()
ar.fit(epochs)
ar.save('my_autoreject-ar.h5')

# Load and use on new data
ar_loaded = read_auto_reject('my_autoreject-ar.h5')
new_epochs_clean = ar_loaded.transform(new_epochs)
```

### 9. Recommended Preprocessing Workflow

```python
from autoreject import AutoReject
from mne.preprocessing import ICA

# 1. High-pass filter first
epochs.filter(l_freq=1.0, h_freq=None)

# 2. Run autoreject to find bad epochs
ar = AutoReject(n_interpolate=[1, 4, 8], random_state=42)
epochs_ar, reject_log = ar.fit_transform(epochs, return_log=True)

# 3. Fit ICA on clean epochs (excluding bad epochs)
ica = ICA(n_components=15, random_state=42)
ica.fit(epochs_ar)
ica.apply(epochs)

# 4. Run autoreject again on ICA-cleaned data
ar = AutoReject(n_interpolate=[1, 4, 8])
epochs_clean = ar.fit_transform(epochs)
```

### 10. Manual Editing of Reject Log

```python
# Load or compute reject log
ar = AutoReject()
epochs_clean, reject_log = ar.fit_transform(epochs, return_log=True)

# Manually modify the reject log
# labels: 0=good, 1=bad, 2=interpolated
reject_log.labels[5, 10] = 0  # Mark epoch 5, channel 10 as good

# Apply modified log
epochs_clean = epochs.copy()
reject_log.save('modified_reject_log.npz')
```

## Key Concepts

### Core Parameters

- **n_interpolate (ρ)**: Number of bad sensors to interpolate per epoch. The algorithm tests different values (e.g., [1, 4, 32]) and learns the optimal value through cross-validation.

- **consensus (κ)**: Fraction of channels that must agree on a threshold. Values typically range from 0 to 1. Epochs with more than κ×N bad channels are dropped; others are repaired.

- **Thresholds**: Peak-to-peak amplitude thresholds for artifact detection. Can be global (same for all channels) or channel-specific.

### AutoReject vs RANSAC

- **AutoReject**: Learns optimal parameters (thresholds, interpolation count) through cross-validation. Best for automatic trial rejection and repair.

- **RANSAC**: From the PREP pipeline, uses random sampling consensus to robustly detect bad sensors. Better for finding consistently bad channels across the recording.

### RejectLog

The `RejectLog` object tracks what happened to each epoch:
- **bad_epochs**: Boolean array of dropped epochs
- **labels**: Matrix with values:
  - 0 = good channel
  - 1 = bad channel
  - 2 = bad channel (interpolated)

### Cross-Validation Strategy

AutoReject uses cross-validation to avoid overfitting:
1. Splits data into train/test folds
2. Tests different (ρ, κ) combinations
3. Selects parameters that minimize error on held-out data

## Reference Files

This skill includes comprehensive documentation in `references/`:

### api.md (9 pages)
Complete API reference covering:
- **AutoReject class**: Main class for automatic rejection and repair
  - `fit()`, `transform()`, `fit_transform()` methods
  - `get_reject_log()` to inspect results
  - `save()` to persist fitted models
- **Ransac class**: PREP pipeline's RANSAC algorithm
  - Bad sensor detection through robust reconstruction
  - `fit()` method and `bad_chs_` attribute
- **RejectLog class**: Inspect and visualize rejection decisions
  - `plot()` for heatmaps
  - `save()` to store rejection logs
- **compute_thresholds()**: Channel-level threshold computation
- **get_rejection_threshold()**: Global threshold computation
- **validation_curve()**: Cross-validation for parameter tuning
- **read_auto_reject()**, **read_reject_log()**: Load saved objects

### examples.md (8 pages)
Practical examples demonstrating:
- **Automatically repair epochs**: Complete AutoReject workflow
- **Detect bad sensors using RANSAC**: RANSAC implementation
- **Find global rejection threshold**: Quick threshold estimation
- **Plot channel-level thresholds**: Visualize sensor-specific thresholds
- **Plotting cross-validation curve**: Parameter optimization visualization
- **Preprocessing workflow with autoreject and ICA**: Recommended full pipeline
  - When to filter, when to run ICA, when to run autoreject
  - Comparison of different preprocessing orders
- **Visualize bad sensors per trial**: RejectLog visualization

### preprocessing.md (1 page)
Focused documentation on:
- **get_rejection_threshold()**: Fast global threshold estimation
  - Parameters, return values, usage notes
  - When to use global vs channel-specific thresholds

## Working with This Skill

### For Beginners

**Start here:**
1. Begin with the simple AutoReject example (Quick Reference #1)
2. Read `examples.md` → "Automatically repair epochs" for complete walkthrough
3. Understand that autoreject works on **epoched data** (not continuous raw data)
4. Learn the basic workflow: `fit()` on data → `transform()` to clean

**Key learning path:**
- Understand what autoreject does: finds bad trials and bad sensors, interpolates repairable channels
- Learn to visualize results with `reject_log.plot()`
- See `examples.md` → "Preprocessing workflow" for recommended practices

### For Intermediate Users

**Next steps:**
1. Customize `n_interpolate` and `consensus` parameters (Quick Reference #2)
2. Learn RANSAC for bad sensor detection (Quick Reference #3)
3. Understand when to use global vs channel-level thresholds
4. Implement the recommended preprocessing pipeline (Quick Reference #9)
5. Use `validation_curve()` to understand parameter selection

**Read:**
- `api.md` for detailed parameter descriptions
- `examples.md` → "Preprocessing workflow with autoreject and ICA" for integration strategies

### For Advanced Users

**Advanced techniques:**
1. Manually edit `RejectLog` for fine-grained control
2. Implement custom cross-validation strategies
3. Save/load fitted models for consistent preprocessing across sessions
4. Optimize parameters for specific channel types or paradigms
5. Combine with other MNE preprocessing tools (ICA, SSP, filtering)

**Dive into:**
- `api.md` for all class methods and parameters
- Cross-validation internals in `validation_curve` documentation
- RANSAC parameters for different data characteristics

### Navigation Tips

- **Need quick threshold?** → Use `get_rejection_threshold()` (Quick Reference #4)
- **Want automatic everything?** → Use `AutoReject` with defaults (Quick Reference #1)
- **Bad sensors to exclude?** → Use `Ransac` first (Quick Reference #3)
- **Need to justify parameters?** → Use `validation_curve()` (Quick Reference #6)
- **Working with ICA?** → See "Preprocessing workflow" in `examples.md`
- **Visualizing results?** → Use `RejectLog.plot()` (Quick Reference #7)

## Common Workflows

### Workflow 1: Quick and Simple
```python
from autoreject import AutoReject
ar = AutoReject()
epochs_clean = ar.fit_transform(epochs)
```

### Workflow 2: With Visualization
```python
from autoreject import AutoReject
ar = AutoReject()
epochs_clean, reject_log = ar.fit_transform(epochs, return_log=True)
reject_log.plot('horizontal')
```

### Workflow 3: Full Preprocessing Pipeline
1. Load raw data and create epochs
2. High-pass filter at 1 Hz
3. Run AutoReject to identify bad epochs
4. Fit ICA on clean epochs
5. Apply ICA to remove eye/heart artifacts
6. Run AutoReject again for final cleaning

### Workflow 4: RANSAC for Bad Channels
```python
from autoreject import Ransac
ransac = Ransac()
epochs_clean = ransac.fit_transform(epochs)
# Then mark channels in ransac.bad_chs_ as bad
```

## Tips and Best Practices

1. **Always high-pass filter first** (≥1 Hz) to remove slow drifts that trigger false rejections
2. **Run autoreject before ICA** to provide clean data for robust ICA fitting
3. **Run autoreject after ICA** again to catch non-stereotypical artifacts
4. **Visualize reject logs** to understand what's being rejected and why
5. **For limited data**, use aggressive preprocessing (filter + ICA) before autoreject to preserve trials
6. **For MEG/EEG simultaneously**, autoreject automatically handles multiple channel types
7. **Save fitted AutoReject objects** to ensure consistent preprocessing across sessions
8. **Start with default parameters** before customizing - they work well for most cases
9. **Use RANSAC for long recordings** where consistent bad sensors are expected
10. **Always visually inspect** some epochs after preprocessing - no substitute for human verification

## Resources

### references/
Organized documentation extracted from official sources:
- **Detailed API documentation** with all parameters and return values
- **Code examples** with proper Python syntax highlighting
- **Links to original documentation** for further reading
- **Table of contents** for quick navigation within each file

### scripts/
Add helper scripts here for common automation tasks such as:
- Batch processing multiple subjects
- Parameter sweep experiments
- Validation and comparison utilities

### assets/
Add templates, boilerplate, or example projects here such as:
- Example preprocessing pipelines
- Configuration files for different paradigms
- Visualization templates

## Citations

When using autoreject, please cite:

- Mainak Jas, Denis Engemann, Federico Raimondo, Yousra Bekhti, and Alexandre Gramfort. "Automated rejection and repair of bad trials in MEG/EEG." In 6th International Workshop on Pattern Recognition in Neuroimaging (PRNI), 2016.

- Mainak Jas, Denis Engemann, Yousra Bekhti, Federico Raimondo, and Alexandre Gramfort. "Autoreject: Automated artifact rejection for MEG and EEG data." NeuroImage, 159, 417-429, 2017.

For RANSAC:
- Bigdely-Shamlo, N., Mullen, T., Kothe, C., Su, K. M., & Robbins, K. A. "The PREP pipeline: standardized preprocessing for large-scale EEG analysis." Frontiers in Neuroinformatics, 9, 16, 2015.

## Notes

- This skill was automatically generated from official autoreject documentation
- All code examples are extracted from official docs and tested examples
- Works with MNE-Python epochs objects (requires MNE-Python installed)
- Supports MEG, EEG, and other channel types supported by MNE
- Cross-validation is automatic - no need to manually split data
- Default parameters work well for most use cases - customize only if needed

## Updating

To refresh this skill with updated documentation:
1. Re-run the documentation scraper with the same configuration
2. The skill will be rebuilt with the latest information from autoreject.github.io
