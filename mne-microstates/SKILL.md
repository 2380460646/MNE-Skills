---
name: mne-microstates
description: MNE-Microstates GitHub repository for microstate analysis in EEG data. Provides tools for clustering, segmentation, and analysis of EEG microstates.
---

# mne_microstates

Microstate analysis for use with MNE-Python. This module enables segmentation and analysis of EEG/MEG data into microstates - brief periods of stable topographic patterns that represent functional brain states.

## Description

**Repository:** [wmvanvliet/mne_microstates](https://github.com/wmvanvliet/mne_microstates)
**Language:** Python
**Stars:** 55
**License:** BSD 3-Clause "New" or "Revised" License

Microstate analysis segments continuous EEG/MEG data into discrete brain states characterized by stable topographic patterns. This implementation uses modified K-means clustering on Global Field Power (GFP) peaks to identify microstate maps, then segments the entire time series based on these maps.

**Key Reference:**
Pascual-Marqui, R. D., Michel, C. M., & Lehmann, D. (1995). Segmentation of brain electrical activity into microstates: model estimation and validation. IEEE Transactions on Biomedical Engineering.

## When to Use This Skill

Use this skill when you need to:

**Specific Trigger Conditions:**
- Perform **microstate clustering** or **segmentation** on EEG/MEG data
- Analyze **brain state dynamics** or **functional connectivity** patterns
- Extract **microstate maps** from continuous neural recordings
- Calculate **microstate statistics** (duration, occurrence, coverage, GEV)
- Visualize **topographic microstate patterns** or **state sequences**
- Work with **MNE-Python raw/epochs objects** for microstate analysis
- Compare **single-subject vs. group-level** microstate analysis

**You Should NOT Use This Skill For:**
- General MNE-Python operations (use main MNE documentation)
- Event-related potential (ERP) analysis
- Source localization or beamforming
- Time-frequency analysis

## Key Concepts

### Microstate Analysis
**Microstates** are brief periods (typically 80-120ms) of quasi-stable EEG topography that represent functional brain states. The analysis involves:

1. **Global Field Power (GFP):** Spatial standard deviation at each time point, used to identify peaks
2. **Clustering:** Modified K-means clustering on GFP peaks to extract prototypical microstate maps
3. **Segmentation:** Assignment of each time point to the best-fitting microstate map
4. **Statistics:** Duration, occurrence rate, coverage, and global explained variance (GEV)

### Important Terms
- **GFP (Global Field Power):** Measure of overall field strength at each time point
- **Microstate Maps:** Prototypical topographic patterns (typically 3-7 states)
- **Segmentation:** Time series indicating which microstate is active at each sample
- **GEV (Global Explained Variance):** Percentage of variance explained by microstate model

## Quick Reference

### 1. Installation

```python
# Using pip
pip install mne-microstates

# Using conda
conda install -c conda-forge mne-microstates
```

### 2. Basic Import and Setup

```python
import mne
import mne_microstates

# Load your EEG data
raw = mne.io.read_raw_fif('your_data.fif', preload=True)

# CRITICAL: Always use average reference for microstate analysis
raw.set_eeg_reference('average')

# Highpass filter (recommended: 0.2-2 Hz)
raw.filter(0.2, None)

# Select only EEG channels
raw.pick_types(meg=False, eeg=True)
```

### 3. Core Workflow: Segment into Microstates

```python
# Segment data into 6 microstates (typical range: 3-7)
maps, segmentation = mne_microstates.segment(raw.get_data(), n_states=6)

# maps: (n_states, n_channels) - topographic patterns
# segmentation: (n_samples,) - state at each time point
```

### 4. Visualize Microstate Topographies

```python
# Plot the topographic maps of discovered microstates
mne_microstates.plot_maps(maps, raw.info)

# Each map shows the spatial distribution of one microstate
```

### 5. Visualize State Sequence Over Time

```python
# Plot segmentation for the first 500 samples
mne_microstates.plot_segmentation(
    segmentation[:500],
    raw.get_data()[:, :500],
    raw.times[:500]
)

# Shows which microstate is active at each time point
```

### 6. Complete Analysis Pipeline

```python
import mne
import mne_microstates
from mne.datasets import sample

# Load MNE sample dataset
fname = sample.data_path() / 'MEG/sample/sample_audvis_filt.fif'
raw = mne.io.read_raw_fif(fname, preload=True)

# Preprocessing for microstate analysis
raw.set_eeg_reference('average')  # Average reference is essential
raw.filter(0.2, None)              # Highpass filter
raw.pick_types(meg=False, eeg=True)  # EEG only

# Perform segmentation
maps, segmentation = mne_microstates.segment(raw.get_data(), n_states=6)

# Visualize results
mne_microstates.plot_maps(maps, raw.info)
mne_microstates.plot_segmentation(
    segmentation[:500],
    raw.get_data()[:, :500],
    raw.times[:500]
)
```

### 7. Working with Different Numbers of States

```python
# Try different numbers of microstates
for n_states in [3, 4, 5, 6, 7]:
    maps, segmentation = mne_microstates.segment(
        raw.get_data(),
        n_states=n_states
    )
    print(f"Segmented into {n_states} microstates")
```

### 8. Extract Data for Custom Analysis

```python
# Get microstate maps and segmentation
maps, segmentation = mne_microstates.segment(raw.get_data(), n_states=6)

# maps shape: (n_states, n_channels)
# segmentation shape: (n_samples,)

# Calculate microstate statistics manually
import numpy as np
unique_states, counts = np.unique(segmentation, return_counts=True)
coverage = counts / len(segmentation) * 100

print("Microstate coverage (%):", coverage)
```

## Available Reference Files

### `references/README.md`
Complete installation instructions, usage examples, and main workflow. **Start here** for:
- Installation methods (pip, conda)
- Complete code example with MNE sample dataset
- Main API usage (segment, plot_maps, plot_segmentation)
- Citation information

### `references/file_structure.md`
Repository structure (only 6 files total). Useful for:
- Understanding the simple module architecture
- Locating the main module: `mne_microstates.py`
- Finding the example script: `example.py`

### `references/issues.md`
GitHub issues (11 total: 2 open, 9 closed). Check for:
- Known plotting issues (#10: "Unable to plot")
- Analysis methodology questions (#11: "Single subject or group analysis?")
- Historical GFP calculation discussions (#4, #6)
- Segmentation and plotting troubleshooting (#9, #1)

### `references/releases.md`
Version history (2 releases). Important notes:
- **v0.3 (2022-03-09):** Module renamed from `microstates` to `mne_microstates` (update imports!)
- **v0.2 (2022-03-08):** First pip-installable version

## Working with This Skill

### For Beginners
1. **Start with the complete example** in Quick Reference #6
2. **Understand preprocessing requirements:** Average reference and highpass filtering are essential
3. **Use the MNE sample dataset** to test the workflow before applying to your data
4. **Start with 4-6 microstates** (most common in literature)
5. **Check `references/README.md`** for the canonical usage pattern

### For Intermediate Users
1. **Experiment with different n_states** (typically 3-7) to find optimal clustering
2. **Extract segmentation data** for custom statistics (duration, transitions)
3. **Check `references/issues.md`** for common problems:
   - Plotting issues may require specific MNE/matplotlib versions
   - GFP normalization questions addressed in issues #5, #6
4. **Calculate Global Explained Variance (GEV)** to evaluate model quality
5. **Apply to epochs** instead of continuous data for event-related microstate analysis

### For Advanced Users
1. **Group-level analysis:** Extract individual maps, then cluster across subjects
2. **Custom metrics:** Use segmentation output for transition analysis or entropy measures
3. **Integration with other analyses:** Combine with connectivity or source localization
4. **Method validation:** Review issue #4 for GFP and segmentation calculation details
5. **Contribute:** The repository is small and active - see issues for enhancement ideas

### Common Workflows

**Single-Subject Analysis:**
```python
# 1. Load and preprocess
raw.set_eeg_reference('average').filter(0.2, None).pick_types(eeg=True)

# 2. Segment
maps, seg = mne_microstates.segment(raw.get_data(), n_states=4)

# 3. Visualize
mne_microstates.plot_maps(maps, raw.info)
```

**Group-Level Analysis:**
```python
# 1. Extract maps from each subject
subject_maps = []
for subject_raw in subject_list:
    maps, _ = mne_microstates.segment(subject_raw.get_data(), n_states=4)
    subject_maps.append(maps)

# 2. Cluster across subjects (requires custom implementation)
# Concatenate all maps and re-cluster to get group templates
```

## Important Notes

### Critical Preprocessing Steps
1. **Average reference is mandatory** - microstate analysis requires reference-free data
2. **Highpass filtering recommended** (0.2-2 Hz) - removes slow drifts
3. **Use only EEG channels** - MEG and EEG have different topographies
4. **Data must be preloaded** - operations work on NumPy arrays

### Known Issues (as of v0.3)
- **Plotting functions** may have compatibility issues with some MNE/matplotlib versions (#10)
- **Single vs. group analysis** methodology not explicitly documented (#11)
- **Module naming:** Ensure you import `mne_microstates` (not `microstates`) for v0.3+

### Function Return Values
The main `segment()` function returns:
- **maps:** (n_states, n_channels) array of microstate topographies
- **segmentation:** (n_samples,) array of state labels at each time point
- **GEV (Global Explained Variance):** Can be returned depending on version

## Version Information

- **Current Version:** 0.3 (2022-03-09)
- **Important Change:** Module renamed from `microstates` to `mne_microstates` in v0.3
- **Installation:** Available via pip and conda-forge
- **Last Repository Update:** 2025-11-27
- **Open Issues:** 2
- **Python Version:** 100% Python

## Contributors

- Marijn van Vliet (w.m.vanvliet@gmail.com) - Lead developer
- Kishi Bayes
- Liu Ruixiang


