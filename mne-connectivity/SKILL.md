---
name: mne-connectivity
description: MNE-Connectivity documentation for functional and effective connectivity analysis in MEG/EEG data. Covers coherence, phase-locking, granger causality, and connectivity visualization.
---

# MNE-Connectivity Skill

Comprehensive assistance with MNE-Connectivity development, providing expert guidance on connectivity analysis for MEG/EEG data.

## When to Use This Skill

Trigger this skill when:
- Computing connectivity between MEG/EEG channels or brain regions
- Analyzing phase-based connectivity (PLI, wPLI, dPLI, PLV)
- Computing coherence or imaginary coherence between signals
- Estimating multivariate connectivity (CaCoh, MIC, MIM)
- Computing Granger causality for directional connectivity
- Working with spectral or time-frequency connectivity
- Analyzing connectivity in sensor or source space
- Visualizing connectivity with circular graphs
- Computing envelope correlations or VAR models
- Debugging connectivity estimation issues

## Key Concepts

### Connectivity Measures

**Phase-Based Measures**
- **PLI (Phase Lag Index)**: Detects phase relationships, robust to volume conduction
- **wPLI (Weighted PLI)**: Improved robustness to noise and outliers
- **dPLI (Directed PLI)**: Distinguishes leading vs. lagging phase relationships
- **PLV (Phase-Locking Value)**: Measures phase synchronization

**Coherency-Based Measures**
- **Coherence (Coh)**: Magnitude of correlation in frequency domain
- **Imaginary Coherence (ImCoh)**: Immune to zero time-lag interactions (volume conduction)
- **CaCoh (Canonical Coherency)**: Multivariate coherency method
- **MIC/MIM**: Multivariate imaginary coherency methods

**Directed Measures**
- **Granger Causality (GC)**: Estimates directionality of information flow
- **Phase Slope Index (PSI)**: Direction of information flow from phase slopes

### When to Use Which Function

**spectral_connectivity_epochs()**
- Use for: Repeated trials of time-locked events (ERP data)
- Computes: Connectivity at each timepoint ACROSS trials
- Best for: High temporal resolution with multiple epochs

**spectral_connectivity_time()**
- Use for: Single trials, resting-state, or continuous data
- Computes: Connectivity OVER TIME for each epoch separately
- Best for: Time-varying connectivity within epochs

### Avoiding Volume Conduction

Methods based on **imaginary part of coherency** (ImCoh, MIC, MIM) discard zero time-lag interactions, avoiding spurious connectivity from volume conduction. Use these for:
- Connectivity within same modality (e.g., EEG-EEG)
- Same reference across signals

## Quick Reference

### Example 1: Computing PLI, wPLI, and dPLI

```python
from mne_connectivity import spectral_connectivity_epochs

# Compute multiple phase-based connectivity measures
con = spectral_connectivity_epochs(
    epochs,
    method=['pli', 'wpli', 'dpli'],
    mode='multitaper',
    fmin=8.,
    fmax=13.,
    faverage=True
)

# Access results
pli = con[0]  # PLI results
wpli = con[1]  # wPLI results
dpli = con[2]  # dPLI results

# Get connectivity data as numpy array
pli_data = pli.get_data()
```

### Example 2: Multivariate Connectivity with CaCoh

```python
from mne_connectivity import spectral_connectivity_epochs, seed_target_multivariate_indices

# Define seed and target indices for multivariate connectivity
seeds = [[0, 1, 2]]  # Channels 0, 1, 2 as seeds
targets = [[3, 4, 5]]  # Channels 3, 4, 5 as targets
indices = seed_target_multivariate_indices(seeds, targets)

# Compute canonical coherency
con = spectral_connectivity_epochs(
    epochs,
    method='cacoh',
    indices=indices,
    fmin=10.,
    fmax=30.,
    rank=([3], [3])  # Optional: specify rank for each group
)

# Extract spatial patterns showing channel contributions
patterns = con.attrs['patterns']
```

### Example 3: Time-Frequency Connectivity

```python
from mne_connectivity import spectral_connectivity_time

# Compute connectivity over time using Morlet wavelets
con = spectral_connectivity_time(
    epochs,
    freqs=np.arange(5, 40, 1),  # 5-40 Hz
    method='plv',
    mode='cwt_morlet',
    n_cycles=7,
    average=True
)

# Result shape: (n_connections, n_freqs, n_times)
data = con.get_data()
```

### Example 4: Granger Causality

```python
from mne_connectivity import spectral_connectivity_epochs

# Define directed connections (seeds -> targets)
indices = (np.array([0, 1]), np.array([2, 3]))

# Compute Granger causality
gc = spectral_connectivity_epochs(
    epochs,
    method=['gc', 'gc_tr'],  # GC and time-reversed GC
    indices=indices,
    fmin=8.,
    fmax=30.,
    gc_n_lags=20  # Number of lags for VAR model
)

# Compute time-reversed Granger causality (TRGC) for robustness
gc_forward = gc[0].get_data()
gc_reversed = gc[1].get_data()
trgc = gc_forward - gc_reversed  # Net directed connectivity
```

### Example 5: Envelope Correlation

```python
from mne_connectivity import envelope_correlation

# Compute envelope correlations with orthogonalization
con = envelope_correlation(
    epochs,
    orthogonalize='pairwise',  # Remove zero-lag correlations
    log=True  # Log-transform envelopes
)

# Returns symmetric correlation matrix
corr_matrix = con.get_data()
```

### Example 6: Connectivity in Source Space

```python
from mne_connectivity import spectral_connectivity_epochs

# First compute source estimates (stcs)
stcs = apply_inverse_epochs(epochs, inverse_operator, lambda2, method='dSPM')

# Define labels (brain regions)
labels = mne.read_labels_from_annot('fsaverage', 'aparc')

# Compute connectivity between labels
con = spectral_connectivity_epochs(
    stcs,
    method='pli',
    mode='multitaper',
    fmin=8.,
    fmax=13.,
    faverage=True
)
```

### Example 7: Visualizing Connectivity

```python
from mne_connectivity.viz import plot_connectivity_circle
from mne.viz import circular_layout

# Get node positions for circular layout
node_order = ['frontal', 'parietal', 'temporal', 'occipital']
node_angles = circular_layout(
    label_names, node_order, start_pos=90
)

# Plot connectivity as circular graph
fig, ax = plot_connectivity_circle(
    con.get_data()[:, :, 0],  # Connectivity matrix (first frequency)
    node_names=label_names,
    n_lines=20,  # Show 20 strongest connections
    node_angles=node_angles,
    title='Alpha-band Connectivity'
)
```

### Example 8: Combining Connectivity Over Epochs

```python
from mne_connectivity import spectral_connectivity_epochs

# Compute connectivity for each epoch separately
con = spectral_connectivity_epochs(
    epochs,
    method='coh',
    mode='multitaper',
    fmin=8.,
    fmax=13.
)

# Combine using custom function
con_median = con.combine(combine='median')

# Or use custom callable
con_custom = con.combine(combine=lambda data: np.median(data, axis=0))
```

### Example 9: Comparing Coherency Methods

```python
from mne_connectivity import spectral_connectivity_epochs, make_signals_in_freq_bands

# Simulate signals with interactions at specific frequencies
data = make_signals_in_freq_bands(
    n_seeds=3,
    n_targets=3,
    freq_band=(10, 12),  # Interaction at 10-12 Hz
    n_epochs=30,
    n_times=200,
    sfreq=100
)

# Compare CaCoh (captures zero-lag) vs MIC (only non-zero lag)
cacoh = spectral_connectivity_epochs(data, method='cacoh', mode='multitaper', fmin=5, fmax=30)
mic = spectral_connectivity_epochs(data, method='mic', mode='multitaper', fmin=5, fmax=30)

# CaCoh captures both zero and non-zero lag interactions
# MIC only captures non-zero lag (immune to volume conduction)
```

### Example 10: Vector Autoregressive (VAR) Model

```python
from mne_connectivity import vector_auto_regression

# Compute VAR model (linear dynamical system)
var = vector_auto_regression(
    epochs,
    times=epochs.times,
    lags=10,  # Model order
    l2_reg=0.0,  # Ridge regularization
    model='avg-epochs'  # One model for all epochs
)

# Simulate data from VAR model
simulated_data = var.simulate(n_samples=1000)

# Predict and compute residuals
predicted = var.predict(epochs.get_data())
residuals = epochs.get_data() - predicted
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

### examples.md (44 pages)
Contains detailed examples covering:
- **Phase-based methods**: Comparing PLI, wPLI, and dPLI
- **Coherency methods**: Comparison of Coh, ImCoh, CaCoh, MIC, MIM
- **Time vs. trial connectivity**: When to use spectral_connectivity_epochs vs spectral_connectivity_time
- **Granger causality**: Computing directed connectivity with time-reversal
- **Source space**: Computing connectivity in source space with MNE inverse solutions
- **Envelope correlations**: Orthogonalized envelope connectivity
- **Multivariate methods**: CaCoh, MIC, MIM with spatial patterns
- **Visualization**: Circular graphs and sensor connectivity plots
- **VAR models**: Linear dynamical systems and time-varying connectivity

### installation.md (1 page)
Installation instructions via pip and conda:
```bash
# Via conda
conda install -c conda-forge mne-connectivity

# Via pip
pip install mne-connectivity
```

## Working with This Skill

### For Beginners
1. Start with **examples.md** for complete worked examples
2. Begin with simple bivariate measures (PLI, coherence)
3. Understand the difference between `spectral_connectivity_epochs()` and `spectral_connectivity_time()`
4. Learn about volume conduction and when to use imaginary coherency methods

### For Specific Tasks

**Computing Connectivity**
- Use `spectral_connectivity_epochs()` for event-related data across trials
- Use `spectral_connectivity_time()` for time-varying connectivity within trials
- Specify `indices` parameter to compute subset of connections

**Avoiding Volume Conduction**
- Use methods based on imaginary part: ImCoh, MIC, MIM
- Appropriate for same-modality data (EEG-EEG, MEG-MEG)

**Multivariate Analysis**
- Use CaCoh, MIC, or MIM for multiple channels simultaneously
- Create indices with `seed_target_multivariate_indices()`
- Extract spatial patterns from `attrs['patterns']`

**Directed Connectivity**
- Use Granger causality ('gc', 'gc_tr') for direction of information flow
- Use dPLI to determine leading vs. lagging phase relationships
- Use PSI (phase_slope_index) for phase-based directionality

### For Advanced Users
- Handle high-dimensional data with `rank` parameter for dimensionality reduction
- Compute connectivity in parallel with `n_jobs` parameter (requires memory mapping)
- Work with ragged indices for unequal numbers of seeds/targets
- Combine connectivity across epochs with custom functions
- Visualize connectivity with circular graphs and custom layouts

## Common Pitfalls

1. **Wrong function choice**: Use `spectral_connectivity_epochs()` for across-trial connectivity, `spectral_connectivity_time()` for within-trial connectivity

2. **Volume conduction**: Use ImCoh/MIC/MIM for same-modality data to avoid spurious connectivity

3. **Insufficient epochs**: Connectivity computed with few epochs will be unreliable (need adequate samples)

4. **Granger causality indices**: Must specify `indices` parameter; cannot compute all-to-all GC

5. **Rank deficiency**: High-dimensional multivariate methods may need `rank` parameter specified

## Resources

### Official Documentation
- Main website: https://mne.tools/mne-connectivity/
- API Reference: Browse examples.md for complete API documentation
- Installation: See installation.md for setup instructions

### Citation
If using MNE-Connectivity in publications, cite:
- Hipp JF et al. (2012). Large-scale cortical correlation structure of spontaneous oscillatory activity. Nat Neurosci, 15(6):884-890.
- And the specific methods you use (references in examples.md)

## Notes

- All connectivity classes return xarray-backed data structures for easy manipulation
- Connectivity results can be saved/loaded with `.save()` and `read_connectivity()`
- Use `.get_data()` method to extract numpy arrays from connectivity objects
- Connectivity indices can be 'all', 'symmetric', or tuple of (seeds, targets)
- Spectral estimation modes: 'multitaper', 'fourier', or 'cwt_morlet'
