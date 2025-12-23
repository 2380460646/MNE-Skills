---
name: mne-icalabel
description: MNE-ICALabel documentation for automatic Independent Component Analysis (ICA) labeling. Helps identify and classify ICA components as brain, muscle, eye, heart, line noise, or other artifacts.
---

# Mne-Icalabel Skill

Comprehensive assistance with mne-icalabel for automatic ICA component classification in EEG/MEG data.

## When to Use This Skill

This skill should be triggered when working with:
- **Automatic ICA artifact labeling** - Using ICLabel or MEGNet to classify ICA components
- **ICA component classification** - Identifying brain vs. artifact components (eye blinks, muscle, heart, line noise)
- **EEG artifact removal** - Cleaning EEG data using ICA decomposition
- **MEG artifact removal** - Cleaning MEG data using MEGNet
- **GUI-based component annotation** - Labeling ICA components interactively
- **BIDS-compliant ICA annotation** - Saving component labels in TSV format
- **Feature extraction** - Getting topomaps, PSDs, or autocorrelation features from ICA

Specific use cases:
- "How do I automatically label ICA components?"
- "Remove eye blink artifacts using ICA"
- "Classify ICA components with ICLabel"
- "Use MEGNet for MEG artifact removal"
- "Save ICA component labels to BIDS format"
- "Extract features from ICA decomposition"

## Key Concepts

### ICA Component Classification
MNE-ICALabel automatically classifies Independent Components into 7 categories:
- **brain** - Neural activity
- **muscle artifact** - Muscle movements
- **eye blink** - Eye blink artifacts
- **heart beat** - Cardiac artifacts (ECG)
- **line noise** - Power line interference
- **channel noise** - Bad channel artifacts
- **other** - Unclassifiable components

### Models Available

**ICLabel** (for EEG):
- Requires extended infomax ICA decomposition
- Data should be average-referenced and filtered [1-100] Hz
- Uses topomaps, PSD, and autocorrelation features
- Originated from EEGLab

**MEGNet** (for MEG):
- Designed specifically for MEG data
- Uses spatiotemporal CNNs
- Classifies into: brain/other, eye movement, heart beat, eye blink

### Preprocessing Requirements

For ICLabel to work optimally:
1. Apply high-pass filter (1 Hz minimum)
2. Apply low-pass filter (100 Hz maximum)
3. Set average reference for EEG
4. Use extended infomax method for ICA

## Quick Reference

### 1. Basic Automatic ICA Labeling (ICLabel)

```python
import mne
from mne.preprocessing import ICA
from mne_icalabel import label_components

# Load and preprocess data
raw = mne.io.read_raw_fif('sample_raw.fif')
raw.crop(tmax=60.0).pick_types(eeg=True, stim=True, eog=True)
raw.load_data()

# Filter data (ICLabel requirement: 1-100 Hz)
filt_raw = raw.copy().filter(l_freq=1.0, h_freq=100.0)

# Set average reference (ICLabel requirement)
filt_raw = filt_raw.set_eeg_reference("average")

# Fit ICA with extended infomax (ICLabel requirement)
ica = ICA(
    n_components=15,
    max_iter="auto",
    method="infomax",
    random_state=97,
    fit_params=dict(extended=True)
)
ica.fit(filt_raw)

# Automatically label components
ic_labels = label_components(filt_raw, ica, method="iclabel")
print(ic_labels["labels"])
```

### 2. Exclude Artifacts and Reconstruct Data

```python
from mne_icalabel import label_components

# Label components automatically
ic_labels = label_components(filt_raw, ica, method="iclabel")

# Extract labels and exclude non-brain components
labels = ic_labels["labels"]
exclude_idx = [
    idx for idx, label in enumerate(labels)
    if label not in ["brain", "other"]
]
print(f"Excluding these ICA components: {exclude_idx}")

# Reconstruct clean data
reconst_raw = raw.copy()
ica.apply(reconst_raw, exclude=exclude_idx)
```

### 3. GUI-Based Component Labeling

```python
from mne.preprocessing import ICA
from mne_icalabel.gui import label_ica_components

# Filter and fit ICA first
filt_raw = raw.copy().filter(l_freq=1.0, h_freq=None)
ica = ICA(n_components=15, max_iter="auto", random_state=97)
ica.fit(filt_raw)

# Launch GUI (modifies ica.labels_ in-place)
gui = label_ica_components(raw, ica)

# After closing GUI, labels are stored in ica.labels_
print(ica.labels_)
# {'brain': [], 'muscle': [], 'eog': [], 'ecg': [],
#  'line_noise': [], 'ch_noise': [], 'other': []}
```

### 4. Save Component Labels to BIDS Format

```python
from mne_icalabel.annotation import write_components_tsv

# After labeling components (GUI or automatic)
fname = 'derivatives/sub-01/eeg/sub-01_task-rest_components.tsv'
write_components_tsv(ica, fname)
```

### 5. Manual Component Marking

```python
from mne_icalabel.annotation import mark_component

# Manually mark a specific component
fname = 'derivatives/sub-01/eeg/sub-01_task-rest_components.tsv'
mark_component(
    component=0,
    fname=fname,
    method='manual',
    label='eye blink',
    author='researcher_name'
)
```

### 6. MEGNet for MEG Data

```python
from mne_icalabel.megnet import megnet_label_components

# Load MEG data
raw = mne.io.read_raw_fif('meg_sample.fif')
raw.crop(tmax=60.0).pick_types(meg='mag')
raw.load_data()

# Filter and fit ICA
filt_raw = raw.copy().filter(l_freq=1.0, h_freq=None)
ica = ICA(n_components=15, max_iter="auto")
ica.fit(filt_raw)

# Label components with MEGNet
ic_labels = megnet_label_components(raw, ica)
```

### 7. Extract ICLabel Features

```python
from mne_icalabel.iclabel import get_iclabel_features

# Get features used by ICLabel network
images, psds, autocorr = get_iclabel_features(filt_raw, ica)

# images: topomap features
# psds: power spectral density features
# autocorr: autocorrelation features
```

### 8. Visualize Component Properties

```python
# Visualize specific components before excluding
ica.plot_properties(raw, picks=[0, 12])

# Plot component topographies
ica.plot_components()

# Plot component time series
ica.plot_sources(raw, show_scrollbars=False)

# Overlay excluded components on data
ica.plot_overlay(raw, exclude=[0], picks="eeg")
```

### 9. Get Component Probabilities

```python
from mne_icalabel import label_components

# Get probability scores for each component
ic_labels = label_components(filt_raw, ica, method="iclabel")

# Access probability matrix
# Columns: brain, muscle, eye blink, heart, line noise, channel noise, other
probs = ic_labels["y_pred_proba"]
print(f"Component 0 probabilities: {probs[0]}")

# Get labels
labels = ic_labels["labels"]
print(f"Component 0 classified as: {labels[0]}")
```

### 10. Complete Workflow Example

```python
import mne
from mne.preprocessing import ICA
from mne_icalabel import label_components

# 1. Load data
raw = mne.io.read_raw_fif('sample.fif')
raw.crop(tmax=60.0).pick_types(eeg=True, eog=True)
raw.load_data()

# 2. Filter (1-100 Hz for ICLabel)
filt_raw = raw.copy().filter(l_freq=1.0, h_freq=100.0)
filt_raw.set_eeg_reference("average")

# 3. Fit ICA with extended infomax
ica = ICA(
    n_components=15,
    method="infomax",
    fit_params=dict(extended=True),
    random_state=97
)
ica.fit(filt_raw)

# 4. Automatically label components
ic_labels = label_components(filt_raw, ica, method="iclabel")

# 5. Exclude artifacts (keep only brain and other)
labels = ic_labels["labels"]
exclude_idx = [
    idx for idx, label in enumerate(labels)
    if label not in ["brain", "other"]
]

# 6. Apply ICA to clean data
clean_raw = raw.copy()
ica.apply(clean_raw, exclude=exclude_idx)
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

### examples.md
Complete working examples from official documentation:
- **Automatic artifact repair with ICLabel** - Full workflow for EEG artifact removal
- **GUI component labeling** - Interactive annotation interface
- Preprocessing steps and visualization
- Component exclusion and reconstruction
- Code examples with expected output

### installation.md
Installation instructions and dependencies:
- **PyPI installation** - `pip install mne-icalabel`
- **Conda installation** - `conda install -c conda-forge mne-icalabel`
- **Backend options** - PyTorch vs ONNX runtime
- **GUI dependencies** - Qt installation (PyQt5/6 or PySide2/6)
- **MEGNet requirements** - onnxruntime for MEG analysis
- MNE-Python version requirements

## Working with This Skill

### For Beginners
1. Start with **installation.md** to set up dependencies
2. Review the **Complete Workflow Example** above (#10)
3. Read **examples.md** for detailed step-by-step tutorials
4. Focus on ICLabel for EEG or MEGNet for MEG data

### For Intermediate Users
1. Use **automatic labeling** (examples #1-2) for standard workflows
2. Explore **component visualization** (#8) to understand classifications
3. Review **probability scores** (#9) for confidence thresholds
4. Implement **BIDS-compliant saving** (#4) for reproducibility

### For Advanced Users
1. Extract **custom features** (#7) for model training
2. Implement **manual annotation** workflows (#5)
3. Combine **automatic + GUI** approaches for hybrid workflows
4. Use **MEGNet** for specialized MEG analysis (#6)

### Common Workflows

**Quick EEG Cleaning:**
```
Load data → Filter (1-100 Hz) → Set reference → Fit ICA → Label components → Exclude artifacts
```

**Manual Review Workflow:**
```
Load data → Filter → Fit ICA → GUI labeling → Save to BIDS → Apply exclusions
```

**MEG Workflow:**
```
Load MEG → Filter → Fit ICA → MEGNet labeling → Exclude artifacts → Save
```

## Important Notes

### ICLabel Requirements
- **Filtering:** Data should be bandpass filtered [1-100] Hz
- **Reference:** EEG should use average reference
- **ICA Method:** Use extended infomax algorithm
- **Performance:** Deviating from these specs may reduce accuracy

### GUI Requirements
- Requires Qt installation (PyQt5/6 or PySide2/6)
- Install separately: `pip install PyQt5` or `pip install PyQt6`
- GUI is in beta - may contain bugs or breaking changes

### BIDS Derivatives
- TSV component saving is experimental
- BIDS-EEG-Derivatives spec is not finalized
- API may change in future versions

### Backend Selection
- **PyTorch:** Better for GPU acceleration
- **ONNX Runtime:** Lighter weight, CPU-friendly
- ICLabel works with both backends
- MEGNet requires ONNX Runtime

## Troubleshooting

**Q: ICLabel gives poor results**
- Check filtering: must be 1-100 Hz
- Verify average reference is applied
- Ensure extended infomax ICA is used
- Use enough components (15+ recommended)

**Q: GUI won't launch**
- Install Qt: `pip install PyQt5` or `pip install PyQt6`
- Check compatibility with your OS
- Try different Qt backend (PyQt vs PySide)

**Q: MEGNet not working**
- Install onnxruntime: `pip install onnxruntime`
- Verify you're using MEG data (not EEG)
- Check data shape and channels

## Citation

If you use MNE-ICALabel, please cite:

**ICLabel:**
Pion-Tonachini, L., Kreutz-Delgado, K., & Makeig, S. (2019). ICLabel: An automated electroencephalographic independent component classifier, dataset, and website. *NeuroImage*, 198, 181-197. doi:10.1016/j.neuroimage.2019.05.026

**MEGNet:**
Treacher, A.H., et al. (2021). MEGnet: Automatic ICA-based artifact removal for MEG using spatiotemporal convolutional neural networks. *NeuroImage*, 241, 118402. doi:10.1016/j.neuroimage.2021.118402
