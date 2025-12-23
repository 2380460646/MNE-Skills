---
name: mne-core
description: MNE-Python core documentation for MEG/EEG neurophysiological data analysis. Covers preprocessing, source estimation, time-frequency analysis, statistics, machine learning, visualization, and artifact rejection.
---

# MNE-Core Skill

Comprehensive assistance with MNE-Python development for MEG/EEG analysis, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:

- **Loading MEG/EEG data** from various formats (FIF, EDF, BrainVision, EEGLAB, etc.)
- **Preprocessing** neurophysiological data (filtering, artifact rejection, epoching)
- **Time-frequency analysis** (spectrograms, ERDS maps, cross-spectral density)
- **Source localization** and inverse solutions (MNE, dSPM, sLORETA, eLORETA, beamformers)
- **Statistical analysis** on sensor or source space data
- **Visualizing** MEG/EEG data, topographies, or source estimates
- **Machine learning/decoding** on neural data
- **Computing forward models** and head models (BEM, sphere models)
- **Working with Epochs, Evoked, or Raw objects**
- **Signal-space projection (SSP)** or ICA for artifact removal
- **Setting up MNE-Python** environments or troubleshooting installations

## Key Concepts

### Core Data Structures
- **Raw**: Continuous MEG/EEG data with methods for filtering, visualization
- **Epochs**: Segmented data around events (trials)
- **Evoked**: Averaged data across epochs (ERPs/ERFs)
- **SourceEstimate (stc)**: Source-localized brain activity
- **Info**: Metadata about channels, sampling rate, etc.

### Important Units
MNE-Python standardizes all data to SI units internally:
- **EEG/EOG/ECG**: Volts
- **MEG magnetometers**: Teslas
- **MEG gradiometers**: Teslas/meter
- **Source estimates**: Amperes·meter

### Coordinate Systems
- **Head coordinates**: Defined by fiducial points (nasion, LPA, RPA)
- **Device coordinates**: MEG sensor array coordinates
- **MRI coordinates**: FreeSurfer surface RAS
- Transformations computed via coregistration

## Quick Reference

### Example 1: Loading and Basic Preprocessing

```python
import mne

# Load raw data
raw = mne.io.read_raw_fif('sample_audvis_raw.fif', preload=True)

# Filter the data (0.1-40 Hz bandpass)
raw.filter(l_freq=0.1, h_freq=40)

# Plot the data
raw.plot(duration=60, start=0)
```

### Example 2: Creating Epochs from Events

```python
# Find events in the data
events = mne.find_events(raw)

# Define epoch parameters
event_id = {'auditory/left': 1, 'auditory/right': 2}
tmin, tmax = -0.2, 0.5

# Create epochs
epochs = mne.Epochs(
    raw, events, event_id,
    tmin, tmax,
    baseline=(None, 0),
    reject=dict(eeg=100e-6),  # reject trials with large artifacts
    preload=True
)

# Average to get evoked response
evoked = epochs.average()
evoked.plot()
```

### Example 3: Time-Frequency Analysis

```python
# Compute power spectral density
epochs.compute_psd().plot()

# Compute time-frequency representation
freqs = np.arange(5, 40, 1)  # frequencies from 5-40 Hz
n_cycles = freqs / 2.  # different number of cycles per frequency

power = mne.time_frequency.tfr_morlet(
    epochs, freqs=freqs, n_cycles=n_cycles,
    return_itc=False, average=True
)
power.plot()
```

### Example 4: Computing Forward Solution

```python
# Set up source space
src = mne.setup_source_space(
    'sample', spacing='oct6',
    subjects_dir=subjects_dir
)

# Compute BEM model
conductivity = (0.3, 0.006, 0.3)  # for skull and scalp
model = mne.make_bem_model(
    subject='sample', ico=4,
    conductivity=conductivity,
    subjects_dir=subjects_dir
)
bem_sol = mne.make_bem_solution(model)

# Compute forward solution
fwd = mne.make_forward_solution(
    raw.info, trans='sample-trans.fif',
    src=src, bem=bem_sol,
    meg=True, eeg=True
)
```

### Example 5: Minimum-Norm Inverse Solution

```python
# Compute noise covariance
noise_cov = mne.compute_covariance(
    epochs, tmax=0.,  # use baseline period
    method='shrunk'
)

# Create inverse operator
inverse_operator = mne.minimum_norm.make_inverse_operator(
    raw.info, fwd, noise_cov,
    loose=0.2, depth=0.8
)

# Apply inverse to evoked data
method = "dSPM"
snr = 3.
lambda2 = 1. / snr ** 2
stc = mne.minimum_norm.apply_inverse(
    evoked, inverse_operator, lambda2,
    method=method, pick_ori=None
)

# Visualize on brain
stc.plot(
    subjects_dir=subjects_dir,
    initial_time=0.1, hemi='both',
    clim=dict(kind='percent', lims=[90, 95, 99])
)
```

### Example 6: Signal-Space Projection (SSP) for Artifacts

```python
# Compute ECG projectors
ecg_projs, ecg_events = mne.preprocessing.compute_proj_ecg(
    raw, n_grad=1, n_mag=1, n_eeg=1,
    average=True
)

# Compute EOG projectors
eog_projs, eog_events = mne.preprocessing.compute_proj_eog(
    raw, n_grad=1, n_mag=1, n_eeg=1,
    average=True
)

# Add projectors to raw data
raw.add_proj(ecg_projs + eog_projs)

# Apply projectors
raw.apply_proj()
```

### Example 7: Beamformer Source Localization

```python
from mne.beamformer import make_lcmv, apply_lcmv

# Compute covariance matrices
data_cov = mne.compute_covariance(
    epochs, tmin=0.04, tmax=0.15,
    method='empirical'
)
noise_cov = mne.compute_covariance(
    epochs, tmin=-0.2, tmax=0,
    method='empirical'
)

# Make LCMV beamformer
filters = make_lcmv(
    epochs.info, fwd, data_cov,
    reg=0.05, noise_cov=noise_cov,
    pick_ori='max-power'
)

# Apply beamformer to evoked data
stc = apply_lcmv(evoked, filters)
stc.plot(subjects_dir=subjects_dir)
```

### Example 8: Statistical Analysis with Permutation Test

```python
from mne.stats import permutation_cluster_test

# Compare two conditions
X = [epochs['condition_1'].get_data(),
     epochs['condition_2'].get_data()]

# Run cluster-based permutation test
T_obs, clusters, cluster_p_values, H0 = permutation_cluster_test(
    X, n_permutations=1000,
    threshold=None, tail=0, n_jobs=1
)

# Visualize significant clusters
evoked_diff = epochs['condition_1'].average() - epochs['condition_2'].average()
evoked_diff.plot_image(
    mask=(cluster_p_values < 0.05).any(axis=0)
)
```

### Example 9: Machine Learning - Decoding

```python
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from mne.decoding import Vectorizer, cross_val_multiscore

# Create sklearn pipeline
clf = make_pipeline(
    Vectorizer(),
    StandardScaler(),
    LogisticRegression(solver='liblinear')
)

# Get data and labels
X = epochs.get_data()
y = epochs.events[:, 2]

# Cross-validation
scores = cross_val_multiscore(clf, X, y, cv=5, n_jobs=1)
print(f"Accuracy: {scores.mean():.2f} +/- {scores.std():.2f}")
```

### Example 10: Working with Metadata

```python
# Create metadata from events
metadata, events, event_id = mne.epochs.make_metadata(
    events=events,
    event_id=event_id,
    tmin=-0.2, tmax=1.5,
    sfreq=raw.info['sfreq'],
    keep_first='stimulus'
)

# Create epochs with metadata
epochs = mne.Epochs(
    raw, events, event_id,
    tmin=-0.2, tmax=0.5,
    metadata=metadata,
    preload=True
)

# Query epochs using pandas-style queries
fast_epochs = epochs['response_time < 0.5']
correct_epochs = epochs['correct == True']
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

### examples.md
Contains practical examples covering:
- **Statistical analysis**: Sensor regression, permutation tests, clustering
- **Dataset tutorials**: Brainstorm, ERP-CORE, and other public datasets
- **Simulation**: Creating simulated data and comparing with estimates
- **Time-frequency**: ERDS maps, spectral analysis, cross-spectral density
- **Inverse solutions**: MNE, dSPM, beamformers (LCMV, DICS)
- **Decoding**: Machine learning applications on neural data

### installation.md
Detailed installation guides:
- **Advanced setup**: Jupyter integration, Qt backends, GPU acceleration
- **IDE integration**: VSCode, Spyder, PyCharm configuration
- **FreeSurfer setup**: For anatomical processing
- **MNE-C installation**: Legacy C tools (if needed)
- **Troubleshooting**: Common installation issues

### inverse.md
Deep technical documentation:
- **Algorithm details**: Mathematical foundations of inverse methods
- **Forward modeling**: BEM, sphere models, coordinate systems
- **Minimum-norm estimates**: Theory and implementation
- **Source space creation**: Surface and volumetric source spaces
- **Covariance computation**: Noise covariance, regularization
- **Morphing**: Aligning source estimates across subjects

### tutorials.md (if available)
Step-by-step tutorials for:
- Getting started with MNE-Python
- Complete analysis pipelines
- Preprocessing workflows
- Source reconstruction tutorials

## Working with This Skill

### For Beginners
1. **Start with basic I/O**: Load data using `mne.io.read_raw_*` functions
2. **Explore your data**: Use `.plot()` methods on Raw, Epochs, Evoked objects
3. **Learn preprocessing**: Filtering (`raw.filter()`), epoching, averaging
4. **Check examples.md**: Look for dataset examples matching your data type

### For Intermediate Users
1. **Time-frequency analysis**: Use `mne.time_frequency` module for spectrograms, ERDS
2. **Artifact rejection**: Implement SSP or ICA for cleaning
3. **Source localization basics**: Start with minimum-norm estimates
4. **Statistical testing**: Apply cluster permutation tests
5. **Reference inverse.md**: For coordinate systems and forward modeling details

### For Advanced Users
1. **Custom beamformers**: Explore LCMV, DICS variants in `mne.beamformer`
2. **Advanced decoding**: Use CSP, temporal decoding, searchlight analysis
3. **Morphing & group analysis**: Average source estimates across subjects
4. **Custom metrics**: Implement new analysis methods using MNE data structures
5. **Dive into inverse.md**: Understand mathematical foundations

### Navigation Tips
- Use **Ctrl+F** to search for specific functions or concepts in reference files
- **examples.md** has ~106 pages of practical code - great for learning patterns
- **inverse.md** has ~515 pages of technical details - reference when needed
- Check function signatures in examples before using in your code

## Common Workflows

### Basic ERP Analysis
1. Load raw data → Filter → Find events → Create epochs → Average → Plot

### Source Localization
1. Coregister MRI ↔ MEG → Compute forward solution → Compute noise covariance → Create inverse operator → Apply to evoked/epochs → Visualize on brain

### Time-Frequency Analysis
1. Load data → Epoch → Compute TFR (Morlet/multitaper) → Average → Plot → Statistical testing

### Artifact Removal
1. Detect artifacts (ECG/EOG) → Compute SSP projectors OR fit ICA → Apply/remove components → Verify cleaning

## Important Functions by Category

### Data I/O
- `mne.io.read_raw_fif()`, `read_raw_edf()`, `read_raw_brainvision()`
- `mne.read_epochs()`, `mne.read_evoked()`
- `raw.save()`, `epochs.save()`, `evoked.save()`

### Preprocessing
- `raw.filter()`, `raw.resample()`, `raw.notch_filter()`
- `mne.Epochs()`, `epochs.drop_bad()`, `epochs.average()`
- `raw.set_eeg_reference()`, `raw.set_montage()`

### Artifact Handling
- `mne.preprocessing.ICA()`
- `mne.preprocessing.compute_proj_ecg()`, `compute_proj_eog()`
- `raw.interpolate_bads()`

### Time-Frequency
- `mne.time_frequency.tfr_morlet()`, `tfr_multitaper()`
- `epochs.compute_psd()`, `raw.compute_psd()`
- `mne.time_frequency.csd_fourier()`, `csd_morlet()`

### Source Analysis
- `mne.setup_source_space()`, `mne.make_bem_model()`
- `mne.make_forward_solution()`
- `mne.minimum_norm.make_inverse_operator()`, `apply_inverse()`
- `mne.beamformer.make_lcmv()`, `apply_lcmv()`

### Statistics
- `mne.stats.permutation_cluster_test()`
- `mne.stats.spatio_temporal_cluster_test()`
- `mne.stats.linear_regression()`

### Visualization
- `.plot()` - available on most objects
- `.plot_topomap()`, `.plot_image()`, `.plot_joint()`
- `stc.plot()` - for source estimates

## Best Practices

1. **Always use preload=True** when you need to filter or modify data
2. **Set random seeds** for reproducibility in permutation tests
3. **Validate artifact rejection** by plotting before/after
4. **Check coordinate systems** when computing forward solutions
5. **Use baseline correction** appropriately for ERPs
6. **Save intermediate results** (e.g., cleaned raw, inverse operators)
7. **Apply SSP projectors** when creating epochs for efficiency

## Resources

- **Official documentation**: https://mne.tools/
- **MNE Forum**: https://mne.discourse.group/
- **GitHub Issues**: https://github.com/mne-tools/mne-python/issues
- **Tutorials**: https://mne.tools/stable/auto_tutorials/index.html
- **Examples Gallery**: https://mne.tools/stable/auto_examples/index.html

## Notes

- This skill was automatically generated from official MNE-Python documentation
- Reference files preserve structure and examples from source docs
- Code examples include proper syntax highlighting
- Quick reference patterns extracted from common usage examples
- Internal units are always SI (Volts, Tesla, etc.) - plotting functions auto-scale

## Updating

To refresh this skill with updated documentation:
1. Re-run the documentation scraper with the same configuration
2. The skill will be rebuilt with the latest information from mne.tools
