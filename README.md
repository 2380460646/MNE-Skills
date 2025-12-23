# MNE Skills Collection

A comprehensive skill collection for MEG/EEG neurophysiological data analysis using MNE-Python and related tools.

## Overview

This repository contains skills for working with MNE-Python ecosystem, covering data preprocessing, artifact removal, connectivity analysis, and microstate analysis.

## Skills Included

### 1. **mne-core**
Core MNE-Python functionality for MEG/EEG data analysis:
- Data loading and preprocessing (filtering, epoching, averaging)
- Source localization (MNE, dSPM, beamformers)
- Time-frequency analysis
- Statistical analysis and machine learning
- Visualization tools

### 2. **mne-connectivity**
Functional and effective connectivity analysis:
- Phase-based measures (PLI, wPLI, dPLI, PLV)
- Coherency methods (Coh, ImCoh, CaCoh, MIC, MIM)
- Granger causality for directional connectivity
- Envelope correlations
- Connectivity visualization

### 3. **mne-icalabel**
Automatic ICA component classification:
- ICLabel for EEG artifact detection
- MEGNet for MEG data
- Identifies brain, muscle, eye, heart, and line noise components
- GUI-based and automatic labeling workflows

### 4. **autoreject**
Automated artifact rejection and repair:
- Automatic detection and rejection of bad trials
- Bad sensor interpolation
- RANSAC for robust bad channel detection
- Optimal threshold computation

### 5. **mne-microstates**
EEG microstate analysis:
- Microstate segmentation and clustering
- Global Field Power (GFP) analysis
- Topographic pattern extraction
- State transition analysis

## Installation

Each skill requires MNE-Python and its dependencies:

```bash
# Core MNE-Python
pip install mne

# Additional packages
pip install mne-connectivity
pip install mne-icalabel
pip install autoreject
pip install mne-microstates
```

## Documentation Structure

Each skill folder contains:
- `SKILL.md` - Comprehensive usage guide
- `references/` - Detailed API documentation and examples

## Common Workflows

### Complete Preprocessing Pipeline
1. Load raw data → Filter (1-40 Hz)
2. Create epochs → AutoReject to remove bad trials
3. Fit ICA → ICLabel to identify artifacts
4. Remove artifact components → Final cleaning

### Source Localization Pipeline
1. Preprocess data → Compute forward solution
2. Estimate noise covariance → Create inverse operator
3. Apply inverse method → Visualize on brain

### Connectivity Analysis Pipeline
1. Preprocess and epoch data
2. Select connectivity measure
3. Compute connectivity → Visualize with circular plots

## Resources

- **MNE-Python**: https://mne.tools/
- **MNE Forum**: https://mne.discourse.group/
- **MNE-Connectivity**: https://mne.tools/mne-connectivity/
- **AutoReject**: https://autoreject.github.io/
- **MNE-ICALabel**: https://github.com/mne-tools/mne-icalabel

## Citation

When using these tools, please cite the appropriate papers (see individual SKILL.md files for specific citations).

## License

Each tool has its own license. Please refer to individual package documentation.
