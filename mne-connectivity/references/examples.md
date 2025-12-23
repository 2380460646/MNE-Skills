# Mne-Connectivity - Examples

**Pages:** 44

---

## Comparing PLI, wPLI, and dPLI#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/dpli_wpli_pli.html

**Contents:**
- Comparing PLI, wPLI, and dPLI#
- Background#
- Capturing Leading/Lagging Phase Relationships with dPLI#
- Robustness to Outliers and Noise with wPLI#
- Demo On MEG Data#
- Conclusions#
- References#

Go to the end to download the full example code.

This example demonstrates the different connectivity information captured by the phase lag index (PLI) [1], weighted phase lag index (wPLI) [2], and directed phase lag index (dPLI) [3] on simulated data.

The formulae for PLI, wPLI, and dPLI are given below. In these equations, \(X_{ij}\) is the cross-spectral density (CSD) between two signals \(i, j\). Importantly, the imaginary component of the CSD is maximal when the signals have a phase difference given by \(k\pi+\frac{\pi}{2}\), and is \(0\) when the phase difference is given by \(k\pi\) (where \(k \in \mathbb{Z}\)). This property provides protection against recognizing volume conduction effects as connectivity, and is the backbone for these methods [2]. In the equations below, \(\mathcal{I}\) refers to the imaginary component, \(\mathcal{H}\) refers to the Heaviside step function, and \(sgn\) refers to the sign function.

\(PLI = |E[sgn(\mathcal{I}(X_{ij}))]|\) [1]

\(wPLI = \frac{|E[\mathcal{I}(X_{ij})]|}{E[|\mathcal{I}(X_{ij})|]}\) [2]

\(dPLI = E[\mathcal{H}(\mathcal{I}(X_{ij}))]\) [3]

All three of these metrics are bounded in the range \([0, 1]\).

For PLI, \(0\) means that signal \(i\) leads and lags signal \(j\) equally often, while a value greater than \(0\) means that there is an imbalance in the likelihood for signal \(i\) to be leading or lagging. A value of \(1\) means that signal \(i\) only leads or only lags signal \(j\).

For wPLI, \(0\) means that the total weight (not the quantity) of all leading relationships equals the total weight of lagging relationships, while a value greater than \(0\) means that there is an imbalance between these weights. A value of \(1\), just as in PLI, means that signal \(i\) only leads or only lags signal \(j\).

With dPLI, we gain the ability to distinguish whether signal \(i\) is leading or lagging signal \(j\), complementing the information provided by PLI or wPLI. A value of \(0.5\) means that signal \(i\) leads and lags signal \(j\) equally often. A value in the range \((0.5, 1.0]\) means that signal \(i\) leads signal \(j\) more often than it lags, with a value of \(1\) meaning that signal \(i\) always leads signal \(j\). A value in the range \([0.0, 0.5)\) means that signal \(i\) lags signal \(j\) more often than it leads, with a value of \(0\) meaning that signal \(i\) always lags signal \(j\). The PLI can actually be extracted from the dPLI by the relationship \(PLI = 2|dPLI - 0.5|\), but this relationship is not invertible (dPLI can not be estimated from the PLI).

Overall, these different approaches are closely related but have subtle differences, as will be demonstrated throughout the rest of this example.

The main advantage of dPLI is that it’s directed, meaning it can differentiate between phase relationships which are leading or lagging. To illustrate this, we generate sinusoids with Gaussian noise. In particular, we generate signals with phase differences of \([-\pi, -\frac{\pi}{2}, 0, \frac{\pi}{2}, \pi]\) relative to a reference signal. A negative difference means that the reference signal is lagging the other signal.

A snippet of this simulated data is shown below. The blue signal is the reference signal.

We will now compute PLI, wPLI, and dPLI for each phase relationship.

The estimated connectivites are shown in the figure below, which provides insight into the differences between PLI/wPLI, and dPLI.

Similarities Of All Measures

Capture presence of connectivity in same situations (phase difference of \(\pm\frac{\pi}{2}\))

Do not predict connectivity when phase difference is a multiple of \(\pi\)

Bounded between \(0\) and \(1\)

How dPLI is Different Than PLI/wPLI

Null connectivity is \(0\) for PLI and wPLI, but \(0.5\) for dPLI

dPLI differentiates whether the reference signal is leading or lagging the other signal (lagging if \(0 <= dPlI < 0.5\), leading if \(0.5 < dPLI <= 1.0\))

The previous experiment illustrated the advantages conferred by dPLI when differentiating leading and lagging phase relationships. This experiment will now focus on understanding the advantages of wPLI, and explore how it extends upon PLI.

The main difference between PLI and wPLI is in how different phase relationships are weighted. In PLI, phase differences are weighted as \(-1\) or \(1\) according to their sign. In wPLI, phase differences are weighted based on their value, meaning that phase differences closer to \(\pm\frac{\pi}{2}\) are weighted more heavily than those close to \(0\) or any other multiple of \(\pi\).

This avoids a discontinuity at the transition between positive and negative phase, treating all phase differences near this transition in a similar way. This provides some robustness against outliers and noise when estimating connectivity. For instance, volume conduction can distort EEG/MEG recordings, wherein signals emanating from the same neural source will be picked up by multiple sensors on the scalp. This can effect connectivity estimations, bringing the relative phase differences between two signals close to \(0\). wPLI minimizes the contribution of phase relationships that are small but non-zero (and may thus be attributed to volume conduciton), while PLI weighs these in the same way as phase relationships of \(\pm\frac{\pi}{2}\).

To demonstrate this, we recreate a result from (Vinck et al, 2011) [2]. Two sinusoids are simulated, where the phase difference for half of the epochs is \(\frac{\pi}{2}\), and is \(-\frac{\pi}{100}\) for the others. We also explore the effect of applying uniform noise to this phase difference.

We can now compute PLI and wPLI

The results from the simulation are shown in the figure below. In the case without noise, the difference between wPLI and PLI is made obvious. In PLI, no connectivity is detected, as the \(-\frac{\pi}{100}\) phase differences are weighted in the exact same way as the \(\frac{\pi}{2}\) relationships. wPLI is able to avoid the cancellation of the \(\frac{\pi}{2}\) relationships.

As noise gets added, PLI increases since the \(-\frac{\pi}{100}\) relationships are made positive more often than the \(\frac{\pi}{2}\) relationships are made negative. However, wPLI maintains an advantage in its ability to distinguish the underlying structure. Beyond a certain point, the noise dominates any pre-defined structure, and both methods behave similarly, tending toward \(0\). For a more detailed analysis of this result and the properties of wPLI, please refer to (Vinck et al, 2011) [2].

To finish this example, we also quickly demonstrate these methods on some sample MEG data recorded during visual stimulation.

In this example, there is strong connectivity between sensors 190-200 and sensors 110-160.

Moreover, after observing the presence of connectivity, dPLI can be used to ascertain the direction of the phase relationship. Here, it appears that the dPLI connectivity in this area is less than \(0.5\), and thus sensors 190-200 are lagging sensors 110-160.

In keeping with the previous simulation, we can see that wPLI identifies stronger connectivity relationships than PLI. This is due to its robustness against volume conduction effects decreasing the detected connectivity strength, as was mentioned earlier.

Both wPLI and dPLI are extensions upon the original PLI method, and provide complementary information about underlying connectivity.

To identify the presence of an underlying phase relationship, wPLI is the method of choice for most researchers as it provides an improvement in robustness over the original PLI method

To know the directionality of the connectivity identified by wPLI, dPLI should be used

Ultimately, these methods work great together, providing a comprehensive estimate of phase-based connectivity.

Cornelis J. Stam, Guido Nolte, and Andreas Daffertshofer. Phase lag index: assessment of functional connectivity from multi channel EEG and MEG with diminished bias from common sources. Human Brain Mapping, 28(11):1178–1193, 2007. doi:10.1002/hbm.20346.

Martin Vinck, Robert Oostenveld, Marijn van Wingerden, Franscesco Battaglia, and Cyriel M.A. Pennartz. An improved index of phase-synchronization for electrophysiological data in the presence of volume-conduction, noise and sample-size bias. NeuroImage, 55(4):1548–1565, 2011. doi:10.1016/j.neuroimage.2011.01.055.

C. J. Stam and E. C. W. van Straaten. Go with the flow: use of a directed phase lag index (dpli) to characterize patterns of phase relations in a large-scale model of brain dynamics. NeuroImage, 62(3):1415–1428, Sep 2012. doi:10.1016/j.neuroimage.2012.05.050.

Total running time of the script: (0 minutes 16.426 seconds)

Download Jupyter notebook: dpli_wpli_pli.ipynb

Download Python source code: dpli_wpli_pli.py

Download zipped: dpli_wpli_pli.zip

Gallery generated by Sphinx-Gallery

Comparing spectral connectivity computed over time or over trials

---

## Comparing spectral connectivity computed over time or over trials#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/compare_connectivity_over_time_over_trial.html

**Contents:**
- Comparing spectral connectivity computed over time or over trials#
- Background#
- Simulated examples#
- Real data demonstration#
- Conclusions#
- References#

Go to the end to download the full example code.

This example demonstrates the difference between spectral connectivity computed over time or over trials.

A brief background on the difference between the two conditions is provided, followed by examples on simulated data and real EEG data.

Spectral connectivity is a method for inferring the relationship between channels decomposed at different frequencies of interest. The channels could be M/EEG sensors or brain regions estimated with source localization.

There are multiple different spectral connectivity measures, e.g. coherence, imaginary part of coherence, phase locking value, and envelope correlations. Additionally, there are also multiple methods to estimate the frequency content, e.g. Fourier transforms, Morlet wavelets and multitapers.

In this example, we focus on the two functions, which both computes connectivity from epoched data mne.Epochs: mne_connectivity.spectral_connectivity_epochs() and mne_connectivity.spectral_connectivity_time().

Both functions contain the options to choose the connectivity measurements of interest and the method to decompose the frequency content. The crucial difference between when to use which function lies on the experimental setup and type of tasks.

If the data is obtained for repeated trials of a time-locked event, e.g. ERP data, then mne_connectivity.spectral_connectivity_epochs() is most likely the corresponding function to utilize.

If the data is obtained from resting-state or free-moving tasks, e.g. a mirror-game paradigm [1], then mne_connectivity.spectral_connectivity_time() might be better suited.

Assumptions and Interpretations

The way connectivity is computed for the two functions are slightly different, thus their interpretations and the hypotheses being tested are also different.

Connectivity over trials, as computed by mne_connectivity.spectral_connectivity_epochs() assume epochs have been created around each trial and the function estimates the connectivity at each timepoint over all the repeated trials for the same event. This gives a high temporal resolution, which is often desired for ERP analysis where you are interested in when an effect occurs. However, this approach is not feasible for single-trial data and will result in errorful values when computed on one epoch.

On the other hand, if you are interested in determining connectivity over time for single-trials or from experiments that do not involve exactly repeated trials, then mne_connectivity.spectral_connectivity_time() should be employed. This function also takes data in the form of mne.Epochs, but it may consist of a single epoch. If there are multiple epochs, the connectivity over time is computed for epoch separately, with the option to average over epochs.

To better illustrate the differences and usages for the two functions, we will employ them on two simulated cases and also analyze a real visual task dataset.

Case 1: Repetitions of the same trial.

Let’s generate some simulated data in the format of mne.EpochsArray. In this case, we will use random data for 3 channels over 5 epochs, but all the epochs are just exact replicates of the first epoch. This simulates when data is collected over an event of interest where we assume the connectivity structure is the same over each event.

First we compute connectivity over trials.

As previously mentioned, connectivity over trials can give connectivity for each timepoint, here in the form of mne_connectivity.SpectroTemporalConnectivity. However, in this example we are not interested in the timing, so we will average over all timepoints. Notice that only mode="cwt_morlet" will return an instance of mne_connectivity.SpectroTemporalConnectivity and mode="fourier" or mode="multitaper" returns an instance of mne_connectivity.SpectralConnectivity, which does not have single timepoint resolution.

We see that when using repeated trials without any noise, the phase coupling between the three electrodes over trials are exactly 1.

We will now compute connectivity over time.

Notice that the connectivity over time function by default gives connectivity for each epoch. We will average over epochs to show similar matrices as before, but it could also be done in the function itself by setting average=True.

We see that the connectivity over time are not 1, since the signals were randomly generated and therefore the phase differences between channels are also random over time.

Case 2: 10 Hz sinus waves with different phases.

In this case, we will generate 10 Hz sinus waves with different phases for each epoch and each channel. In this case we would expect the connectivity over time between channels to be 1, but not the connectivity over trials.

First we compute connectivity over trials.

We see that connectivity over trials are not 1, since the phase differences between two channels are not the same over trials.

We will now compute connectivity over time.

We see that for case 2, the connectivity over time is approximately 1, since the phase differences over time between two channels are synchronized.

To finish this example, we will compute connectivity for a sample EEG data.

The sample data consist of repeated trials with a visual stimuli, thus we use mne_connectivity.spectral_connectivity_epochs() to compute connectivity over trials.

Visual tasks are known for evoking event related P1 and N1 responses, which occurs around 100 and 170 ms after stimuli presentation in posterior sites. Additionally, increased theta and alpha phase locking have also been observed during the time window of P1 and N1 [2]. Here, we will therefore analyze phase connectivity in the theta band around P1

Notice we have shortened the wavelets to 4 cycles since we only have 1.6s epochs and are looking at theta activity. This might make the connectivity measurements more sensitive to noise.

We see that around the timing of the P1 evoked response, there is high theta phase coupling on a global scale. To investigate in more details the individual channels, we visualize the connectivity matrix at the timepoint with most global theta connectivity after stimulus presentation and plot the sensor connectivity of the 20 highest connections

In this example we have looked at the differences between connectivity over time and connectivity over trials and demonstrated the corresponding functions implemented in mne_connectivity on simulated data.

Both functions serve their specific roles, and it’s important to use the correct function for the corresponding task to interpret the analysis.

We also briefly analyzed a visual task EEG sample, using mne_connectivity.spectral_connectivity_epochs() where we found that there was high global theta connectivity around the timepoint of the P1 evoked response. Further analysis revealed the highest connections at this timepoint were between occipital and frontal areas.

Marius Zimmermann, Arianna Schiano Lomoriello, and Ivana Konvalinka. Intra-individual behavioural and neural signatures of audience effects and interactions in a mirror-game paradigm. Royal Society Open Science, 2022. doi:10.1098/rsos.211352.

Wolfgang Klimesch, Bärbel Schack, Manuel Schabus, Michael Doppelmayr, Walter Gruber, and Paul Sauseng. Phase-locked alpha and theta oscillations generate the p1–n1 complex and are related to memory performance. Cognitive Brain Research, 19(3):302–316, 2004. doi:https://doi.org/10.1016/j.cogbrainres.2003.11.016.

Total running time of the script: (0 minutes 26.000 seconds)

Download Jupyter notebook: compare_connectivity_over_time_over_trial.ipynb

Download Python source code: compare_connectivity_over_time_over_trial.py

Download zipped: compare_connectivity_over_time_over_trial.zip

Gallery generated by Sphinx-Gallery

Comparing PLI, wPLI, and dPLI

Comparison of coherency-based methods

---

## Comparison of coherency-based methods#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/compare_coherency_methods.html

**Contents:**
- Comparison of coherency-based methods#
- An introduction to coherency-based connectivity methods#
- Zero and non-zero time-lag interactions#
- When different coherency-based methods are most appropriate#
- Bivariate vs. multivariate coherency methods#
- Alternative approaches to computing connectivity#
- Conclusion#
- References#

Go to the end to download the full example code.

This example demonstrates the distinct forms of information captured by coherency-based connectivity methods, and highlights the scenarios in which these different methods should be applied.

MNE-Connectivity supports several methods based on coherency. These are:

coherence (Coh; absolute coherency)

imaginary part of coherency (ImCoh)

canonical coherency (CaCoh)

maximised imaginary part of coherency (MIC)

multivariate interaction measure (MIM)

All of these methods centre on Cohy, a complex-valued estimate of the correlation between signals in the frequency domain. It is an undirected measure of connectivity, being invariant to the direction of information flow between signals.

The common approach for handling these complex-valued coherency scores is to either take their absolute values (Coh) or their imaginary values (ImCoh [1]).

In addition to these traditional bivariate connectivity measures (i.e. between two signals), advanced multivariate measures (i.e. between groups of signals) have also been developed based on Cohy (CaCoh [2]; can take the absolute value for a multivariate form of Coh; see Compute multivariate coherency/coherence) or ImCoh (MIC & MIM [3]; see Compute multivariate measures of the imaginary part of coherency).

Despite their similarities, there are distinct scenarios in which these different methods are most appropriate, as we will show in this example.

The key difference between Cohy/Coh and ImCoh is how information about zero time-lag interactions is captured.

We generally assume that communication within the brain involves some delay in the flow of information (i.e. a non-zero time-lag). This reflects the time taken for: the propagation of action potentials along axons; the release of neurotransmitters from presynaptic terminals and binding to receptors on postsynaptic terminals; etc…

In contrast, interactions with no delay (i.e. a zero time-lag) are often considered to reflect non-physiological activity, such as volume conduction - the propagation of electrical activity through the brain’s conductive tissue from a single source to multiple electrodes simultaneously [1]. Such interactions therefore do not reflect genuine, physiological communication between brain regions. Naturally, having a method that can discard spurious zero time-lag connectivity estimates is very desirable.

Note: Not all zero time-lag interactions are necessarily non-physiological [4].

To demonstrate the differences in how Cohy/Coh and ImCoh handle zero time-lag interactions, we simulate two sets of data with:

A non-zero time-lag interaction at 10-12 Hz.

A zero time-lag interaction at 23-25 Hz.

We compute the connectivity of these simulated signals using CaCoh (a multivariate form of Cohy/Coh) and MIC (a multivariate form of ImCoh).

As you can see, both CaCoh and MIC capture the non-zero time-lag interaction at 10-12 Hz, however only CaCoh captures the zero time-lag interaction at 23-25 Hz.

The different interactions (not) captured by CaCoh and MIC can be understood by visualising the complex values of the interactions.

Above, we plot the complex-valued CaCoh scores for the 10-12 Hz and 23-25 Hz interactions as vectors with origin \((0, 0)\) bound within a circle of radius 1 (reflecting the fact that coherency scores span the set of complex values in the range \([-1, 1]\)).

The circumference of the circle spans the range \((-\pi, \pi]\). The real axis corresponds to vectors with angles of 0° (\(0\pi\); positive values) or 180° (\(\pi\); negative values). The imaginary axis corresponds to vectors with angles of 90° (\(\frac{1}{2}\pi\); positive values) or -90° (\(-\frac{1}{2}\pi\); negative values).

Zero time-lag interactions have angles of 0° and 180° (i.e. no phase difference), corresponding to a non-zero real component, but a zero-valued imaginary component. We see this nicely for the 23-25 Hz interaction, which has an angle of ~0°. Taking the absolute CaCoh value shows us the magnitude of this interaction to be ~0.9. However, first projecting this information to the imaginary axis gives us a magnitude of ~0.

In contrast, non-zero time-lag interactions do not lie on the real axis (i.e. a phase difference), corresponding to non-zero real and imaginary components. We see this nicely for the 10-12 Hz interaction, which has an angle of ~-75°. Taking the absolute CaCoh value shows us the magnitude of this interaction to be ~0.9, which is also seen when first projecting this information to the imaginary axis.

This distinction is why connectivity methods utilising information from both real and imaginary components (Cohy, Coh, CaCoh) capture both zero and non-zero time-lag interactions, whereas methods using only the imaginary component (ImCoh, MIC, MIM) capture only non-zero time-lag interactions.

The ability to capture these different interactions is not a feature specific to multivariate connectivity methods, as shown below for the bivariate methods Coh and ImCoh.

With this information, we can define situations under which these different approaches are most appropriate.

In situations where non-physiological zero time-lag interactions are assumed, methods based on only the imaginary part of coherency (ImCoh, MIC, MIM) should be used. Examples of situations include:

Connectivity between channels of a single modality.

Connectivity between channels of different modalities where the same reference is used.

Note that this applies not only to sensor-space signals, but also to source-space signals where remnants of these non-physiological interactions may remain even after source reconstruction.

In situations where non-physiological zero time-lag interactions are not assumed, methods based on real and imaginary parts of coherency (Cohy, Coh, CaCoh) should be used. An example includes:

Connectivity between channels of different modalities where different references are used.

Equally, when there are no non-physiological zero time-lag interactions, one should not use methods based on only the imaginary part of coherency. There are two key reasons:

1. Discarding physiological zero time-lag interactions

First, not all zero time-lag interactions are non-physiological [4]. Accordingly, methods based on only the imaginary part of coherency may lead to information about genuine connectivity being lost.

In situations where non-physiological zero time-lag interactions are present, the potential loss of physiological information is generally acceptable to avoid spurious connectivity estimates. However, unnecessarily discarding this information can of course be detrimental.

2. Biasing interactions based on the angle of interaction

Depending on their angles, two non-zero time-lag interactions may have the same magnitude in the complex plane, but different magnitudes when projected to the imaginary axis.

This is demonstrated below, where we simulate 2 interactions with non-zero time-lags at 10-12 Hz and 23-25 Hz. Computing the connectivity, we see how both interactions have a similar magnitude (~0.9), but different angles (~-45° for 10-12 Hz; ~-90° for 23-25 Hz).

Plotting the connectivity values for CaCoh and MIC, we see how the 10-12 Hz and 23-25 Hz interactions have a similar magnitude for CaCoh, whereas the MIC scores for the 10-12 Hz interaction are lower than for the 23-25 Hz interaction.

This difference reflects the fact that as the angle of interaction deviates from \(\pm\) 90°, less information will be represented in the imaginary part of coherency. Accordingly, considering only the imaginary part of coherency can bias connectivity estimates based on the angle of interaction.

In situations where non-physiological zero time-lag interactions are present, this phase angle-dependent bias is generally acceptable to avoid spurious connectivity estimates. However in situations where non-physiological zero time-lag interactions are not present, such a bias is clearly problematic.

Again, these considerations are not specific to multivariate methods, as shown below with Coh and ImCoh.

As we have seen, coherency-based methods can be bivariate (Cohy, Coh, ImCoh) and multivariate (CaCoh, MIC, MIM). Whilst both forms capture the same information, there are several benefits to using multivariate methods when investigating connectivity between many signals.

The multivariate methods can be used to capture the most relevant interactions between two groups of signals, representing this information in the component, rather than signal space.

The dimensionality reduction associated with these methods offers: a much easier interpretation of the results; a higher signal-to-noise ratio compared to e.g. averaging bivariate connectivity estimates across multiple pairs of signals; and even reduced bias in what information is captured [3].

Furthermore, despite the dimensionality reduction of multivariate methods it is still possible to investigate the topographies of connectivity, with spatial patterns of connectivity being returned alongside the connectivity values themselves [5].

More information about the multivariate coherency-based methods can be found in the following examples:

CaCoh - Compute multivariate coherency/coherence

MIC & MIM - Compute multivariate measures of the imaginary part of coherency

Coherency-based methods are only some of the many approaches available in MNE-Connectivity for studying interactions between signals. Other non-directed measures include those based on the phase-lag index [6][7] (see also Comparing PLI, wPLI, and dPLI) and phase locking value [8][9].

Furthermore, directed measures of connectivity which determine the direction of information flow are also available, including a variant of the phase-lag index [10] (see also Comparing PLI, wPLI, and dPLI), the phase slope index [11] (see also mne_connectivity.phase_slope_index()), and Granger causality [12][13] (see also Compute directionality of connectivity with multivariate Granger causality).

Altogether, there are clear scenarios in which different coherency-based methods are appropriate.

Methods based on the imaginary part of coherency alone (ImCoh, MIC, MIM) should be used when non-physiological zero time-lag interactions are present.

In contrast, methods based on the real and imaginary parts of coherency (Cohy, Coh, CaCoh) should be used when non-physiological zero time-lag interactions are absent.

Guido Nolte, Ou Bai, Lewis Wheaton, Zoltan Mari, Sherry Vorbach, and Mark Hallett. Identifying true brain interaction from EEG data using the imaginary part of coherency. Clinical Neurophysiology, 115(10):2292–2307, 2004. doi:10.1016/j.clinph.2004.04.029.

Carmen Vidaurre, Guido Nolte, Ingmar E.J. de Vries, M. Gómez, Tjeerd W. Boonstra, K.-R. Müller, Arno Villringer, and Vadim V. Nikulin. Canonical maximization of coherence: a novel tool for investigation of neuronal interactions between two datasets. NeuroImage, 201:116009, 2019. doi:10.1016/j.neuroimage.2019.116009.

Arne Ewald, Laura Marzetti, Filippo Zappasodi, Frank C. Meinecke, and Guido Nolte. Estimating true brain connectivity from EEG/MEG data invariant to linear and static transformations in sensor space. NeuroImage, 60(1):476–488, 2012. doi:10.1016/j.neuroimage.2011.11.084.

Atthaphon Viriyopase, Ingo Bojak, Magteld Zeitler, and Stan Gielen. When long-range zero-lag synchronization is feasible in cortical networks. Frontiers in Computational Neuroscience, 6:49, 2012. doi:10.3389/fncom.2012.00049.

Stefan Haufe, Frank Meinecke, Kai Görgen, Sven Dähne, John-Dylan Haynes, Benjamin Blankertz, and Felix Bießmann. On the interpretation of weight vectors of linear models in multivariate neuroimaging. NeuroImage, 87:96–110, 2014. doi:10.1016/j.neuroimage.2013.10.067.

Cornelis J. Stam, Guido Nolte, and Andreas Daffertshofer. Phase lag index: assessment of functional connectivity from multi channel EEG and MEG with diminished bias from common sources. Human Brain Mapping, 28(11):1178–1193, 2007. doi:10.1002/hbm.20346.

Martin Vinck, Robert Oostenveld, Marijn van Wingerden, Franscesco Battaglia, and Cyriel M.A. Pennartz. An improved index of phase-synchronization for electrophysiological data in the presence of volume-conduction, noise and sample-size bias. NeuroImage, 55(4):1548–1565, 2011. doi:10.1016/j.neuroimage.2011.01.055.

Jean-Philippe Lachaux, Eugenio Rodriguez, Jacques Martinerie, and Francisco J. Varela. Measuring phase synchrony in brain signals. Human Brain Mapping, 8(4):194–208, 1999. doi:10.1002/(SICI)1097-0193(1999)8:4<194::AID-HBM4>3.0.CO;2-C.

Ernesto Pereda Ricardo Bruña, Fernando Maestú. Phase locking value revisited: teaching new tricks to an old dog. Journal of Neural Engineering, 15(5):056011, 2018. doi:10.1088/1741-2552/aacfe4.

C. J. Stam and E. C. W. van Straaten. Go with the flow: use of a directed phase lag index (dpli) to characterize patterns of phase relations in a large-scale model of brain dynamics. NeuroImage, 62(3):1415–1428, Sep 2012. doi:10.1016/j.neuroimage.2012.05.050.

Guido Nolte, Andreas Ziehe, Vadim V. Nikulin, Alois Schlögl, Nicole Krämer, Tom Brismar, and Klaus-Robert Müller. Robustly estimating the flow direction of information in complex physical systems. Physical Review Letters, 2008. doi:10.1103/PhysRevLett.100.234101.

Lionel Barnett and Anil K. Seth. Granger causality for state-space models. Physical Review E, 91(4):040101, 2015. doi:10.1103/PhysRevE.91.040101.

Irene Winkler, Danny Panknin, Daniel Bartz, Klaus-Robert Müller, and Stefan Haufe. Validity of time reversal for testing granger causality. IEEE Transactions on Signal Processing, 64(11):2746–2760, 2016. doi:10.1109/TSP.2016.2531628.

Total running time of the script: (0 minutes 3.147 seconds)

Download Jupyter notebook: compare_coherency_methods.ipynb

Download Python source code: compare_coherency_methods.py

Download zipped: compare_coherency_methods.zip

Gallery generated by Sphinx-Gallery

Comparing spectral connectivity computed over time or over trials

Compute Phase Slope Index (PSI) in source space for a visual stimulus

---

## Compute all-to-all connectivity in sensor space#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/sensor_connectivity.html

**Contents:**
- Compute all-to-all connectivity in sensor space#

Go to the end to download the full example code.

Computes the Phase Lag Index (PLI) between all gradiometers and shows the connectivity in 3D using the helmet geometry. The left visual stimulation data are used which produces strong connectvitiy in the right occipital sensors.

Total running time of the script: (0 minutes 2.913 seconds)

Download Jupyter notebook: sensor_connectivity.ipynb

Download Python source code: sensor_connectivity.py

Download zipped: sensor_connectivity.zip

Gallery generated by Sphinx-Gallery

Compute Phase Slope Index (PSI) in source space for a visual stimulus

Compute coherence in source space using a MNE inverse solution

---

## Compute coherence in source space using a MNE inverse solution#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/mne_inverse_coherence_epochs.html

**Contents:**
- Compute coherence in source space using a MNE inverse solution#
- Read the data#
- Choose channels for coherence estimation#
- Compute the coherence between sources#
- Generate coherence sources and plot#

Go to the end to download the full example code.

This example computes the coherence between a seed in the left auditory cortex and the rest of the brain based on single-trial MNE-dSPM inverse solutions.

First we’ll read in the sample MEG data that we’ll use for computing coherence between channels. We’ll convert this into epochs in order to compute the event-related coherence.

Next we’ll calculate our channel sources. Then we’ll find the most active vertex in the left auditory cortex, which we will later use as seed for the connectivity computation.

Compute the inverse solution for each epoch. By using “return_generator=True” stcs will be a generator object instead of a list. This allows us so to compute the coherence without having to keep all source estimates in memory.

Now we are ready to compute the coherence in the alpha and beta band. fmin and fmax specify the lower and upper freq. for each band, respectively.

To speed things up, we use 2 parallel jobs and use mode=’fourier’, which uses a FFT with a Hanning window to compute the spectra (instead of a multitaper estimation, which has a lower variance but is slower). By using faverage=True, we directly average the coherence in the alpha and beta band, i.e., we will only get 2 frequency bins.

Finally, we’ll generate a SourceEstimate with the coherence. This is simple since we used a single seed. For more than one seed we would have to choose one of the slices within coh.

We use a hack to save the frequency axis as time.

Finally, we’ll plot this source estimate on the brain.

Total running time of the script: (0 minutes 14.711 seconds)

Download Jupyter notebook: mne_inverse_coherence_epochs.ipynb

Download Python source code: mne_inverse_coherence_epochs.py

Download zipped: mne_inverse_coherence_epochs.zip

Gallery generated by Sphinx-Gallery

Compute all-to-all connectivity in sensor space

Compute directionality of connectivity with multivariate Granger causality

---

## Compute directionality of connectivity with multivariate Granger causality#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/granger_causality.html

**Contents:**
- Compute directionality of connectivity with multivariate Granger causality#
- Background#
- Drivers and receivers: analysing the net direction of information flow#
- Improving the robustness of connectivity estimates with time-reversal#
- Controlling spectral smoothing with the number of lags#
- Handling high-dimensional data#
- References#

Go to the end to download the full example code.

This example demonstrates how Granger causality based on state-space models [1] can be used to compute directed connectivity between sensors in a multivariate manner. Furthermore, the use of time-reversal for improving the robustness of directed connectivity estimates to noise in the data is discussed [2].

Multivariate forms of signal analysis allow you to simultaneously consider the activity of multiple signals. In the case of connectivity, the interaction between multiple sensors can be analysed at once, producing a single connectivity spectrum. This approach brings not only practical benefits (e.g. easier interpretability of results from the dimensionality reduction), but can also offer methodological improvements (e.g. enhanced signal-to-noise ratio and reduced bias).

Additionally, it can be of interest to examine the directionality of connectivity between signals, providing additional clarity to how information flows in a system. One such directed measure of connectivity is Granger causality (GC). A signal, \(\boldsymbol{x}\), is said to Granger-cause another signal, \(\boldsymbol{y}\), if information from the past of \(\boldsymbol{x}\) improves the prediction of the present of \(\boldsymbol{y}\) over the case where only information from the past of \(\boldsymbol{y}\) is used. Note: GC does not make any assertions about the true causality between signals.

The degree to which \(\boldsymbol{x}\) and \(\boldsymbol{y}\) can be used to predict one another in a linear model can be quantified using vector autoregressive (VAR) models. Considering the simpler case of time domain connectivity, the VAR models are as follows:

\(y_t = \sum_{k=1}^{K} a_k y_{t-k} + \xi_t^y\) , \(Var(\xi_t^y) := \Sigma_y\) ,

and \(\boldsymbol{z}_t = \sum_{k=1}^K \boldsymbol{A}_k \boldsymbol{z}_{t-k} + \boldsymbol{\epsilon}_t\) , \(\boldsymbol{\Sigma} := \langle \boldsymbol{\epsilon}_t \boldsymbol{\epsilon}_t^T \rangle = \begin{bmatrix} \Sigma_{xx} & \Sigma_{xy} \\ \Sigma_{yx} & \Sigma_{yy} \end{bmatrix}\) ,

representing the reduced and full VAR models, respectively, where: \(K\) is the order of the VAR model, determining the number of lags, \(k\), used; \(\boldsymbol{Z} := \begin{bmatrix} \boldsymbol{x} \\ \boldsymbol{y} \end{bmatrix}\); \(\boldsymbol{A}\) is a matrix of coefficients explaining the contribution of past entries of \(\boldsymbol{Z}\) to its current value; and \(\xi\) and \(\boldsymbol{\epsilon}\) are the residuals of the VAR models. In this way, the information of the signals at time \(t\) can be represented as a weighted form of the information from the previous timepoints, plus some residual information not encoded in the signals’ past. In practice, VAR model parameters are computed from an autocovariance sequence generated from the time-series data using the Yule-Walker equations [3].

The residuals, or errors, represent how much information about the present state of the signals is not explained by their past. We can therefore estimate how much \(\boldsymbol{x}\) Granger-causes \(\boldsymbol{y}\) by comparing the variance of the residuals of the reduced VAR model (\(\Sigma_y\); i.e. how much the present of \(\boldsymbol{y}\) is not explained by its own past) and of the full VAR model (\(\Sigma_{yy}\); i.e. how much the present of \(\boldsymbol{y}\) is not explained by both its own past and that of \(\boldsymbol{x}\)):

\(F_{x \rightarrow y} = ln \Large{(\frac{\Sigma_y}{\Sigma_{yy}})}\) ,

where \(F\) is the Granger score. For example, if \(\boldsymbol{x}\) contains no information about \(\boldsymbol{y}\), the residuals of the reduced and full VAR models will be identical, and \(F_{x \rightarrow y}\) will naturally be 0, indicating that information from \(\boldsymbol{x}\) does not flow to \(\boldsymbol{y}\). In contrast, if \(\boldsymbol{x}\) does help to predict \(\boldsymbol{y}\), the residual of the full model will be smaller than that of the reduced model. \(\Large{\frac{\Sigma_y} {\Sigma_{yy}}}\) will therefore be greater than 1, leading to a Granger score > 0. Granger scores are bound between \([0, \infty)\).

These same principles apply to spectral GC, which provides information about the directionality of connectivity for individual frequencies. For spectral GC, the autocovariance sequence is generated from an inverse Fourier transform applied to the cross-spectral density of the signals. Additionally, a spectral transfer function is used to translate information from the VAR models back into the frequency domain before computing the final Granger scores.

Barnett and Seth (2015) [1] have defined a multivariate form of spectral GC based on state-space models, enabling the estimation of information flow between whole sets of signals simultaneously:

\(F_{A \rightarrow B}(f) = \Re ln \Large{(\frac{ det(\boldsymbol{S}_{BB}(f))}{det(\boldsymbol{S}_{BB}(f) - \boldsymbol{H}_{BA}(f) \boldsymbol{\Sigma}_{AA \lvert B} \boldsymbol{H}_{BA}^*(f))})}\) ,

where: \(A\) and \(B\) are the seeds and targets, respectively; \(f\) is a given frequency; \(\boldsymbol{H}\) is the spectral transfer function; \(\boldsymbol{\Sigma}\) is the innovations form residuals’ covariance matrix of the state-space model; \(\boldsymbol{S}\) is \(\boldsymbol{\Sigma}\) transformed by \(\boldsymbol{H}\); and \(\boldsymbol{\Sigma}_{IJ \lvert K} := \boldsymbol{\Sigma}_{IJ} - \boldsymbol{\Sigma}_{IK} \boldsymbol{\Sigma}_{KK}^{-1} \boldsymbol{\Sigma}_{KJ}\), representing a partial covariance matrix. The same principles apply as before: a numerator greater than the denominator means that information from the seed signals aids the prediction of activity in the target signals, leading to a Granger score > 0.

There are several benefits to a state-space approach for computing GC: compared to traditional autoregressive-based approaches, the use of state-space models offers reduced statistical bias and increased statistical power; furthermore, the dimensionality reduction offered by the multivariate nature of the approach can aid in the interpretability and subsequent analysis of the results.

To demonstrate the use of GC for estimating directed connectivity, we start by loading some example MEG data and dividing it into two-second-long epochs.

We will focus on connectivity between sensors over the parietal and occipital cortices, with 20 parietal sensors designated as group A, and 22 occipital sensors designated as group B.

Plotting the results, we see that there is a flow of information from our parietal sensors (group A) to our occipital sensors (group B) with a noticeable peak at ~8 Hz, and smaller peaks at 18 and 26 Hz.

Although analysing connectivity in a given direction can be of interest, there may exist a bidirectional relationship between signals. In such cases, identifying the signals that dominate information flow (the drivers) may be desired. For this, we can simply subtract the Granger scores in the opposite direction, giving us the net GC score:

\(F_{A \rightarrow B}^{net} := F_{A \rightarrow B} - F_{B \rightarrow A}\).

Doing so, we see that the flow of information across the spectrum remains dominant from parietal to occipital sensors (indicated by the positive-valued Granger scores), with similar peaks around 10, 18, and 26 Hz.

One limitation of GC methods is the risk of connectivity estimates being contaminated with noise. For instance, consider the case where, due to volume conduction, multiple sensors detect activity from the same source. Naturally, information recorded at these sensors mutually help to predict the activity of one another, leading to spurious estimates of directed connectivity which one may incorrectly attribute to information flow between different brain regions. On the other hand, even if there is no source mixing, the presence of correlated noise between sensors can similarly bias directed connectivity estimates.

To address this issue, Haufe et al. (2013) [4] propose contrasting causality scores obtained on the original time-series to those obtained on the reversed time-series. The idea behind this approach is as follows: if temporal order is crucial in distinguishing a driver from a recipient, then reversing the temporal order should reduce, if not flip, an estimate of directed connectivity. In practice, time-reversal is implemented as a transposition of the autocovariance sequence used to compute GC [5].

Several studies have shown that that such an approach can reduce the degree of false-positive connectivity estimates (even performing favourably against other methods such as the phase slope index) [6] and retain the ability to correctly identify the net direction of information flow akin to net GC [2][4]. This approach is termed time-reversed GC (TRGC):

\(\tilde{D}_{A \rightarrow B}^{net} := F_{A \rightarrow B}^{net} - F_{\tilde{A} \rightarrow \tilde{B}}^{net}\) ,

where \(\sim\) represents time-reversal, and:

\(F_{\tilde{A} \rightarrow \tilde{B}}^{net} := F_{\tilde{A} \rightarrow \tilde{B}} - F_{\tilde{B} \rightarrow \tilde{A}}\).

GC on time-reversed signals can be computed simply with method=['gc_tr'], which will perform the time-reversal of the signals for the end-user. Note that time-reversed results should only be interpreted in the context of net results, i.e. with \(\tilde{D}_{A \rightarrow B}^{net}\). In the example below, notice how the outputs are not used directly, but rather used to produce net scores of the time-reversed signals. The net scores of the time-reversed signals can then be subtracted from the net scores of the original signals to produce the final TRGC scores.

Plotting the TRGC results reveals a very different picture compared to net GC. For one, there is now a dominance of information flow ~6 Hz from occipital to parietal sensors (indicated by the negative-valued Granger scores). Additionally, the peak ~10 Hz is less dominant in the spectrum, with parietal to occipital information flow between 13-20 Hz being much more prominent. The stark difference between net GC and TRGC results indicates that the net GC spectrum was contaminated by spurious connectivity resulting from source mixing or correlated noise in the recordings. Altogether, the use of TRGC instead of net GC is generally advised.

One important parameter when computing GC is the number of lags used when computing the VAR model. A lower number of lags reduces the computational cost, but in the context of spectral GC, leads to a smoothing of Granger scores across frequencies. The number of lags can be specified using the gc_n_lags parameter. The default value is 40, however there is no correct number of lags to use when computing GC. Instead, you have to use your own best judgement of whether or not your Granger scores look overly smooth.

Below is a comparison of Granger scores computed with a different number of lags. In the above examples we used 20 lags, which we will compare to Granger scores computed with 60 lags. As you can see, the spectra of Granger scores computed with 60 lags is noticeably less smooth, but it does share the same overall pattern.

An important issue to consider when computing multivariate GC is that the data GC is computed on should not be rank deficient (i.e. must have full rank). More specifically, the autocovariance matrix must not be singular or close to singular.

In the case that your data is not full rank and rank is left as None, an automatic rank computation is performed and an appropriate degree of dimensionality reduction will be enforced. The rank of the data is determined by computing the singular values of the data and finding those within a factor of \(1e^{-6}\) relative to the largest singular value.

Whilst unlikely, there may be scenarios in which this threshold is too lenient. In these cases, you should inspect the singular values of your data to identify an appropriate degree of dimensionality reduction to perform, which you can then specify manually using the rank argument. The code below shows one possible approach for finding an appropriate rank of close-to-singular data with a more conservative threshold.

Nonethless, even in situations where you specify an appropriate rank, it is not guaranteed that the subsequently-computed autocovariance sequence will retain this non-singularity (this can depend on, e.g. the number of lags). Hence, you may also encounter situations where you have to specify a rank less than that of your data to ensure that the autocovariance sequence is non-singular.

In the above examples, notice how a rank of 5 was given, despite there being 20 channels in the seeds and targets. Attempting to compute GC on the original data would not succeed, given that the resulting autocovariance sequence is singular, as the example below shows.

Rigorous checks are implemented to identify any such instances which would otherwise cause the GC computation to produce erroneous results. You can therefore be confident as an end-user that these cases will be caught.

Finally, when comparing GC scores across recordings, it is highly recommended to estimate connectivity from the same number of channels (or equally from the same degree of rank subspace projection) to avoid biases in connectivity estimates. Bias can be avoided by specifying a consistent rank subspace to project to using the rank argument, standardising your connectivity estimates regardless of changes in e.g. the number of channels across recordings. Note that this does not refer to the number of seeds and targets within a connection being identical, rather to the number of seeds and targets across connections.

Lionel Barnett and Anil K. Seth. Granger causality for state-space models. Physical Review E, 91(4):040101, 2015. doi:10.1103/PhysRevE.91.040101.

Irene Winkler, Danny Panknin, Daniel Bartz, Klaus-Robert Müller, and Stefan Haufe. Validity of time reversal for testing granger causality. IEEE Transactions on Signal Processing, 64(11):2746–2760, 2016. doi:10.1109/TSP.2016.2531628.

Peter Whittle. On the fitting of multivariate autoregressions, and the approximate canonical factorization of a spectral density matrix. Biometrika, 50(1-2):129–134, 1963. doi:10.1093/biomet/50.1-2.129.

Stefan Haufe, Vadim V Nikulin, Klaus-Robert Müller, and Guido Nolte. A critical assessment of connectivity measures for eeg data: a simulation study. NeuroImage, 64:120–133, 2013. doi:10.1016/j.neuroimage.2012.09.036.

Stefan Haufe, Vadim V Nikulin, and Guido Nolte. Alleviating the influence of weak data asymmetries on granger-causal analyses. In Latent Variable Analysis and Signal Separation: 10th International Conference, LVA/ICA 2012, Tel Aviv, Israel, March 12-15, 2012. Proceedings 10, 25–33. Springer, 2012. doi:10.1007/978-3-642-28551-6_4.

Martin Vinck, Lisanne Huurdeman, Conrado A Bosman, Pascal Fries, Francesco P Battaglia, Cyriel MA Pennartz, and Paul H Tiesinga. How to detect the granger-causal flow direction in the presence of additive noise? NeuroImage, 108:301–318, 2015. doi:10.1016/j.neuroimage.2014.12.017.

Total running time of the script: (0 minutes 57.924 seconds)

Download Jupyter notebook: granger_causality.ipynb

Download Python source code: granger_causality.py

Download zipped: granger_causality.zip

Gallery generated by Sphinx-Gallery

Compute coherence in source space using a MNE inverse solution

Compute envelope correlations in source space

---

## Compute envelope correlations in source space#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/mne_inverse_envelope_correlation.html

**Contents:**
- Compute envelope correlations in source space#
- Compute the forward and inverse#
- Do pairwise-orthogonalized envelope correlation#
- Do symmetric-orthogonalized envelope correlation#
- References#

Go to the end to download the full example code.

Compute envelope correlations of orthogonalized activity [1][2] using pairwise and symmetric orthogonalization [3] in source space using resting state CTF data.

Note that the original procedure for symmetric orthogonalization in [3] is:

Extract inverse label data from raw

Symmetric orthogonalization

Hilbert transform and absolute value

Here we follow the procedure:

Epoch data, then for each

Extract inverse label data for each epoch

Symmetric orthogonalization for each epoch

Band-pass filter each epoch

Hilbert transform and absolute value (inside envelope_correlation)

The differences between these two should hopefully be fairly minimal given the pairwise orthogonalization used in [2] used a similar pipeline.

Here we do some things in the name of speed, such as crop (which will hurt SNR) and downsample. Then we compute SSP projectors and apply them.

Now we create epochs and prepare to band-pass filter them.

Here we need the number of labels to be less than the rank of the data (here around 200), because all label time courses are orthogonalized relative to one another. 'aparc_sub' has over 400 labels, so here we use 'aparc.a2009s', which has fewer than 200.

Joerg F Hipp, David J Hawellek, Maurizio Corbetta, Markus Siegel, and Andreas K Engel. Large-scale cortical correlation structure of spontaneous oscillatory activity. Nature Neuroscience, 15(6):884–890, 2012. doi:10.1038/nn.3101.

Sheraz Khan, Javeria A. Hashmi, Fahimeh Mamashli, Konstantinos Michmizos, Manfred G. Kitzbichler, Hari Bharadwaj, Yousra Bekhti, Santosh Ganesan, Keri-Lee A. Garel, Susan Whitfield-Gabrieli, Randy L. Gollub, Jian Kong, Lucia M. Vaina, Kunjan D. Rana, Steven M. Stufflebeam, Matti S. Hämäläinen, and Tal Kenet. Maturation trajectories of cortical resting-state networks depend on the mediating frequency band. NeuroImage, 174:57–68, 2018. doi:10.1016/j.neuroimage.2018.02.018.

G. L. Colclough, M. J. Brookes, S. M. Smith, and M. W. Woolrich. A symmetric multivariate leakage correction for MEG connectomes. NeuroImage, 117:439–448, August 2015. doi:10.1016/j.neuroimage.2015.03.071.

Total running time of the script: (1 minutes 1.933 seconds)

Download Jupyter notebook: mne_inverse_envelope_correlation.ipynb

Download Python source code: mne_inverse_envelope_correlation.py

Download zipped: mne_inverse_envelope_correlation.zip

Gallery generated by Sphinx-Gallery

Compute directionality of connectivity with multivariate Granger causality

Compute envelope correlations in volume source space

---

## Compute envelope correlations in volume source space#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/mne_inverse_envelope_correlation_volume.html

**Contents:**
- Compute envelope correlations in volume source space#
- Compute the forward and inverse#
- Compute label time series and do envelope correlation#
- Compute the degree and plot it#
- References#

Go to the end to download the full example code.

Compute envelope correlations of orthogonalized activity [1][2] in source space using resting state CTF data in a volume source space.

Here we do some things in the name of speed, such as crop (which will hurt SNR) and downsample. Then we compute SSP projectors and apply them.

Now we band-pass filter our data and create epochs.

Joerg F Hipp, David J Hawellek, Maurizio Corbetta, Markus Siegel, and Andreas K Engel. Large-scale cortical correlation structure of spontaneous oscillatory activity. Nature Neuroscience, 15(6):884–890, 2012. doi:10.1038/nn.3101.

Sheraz Khan, Javeria A. Hashmi, Fahimeh Mamashli, Konstantinos Michmizos, Manfred G. Kitzbichler, Hari Bharadwaj, Yousra Bekhti, Santosh Ganesan, Keri-Lee A. Garel, Susan Whitfield-Gabrieli, Randy L. Gollub, Jian Kong, Lucia M. Vaina, Kunjan D. Rana, Steven M. Stufflebeam, Matti S. Hämäläinen, and Tal Kenet. Maturation trajectories of cortical resting-state networks depend on the mediating frequency band. NeuroImage, 174:57–68, 2018. doi:10.1016/j.neuroimage.2018.02.018.

Total running time of the script: (0 minutes 31.197 seconds)

Download Jupyter notebook: mne_inverse_envelope_correlation_volume.ipynb

Download Python source code: mne_inverse_envelope_correlation_volume.py

Download zipped: mne_inverse_envelope_correlation_volume.zip

Gallery generated by Sphinx-Gallery

Compute envelope correlations in source space

Compute full spectrum source space connectivity between labels

---

## Compute full spectrum source space connectivity between labels#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/mne_inverse_connectivity_spectrum.html

**Contents:**
- Compute full spectrum source space connectivity between labels#

Go to the end to download the full example code.

The connectivity is computed between 4 labels across the spectrum between 7.5 Hz and 40 Hz.

Total running time of the script: (0 minutes 2.393 seconds)

Download Jupyter notebook: mne_inverse_connectivity_spectrum.ipynb

Download Python source code: mne_inverse_connectivity_spectrum.py

Download zipped: mne_inverse_connectivity_spectrum.zip

Gallery generated by Sphinx-Gallery

Compute envelope correlations in volume source space

Compute mixed source space connectivity and visualize it using a circular graph

---

## Compute mixed source space connectivity and visualize it using a circular graph#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/mixed_source_space_connectivity.html

**Contents:**
- Compute mixed source space connectivity and visualize it using a circular graph#
- Save the figure (optional)#

Go to the end to download the full example code.

This example computes the all-to-all connectivity between 75 regions in a mixed source space based on dSPM inverse solutions and a FreeSurfer cortical parcellation. The connectivity is visualized using a circular graph which is ordered based on the locations of the regions in the axial plane.

By default matplotlib does not save using the facecolor, even though this was set when the figure was generated. If not set via savefig, the labels, title, and legend will be cut off from the output png file.

Total running time of the script: (0 minutes 16.801 seconds)

Download Jupyter notebook: mixed_source_space_connectivity.ipynb

Download Python source code: mixed_source_space_connectivity.py

Download zipped: mixed_source_space_connectivity.zip

Gallery generated by Sphinx-Gallery

Compute full spectrum source space connectivity between labels

Compute multivariate coherency/coherence

---

## Compute multivariate coherency/coherence#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/cacoh.html

**Contents:**
- Compute multivariate coherency/coherence#
- Background#
- Data Simulation#
- Computing CaCoh#
- CaCoh versus coherence#
- Extracting spatial information from CaCoh#
- Handling high-dimensional data#
- Limitations#
- References#

Go to the end to download the full example code.

This example demonstrates how canonical coherency (CaCoh) [1] - a multivariate method based on coherency - can be used to compute connectivity between whole sets of sensors, alongside spatial patterns of the connectivity.

Multivariate forms of signal analysis allow you to simultaneously consider the activity of multiple signals. In the case of connectivity, the interaction between multiple sensors can be analysed at once, producing a single connectivity spectrum. This approach brings not only practical benefits (e.g. easier interpretability of results from the dimensionality reduction), but can also offer methodological improvements (e.g. enhanced signal-to-noise ratio).

A popular bivariate measure of connectivity is coherency/coherence, which looks at the correlation between two signals in the frequency domain. However, in cases where interactions between multiple signals are of interest, computing connectivity between all possible combinations of signals leads to a very large number of results which is difficult to interpret. A common approach is to average results across these connections, however this risks reducing the signal-to-noise ratio of results and burying interactions that are present between only a small number of channels.

Canonical coherency (CaCoh) is a multivariate form of coherency that uses eigendecomposition-derived spatial filters to extract the underlying components of connectivity in a frequency-resolved manner [1]. This approach goes beyond simply aggregating information across all possible combinations of signals.

It is similar to multivariate methods based on the imaginary part of coherency (MIC & MIM [2]; see Compute multivariate measures of the imaginary part of coherency and Comparison of coherency-based methods).

To demonstrate the CaCoh method, we will use some simulated data consisting of two sets of interactions between signals in a given frequency range:

5 seeds and 3 targets interacting in the 10-12 Hz frequency range.

5 seeds and 3 targets interacting in the 23-25 Hz frequency range.

We can consider the seeds and targets to be signals of different modalities, e.g. cortical EEG signals and subcortical LFP signals, cortical EEG signals and muscular EMG signals, etc…. We use the make_signals_in_freq_bands() function to simulate these signals.

Having simulated the signals, we can create the indices for computing connectivity between all seeds and all targets in a single multivariate connection (see Working with ragged indices for multivariate connectivity for more information), after which we compute connectivity.

For CaCoh, a set of spatial filters are found that will maximise the estimated connectivity between the seed and target signals. These maximising filters correspond to the eigenvectors with the largest eigenvalue, derived from an eigendecomposition of information from the cross-spectral density (Eq. 8 of [1]):

\(\textrm{CaCoh}=\Large{\frac{\boldsymbol{a}^T\boldsymbol{D}(\Phi) \boldsymbol{b}}{\sqrt{\boldsymbol{a}^T\boldsymbol{a}\boldsymbol{b}^T \boldsymbol{b}}}}\)

where: \(\boldsymbol{D}(\Phi)\) is the cross-spectral density between seeds and targets transformed for a given phase angle \(\Phi\); and \(\boldsymbol{a}\) and \(\boldsymbol{b}\) are eigenvectors for the seeds and targets, such that \(\boldsymbol{a}^T\boldsymbol{D}(\Phi) \boldsymbol{b}\) maximises coherency between the seeds and targets. All elements are frequency-dependent, however this is omitted for readability.

CaCoh is complex-valued in the range \([-1, 1]\) where the sign reflects the phase angle of the interaction (like for coherency). Taking the absolute value is akin to taking the coherence, which is the magnitude of the interaction regardless of phase angle.

As you can see below, using CaCoh we have summarised the most relevant connectivity information from our 10 seed channels and 6 target channels as a single spectrum of connectivity values. This lower-dimensional representation of signal interactions is much more interpretable when analysing connectivity in complex systems such as the brain.

Note that we plot the absolute values of the results (coherence) rather than the complex values (coherency). The absolute value of connectivity will generally be of most interest. However, information such as the phase of interaction can only be extracted from the complex-valued results, e.g. with the numpy.angle() function.

To further demonstrate the signal-to-noise ratio benefits of CaCoh, below we compute connectivity between each seed and target using bivariate coherence. With our 10 seeds and 6 targets, this gives us a total of 60 unique connections which is very difficult to interpret without aggregating some information. A common approach is to simply average across these connections, which we do below.

Plotting the bivariate and multivariate results together, we can see that coherence still captures the interactions at 10-12 Hz and 23-25 Hz, however the scale of the connectivity is much smaller. This reflects the fact that CaCoh is able to capture the relevant components of interactions between multiple signals, regardless of whether they are present in all channels.

The ability of multivariate connectivity methods to capture the underlying components of connectivity is extremely useful when dealing with data from a large number of channels, with inter-channel interactions at distinct frequencies, a problem explored in more detail in the Compute multivariate measures of the imaginary part of coherency example.

Whilst a lower-dimensional representation of connectivity information is useful, we lose information about which channels are involved in the connectivity. Thankfully, this information can be recovered by constructing spatial patterns of connectivity from the spatial filters [3].

The spatial patterns are stored under attrs['patterns'] of the connectivity class, with one value per frequency for each channel in the seeds and targets. The patterns can be positive- and negative-valued. Sign differences of the patterns can be used to visualise the orientation of underlying dipole sources, whereas their absolute value reflects the strength of a channel’s contribution to the connectivity component. The spatial patterns are not bound between \([-1, 1]\).

Averaging across the patterns in the 10-12 Hz and 23-25 Hz ranges, we can see how it is possible to identify which channels are contributing to connectivity at different frequencies.

For an example on interpreting spatial filters with real data, see the Compute multivariate measures of the imaginary part of coherency example.

An important issue to consider when using these multivariate methods is overfitting, which risks biasing connectivity estimates to maximise noise in the data. This risk can be reduced by performing a preliminary dimensionality reduction prior to estimating the connectivity with a singular value decomposition (Eq. 15 of [1]). The degree of this dimensionality reduction can be specified using the rank argument, which by default will not perform any dimensionality reduction (assuming your data is full rank; see below if not). Choosing an expected rank of the data requires a priori knowledge about the number of components you expect to observe in the data.

When comparing CaCoh scores across recordings, it is highly recommended to estimate connectivity from the same number of channels (or equally from the same degree of rank subspace projection) to avoid biases in connectivity estimates. Bias can be avoided by specifying a consistent rank subspace to project to using the rank argument, standardising your connectivity estimates regardless of changes in e.g. the number of channels across recordings. Note that this does not refer to the number of seeds and targets within a connection being identical, rather to the number of seeds and targets across connections.

Here, we project our seed and target data to only the first 2 components of our rank subspace. Results show that the general spectral pattern of connectivity is retained in the rank subspace-projected data, suggesting that a fair degree of redundant connectivity information is contained in the excluded components of the seed and target data.

We also assert that the spatial patterns of MIC are returned in the original sensor space despite this rank subspace projection, being reconstructed using the products of the singular value decomposition (Eqs. 46 & 47 of [2]).

See Compute multivariate measures of the imaginary part of coherency for an example of applying the rank subspace projection to real data with a large number of channels.

In the case that your data is not full rank and rank is left as None, an automatic rank computation is performed and an appropriate degree of dimensionality reduction will be enforced. The rank of the data is determined by computing the singular values of the data and finding those within a factor of \(1e^{-6}\) relative to the largest singular value.

Whilst unlikely, there may be scenarios in which this threshold is too lenient. In these cases, you should inspect the singular values of your data to identify an appropriate degree of dimensionality reduction to perform, which you can then specify manually using the rank argument. The code below shows one possible approach for finding an appropriate rank of close-to-singular data with a more conservative threshold.

Multivariate methods offer many benefits in the form of dimensionality reduction and signal-to-noise ratio improvements. However, no method is perfect. When we simulated the data, we mentioned how we considered the seeds and targets to be signals of different modalities. This is an important factor in whether CaCoh should be used over methods based solely on the imaginary part of coherency such as MIC and MIM.

In short, if you want to examine connectivity between signals from the same modality or from different modalities using a shared reference, you should consider using another method instead of CaCoh. Rather, methods based on the imaginary part of coherency such as MIC and MIM should be used to avoid spurious connectivity estimates stemming from e.g. volume conduction artefacts.

On the other hand, if you want to examine connectivity between signals from different modalities using different references, CaCoh is a more appropriate method than MIC/MIM. This is because volume conduction artefacts are of less concern, and CaCoh does not risk biasing connectivity estimates towards interactions with particular phase lags like MIC/MIM.

These scenarios are described in more detail in the Comparison of coherency-based methods example.

Carmen Vidaurre, Guido Nolte, Ingmar E.J. de Vries, M. Gómez, Tjeerd W. Boonstra, K.-R. Müller, Arno Villringer, and Vadim V. Nikulin. Canonical maximization of coherence: a novel tool for investigation of neuronal interactions between two datasets. NeuroImage, 201:116009, 2019. doi:10.1016/j.neuroimage.2019.116009.

Arne Ewald, Laura Marzetti, Filippo Zappasodi, Frank C. Meinecke, and Guido Nolte. Estimating true brain connectivity from EEG/MEG data invariant to linear and static transformations in sensor space. NeuroImage, 60(1):476–488, 2012. doi:10.1016/j.neuroimage.2011.11.084.

Stefan Haufe, Frank Meinecke, Kai Görgen, Sven Dähne, John-Dylan Haynes, Benjamin Blankertz, and Felix Bießmann. On the interpretation of weight vectors of linear models in multivariate neuroimaging. NeuroImage, 87:96–110, 2014. doi:10.1016/j.neuroimage.2013.10.067.

Total running time of the script: (0 minutes 2.305 seconds)

Download Jupyter notebook: cacoh.ipynb

Download Python source code: cacoh.py

Download zipped: cacoh.zip

Gallery generated by Sphinx-Gallery

Compute mixed source space connectivity and visualize it using a circular graph

Compute multivariate measures of the imaginary part of coherency

---

## Compute multivariate measures of the imaginary part of coherency#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/mic_mim.html

**Contents:**
- Compute multivariate measures of the imaginary part of coherency#
- Background#
- Maximised imaginary part of coherency (MIC)#
- Multivariate interaction measure (MIM)#
- Handling high-dimensional data#
- Limitations#
- References#

Go to the end to download the full example code.

This example demonstrates how multivariate methods based on the imaginary part of coherency [1] can be used to compute connectivity between whole sets of sensors, and how spatial patterns of this connectivity can be interpreted.

The methods in question are: the maximised imaginary part of coherency (MIC); and the multivariate interaction measure (MIM; as well as its extension, the global interaction measure, GIM).

Multivariate forms of signal analysis allow you to simultaneously consider the activity of multiple signals. In the case of connectivity, the interaction between multiple sensors can be analysed at once, producing a single connectivity spectrum. This approach brings not only practical benefits (e.g. easier interpretability of results from the dimensionality reduction), but can also offer methodological improvements (e.g. enhanced signal-to-noise ratio and reduced bias).

A popular bivariate measure of connectivity is the imaginary part of coherency, which looks at the correlation between two signals in the frequency domain and is immune to spurious connectivity arising from volume conduction artefacts [2]. However, in cases where interactions between multiple signals are of interest, computing connectivity between all possible combinations of signals leads to a very large number of results which is difficult to interpret. A common approach is to average results across these connections, however this risks reducing the signal-to-noise ratio of results and burying interactions that are present between only a small number of channels.

Additionally, this bivariate measure is susceptible to biased estimates of connectivity based on the spatial proximity of sensors [1] depending on the degree of source mixing in the signals.

To overcome these limitations, spatial filters derived from eigendecompositions allow connectivity to be analysed in a multivariate manner, removing the source mixing-dependent bias and increasing the signal-to-noise ratio of connectivity estimates [1]. This approach goes beyond simply aggregating information across all possible combinations of signals, instead extracting the underlying components of connectivity in a frequency-resolved manner.

This leads to the following methods: the maximised imaginary part of coherency (MIC); and the multivariate interaction measure (MIM). These methods are similar to the multivariate method based on coherency (CaCoh [3]; see Compute multivariate coherency/coherence and Comparison of coherency-based methods).

We start by loading some example MEG data and dividing it into two-second-long epochs.

We will focus on connectivity between sensors over the left and right hemispheres, with 75 sensors in the left hemisphere designated as seeds, and 76 sensors in the right hemisphere designated as targets.

By averaging across each connection between the seeds and targets, we can see that the bivariate measure of the imaginary part of coherency estimates a strong peak in connectivity between seeds and targets around 13-18 Hz, with a weaker peak around 27 Hz.

For MIC, a set of spatial filters are found that will maximise the estimated connectivity between the seed and target signals. These maximising filters correspond to the eigenvectors with the largest eigenvalue, derived from an eigendecomposition of information from the cross-spectral density (Eq. 7 of [1]):

\(\textrm{MIC}=\Large{\frac{\boldsymbol{\alpha}^T \boldsymbol{E \beta}} {\parallel\boldsymbol{\alpha}\parallel \parallel\boldsymbol{\beta} \parallel}}\),

where \(\boldsymbol{\alpha}\) and \(\boldsymbol{\beta}\) are the spatial filters for the seeds and targets, respectively, and \(\boldsymbol{E}\) is the imaginary part of the transformed cross-spectral density between the seeds and targets. All elements are frequency-dependent, however this is omitted for readability. MIC is bound between \([-1, 1]\) where the absolute value reflects connectivity strength and the sign reflects the phase angle difference between signals.

MIC can also be computed between identical sets of seeds and targets, allowing connectivity within a single set of signals to be estimated. This is possible as a result of the exclusion of zero phase lag components from the connectivity estimates, which would otherwise return a perfect correlation.

In this instance, we see MIC reveal that in addition to the 13-18 Hz peak, a previously unobserved peak in connectivity around 9 Hz is present. Furthermore, the previous peak around 27 Hz is much less pronounced. This may indicate that the connectivity was the result of some distal interaction exacerbated by strong source mixing, which biased the bivariate connectivity estimate.

Furthermore, spatial patterns of connectivity can be constructed from the spatial filters to give a picture of the location of the channels involved in the connectivity [4]. This information is stored under attrs['patterns'] of the connectivity class, with one value per frequency for each channel in the seeds and targets. As with MIC, the absolute value of the patterns reflect the strength, however the sign differences can be used to visualise the orientation of the underlying dipole sources. The spatial patterns are not bound between \([-1, 1]\).

Here, we average across the patterns in the 13-18 Hz range. Plotting the patterns shows that the greatest connectivity between the left and right hemispheres occurs at the left and right posterior and left central regions, based on the areas with the largest absolute values. Using the signs of the values, we can infer the existence of a dipole source between the central and posterior regions of the left hemisphere accounting for the connectivity contributions (represented on the plot as a green line).

Note: The spatial patterns are not a substitute for source reconstruction. If you need the spatial patterns in source space, you should perform source reconstruction before computing connectivity (see e.g. Compute coherence in source space using a MNE inverse solution).

Although it can be useful to analyse the single, largest connectivity component with MIC, multiple such components exist and can be examined with MIM. MIM can be thought of as an average of all connectivity components between the seeds and targets, and can be useful for an exploration of all available components. It is unnecessary to use the spatial filters of each component explicitly, and instead the desired result can be achieved from \(E\) alone (Eq. 14 of [1]):

\(\textrm{MIM}=tr(\boldsymbol{EE}^T)\),

where again the frequency dependence is omitted.

Unlike MIC, MIM is positive-valued and can be > 1. Without normalisation, MIM can be thought of as reflecting the total interaction between the seeds and targets. MIM can be normalised to lie in the range \([0, 1]\) by dividing the scores by the number of unique channels in the seeds and targets. Normalised MIM represents the interaction per channel, which can be biased by factors such as the presence of channels with little to no interaction. In line with the preferences of the method’s authors [1], since normalisation alters the interpretability of the results, normalisation is not performed by default.

Here we see MIM reveal the strongest connectivity component to be around 10 Hz, with the higher frequency 13-18 Hz connectivity no longer being so prominent. This suggests that, across all components in the data, there may be more lower frequency connectivity sources than higher frequency sources. Thus, when combining these different components in MIM, the peak around 10 Hz remains, but the 13-18 Hz connectivity is diminished relative to the single, largest connectivity component of MIC.

Looking at the values for normalised MIM, we see it has a maximum of ~0.1. The relatively small connectivity values thus indicate that many of the channels show little to no interaction.

Additionally, the instance where the seeds and targets are identical can be considered as a special case of MIM: the global interaction measure (GIM; Eq. 15 of [1]). Again, this allows connectivity within a single set of signals to be estimated. Computing GIM follows from Eq. 14, however since each interaction is considered twice, correcting the connectivity by a factor of \(\frac{1}{2}\) is necessary (the correction is performed automatically in this implementation). Like MIM, GIM can also be > 1, but it can again be normalised to lie in the range \([0, 1]\) by dividing by the number of unique channels in the seeds and targets. However, since normalisation alters the interpretability of the results (i.e. interaction per channel for normalised GIM vs. total interaction for standard GIM), GIM is not normalised by default.

With GIM, we find a broad connectivity peak around 10 Hz, with an additional peak around 20 Hz. The differences observed with GIM highlight the presence of interactions within each hemisphere that are absent for MIC or MIM. Furthermore, the values for normalised GIM are higher than for MIM, with a maximum of ~0.2, again indicating the presence of interactions across channels within each hemisphere.

An important issue to consider when using these multivariate methods is overfitting, which risks biasing connectivity estimates to maximise noise in the data. This risk can be reduced by performing a preliminary dimensionality reduction prior to estimating the connectivity with a singular value decomposition (Eqs. 32 & 33 of [1]). The degree of this dimensionality reduction can be specified using the rank argument, which by default will not perform any dimensionality reduction (assuming your data is full rank; see below if not). Choosing an expected rank of the data requires a priori knowledge about the number of components you expect to observe in the data.

When comparing MIC/MIM scores across recordings, it is highly recommended to estimate connectivity from the same number of channels (or equally from the same degree of rank subspace projection) to avoid biases in connectivity estimates. Bias can be avoided by specifying a consistent rank subspace to project to using the rank argument, standardising your connectivity estimates regardless of changes in e.g. the number of channels across recordings. Note that this does not refer to the number of seeds and targets within a connection being identical, rather to the number of seeds and targets across connections.

Here, we will project our seed and target data to only the first 25 components of our rank subspace. Results for MIM show that the general spectral pattern of connectivity is retained in the rank subspace-projected data, suggesting that a fair degree of redundant connectivity information is contained in the remaining 50 components of the seed and target data. We also assert that the spatial patterns of MIC are returned in the original sensor space despite this rank subspace projection, being reconstructed using the products of the singular value decomposition (Eqs. 46 & 47 of [1]).

In the case that your data is not full rank and rank is left as None, an automatic rank computation is performed and an appropriate degree of dimensionality reduction will be enforced. The rank of the data is determined by computing the singular values of the data and finding those within a factor of \(1e^{-6}\) relative to the largest singular value.

Whilst unlikely, there may be scenarios in which this threshold is too lenient. In these cases, you should inspect the singular values of your data to identify an appropriate degree of dimensionality reduction to perform, which you can then specify manually using the rank argument. The code below shows one possible approach for finding an appropriate rank of close-to-singular data with a more conservative threshold.

These multivariate methods offer many benefits in the form of dimensionality reduction, signal-to-noise ratio improvements, and invariance to estimate-biasing source mixing; however, no method is perfect. Important considerations must be taken into account when choosing methods based on the imaginary part of coherency such as MIC or MIM versus those based on coherency/coherence, such as CaCoh.

In short, if you want to examine connectivity between signals from the same modality or from different modalities using a shared reference, you should consider using MIC and MIM to avoid spurious connectivity estimates stemming from e.g. volume conduction artefacts.

On the other hand, if you want to examine connectivity between signals from different modalities using different references, CaCoh is a more appropriate method than MIC/MIM. This is because volume conduction artefacts are of less concern, and CaCoh does not risk biasing connectivity estimates towards interactions with particular phase lags like MIC/MIM.

These scenarios are described in more detail in the Comparison of coherency-based methods example.

Arne Ewald, Laura Marzetti, Filippo Zappasodi, Frank C. Meinecke, and Guido Nolte. Estimating true brain connectivity from EEG/MEG data invariant to linear and static transformations in sensor space. NeuroImage, 60(1):476–488, 2012. doi:10.1016/j.neuroimage.2011.11.084.

Guido Nolte, Ou Bai, Lewis Wheaton, Zoltan Mari, Sherry Vorbach, and Mark Hallett. Identifying true brain interaction from EEG data using the imaginary part of coherency. Clinical Neurophysiology, 115(10):2292–2307, 2004. doi:10.1016/j.clinph.2004.04.029.

Carmen Vidaurre, Guido Nolte, Ingmar E.J. de Vries, M. Gómez, Tjeerd W. Boonstra, K.-R. Müller, Arno Villringer, and Vadim V. Nikulin. Canonical maximization of coherence: a novel tool for investigation of neuronal interactions between two datasets. NeuroImage, 201:116009, 2019. doi:10.1016/j.neuroimage.2019.116009.

Stefan Haufe, Frank Meinecke, Kai Görgen, Sven Dähne, John-Dylan Haynes, Benjamin Blankertz, and Felix Bießmann. On the interpretation of weight vectors of linear models in multivariate neuroimaging. NeuroImage, 87:96–110, 2014. doi:10.1016/j.neuroimage.2013.10.067.

Total running time of the script: (0 minutes 23.625 seconds)

Download Jupyter notebook: mic_mim.ipynb

Download Python source code: mic_mim.py

Download zipped: mic_mim.zip

Gallery generated by Sphinx-Gallery

Compute multivariate coherency/coherence

Compute seed-based time-frequency connectivity in sensor space

---

## Compute Phase Slope Index (PSI) in source space for a visual stimulus#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/mne_inverse_psi_visual.html

**Contents:**
- Compute Phase Slope Index (PSI) in source space for a visual stimulus#
- References#

Go to the end to download the full example code.

This example demonstrates how the phase slope index (PSI) [1] can be computed in source space based on single trial dSPM source estimates. In addition, the example shows advanced usage of the connectivity estimation routines by first extracting a label time course for each epoch and then combining the label time course with the single trial source estimates to compute the connectivity.

The result clearly shows how the activity in the visual label precedes more widespread activity (as a postivive PSI means the label time course is leading).

Guido Nolte, Andreas Ziehe, Vadim V. Nikulin, Alois Schlögl, Nicole Krämer, Tom Brismar, and Klaus-Robert Müller. Robustly estimating the flow direction of information in complex physical systems. Physical Review Letters, 2008. doi:10.1103/PhysRevLett.100.234101.

Total running time of the script: (0 minutes 14.998 seconds)

Download Jupyter notebook: mne_inverse_psi_visual.ipynb

Download Python source code: mne_inverse_psi_visual.py

Download zipped: mne_inverse_psi_visual.zip

Gallery generated by Sphinx-Gallery

Comparison of coherency-based methods

Compute all-to-all connectivity in sensor space

---

## Compute seed-based time-frequency connectivity in sensor space#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/cwt_sensor_connectivity.html

**Contents:**
- Compute seed-based time-frequency connectivity in sensor space#
- References#

Go to the end to download the full example code.

Computes the connectivity between a seed-gradiometer close to the visual cortex and all other gradiometers. The connectivity is computed in the time-frequency domain using Morlet wavelets and the debiased squared weighted phase lag index [1] is used as connectivity metric.

Martin Vinck, Robert Oostenveld, Marijn van Wingerden, Franscesco Battaglia, and Cyriel M.A. Pennartz. An improved index of phase-synchronization for electrophysiological data in the presence of volume-conduction, noise and sample-size bias. NeuroImage, 55(4):1548–1565, 2011. doi:10.1016/j.neuroimage.2011.01.055.

Total running time of the script: (0 minutes 3.978 seconds)

Download Jupyter notebook: cwt_sensor_connectivity.ipynb

Download Python source code: cwt_sensor_connectivity.py

Download zipped: cwt_sensor_connectivity.zip

Gallery generated by Sphinx-Gallery

Compute multivariate measures of the imaginary part of coherency

Compute source space connectivity and visualize it using a circular graph

---

## Compute source space connectivity and visualize it using a circular graph#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/mne_inverse_label_connectivity.html

**Contents:**
- Compute source space connectivity and visualize it using a circular graph#
- Load our data#
- Compute inverse solutions and their connectivity#
- Make a connectivity plot#
- Make multiple connectivity plots in the same figure#
- Save the figure (optional)#

Go to the end to download the full example code.

This example computes the all-to-all connectivity between 68 regions in source space based on dSPM inverse solutions and a FreeSurfer cortical parcellation. The connectivity is visualized using a circular graph which is ordered based on the locations of the regions in the axial plane.

First we’ll load the data we’ll use in connectivity estimation. We’ll use the sample MEG data provided with MNE.

Next, we need to compute the inverse solution for this data. This will return the sources / source activity that we’ll use in computing connectivity. We’ll compute the connectivity in the alpha band of these sources. We can specify particular frequencies to include in the connectivity with the fmin and fmax flags. Notice from the status messages how mne-python:

reads an epoch from the raw file

applies SSP and baseline correction

computes the inverse to obtain a source estimate

averages the source estimate to obtain a time series for each label

includes the label time series in the connectivity computation

moves to the next epoch.

This behaviour is because we are using generators. Since we only need to operate on the data one epoch at a time, using a generator allows us to compute connectivity in a computationally efficient manner where the amount of memory (RAM) needed is independent from the number of epochs.

Now, we visualize this connectivity using a circular graph layout.

We can also assign these connectivity plots to axes in a figure. Below we’ll show the connectivity plot using two different connectivity methods.

By default matplotlib does not save using the facecolor, even though this was set when the figure was generated. If not set via savefig, the labels, title, and legend will be cut off from the output png file.

Total running time of the script: (0 minutes 5.581 seconds)

Download Jupyter notebook: mne_inverse_label_connectivity.ipynb

Download Python source code: mne_inverse_label_connectivity.py

Download zipped: mne_inverse_label_connectivity.zip

Gallery generated by Sphinx-Gallery

Compute seed-based time-frequency connectivity in sensor space

Using the connectivity classes

---

## Compute vector autoregressive model (linear system)#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/dynamic/mne_var_connectivity.html

**Contents:**
- Compute vector autoregressive model (linear system)#
- Load the data#
- Crop the data for this example#
- Create Windows of Data (Epochs) Using MNE-Python#
- Compute the VAR model for all windows#
- Evaluate the VAR model fit#
- Compute one VAR model using all epochs#
- Evaluate model fit again#

Go to the end to download the full example code.

Compute a VAR (linear system) model from time-series activity [1] using a continuous iEEG recording.

In this example, we will demonstrate how to compute a VAR model with different statistical assumptions.

Here, we first download an ECoG dataset that was recorded from a patient with epilepsy. To facilitate loading the data, we use mne-bids.

Then, we will do some basic filtering and preprocessing using MNE-Python.

We find the onset time of the seizure and remove all data after that time. In this example, we are only interested in analyzing the interictal (non-seizure) data period.

One might be interested in analyzing the seizure period also, which we leave as an exercise for our readers!

We have a continuous iEEG snapshot that is about 60 seconds long (after cropping). We would like to estimate a VAR model over a sliding window of 500 milliseconds with a 250 millisecond step size.

We can use mne.make_fixed_length_epochs to create an Epochs data structure representing this sliding window.

Now, we are ready to compute our VAR model. We will compute a VAR model for each Epoch and return an EpochConnectivity data structure. Each Epoch here represents a separate VAR model. Taken together, these represent a time-varying linear system.

We can now evaluate the model fit by computing the residuals of the model and visualizing them. In addition, we can evaluate the covariance of the residuals. This will compute an independent VAR model for each epoch (window) of data.

By setting model='dynamic', we instead treat each Epoch as a sample of the same VAR model and thus we only estimate one VAR model. One might do this when one suspects the data is stationary and one VAR model represents all epochs.

We can now evaluate the model fit again as done earlier. This model fit will of course have higher residuals than before as we are only fitting 1 VAR model to all the epochs.

Total running time of the script: (0 minutes 57.345 seconds)

Download Jupyter notebook: mne_var_connectivity.ipynb

Download Python source code: mne_var_connectivity.py

Download zipped: mne_var_connectivity.zip

Gallery generated by Sphinx-Gallery

Dynamic Connectivity Examples

---

## Dynamic Connectivity Examples#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/dynamic/index.html

**Contents:**
- Dynamic Connectivity Examples#

Examples demonstrating connectivity analysis with dynamics. For example, this can be a vector auto-regressive model (also known as a linear dynamical system). These classes of models are generative and model the dynamics and evolution of the data.

Compute vector autoregressive model (linear system)

Working with ragged indices for multivariate connectivity

Compute vector autoregressive model (linear system)

---

## Examples#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/index.html

**Contents:**
- Examples#
- Dynamic Connectivity Examples#

Examples demonstrating connectivity analysis in sensor and source space.

Comparing PLI, wPLI, and dPLI

Comparing spectral connectivity computed over time or over trials

Comparison of coherency-based methods

Compute Phase Slope Index (PSI) in source space for a visual stimulus

Compute all-to-all connectivity in sensor space

Compute coherence in source space using a MNE inverse solution

Compute directionality of connectivity with multivariate Granger causality

Compute envelope correlations in source space

Compute envelope correlations in volume source space

Compute full spectrum source space connectivity between labels

Compute mixed source space connectivity and visualize it using a circular graph

Compute multivariate coherency/coherence

Compute multivariate measures of the imaginary part of coherency

Compute seed-based time-frequency connectivity in sensor space

Compute source space connectivity and visualize it using a circular graph

Using the connectivity classes

Working with ragged indices for multivariate connectivity

Examples demonstrating connectivity analysis with dynamics. For example, this can be a vector auto-regressive model (also known as a linear dynamical system). These classes of models are generative and model the dynamics and evolution of the data.

Compute vector autoregressive model (linear system)

Download all examples in Python source code: auto_examples_python.zip

Download all examples in Jupyter notebooks: auto_examples_jupyter.zip

Gallery generated by Sphinx-Gallery

mne_connectivity.make_signals_in_freq_bands

Comparing PLI, wPLI, and dPLI

---

## mne_connectivity.check_indices#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.check_indices.html

**Contents:**
- mne_connectivity.check_indices#

Check indices parameter for bivariate connectivity.

Tuple containing index pairs.

Indices for bivariate connectivity should be a tuple of length 2, containing the channel indices for the seed and target channel pairs, respectively. Seed and target indices should be equal-length array-likes of integers representing the indices of the individual channels in the data.

mne_connectivity.seed_target_multivariate_indices

mne_connectivity.select_order

---

## mne_connectivity.Connectivity#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.Connectivity.html

**Contents:**
- mne_connectivity.Connectivity#
- Examples using mne_connectivity.Connectivity#

Connectivity class without frequency or time component.

This is an array of shape (n_connections,), or (n_nodes, n_nodes). This describes a connectivity matrix/graph that does not vary over time, frequency, or epochs.

The connectivity data that is a raveled array of (n_estimated_nodes, ...) shape. The n_estimated_nodes is equal to n_nodes_in * n_nodes_out if one is computing the full connectivity, or a subset of nodes equal to the length of indices passed in.

The number of nodes in the dataset used to compute connectivity. This should be equal to the number of signals in the original dataset.

The names of the nodes of the dataset used to compute connectivity. If ‘None’ (default), then names will be a list of integers from 0 to n_nodes. If a list of names, then it must be equal in length to n_nodes.

The indices of relevant connectivity data. If 'all' (default), then data is connectivity between all nodes. If 'symmetric', then data is symmetric connectivity between all nodes. If a tuple, then the first list represents the “in nodes”, and the second list represents the “out nodes”. See “Notes” for more information.

The method name used to compute connectivity.

The number of epochs used in the computation of connectivity, by default None.

Extra connectivity parameters. These may include freqs for spectral connectivity, and/or times for connectivity over time. In addition, these may include extra parameters that are stored as xarray attrs.

Xarray attributes of connectivity.

Generate block companion matrix.

The coordinates of the xarray data.

The dimensions of the xarray data.

Indices of connectivity data.

The method used to compute connectivity.

The number of epochs the connectivity data varies over.

Number of epochs used in computation of connectivity.

The number of nodes in the original dataset.

Shape of raveled connectivity.

Xarray of the connectivity data.

Append another connectivity structure.

Combine connectivity data over epochs.

Get connectivity data as a numpy array.

plot_circle(**kwargs)

Visualize connectivity as a circular graph.

Predict samples on actual data.

rename_nodes(mapping)

Save connectivity data to disk.

simulate(n_samples[, noise_func, random_state])

Simulate vector autoregressive (VAR) model.

get_epoch_annotations

Append another connectivity structure.

The Epoched Connectivity class to append.

The altered Epoched Connectivity class.

Xarray attributes of connectivity.

Combine connectivity data over epochs.

How to combine correlation estimates across epochs. Default is ‘mean’. If callable, it must accept one positional input. For example:

The combined connectivity data structure.

Generate block companion matrix.

Returns the data matrix if the model is VAR(1).

The coordinates of the xarray data.

The dimensions of the xarray data.

Get connectivity data as a numpy array.

How to format the output, by default ‘raveled’, which will represent each connectivity matrix as a (n_nodes_in * n_nodes_out,) list. If ‘dense’, then will return each connectivity matrix as a 2D array. If ‘compact’ (default) then will return ‘raveled’ if indices were defined as a list of tuples, or dense if indices is ‘all’. Multivariate connectivity data cannot be returned in a dense form.

The output connectivity data.

Indices of connectivity data.

Either ‘all’ for all-to-all connectivity, ‘symmetric’ for symmetric all-to-all connectivity, or a tuple of lists representing the node-to-nodes that connectivity was computed.

The method used to compute connectivity.

The number of epochs the connectivity data varies over.

Number of epochs used in computation of connectivity.

Can be ‘None’, if there was no epochs used. This is equivalent to the number of epochs, if there is no combining of epochs.

The number of nodes in the original dataset.

Even if indices defines a subset of nodes that were computed, this should be the total number of nodes in the original dataset.

Visualize connectivity as a circular graph.

Node names. The order corresponds to the order in con.

Two arrays with indices of connections for which the connections strengths are defined in con. Only needed if con is a 1D array.

If not None, only the n_lines strongest connections (strength=abs(con)) are drawn.

Array with node positions in degrees. If None, the nodes are equally spaced on the circle. See mne.viz.circular_layout.

Width of each node in degrees. If None, the minimum angle between any two nodes is used as the width.

The relative height of the colored bar labeling each node. Default 1.0 is the standard height.

List with the color to use for each node. If fewer colors than nodes are provided, the colors will be repeated. Any color supported by matplotlib can be used, e.g., RGBA tuples, named colors.

Color to use for background. See matplotlib.colors.

Color to use for text. See matplotlib.colors.

Color to use for lines around nodes. See matplotlib.colors.

Line width to use for connections.

Colormap to use for coloring the connections.

Minimum value for colormap. If None, it is determined automatically.

Maximum value for colormap. If None, it is determined automatically.

Display a colorbar or not.

Size of the colorbar.

Position of the colorbar.

Font size to use for title.

Font size to use for node names.

Font size to use for colorbar.

Space to add around figure to accommodate long labels.

The axes to use to plot the connectivity circle.

The figure to use. If None, a new figure with the specified background color will be created.

Deprecated: will be removed in version 0.5.

Location of the subplot when creating figures with multiple plots. E.g. 121 or (1, 2, 1) for 1 row, 2 columns, plot 1. See matplotlib.pyplot.subplot.

Deprecated: will be removed in version 0.5.

When enabled, left-click on a node to show only connections to that node. Right-click shows all connections.

This code is based on a circle graph example by Nicolas P. Rougier

By default, matplotlib.pyplot.savefig() does not take facecolor into account when saving, even if set when a figure is generated. This can be addressed via, e.g.:

If facecolor is not set via matplotlib.pyplot.savefig(), the figure labels, title, and legend may be cut off in the output figure.

Predict samples on actual data.

The result of this function is used for calculating the residuals.

Epoched or continuous data set. Has shape (n_epochs, n_signals, n_times) or (n_signals, n_times).

Data as predicted by the VAR model of shape same as data.

Residuals are obtained by r = x - var.predict(x).

To compute residual covariances:

Mapping from original node names (keys) to new node names (values).

Save connectivity data to disk.

Can later be loaded using the function mne_connectivity.read_connectivity().

The filepath to save the data. Data is saved as netCDF files (.nc extension).

Shape of raveled connectivity.

Simulate vector autoregressive (VAR) model.

This function generates data from the VAR model.

Number of samples to generate.

This function is used to create the generating noise process. If set to None, Gaussian white noise with zero mean and unit variance is used.

If random_state is an int, it will be used as a seed for RandomState. If None, the seed will be obtained from the operating system (see RandomState for details). Default is None.

Xarray of the connectivity data.

Compute vector autoregressive model (linear system)

mne_connectivity.TemporalConnectivity

---

## mne_connectivity.degree#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.degree.html

**Contents:**
- mne_connectivity.degree#
- Examples using mne_connectivity.degree#

Compute the undirected degree of a connectivity matrix.

The connectivity matrix.

The proportion of edges to keep in the graph before computing the degree. The value should be between 0 and 1.

During thresholding, the symmetry of the connectivity matrix is auto-detected based on numpy.allclose() of it with its transpose.

Compute envelope correlations in source space

Compute envelope correlations in volume source space

mne_connectivity.symmetric_orth

mne_connectivity.seed_target_indices

---

## mne_connectivity.envelope_correlation#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.envelope_correlation.html

**Contents:**
- mne_connectivity.envelope_correlation#
- Examples using mne_connectivity.envelope_correlation#

Compute the envelope correlation.

The data from which to compute connectivity. The array-like object can also be a list/generator of array, each with shape (n_signals, n_times), or a SourceEstimate object (and stc.data will be used). If it’s float data, the Hilbert transform will be applied; if it’s complex data, it’s assumed the Hilbert has already been applied.

A list of names associated with the signals in data. If None, will be a list of indices of the number of nodes.

Whether to orthogonalize with the pairwise method or not. Defaults to ‘pairwise’. Note that when False, the correlation matrix will not be returned with absolute values.

If True (default False), square and take the log before orthonalizing envelopes or computing correlations.

If True (default), then take the absolute value of correlation coefficients before making each epoch’s correlation matrix symmetric (and thus before combining matrices across epochs). Only used when orthogonalize='pairwise'.

Control verbosity of the logging output. If None, use the default verbosity level. See the logging documentation and mne.verbose() for details. Should only be passed as a keyword argument.

The pairwise orthogonal envelope correlations. This matrix is symmetric. The array will have three dimensions, the first of which is n_epochs. The data shape would be (n_epochs, (n_nodes + 1) * n_nodes / 2).

This function computes the power envelope correlation between orthogonalized signals [1][2].

If you would like to combine Epochs after the fact using some function over the Epochs axis, see the combine function from EpochConnectivity classes.

Joerg F Hipp, David J Hawellek, Maurizio Corbetta, Markus Siegel, and Andreas K Engel. Large-scale cortical correlation structure of spontaneous oscillatory activity. Nature Neuroscience, 15(6):884–890, 2012. doi:10.1038/nn.3101.

Sheraz Khan, Javeria A. Hashmi, Fahimeh Mamashli, Konstantinos Michmizos, Manfred G. Kitzbichler, Hari Bharadwaj, Yousra Bekhti, Santosh Ganesan, Keri-Lee A. Garel, Susan Whitfield-Gabrieli, Randy L. Gollub, Jian Kong, Lucia M. Vaina, Kunjan D. Rana, Steven M. Stufflebeam, Matti S. Hämäläinen, and Tal Kenet. Maturation trajectories of cortical resting-state networks depend on the mediating frequency band. NeuroImage, 174:57–68, 2018. doi:10.1016/j.neuroimage.2018.02.018.

Compute envelope correlations in source space

Compute envelope correlations in volume source space

mne_connectivity.EpochSpectroTemporalConnectivity

mne_connectivity.phase_slope_index

---

## mne_connectivity.EpochConnectivity#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.EpochConnectivity.html

**Contents:**
- mne_connectivity.EpochConnectivity#

Epoch connectivity class.

This is an array of shape (n_epochs, n_connections), or (n_epochs, n_nodes, n_nodes). This describes how connectivity varies for different epochs.

The connectivity data that is a raveled array of (n_estimated_nodes, ...) shape. The n_estimated_nodes is equal to n_nodes_in * n_nodes_out if one is computing the full connectivity, or a subset of nodes equal to the length of indices passed in.

The number of nodes in the dataset used to compute connectivity. This should be equal to the number of signals in the original dataset.

The names of the nodes of the dataset used to compute connectivity. If ‘None’ (default), then names will be a list of integers from 0 to n_nodes. If a list of names, then it must be equal in length to n_nodes.

The indices of relevant connectivity data. If 'all' (default), then data is connectivity between all nodes. If 'symmetric', then data is symmetric connectivity between all nodes. If a tuple, then the first list represents the “in nodes”, and the second list represents the “out nodes”. See “Notes” for more information.

The method name used to compute connectivity.

The number of epochs used in the computation of connectivity, by default None.

Extra connectivity parameters. These may include freqs for spectral connectivity, and/or times for connectivity over time. In addition, these may include extra parameters that are stored as xarray attrs.

Xarray attributes of connectivity.

Generate block companion matrix.

The coordinates of the xarray data.

The dimensions of the xarray data.

Indices of connectivity data.

The method used to compute connectivity.

The number of epochs the connectivity data varies over.

Number of epochs used in computation of connectivity.

The number of nodes in the original dataset.

Shape of raveled connectivity.

Xarray of the connectivity data.

Append another connectivity structure.

Combine connectivity data over epochs.

Get connectivity data as a numpy array.

plot_circle(**kwargs)

Visualize connectivity as a circular graph.

Predict samples on actual data.

rename_nodes(mapping)

Save connectivity data to disk.

simulate(n_samples[, noise_func, random_state])

Simulate vector autoregressive (VAR) model.

get_epoch_annotations

Append another connectivity structure.

The Epoched Connectivity class to append.

The altered Epoched Connectivity class.

Xarray attributes of connectivity.

Combine connectivity data over epochs.

How to combine correlation estimates across epochs. Default is ‘mean’. If callable, it must accept one positional input. For example:

The combined connectivity data structure.

Generate block companion matrix.

Returns the data matrix if the model is VAR(1).

The coordinates of the xarray data.

The dimensions of the xarray data.

Get connectivity data as a numpy array.

How to format the output, by default ‘raveled’, which will represent each connectivity matrix as a (n_nodes_in * n_nodes_out,) list. If ‘dense’, then will return each connectivity matrix as a 2D array. If ‘compact’ (default) then will return ‘raveled’ if indices were defined as a list of tuples, or dense if indices is ‘all’. Multivariate connectivity data cannot be returned in a dense form.

The output connectivity data.

Indices of connectivity data.

Either ‘all’ for all-to-all connectivity, ‘symmetric’ for symmetric all-to-all connectivity, or a tuple of lists representing the node-to-nodes that connectivity was computed.

The method used to compute connectivity.

The number of epochs the connectivity data varies over.

Number of epochs used in computation of connectivity.

Can be ‘None’, if there was no epochs used. This is equivalent to the number of epochs, if there is no combining of epochs.

The number of nodes in the original dataset.

Even if indices defines a subset of nodes that were computed, this should be the total number of nodes in the original dataset.

Visualize connectivity as a circular graph.

Node names. The order corresponds to the order in con.

Two arrays with indices of connections for which the connections strengths are defined in con. Only needed if con is a 1D array.

If not None, only the n_lines strongest connections (strength=abs(con)) are drawn.

Array with node positions in degrees. If None, the nodes are equally spaced on the circle. See mne.viz.circular_layout.

Width of each node in degrees. If None, the minimum angle between any two nodes is used as the width.

The relative height of the colored bar labeling each node. Default 1.0 is the standard height.

List with the color to use for each node. If fewer colors than nodes are provided, the colors will be repeated. Any color supported by matplotlib can be used, e.g., RGBA tuples, named colors.

Color to use for background. See matplotlib.colors.

Color to use for text. See matplotlib.colors.

Color to use for lines around nodes. See matplotlib.colors.

Line width to use for connections.

Colormap to use for coloring the connections.

Minimum value for colormap. If None, it is determined automatically.

Maximum value for colormap. If None, it is determined automatically.

Display a colorbar or not.

Size of the colorbar.

Position of the colorbar.

Font size to use for title.

Font size to use for node names.

Font size to use for colorbar.

Space to add around figure to accommodate long labels.

The axes to use to plot the connectivity circle.

The figure to use. If None, a new figure with the specified background color will be created.

Deprecated: will be removed in version 0.5.

Location of the subplot when creating figures with multiple plots. E.g. 121 or (1, 2, 1) for 1 row, 2 columns, plot 1. See matplotlib.pyplot.subplot.

Deprecated: will be removed in version 0.5.

When enabled, left-click on a node to show only connections to that node. Right-click shows all connections.

This code is based on a circle graph example by Nicolas P. Rougier

By default, matplotlib.pyplot.savefig() does not take facecolor into account when saving, even if set when a figure is generated. This can be addressed via, e.g.:

If facecolor is not set via matplotlib.pyplot.savefig(), the figure labels, title, and legend may be cut off in the output figure.

Predict samples on actual data.

The result of this function is used for calculating the residuals.

Epoched or continuous data set. Has shape (n_epochs, n_signals, n_times) or (n_signals, n_times).

Data as predicted by the VAR model of shape same as data.

Residuals are obtained by r = x - var.predict(x).

To compute residual covariances:

Mapping from original node names (keys) to new node names (values).

Save connectivity data to disk.

Can later be loaded using the function mne_connectivity.read_connectivity().

The filepath to save the data. Data is saved as netCDF files (.nc extension).

Shape of raveled connectivity.

Simulate vector autoregressive (VAR) model.

This function generates data from the VAR model.

Number of samples to generate.

This function is used to create the generating noise process. If set to None, Gaussian white noise with zero mean and unit variance is used.

If random_state is an int, it will be used as a seed for RandomState. If None, the seed will be obtained from the operating system (see RandomState for details). Default is None.

Xarray of the connectivity data.

mne_connectivity.SpectroTemporalConnectivity

mne_connectivity.EpochTemporalConnectivity

---

## mne_connectivity.EpochSpectralConnectivity#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.EpochSpectralConnectivity.html

**Contents:**
- mne_connectivity.EpochSpectralConnectivity#

Spectral connectivity class over Epochs.

This is an array of shape (n_epochs, n_connections, n_freqs), or (n_epochs, n_nodes, n_nodes, n_freqs). This describes how connectivity varies over frequencies for different epochs.

The connectivity data that is a raveled array of (n_estimated_nodes, ...) shape. The n_estimated_nodes is equal to n_nodes_in * n_nodes_out if one is computing the full connectivity, or a subset of nodes equal to the length of indices passed in.

The frequencies at which the connectivity data is computed over. If the frequencies are “frequency bands” (i.e. gamma band), then these are the median of those bands.

The number of nodes in the dataset used to compute connectivity. This should be equal to the number of signals in the original dataset.

The names of the nodes of the dataset used to compute connectivity. If ‘None’ (default), then names will be a list of integers from 0 to n_nodes. If a list of names, then it must be equal in length to n_nodes.

The indices of relevant connectivity data. If 'all' (default), then data is connectivity between all nodes. If 'symmetric', then data is symmetric connectivity between all nodes. If a tuple, then the first list represents the “in nodes”, and the second list represents the “out nodes”. See “Notes” for more information.

The method name used to compute connectivity.

The type of method used to compute spectral analysis, by default None.

Extra connectivity parameters. These may include freqs for spectral connectivity, and/or times for connectivity over time. In addition, these may include extra parameters that are stored as xarray attrs.

Xarray attributes of connectivity.

Generate block companion matrix.

The coordinates of the xarray data.

The dimensions of the xarray data.

The frequency points of the connectivity data.

Indices of connectivity data.

The method used to compute connectivity.

The number of epochs the connectivity data varies over.

Number of epochs used in computation of connectivity.

The number of nodes in the original dataset.

Shape of raveled connectivity.

Xarray of the connectivity data.

Append another connectivity structure.

Combine connectivity data over epochs.

Get connectivity data as a numpy array.

plot_circle(**kwargs)

Visualize connectivity as a circular graph.

Predict samples on actual data.

rename_nodes(mapping)

Save connectivity data to disk.

simulate(n_samples[, noise_func, random_state])

Simulate vector autoregressive (VAR) model.

get_epoch_annotations

Append another connectivity structure.

The Epoched Connectivity class to append.

The altered Epoched Connectivity class.

Xarray attributes of connectivity.

Combine connectivity data over epochs.

How to combine correlation estimates across epochs. Default is ‘mean’. If callable, it must accept one positional input. For example:

The combined connectivity data structure.

Generate block companion matrix.

Returns the data matrix if the model is VAR(1).

The coordinates of the xarray data.

The dimensions of the xarray data.

The frequency points of the connectivity data.

If these are computed over a frequency band, it will be the median frequency of the frequency band.

Get connectivity data as a numpy array.

How to format the output, by default ‘raveled’, which will represent each connectivity matrix as a (n_nodes_in * n_nodes_out,) list. If ‘dense’, then will return each connectivity matrix as a 2D array. If ‘compact’ (default) then will return ‘raveled’ if indices were defined as a list of tuples, or dense if indices is ‘all’. Multivariate connectivity data cannot be returned in a dense form.

The output connectivity data.

Indices of connectivity data.

Either ‘all’ for all-to-all connectivity, ‘symmetric’ for symmetric all-to-all connectivity, or a tuple of lists representing the node-to-nodes that connectivity was computed.

The method used to compute connectivity.

The number of epochs the connectivity data varies over.

Number of epochs used in computation of connectivity.

Can be ‘None’, if there was no epochs used. This is equivalent to the number of epochs, if there is no combining of epochs.

The number of nodes in the original dataset.

Even if indices defines a subset of nodes that were computed, this should be the total number of nodes in the original dataset.

Visualize connectivity as a circular graph.

Node names. The order corresponds to the order in con.

Two arrays with indices of connections for which the connections strengths are defined in con. Only needed if con is a 1D array.

If not None, only the n_lines strongest connections (strength=abs(con)) are drawn.

Array with node positions in degrees. If None, the nodes are equally spaced on the circle. See mne.viz.circular_layout.

Width of each node in degrees. If None, the minimum angle between any two nodes is used as the width.

The relative height of the colored bar labeling each node. Default 1.0 is the standard height.

List with the color to use for each node. If fewer colors than nodes are provided, the colors will be repeated. Any color supported by matplotlib can be used, e.g., RGBA tuples, named colors.

Color to use for background. See matplotlib.colors.

Color to use for text. See matplotlib.colors.

Color to use for lines around nodes. See matplotlib.colors.

Line width to use for connections.

Colormap to use for coloring the connections.

Minimum value for colormap. If None, it is determined automatically.

Maximum value for colormap. If None, it is determined automatically.

Display a colorbar or not.

Size of the colorbar.

Position of the colorbar.

Font size to use for title.

Font size to use for node names.

Font size to use for colorbar.

Space to add around figure to accommodate long labels.

The axes to use to plot the connectivity circle.

The figure to use. If None, a new figure with the specified background color will be created.

Deprecated: will be removed in version 0.5.

Location of the subplot when creating figures with multiple plots. E.g. 121 or (1, 2, 1) for 1 row, 2 columns, plot 1. See matplotlib.pyplot.subplot.

Deprecated: will be removed in version 0.5.

When enabled, left-click on a node to show only connections to that node. Right-click shows all connections.

This code is based on a circle graph example by Nicolas P. Rougier

By default, matplotlib.pyplot.savefig() does not take facecolor into account when saving, even if set when a figure is generated. This can be addressed via, e.g.:

If facecolor is not set via matplotlib.pyplot.savefig(), the figure labels, title, and legend may be cut off in the output figure.

Predict samples on actual data.

The result of this function is used for calculating the residuals.

Epoched or continuous data set. Has shape (n_epochs, n_signals, n_times) or (n_signals, n_times).

Data as predicted by the VAR model of shape same as data.

Residuals are obtained by r = x - var.predict(x).

To compute residual covariances:

Mapping from original node names (keys) to new node names (values).

Save connectivity data to disk.

Can later be loaded using the function mne_connectivity.read_connectivity().

The filepath to save the data. Data is saved as netCDF files (.nc extension).

Shape of raveled connectivity.

Simulate vector autoregressive (VAR) model.

This function generates data from the VAR model.

Number of samples to generate.

This function is used to create the generating noise process. If set to None, Gaussian white noise with zero mean and unit variance is used.

If random_state is an int, it will be used as a seed for RandomState. If None, the seed will be obtained from the operating system (see RandomState for details). Default is None.

Xarray of the connectivity data.

mne_connectivity.EpochTemporalConnectivity

mne_connectivity.EpochSpectroTemporalConnectivity

---

## mne_connectivity.EpochSpectroTemporalConnectivity#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.EpochSpectroTemporalConnectivity.html

**Contents:**
- mne_connectivity.EpochSpectroTemporalConnectivity#

Spectrotemporal connectivity class over Epochs.

This is an array of shape (n_epochs, n_connections, n_freqs, n_times), or (n_epochs, n_nodes, n_nodes, n_freqs, n_times). This describes how connectivity varies over frequencies and time for different epochs.

The connectivity data that is a raveled array of (n_estimated_nodes, ...) shape. The n_estimated_nodes is equal to n_nodes_in * n_nodes_out if one is computing the full connectivity, or a subset of nodes equal to the length of indices passed in.

The frequencies at which the connectivity data is computed over. If the frequencies are “frequency bands” (i.e. gamma band), then these are the median of those bands.

The times at which the connectivity data is computed over.

The number of nodes in the dataset used to compute connectivity. This should be equal to the number of signals in the original dataset.

The names of the nodes of the dataset used to compute connectivity. If ‘None’ (default), then names will be a list of integers from 0 to n_nodes. If a list of names, then it must be equal in length to n_nodes.

The indices of relevant connectivity data. If 'all' (default), then data is connectivity between all nodes. If 'symmetric', then data is symmetric connectivity between all nodes. If a tuple, then the first list represents the “in nodes”, and the second list represents the “out nodes”. See “Notes” for more information.

The method name used to compute connectivity.

The type of method used to compute spectral analysis, by default None.

Extra connectivity parameters. These may include freqs for spectral connectivity, and/or times for connectivity over time. In addition, these may include extra parameters that are stored as xarray attrs.

Xarray attributes of connectivity.

Generate block companion matrix.

The coordinates of the xarray data.

The dimensions of the xarray data.

The frequency points of the connectivity data.

Indices of connectivity data.

The method used to compute connectivity.

The number of epochs the connectivity data varies over.

Number of epochs used in computation of connectivity.

The number of nodes in the original dataset.

Shape of raveled connectivity.

The time points of the connectivity data.

Xarray of the connectivity data.

Append another connectivity structure.

Combine connectivity data over epochs.

Get connectivity data as a numpy array.

plot_circle(**kwargs)

Visualize connectivity as a circular graph.

Predict samples on actual data.

rename_nodes(mapping)

Save connectivity data to disk.

simulate(n_samples[, noise_func, random_state])

Simulate vector autoregressive (VAR) model.

get_epoch_annotations

Append another connectivity structure.

The Epoched Connectivity class to append.

The altered Epoched Connectivity class.

Xarray attributes of connectivity.

Combine connectivity data over epochs.

How to combine correlation estimates across epochs. Default is ‘mean’. If callable, it must accept one positional input. For example:

The combined connectivity data structure.

Generate block companion matrix.

Returns the data matrix if the model is VAR(1).

The coordinates of the xarray data.

The dimensions of the xarray data.

The frequency points of the connectivity data.

If these are computed over a frequency band, it will be the median frequency of the frequency band.

Get connectivity data as a numpy array.

How to format the output, by default ‘raveled’, which will represent each connectivity matrix as a (n_nodes_in * n_nodes_out,) list. If ‘dense’, then will return each connectivity matrix as a 2D array. If ‘compact’ (default) then will return ‘raveled’ if indices were defined as a list of tuples, or dense if indices is ‘all’. Multivariate connectivity data cannot be returned in a dense form.

The output connectivity data.

Indices of connectivity data.

Either ‘all’ for all-to-all connectivity, ‘symmetric’ for symmetric all-to-all connectivity, or a tuple of lists representing the node-to-nodes that connectivity was computed.

The method used to compute connectivity.

The number of epochs the connectivity data varies over.

Number of epochs used in computation of connectivity.

Can be ‘None’, if there was no epochs used. This is equivalent to the number of epochs, if there is no combining of epochs.

The number of nodes in the original dataset.

Even if indices defines a subset of nodes that were computed, this should be the total number of nodes in the original dataset.

Visualize connectivity as a circular graph.

Node names. The order corresponds to the order in con.

Two arrays with indices of connections for which the connections strengths are defined in con. Only needed if con is a 1D array.

If not None, only the n_lines strongest connections (strength=abs(con)) are drawn.

Array with node positions in degrees. If None, the nodes are equally spaced on the circle. See mne.viz.circular_layout.

Width of each node in degrees. If None, the minimum angle between any two nodes is used as the width.

The relative height of the colored bar labeling each node. Default 1.0 is the standard height.

List with the color to use for each node. If fewer colors than nodes are provided, the colors will be repeated. Any color supported by matplotlib can be used, e.g., RGBA tuples, named colors.

Color to use for background. See matplotlib.colors.

Color to use for text. See matplotlib.colors.

Color to use for lines around nodes. See matplotlib.colors.

Line width to use for connections.

Colormap to use for coloring the connections.

Minimum value for colormap. If None, it is determined automatically.

Maximum value for colormap. If None, it is determined automatically.

Display a colorbar or not.

Size of the colorbar.

Position of the colorbar.

Font size to use for title.

Font size to use for node names.

Font size to use for colorbar.

Space to add around figure to accommodate long labels.

The axes to use to plot the connectivity circle.

The figure to use. If None, a new figure with the specified background color will be created.

Deprecated: will be removed in version 0.5.

Location of the subplot when creating figures with multiple plots. E.g. 121 or (1, 2, 1) for 1 row, 2 columns, plot 1. See matplotlib.pyplot.subplot.

Deprecated: will be removed in version 0.5.

When enabled, left-click on a node to show only connections to that node. Right-click shows all connections.

This code is based on a circle graph example by Nicolas P. Rougier

By default, matplotlib.pyplot.savefig() does not take facecolor into account when saving, even if set when a figure is generated. This can be addressed via, e.g.:

If facecolor is not set via matplotlib.pyplot.savefig(), the figure labels, title, and legend may be cut off in the output figure.

Predict samples on actual data.

The result of this function is used for calculating the residuals.

Epoched or continuous data set. Has shape (n_epochs, n_signals, n_times) or (n_signals, n_times).

Data as predicted by the VAR model of shape same as data.

Residuals are obtained by r = x - var.predict(x).

To compute residual covariances:

Mapping from original node names (keys) to new node names (values).

Save connectivity data to disk.

Can later be loaded using the function mne_connectivity.read_connectivity().

The filepath to save the data. Data is saved as netCDF files (.nc extension).

Shape of raveled connectivity.

Simulate vector autoregressive (VAR) model.

This function generates data from the VAR model.

Number of samples to generate.

This function is used to create the generating noise process. If set to None, Gaussian white noise with zero mean and unit variance is used.

If random_state is an int, it will be used as a seed for RandomState. If None, the seed will be obtained from the operating system (see RandomState for details). Default is None.

The time points of the connectivity data.

Xarray of the connectivity data.

mne_connectivity.EpochSpectralConnectivity

mne_connectivity.envelope_correlation

---

## mne_connectivity.EpochTemporalConnectivity#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.EpochTemporalConnectivity.html

**Contents:**
- mne_connectivity.EpochTemporalConnectivity#
- Examples using mne_connectivity.EpochTemporalConnectivity#

Temporal connectivity class over Epochs.

This is an array of shape (n_epochs, n_connections, n_times), or (n_epochs, n_nodes, n_nodes, n_times). This describes how connectivity varies over time for different epochs.

The connectivity data that is a raveled array of (n_estimated_nodes, ...) shape. The n_estimated_nodes is equal to n_nodes_in * n_nodes_out if one is computing the full connectivity, or a subset of nodes equal to the length of indices passed in.

The times at which the connectivity data is computed over.

The number of nodes in the dataset used to compute connectivity. This should be equal to the number of signals in the original dataset.

The names of the nodes of the dataset used to compute connectivity. If ‘None’ (default), then names will be a list of integers from 0 to n_nodes. If a list of names, then it must be equal in length to n_nodes.

The indices of relevant connectivity data. If 'all' (default), then data is connectivity between all nodes. If 'symmetric', then data is symmetric connectivity between all nodes. If a tuple, then the first list represents the “in nodes”, and the second list represents the “out nodes”. See “Notes” for more information.

The method name used to compute connectivity.

Extra connectivity parameters. These may include freqs for spectral connectivity, and/or times for connectivity over time. In addition, these may include extra parameters that are stored as xarray attrs.

Xarray attributes of connectivity.

Generate block companion matrix.

The coordinates of the xarray data.

The dimensions of the xarray data.

Indices of connectivity data.

The method used to compute connectivity.

The number of epochs the connectivity data varies over.

Number of epochs used in computation of connectivity.

The number of nodes in the original dataset.

Shape of raveled connectivity.

The time points of the connectivity data.

Xarray of the connectivity data.

Append another connectivity structure.

Combine connectivity data over epochs.

Get connectivity data as a numpy array.

plot_circle(**kwargs)

Visualize connectivity as a circular graph.

Predict samples on actual data.

rename_nodes(mapping)

Save connectivity data to disk.

simulate(n_samples[, noise_func, random_state])

Simulate vector autoregressive (VAR) model.

get_epoch_annotations

Append another connectivity structure.

The Epoched Connectivity class to append.

The altered Epoched Connectivity class.

Xarray attributes of connectivity.

Combine connectivity data over epochs.

How to combine correlation estimates across epochs. Default is ‘mean’. If callable, it must accept one positional input. For example:

The combined connectivity data structure.

Generate block companion matrix.

Returns the data matrix if the model is VAR(1).

The coordinates of the xarray data.

The dimensions of the xarray data.

Get connectivity data as a numpy array.

How to format the output, by default ‘raveled’, which will represent each connectivity matrix as a (n_nodes_in * n_nodes_out,) list. If ‘dense’, then will return each connectivity matrix as a 2D array. If ‘compact’ (default) then will return ‘raveled’ if indices were defined as a list of tuples, or dense if indices is ‘all’. Multivariate connectivity data cannot be returned in a dense form.

The output connectivity data.

Indices of connectivity data.

Either ‘all’ for all-to-all connectivity, ‘symmetric’ for symmetric all-to-all connectivity, or a tuple of lists representing the node-to-nodes that connectivity was computed.

The method used to compute connectivity.

The number of epochs the connectivity data varies over.

Number of epochs used in computation of connectivity.

Can be ‘None’, if there was no epochs used. This is equivalent to the number of epochs, if there is no combining of epochs.

The number of nodes in the original dataset.

Even if indices defines a subset of nodes that were computed, this should be the total number of nodes in the original dataset.

Visualize connectivity as a circular graph.

Node names. The order corresponds to the order in con.

Two arrays with indices of connections for which the connections strengths are defined in con. Only needed if con is a 1D array.

If not None, only the n_lines strongest connections (strength=abs(con)) are drawn.

Array with node positions in degrees. If None, the nodes are equally spaced on the circle. See mne.viz.circular_layout.

Width of each node in degrees. If None, the minimum angle between any two nodes is used as the width.

The relative height of the colored bar labeling each node. Default 1.0 is the standard height.

List with the color to use for each node. If fewer colors than nodes are provided, the colors will be repeated. Any color supported by matplotlib can be used, e.g., RGBA tuples, named colors.

Color to use for background. See matplotlib.colors.

Color to use for text. See matplotlib.colors.

Color to use for lines around nodes. See matplotlib.colors.

Line width to use for connections.

Colormap to use for coloring the connections.

Minimum value for colormap. If None, it is determined automatically.

Maximum value for colormap. If None, it is determined automatically.

Display a colorbar or not.

Size of the colorbar.

Position of the colorbar.

Font size to use for title.

Font size to use for node names.

Font size to use for colorbar.

Space to add around figure to accommodate long labels.

The axes to use to plot the connectivity circle.

The figure to use. If None, a new figure with the specified background color will be created.

Deprecated: will be removed in version 0.5.

Location of the subplot when creating figures with multiple plots. E.g. 121 or (1, 2, 1) for 1 row, 2 columns, plot 1. See matplotlib.pyplot.subplot.

Deprecated: will be removed in version 0.5.

When enabled, left-click on a node to show only connections to that node. Right-click shows all connections.

This code is based on a circle graph example by Nicolas P. Rougier

By default, matplotlib.pyplot.savefig() does not take facecolor into account when saving, even if set when a figure is generated. This can be addressed via, e.g.:

If facecolor is not set via matplotlib.pyplot.savefig(), the figure labels, title, and legend may be cut off in the output figure.

Predict samples on actual data.

The result of this function is used for calculating the residuals.

Epoched or continuous data set. Has shape (n_epochs, n_signals, n_times) or (n_signals, n_times).

Data as predicted by the VAR model of shape same as data.

Residuals are obtained by r = x - var.predict(x).

To compute residual covariances:

Mapping from original node names (keys) to new node names (values).

Save connectivity data to disk.

Can later be loaded using the function mne_connectivity.read_connectivity().

The filepath to save the data. Data is saved as netCDF files (.nc extension).

Shape of raveled connectivity.

Simulate vector autoregressive (VAR) model.

This function generates data from the VAR model.

Number of samples to generate.

This function is used to create the generating noise process. If set to None, Gaussian white noise with zero mean and unit variance is used.

If random_state is an int, it will be used as a seed for RandomState. If None, the seed will be obtained from the operating system (see RandomState for details). Default is None.

The time points of the connectivity data.

Xarray of the connectivity data.

Compute envelope correlations in source space

mne_connectivity.EpochConnectivity

mne_connectivity.EpochSpectralConnectivity

---

## mne_connectivity.make_signals_in_freq_bands#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.make_signals_in_freq_bands.html

**Contents:**
- mne_connectivity.make_signals_in_freq_bands#
- Examples using mne_connectivity.make_signals_in_freq_bands#

Simulate signals interacting in a given frequency band.

Number of seed channels to simulate.

Number of target channels to simulate.

Frequency band where the connectivity should be simulated, where the first entry corresponds to the lower frequency, and the second entry to the higher frequency.

Number of epochs in the simulated data.

Number of timepoints each epoch of the simulated data.

Sampling frequency of the simulated data, in Hz.

Transition bandwidth of the filter to apply to isolate activity in freq_band, in Hz. These are passed to the l_bandwidth and h_bandwidth keyword arguments in mne.filter.create_filter().

Signal-to-noise ratio of the simulated data in the range [0, 1].

Number of timepoints for the delay of connectivity between the seeds and targets. If > 0, the target data is a delayed form of the seed data. If < 0, the seed data is a delayed form of the target data.

Earliest time of each epoch.

Names of the channels in the simulated data. If None, the channels are named according to their index and the frequency band of interaction. If specified, must be a list of n_seeds + n_targets channel names.

Types of the channels in the simulated data. If specified as a list, must be a list of n_seeds + n_targets channel names.

Seed to use for the random number generator. If None, no seed is specified.

The simulated data stored in an mne.EpochsArray object. The channels are arranged according to seeds, then targets.

Signals are simulated as a single source of activity in the given frequency band and projected into n_seeds + n_targets noise channels.

Comparison of coherency-based methods

Compute multivariate coherency/coherence

mne_connectivity.viz.plot_connectivity_circle

---

## mne_connectivity.phase_slope_index#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.phase_slope_index.html

**Contents:**
- mne_connectivity.phase_slope_index#
- Examples using mne_connectivity.phase_slope_index#

Compute the Phase Slope Index (PSI) connectivity measure.

The PSI is an effective connectivity measure, i.e., a measure which can give an indication of the direction of the information flow (causality). For two time series, and one computes the PSI between the first and the second time series as follows

indices = (np.array([0]), np.array([1])) psi = phase_slope_index(data, indices=indices, …)

A positive value means that time series 0 is ahead of time series 1 and a negative value means the opposite.

The PSI is computed from the coherency (see spectral_connectivity_epochs), details can be found in [1].

Can also be a list/generator of array, shape =(n_signals, n_times); list/generator of SourceEstimate; or Epochs. The data from which to compute connectivity. Note that it is also possible to combine multiple signals by providing a list of tuples, e.g., data = [(arr_0, stc_0), (arr_1, stc_1), (arr_2, stc_2)], corresponds to 3 epochs, and arr_* could be an array with the same number of time points as stc_*.

The names of the nodes of the dataset used to compute connectivity. If ‘None’ (default), then names will be a list of integers from 0 to n_nodes. If a list of names, then it must be equal in length to n_nodes.

Two arrays with indices of connections for which to compute connectivity. If None, all connections are computed.

The sampling frequency.

Spectrum estimation mode can be either: ‘multitaper’, ‘fourier’, or ‘cwt_morlet’.

The lower frequency of interest. Multiple bands are defined using a tuple, e.g., (8., 20.) for two bands with 8Hz and 20Hz lower freq. If None the frequency corresponding to an epoch length of 5 cycles is used.

The upper frequency of interest. Multiple bands are dedined using a tuple, e.g. (13., 30.) for two band with 13Hz and 30Hz upper freq.

Time to start connectivity estimation.

Time to end connectivity estimation.

The bandwidth of the multitaper windowing function in Hz. Only used in ‘multitaper’ mode.

Use adaptive weights to combine the tapered spectra into PSD. Only used in ‘multitaper’ mode.

Only use tapers with more than 90 percent spectral concentration within bandwidth. Only used in ‘multitaper’ mode.

Array of frequencies of interest. Only used in ‘cwt_morlet’ mode.

Number of cycles. Fixed number or one per frequency. Only used in ‘cwt_morlet’ mode.

How many connections to compute at once (higher numbers are faster but require more memory).

How many epochs to process in parallel.

If not None, override default verbose level (see mne.verbose() for more info). If used, it should be passed as a keyword-argument only.

Computed connectivity measure(s). Either a SpectralConnnectivity, or SpectroTemporalConnectivity container. The shape of each array is either (n_signals ** 2, n_bands) mode: ‘multitaper’ or ‘fourier’ (n_signals ** 2, n_bands, n_times) mode: ‘cwt_morlet’ when “indices” is None, or (n_con, n_bands) mode: ‘multitaper’ or ‘fourier’ (n_con, n_bands, n_times) mode: ‘cwt_morlet’ when “indices” is specified and “n_con = len(indices[0])”.

Guido Nolte, Andreas Ziehe, Vadim V. Nikulin, Alois Schlögl, Nicole Krämer, Tom Brismar, and Klaus-Robert Müller. Robustly estimating the flow direction of information in complex physical systems. Physical Review Letters, 2008. doi:10.1103/PhysRevLett.100.234101.

Comparison of coherency-based methods

Compute Phase Slope Index (PSI) in source space for a visual stimulus

mne_connectivity.envelope_correlation

mne_connectivity.vector_auto_regression

---

## mne_connectivity.read_connectivity#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.read_connectivity.html

**Contents:**
- mne_connectivity.read_connectivity#

Read connectivity data from netCDF file.

A connectivity class.

mne_connectivity.spectral_connectivity_time

mne_connectivity.symmetric_orth

---

## mne_connectivity.seed_target_indices#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.seed_target_indices.html

**Contents:**
- mne_connectivity.seed_target_indices#
- Examples using mne_connectivity.seed_target_indices#

Generate indices parameter for bivariate seed-based connectivity.

Indices of signals for which to compute connectivity.

The indices parameter used for connectivity computation.

seeds and targets should be array-likes or integers representing the indices of the channel pairs in the data for each connection. seeds and targets will be expanded such that connectivity will be computed between each seed and each target. E.g. the seeds and targets:

would be returned as:

where the indices have been expanded to have shape (2, n_cons), where n_cons = n_unique_seeds * n_unique_targets.

Comparison of coherency-based methods

Compute Phase Slope Index (PSI) in source space for a visual stimulus

Compute coherence in source space using a MNE inverse solution

Compute multivariate coherency/coherence

Compute multivariate measures of the imaginary part of coherency

Compute seed-based time-frequency connectivity in sensor space

mne_connectivity.degree

mne_connectivity.seed_target_multivariate_indices

---

## mne_connectivity.seed_target_multivariate_indices#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.seed_target_multivariate_indices.html

**Contents:**
- mne_connectivity.seed_target_multivariate_indices#

Generate indices parameter for multivariate seed-based connectivity.

The indices as a numpy object array.

seeds and targets should be array-likes representing the indices of the channel sets in the data for each connection. The indices for each connection should be an array-like of integers representing the individual channels in the data. The length of indices for each connection do not need to be equal. Furthermore, all indices within a connection must be unique.

Because the number of channels per connection can vary, the indices are stored as numpy arrays with dtype=object. E.g. seeds and targets:

would be returned as:

Even if the number of channels does not vary, the indices will still be stored as object arrays for compatibility.

More information on working with multivariate indices and handling connections where the number of seeds and targets are not equal can be found in the Working with ragged indices for multivariate connectivity example.

mne_connectivity.seed_target_indices

mne_connectivity.check_indices

---

## mne_connectivity.select_order#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.select_order.html

**Contents:**
- mne_connectivity.select_order#

Compute lag order selections based on information criterion.

Selects a lag order based on each of the available information criteria.

Endogenous variable, that predicts the exogenous.

The maximum number of lags to check. Will then check from 1 to maxlags. If None, defaults to 12 * (n_times / 100.)**(1./4).

The selected orders based on the following information criterion. * aic : Akaike * fpe : Final prediction error * hqic : Hannan-Quinn * bic : Bayesian a.k.a. Schwarz

The selected order is then stored as the value.

mne_connectivity.check_indices

mne_connectivity.viz.plot_sensors_connectivity

---

## mne_connectivity.SpectralConnectivity#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.SpectralConnectivity.html

**Contents:**
- mne_connectivity.SpectralConnectivity#
- Examples using mne_connectivity.SpectralConnectivity#

Spectral connectivity class.

This class stores connectivity data that varies over frequencies. The underlying data is an array of shape (n_connections, n_freqs), or (n_nodes, n_nodes, n_freqs).

The connectivity data that is a raveled array of (n_estimated_nodes, ...) shape. The n_estimated_nodes is equal to n_nodes_in * n_nodes_out if one is computing the full connectivity, or a subset of nodes equal to the length of indices passed in.

The frequencies at which the connectivity data is computed over. If the frequencies are “frequency bands” (i.e. gamma band), then these are the median of those bands.

The number of nodes in the dataset used to compute connectivity. This should be equal to the number of signals in the original dataset.

The names of the nodes of the dataset used to compute connectivity. If ‘None’ (default), then names will be a list of integers from 0 to n_nodes. If a list of names, then it must be equal in length to n_nodes.

The indices of relevant connectivity data. If 'all' (default), then data is connectivity between all nodes. If 'symmetric', then data is symmetric connectivity between all nodes. If a tuple, then the first list represents the “in nodes”, and the second list represents the “out nodes”. See “Notes” for more information.

The method name used to compute connectivity.

The type of method used to compute spectral analysis, by default None.

The number of epochs used in the computation of connectivity, by default None.

Extra connectivity parameters. These may include freqs for spectral connectivity, and/or times for connectivity over time. In addition, these may include extra parameters that are stored as xarray attrs.

Xarray attributes of connectivity.

Generate block companion matrix.

The coordinates of the xarray data.

The dimensions of the xarray data.

The frequency points of the connectivity data.

Indices of connectivity data.

The method used to compute connectivity.

The number of epochs the connectivity data varies over.

Number of epochs used in computation of connectivity.

The number of nodes in the original dataset.

Shape of raveled connectivity.

Xarray of the connectivity data.

Append another connectivity structure.

Combine connectivity data over epochs.

Get connectivity data as a numpy array.

plot_circle(**kwargs)

Visualize connectivity as a circular graph.

Predict samples on actual data.

rename_nodes(mapping)

Save connectivity data to disk.

simulate(n_samples[, noise_func, random_state])

Simulate vector autoregressive (VAR) model.

get_epoch_annotations

Append another connectivity structure.

The Epoched Connectivity class to append.

The altered Epoched Connectivity class.

Xarray attributes of connectivity.

Combine connectivity data over epochs.

How to combine correlation estimates across epochs. Default is ‘mean’. If callable, it must accept one positional input. For example:

The combined connectivity data structure.

Generate block companion matrix.

Returns the data matrix if the model is VAR(1).

The coordinates of the xarray data.

The dimensions of the xarray data.

The frequency points of the connectivity data.

If these are computed over a frequency band, it will be the median frequency of the frequency band.

Get connectivity data as a numpy array.

How to format the output, by default ‘raveled’, which will represent each connectivity matrix as a (n_nodes_in * n_nodes_out,) list. If ‘dense’, then will return each connectivity matrix as a 2D array. If ‘compact’ (default) then will return ‘raveled’ if indices were defined as a list of tuples, or dense if indices is ‘all’. Multivariate connectivity data cannot be returned in a dense form.

The output connectivity data.

Indices of connectivity data.

Either ‘all’ for all-to-all connectivity, ‘symmetric’ for symmetric all-to-all connectivity, or a tuple of lists representing the node-to-nodes that connectivity was computed.

The method used to compute connectivity.

The number of epochs the connectivity data varies over.

Number of epochs used in computation of connectivity.

Can be ‘None’, if there was no epochs used. This is equivalent to the number of epochs, if there is no combining of epochs.

The number of nodes in the original dataset.

Even if indices defines a subset of nodes that were computed, this should be the total number of nodes in the original dataset.

Visualize connectivity as a circular graph.

Node names. The order corresponds to the order in con.

Two arrays with indices of connections for which the connections strengths are defined in con. Only needed if con is a 1D array.

If not None, only the n_lines strongest connections (strength=abs(con)) are drawn.

Array with node positions in degrees. If None, the nodes are equally spaced on the circle. See mne.viz.circular_layout.

Width of each node in degrees. If None, the minimum angle between any two nodes is used as the width.

The relative height of the colored bar labeling each node. Default 1.0 is the standard height.

List with the color to use for each node. If fewer colors than nodes are provided, the colors will be repeated. Any color supported by matplotlib can be used, e.g., RGBA tuples, named colors.

Color to use for background. See matplotlib.colors.

Color to use for text. See matplotlib.colors.

Color to use for lines around nodes. See matplotlib.colors.

Line width to use for connections.

Colormap to use for coloring the connections.

Minimum value for colormap. If None, it is determined automatically.

Maximum value for colormap. If None, it is determined automatically.

Display a colorbar or not.

Size of the colorbar.

Position of the colorbar.

Font size to use for title.

Font size to use for node names.

Font size to use for colorbar.

Space to add around figure to accommodate long labels.

The axes to use to plot the connectivity circle.

The figure to use. If None, a new figure with the specified background color will be created.

Deprecated: will be removed in version 0.5.

Location of the subplot when creating figures with multiple plots. E.g. 121 or (1, 2, 1) for 1 row, 2 columns, plot 1. See matplotlib.pyplot.subplot.

Deprecated: will be removed in version 0.5.

When enabled, left-click on a node to show only connections to that node. Right-click shows all connections.

This code is based on a circle graph example by Nicolas P. Rougier

By default, matplotlib.pyplot.savefig() does not take facecolor into account when saving, even if set when a figure is generated. This can be addressed via, e.g.:

If facecolor is not set via matplotlib.pyplot.savefig(), the figure labels, title, and legend may be cut off in the output figure.

Predict samples on actual data.

The result of this function is used for calculating the residuals.

Epoched or continuous data set. Has shape (n_epochs, n_signals, n_times) or (n_signals, n_times).

Data as predicted by the VAR model of shape same as data.

Residuals are obtained by r = x - var.predict(x).

To compute residual covariances:

Mapping from original node names (keys) to new node names (values).

Save connectivity data to disk.

Can later be loaded using the function mne_connectivity.read_connectivity().

The filepath to save the data. Data is saved as netCDF files (.nc extension).

Shape of raveled connectivity.

Simulate vector autoregressive (VAR) model.

This function generates data from the VAR model.

Number of samples to generate.

This function is used to create the generating noise process. If set to None, Gaussian white noise with zero mean and unit variance is used.

If random_state is an int, it will be used as a seed for RandomState. If None, the seed will be obtained from the operating system (see RandomState for details). Default is None.

Xarray of the connectivity data.

Comparing PLI, wPLI, and dPLI

Comparison of coherency-based methods

Compute Phase Slope Index (PSI) in source space for a visual stimulus

Compute all-to-all connectivity in sensor space

Compute coherence in source space using a MNE inverse solution

Compute directionality of connectivity with multivariate Granger causality

Compute full spectrum source space connectivity between labels

Compute mixed source space connectivity and visualize it using a circular graph

Compute multivariate coherency/coherence

Compute multivariate measures of the imaginary part of coherency

Compute source space connectivity and visualize it using a circular graph

Working with ragged indices for multivariate connectivity

mne_connectivity.TemporalConnectivity

mne_connectivity.SpectroTemporalConnectivity

---

## mne_connectivity.spectral_connectivity_epochs#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.spectral_connectivity_epochs.html

**Contents:**
- mne_connectivity.spectral_connectivity_epochs#
- Examples using mne_connectivity.spectral_connectivity_epochs#

Compute frequency- and time-frequency-domain connectivity measures.

The connectivity method(s) are specified using the “method” parameter. All methods are based on estimates of the cross- and power spectral densities (CSD/PSD) Sxy and Sxx, Syy.

The data from which to compute connectivity. Note that it is also possible to combine multiple signals by providing a list of tuples, e.g., data = [(arr_0, stc_0), (arr_1, stc_1), (arr_2, stc_2)], corresponds to 3 epochs, and arr_* could be an array with the same number of time points as stc_*. The array-like object can also be a list/generator of array, shape =(n_signals, n_times), or a list/generator of SourceEstimate or VolSourceEstimate objects.

The names of the nodes of the dataset used to compute connectivity. If ‘None’ (default), then names will be a list of integers from 0 to n_nodes. If a list of names, then it must be equal in length to n_nodes.

Connectivity measure(s) to compute. These can be ['coh', 'cohy', 'imcoh', 'cacoh', 'mic', 'mim', 'plv', 'ciplv', 'ppc', 'pli', 'dpli', 'wpli', 'wpli2_debiased', 'gc', 'gc_tr']. These are:

‘imcoh’ : Imaginary part of Coherency

‘cacoh’ : Canonical Coherency (CaCoh)

‘mic’ : Maximised Imaginary part of Coherency (MIC)

‘mim’ : Multivariate Interaction Measure (MIM)

‘plv’ : Phase-Locking Value (PLV)

‘ciplv’ : Corrected Imaginary PLV (ciPLV)

‘ppc’ : Pairwise Phase Consistency (PPC)

‘pli’ : Phase Lag Index (PLI)

‘pli2_unbiased’ : Unbiased estimator of squared PLI

‘dpli’ : Directed PLI (DPLI)

‘wpli’ : Weighted PLI (WPLI)

‘wpli2_debiased’ : Debiased estimator of squared WPLI

‘gc’ : State-space Granger Causality (GC)

‘gc_tr’ : State-space GC on time-reversed signals

Multivariate methods (['cacoh', 'mic', 'mim', 'gc', 'gc_tr']) cannot be called with the other methods.

Two arrays with indices of connections for which to compute connectivity. If a bivariate method is called, each array for the seeds and targets should contain the channel indices for each bivariate connection. If a multivariate method is called, each array for the seeds and targets should consist of nested arrays containing the channel indices for each multivariate connection. If None, connections between all channels are computed, unless a Granger causality method is called, in which case an error is raised.

The sampling frequency. Required if data is not Epochs.

Spectrum estimation mode can be either: ‘multitaper’, ‘fourier’, or ‘cwt_morlet’.

The lower frequency of interest. Multiple bands are defined using a tuple, e.g., (8., 20.) for two bands with 8Hz and 20Hz lower freq.

The upper frequency of interest. Multiple bands are dedined using a tuple, e.g. (13., 30.) for two band with 13Hz and 30Hz upper freq.

Omit every “(fskip + 1)-th” frequency bin to decimate in frequency domain.

Average connectivity scores for each frequency band. If True, the output freqs will be a list with arrays of the frequencies that were averaged.

Time to start connectivity estimation. Note: when “data” is an array, the first sample is assumed to be at time 0. For other types (Epochs, etc.), the time information contained in the object is used to compute the time indices.

Time to end connectivity estimation. Note: when “data” is an array, the first sample is assumed to be at time 0. For other types (Epochs, etc.), the time information contained in the object is used to compute the time indices.

The bandwidth of the multitaper windowing function in Hz. Only used in ‘multitaper’ mode.

Use adaptive weights to combine the tapered spectra into PSD. Only used in ‘multitaper’ mode.

Only use tapers with more than 90 percent spectral concentration within bandwidth. Only used in ‘multitaper’ mode.

Array of frequencies of interest. Only used in ‘cwt_morlet’ mode.

Number of cycles. Fixed number or one per frequency. Only used in ‘cwt_morlet’ mode.

Number of lags to use for the vector autoregressive model when computing Granger causality. Higher values increase computational cost, but reduce the degree of spectral smoothing in the results. Only used if method contains any of ['gc', 'gc_tr'].

Two arrays with the rank to project the seed and target data to, respectively, using singular value decomposition. If None, the rank of the data is computed and projected to. Only used if method contains any of ['cacoh', 'mic', 'mim', 'gc', 'gc_tr'].

How many connections to compute at once (higher numbers are faster but require more memory).

How many samples to process in parallel.

If not None, override default verbose level (see mne.verbose() for more info). If used, it should be passed as a keyword-argument only.

Computed connectivity measure(s). Either an instance of SpectralConnectivity or SpectroTemporalConnectivity. The shape of the connectivity result will be:

(n_cons, n_freqs) for multitaper or fourier modes

(n_cons, n_freqs, n_times) for cwt_morlet mode

n_cons = n_signals ** 2 for bivariate methods with indices=None

n_cons = 1 for multivariate methods with indices=None

n_cons = len(indices[0]) for bivariate and multivariate methods when indices is supplied.

Please note that the interpretation of the measures in this function depends on the data and underlying assumptions and does not necessarily reflect a causal relationship between brain regions.

These measures are not to be interpreted over time. Each Epoch passed into the dataset is interpreted as an independent sample of the same connectivity structure. Within each Epoch, it is assumed that the spectral measure is stationary. The spectral measures implemented in this function are computed across Epochs. Thus, spectral measures computed with only one Epoch will result in errorful values and spectral measures computed with few Epochs will be unreliable. Please see spectral_connectivity_time for time-resolved connectivity estimation.

The spectral densities can be estimated using a multitaper method with digital prolate spheroidal sequence (DPSS) windows, a discrete Fourier transform with Hanning windows, or a continuous wavelet transform using Morlet wavelets. The spectral estimation mode is specified using the “mode” parameter.

By default, the connectivity between all signals is computed (only connections corresponding to the lower-triangular part of the connectivity matrix). If one is only interested in the connectivity between some signals, the “indices” parameter can be used. For example, to compute the connectivity between the signal with index 0 and signals “2, 3, 4” (a total of 3 connections) one can use the following:

In this case con.get_data().shape = (3, n_freqs). The connectivity scores are in the same order as defined indices.

For multivariate methods, this is handled differently. If “indices” is None, connectivity between all signals will be computed and a single connectivity spectrum will be returned (this is not possible if a Granger causality method is called). If “indices” is specified, seed and target indices for each connection should be specified as nested array-likes. For example, to compute the connectivity between signals (0, 1) -> (2, 3) and (0, 1) -> (4, 5), indices should be specified as:

More information on working with multivariate indices and handling connections where the number of seeds and targets are not equal can be found in the Working with ragged indices for multivariate connectivity example.

Supported Connectivity Measures

The connectivity method(s) is specified using the “method” parameter. The following methods are supported (note: E[] denotes average over epochs). Multiple measures can be computed at once by using a list/tuple, e.g., ['coh', 'pli'] to compute coherence and PLI.

‘coh’ : Coherence given by:

‘cohy’ : Coherency given by:

‘imcoh’ : Imaginary coherence [1] given by:

‘cacoh’ : Canonical Coherency (CaCoh) [2] given by:

\(\textrm{CaCoh}=\Large{\frac{\boldsymbol{a}^T\boldsymbol{D} (\Phi)\boldsymbol{b}}{\sqrt{\boldsymbol{a}^T\boldsymbol{a} \boldsymbol{b}^T\boldsymbol{b}}}}\)

where: \(\boldsymbol{D}(\Phi)\) is the cross-spectral density between seeds and targets transformed for a given phase angle \(\Phi\); and \(\boldsymbol{a}\) and \(\boldsymbol{b}\) are eigenvectors for the seeds and targets, such that \(\boldsymbol{a}^T\boldsymbol{D}(\Phi)\boldsymbol{b}\) maximises coherency between the seeds and targets. Taking the absolute value of the results gives maximised coherence.

‘mic’ : Maximised Imaginary part of Coherency (MIC) [3] given by:

\(\textrm{MIC}=\Large{\frac{\boldsymbol{\alpha}^T \boldsymbol{E \beta}}{\parallel\boldsymbol{\alpha}\parallel \parallel\boldsymbol{\beta}\parallel}}\)

where: \(\boldsymbol{E}\) is the imaginary part of the transformed cross-spectral density between seeds and targets; and \(\boldsymbol{\alpha}\) and \(\boldsymbol{\beta}\) are eigenvectors for the seeds and targets, such that \(\boldsymbol{\alpha}^T \boldsymbol{E \beta}\) maximises the imaginary part of coherency between the seeds and targets.

‘mim’ : Multivariate Interaction Measure (MIM) [3] given by:

\(\textrm{MIM}=tr(\boldsymbol{EE}^T)\)

where \(\boldsymbol{E}\) is the imaginary part of the transformed cross-spectral density between seeds and targets.

‘plv’ : Phase-Locking Value (PLV) [4] given by:

‘ciplv’ : corrected imaginary PLV (ciPLV) [5] given by:

‘ppc’ : Pairwise Phase Consistency (PPC), an unbiased estimator of squared PLV [6].

‘pli’ : Phase Lag Index (PLI) [7] given by:

‘pli2_unbiased’ : Unbiased estimator of squared PLI [8].

‘dpli’ : Directed Phase Lag Index (DPLI) [9] given by (where H is the Heaviside function):

‘wpli’ : Weighted Phase Lag Index (WPLI) [8] given by:

‘wpli2_debiased’ : Debiased estimator of squared WPLI [8].

‘gc’ : State-space Granger Causality (GC) [10] given by:

\(GC = ln\Large{(\frac{\lvert\boldsymbol{S}_{tt}\rvert}{\lvert \boldsymbol{S}_{tt}-\boldsymbol{H}_{ts}\boldsymbol{\Sigma}_{ss \lvert t}\boldsymbol{H}_{ts}^*\rvert}})\)

where: \(s\) and \(t\) represent the seeds and targets, respectively; \(\boldsymbol{H}\) is the spectral transfer function; \(\boldsymbol{\Sigma}\) is the residuals matrix of the autoregressive model; and \(\boldsymbol{S}\) is \(\boldsymbol{\Sigma}\) transformed by \(\boldsymbol{H}\).

‘gc_tr’ : State-space GC on time-reversed signals [10][11] given by the same equation as for ‘gc’, but where the autocovariance sequence from which the autoregressive model is produced is transposed to mimic the reversal of the original signal in time [12].

Guido Nolte, Ou Bai, Lewis Wheaton, Zoltan Mari, Sherry Vorbach, and Mark Hallett. Identifying true brain interaction from EEG data using the imaginary part of coherency. Clinical Neurophysiology, 115(10):2292–2307, 2004. doi:10.1016/j.clinph.2004.04.029.

Carmen Vidaurre, Guido Nolte, Ingmar E.J. de Vries, M. Gómez, Tjeerd W. Boonstra, K.-R. Müller, Arno Villringer, and Vadim V. Nikulin. Canonical maximization of coherence: a novel tool for investigation of neuronal interactions between two datasets. NeuroImage, 201:116009, 2019. doi:10.1016/j.neuroimage.2019.116009.

Arne Ewald, Laura Marzetti, Filippo Zappasodi, Frank C. Meinecke, and Guido Nolte. Estimating true brain connectivity from EEG/MEG data invariant to linear and static transformations in sensor space. NeuroImage, 60(1):476–488, 2012. doi:10.1016/j.neuroimage.2011.11.084.

Jean-Philippe Lachaux, Eugenio Rodriguez, Jacques Martinerie, and Francisco J. Varela. Measuring phase synchrony in brain signals. Human Brain Mapping, 8(4):194–208, 1999. doi:10.1002/(SICI)1097-0193(1999)8:4<194::AID-HBM4>3.0.CO;2-C.

Ernesto Pereda Ricardo Bruña, Fernando Maestú. Phase locking value revisited: teaching new tricks to an old dog. Journal of Neural Engineering, 15(5):056011, 2018. doi:10.1088/1741-2552/aacfe4.

Martin Vinck, Marijn van Wingerden, Thilo Womelsdorf, Pascal Fries, and Cyriel M.A. Pennartz. The pairwise phase consistency: a bias-free measure of rhythmic neuronal synchronization. NeuroImage, 51(1):112–122, 2010. doi:10.1016/j.neuroimage.2010.01.073.

Cornelis J. Stam, Guido Nolte, and Andreas Daffertshofer. Phase lag index: assessment of functional connectivity from multi channel EEG and MEG with diminished bias from common sources. Human Brain Mapping, 28(11):1178–1193, 2007. doi:10.1002/hbm.20346.

Martin Vinck, Robert Oostenveld, Marijn van Wingerden, Franscesco Battaglia, and Cyriel M.A. Pennartz. An improved index of phase-synchronization for electrophysiological data in the presence of volume-conduction, noise and sample-size bias. NeuroImage, 55(4):1548–1565, 2011. doi:10.1016/j.neuroimage.2011.01.055.

C. J. Stam and E. C. W. van Straaten. Go with the flow: use of a directed phase lag index (dpli) to characterize patterns of phase relations in a large-scale model of brain dynamics. NeuroImage, 62(3):1415–1428, Sep 2012. doi:10.1016/j.neuroimage.2012.05.050.

Lionel Barnett and Anil K. Seth. Granger causality for state-space models. Physical Review E, 91(4):040101, 2015. doi:10.1103/PhysRevE.91.040101.

Irene Winkler, Danny Panknin, Daniel Bartz, Klaus-Robert Müller, and Stefan Haufe. Validity of time reversal for testing granger causality. IEEE Transactions on Signal Processing, 64(11):2746–2760, 2016. doi:10.1109/TSP.2016.2531628.

Stefan Haufe, Vadim V Nikulin, and Guido Nolte. Alleviating the influence of weak data asymmetries on granger-causal analyses. In Latent Variable Analysis and Signal Separation: 10th International Conference, LVA/ICA 2012, Tel Aviv, Israel, March 12-15, 2012. Proceedings 10, 25–33. Springer, 2012. doi:10.1007/978-3-642-28551-6_4.

Comparing PLI, wPLI, and dPLI

Comparing spectral connectivity computed over time or over trials

Comparison of coherency-based methods

Compute all-to-all connectivity in sensor space

Compute coherence in source space using a MNE inverse solution

Compute directionality of connectivity with multivariate Granger causality

Compute full spectrum source space connectivity between labels

Compute mixed source space connectivity and visualize it using a circular graph

Compute multivariate coherency/coherence

Compute multivariate measures of the imaginary part of coherency

Compute seed-based time-frequency connectivity in sensor space

Compute source space connectivity and visualize it using a circular graph

Using the connectivity classes

Working with ragged indices for multivariate connectivity

mne_connectivity.vector_auto_regression

mne_connectivity.spectral_connectivity_time

---

## mne_connectivity.spectral_connectivity_time#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.spectral_connectivity_time.html

**Contents:**
- mne_connectivity.spectral_connectivity_time#
- Examples using mne_connectivity.spectral_connectivity_time#

Compute time-frequency-domain connectivity measures.

This function computes spectral connectivity over time from epoched data. The data may consist of a single epoch.

The connectivity method(s) are specified using the method parameter. All methods are based on time-resolved estimates of the cross- and power spectral densities (CSD/PSD) Sxy and Sxx, Syy.

The data from which to compute connectivity.

Array of frequencies of interest for time-frequency decomposition. Only the frequencies within the range specified by fmin and fmax are used.

Connectivity measure(s) to compute. These can be ['coh', 'cacoh', 'mic', 'mim', 'plv', 'ciplv', 'pli', 'wpli', 'gc', 'gc_tr']. These are:

‘cacoh’ : Canonical Coherency (CaCoh)

‘mic’ : Maximised Imaginary part of Coherency (MIC)

‘mim’ : Multivariate Interaction Measure (MIM)

‘plv’ : Phase-Locking Value (PLV)

‘ciplv’ : Corrected Imaginary PLV (ciPLV)

‘pli’ : Phase Lag Index (PLI)

‘wpli’ : Weighted PLI (WPLI)

‘gc’ : State-space Granger Causality (GC)

‘gc_tr’ : State-space GC on time-reversed signals

Multivariate methods (['cacoh', 'mic', 'mim', 'gc', 'gc_tr']) cannot be called with the other methods.

Average connectivity scores over epochs. If True, output will be an instance of SpectralConnectivity, otherwise EpochSpectralConnectivity.

Two arrays with indices of connections for which to compute connectivity. If a bivariate method is called, each array for the seeds and targets should contain the channel indices for the each bivariate connection. If a multivariate method is called, each array for the seeds and targets should consist of nested arrays containing the channel indices for each multivariate connection. If None, connections between all channels are computed, unless a Granger causality method is called, in which case an error is raised.

The sampling frequency. Required if data is not Epochs.

The lower frequency of interest. Multiple bands are defined using a tuple, e.g., (8., 20.) for two bands with 8 Hz and 20 Hz lower bounds. If None, the lowest frequency in freqs is used.

The upper frequency of interest. Multiple bands are defined using a tuple, e.g. (13., 30.) for two band with 13 Hz and 30 Hz upper bounds. If None, the highest frequency in freqs is used.

Omit every (fskip + 1)-th frequency bin to decimate in frequency domain.

Average connectivity scores for each frequency band. If True, the output freqs will be an array of the median frequencies of each band.

Amount of time to consider for the temporal smoothing in seconds. If zero, no temporal smoothing is applied.

Number of points for frequency smoothing. By default, 1 is used which is equivalent to no smoothing.

Smoothing kernel type. Choose either ‘square’ or ‘hanning’.

Amount of time to consider as padding at the beginning and end of each epoch in seconds. See Notes for more information.

Time-frequency decomposition method. Can be either: ‘multitaper’, or ‘cwt_morlet’. See mne.time_frequency.tfr_array_multitaper() and mne.time_frequency.tfr_array_morlet() for reference.

Product between the temporal window length (in seconds) and the full frequency bandwidth (in Hz). This product can be seen as the surface of the window on the time/frequency plane and controls the frequency bandwidth (thus the frequency resolution) and the number of good tapers. See mne.time_frequency.tfr_array_multitaper() documentation.

Number of cycles in the wavelet, either a fixed number or one per frequency. The number of cycles n_cycles and the frequencies of interest cwt_freqs define the temporal window length. For details, see mne.time_frequency.tfr_array_morlet() documentation.

Number of lags to use for the vector autoregressive model when computing Granger causality. Higher values increase computational cost, but reduce the degree of spectral smoothing in the results. Only used if method contains any of ['gc', 'gc_tr'].

Two arrays with the rank to project the seed and target data to, respectively, using singular value decomposition. If None, the rank of the data is computed and projected to. Only used if method contains any of ['cacoh', 'mic', 'mim', 'gc', 'gc_tr'].

To reduce memory usage, decimation factor after time-frequency decomposition. Returns tfr[…, ::decim].

Number of connections to compute in parallel. Memory mapping must be activated. Please see the Notes section for details.

If not None, override default verbose level (see mne.verbose() for more info). If used, it should be passed as a keyword-argument only.

Computed connectivity measure(s). An instance of EpochSpectralConnectivity, SpectralConnectivity or a list of instances corresponding to connectivity measures if several connectivity measures are specified. The shape of each connectivity dataset is (n_epochs, n_cons, n_freqs). When “indices” is None and a bivariate method is called, “n_cons = n_signals ** 2”, or if a multivariate method is called “n_cons = 1”. When “indices” is specified, “n_con = len(indices[0])” for bivariate and multivariate methods.

Please note that the interpretation of the measures in this function depends on the data and underlying assumptions and does not necessarily reflect a causal relationship between brain regions.

The connectivity measures are computed over time within each epoch and optionally averaged over epochs. High connectivity values indicate that the phase coupling (interpreted as estimated connectivity) differences between signals stay consistent over time.

The spectral densities can be estimated using a multitaper method with digital prolate spheroidal sequence (DPSS) windows, or a continuous wavelet transform using Morlet wavelets. The spectral estimation mode is specified using the mode parameter.

When using the multitaper spectral estimation method, the cross-spectral density is computed separately for each taper and aggregated using a weighted average, where the weights correspond to the concentration ratios between the DPSS windows.

Spectral estimation using multitaper or Morlet wavelets introduces edge effects that depend on the length of the wavelet. To remove edge effects, the parameter padding can be used to prune the edges of the signal. Please see the documentation of mne.time_frequency.tfr_array_multitaper() and mne.time_frequency.tfr_array_morlet() for details on wavelet length (i.e., time window length).

By default, the connectivity between all signals is computed (only connections corresponding to the lower-triangular part of the connectivity matrix). If one is only interested in the connectivity between some signals, the “indices” parameter can be used. For example, to compute the connectivity between the signal with index 0 and signals “2, 3, 4” (a total of 3 connections) one can use the following:

In this case con.get_data().shape = (3, n_freqs). The connectivity scores are in the same order as defined indices.

For multivariate methods, this is handled differently. If “indices” is None, connectivity between all signals will be computed and a single connectivity spectrum will be returned (this is not possible if a Granger causality method is called). If “indices” is specified, seed and target indices for each connection should be specified as nested array-likes. For example, to compute the connectivity between signals (0, 1) -> (2, 3) and (0, 1) -> (4, 5), indices should be specified as:

More information on working with multivariate indices and handling connections where the number of seeds and targets are not equal can be found in the Working with ragged indices for multivariate connectivity example.

Supported Connectivity Measures

The connectivity method(s) is specified using the method parameter. The following methods are supported (note: E[] denotes average over epochs). Multiple measures can be computed at once by using a list/tuple, e.g., ['coh', 'pli'] to compute coherence and PLI.

‘coh’ : Coherence given by:

‘cacoh’ : Canonical Coherency (CaCoh) [1] given by:

\(\textrm{CaCoh}=\Large{\frac{\boldsymbol{a}^T\boldsymbol{D} (\Phi)\boldsymbol{b}}{\sqrt{\boldsymbol{a}^T\boldsymbol{a} \boldsymbol{b}^T\boldsymbol{b}}}}\)

where: \(\boldsymbol{D}(\Phi)\) is the cross-spectral density between seeds and targets transformed for a given phase angle \(\Phi\); and \(\boldsymbol{a}\) and \(\boldsymbol{b}\) are eigenvectors for the seeds and targets, such that \(\boldsymbol{a}^T\boldsymbol{D}(\Phi)\boldsymbol{b}\) maximises coherency between the seeds and targets. Taking the absolute value of the results gives maximised coherence.

‘mic’ : Maximised Imaginary part of Coherency (MIC) [2] given by:

\(\textrm{MIC}=\Large{\frac{\boldsymbol{\alpha}^T \boldsymbol{E \beta}}{\parallel\boldsymbol{\alpha}\parallel \parallel\boldsymbol{\beta}\parallel}}\)

where: \(\boldsymbol{E}\) is the imaginary part of the transformed cross-spectral density between seeds and targets; and \(\boldsymbol{\alpha}\) and \(\boldsymbol{\beta}\) are eigenvectors for the seeds and targets, such that \(\boldsymbol{\alpha}^T \boldsymbol{E \beta}\) maximises the imaginary part of coherency between the seeds and targets.

‘mim’ : Multivariate Interaction Measure (MIM) [2] given by:

\(\textrm{MIM}=tr(\boldsymbol{EE}^T)\)

where \(\boldsymbol{E}\) is the imaginary part of the transformed cross-spectral density between seeds and targets.

‘plv’ : Phase-Locking Value (PLV) [3] given by:

‘ciplv’ : Corrected imaginary PLV (ciPLV) [4] given by:

‘pli’ : Phase Lag Index (PLI) [5] given by:

‘wpli’ : Weighted Phase Lag Index (WPLI) [6] given by:

‘gc’ : State-space Granger Causality (GC) [7] given by:

\(GC = ln\Large{(\frac{\lvert\boldsymbol{S}_{tt}\rvert}{\lvert \boldsymbol{S}_{tt}-\boldsymbol{H}_{ts}\boldsymbol{\Sigma}_{ss \lvert t}\boldsymbol{H}_{ts}^*\rvert}})\)

where: \(s\) and \(t\) represent the seeds and targets, respectively; \(\boldsymbol{H}\) is the spectral transfer function; \(\boldsymbol{\Sigma}\) is the residuals matrix of the autoregressive model; and \(\boldsymbol{S}\) is \(\boldsymbol{\Sigma}\) transformed by \(\boldsymbol{H}\).

‘gc_tr’ : State-space GC on time-reversed signals [7][8] given by the same equation as for ‘gc’, but where the autocovariance sequence from which the autoregressive model is produced is transposed to mimic the reversal of the original signal in time [9].

Parallel computation can be activated by setting the n_jobs parameter. Under the hood, this utilizes the joblib library. For effective parallelization, you should activate memory mapping in MNE-Python by setting MNE_MEMMAP_MIN_SIZE and MNE_CACHE_DIR. Activating memory mapping will make joblib store arrays greater than the minimum size on disc, and forego direct RAM access for more efficient processing. For example, in your code, run

mne.set_config(‘MNE_MEMMAP_MIN_SIZE’, ‘10M’) mne.set_config(‘MNE_CACHE_DIR’, ‘/dev/shm’)

When MNE_MEMMAP_MIN_SIZE=None, the underlying joblib implementation results in pickling and unpickling the whole array each time a pair of indices is accessed, which is slow, compared to memory mapping the array.

This function is based on the frites.conn.conn_spec implementation in Frites.

Added in version 0.3.

Carmen Vidaurre, Guido Nolte, Ingmar E.J. de Vries, M. Gómez, Tjeerd W. Boonstra, K.-R. Müller, Arno Villringer, and Vadim V. Nikulin. Canonical maximization of coherence: a novel tool for investigation of neuronal interactions between two datasets. NeuroImage, 201:116009, 2019. doi:10.1016/j.neuroimage.2019.116009.

Arne Ewald, Laura Marzetti, Filippo Zappasodi, Frank C. Meinecke, and Guido Nolte. Estimating true brain connectivity from EEG/MEG data invariant to linear and static transformations in sensor space. NeuroImage, 60(1):476–488, 2012. doi:10.1016/j.neuroimage.2011.11.084.

Jean-Philippe Lachaux, Eugenio Rodriguez, Jacques Martinerie, and Francisco J. Varela. Measuring phase synchrony in brain signals. Human Brain Mapping, 8(4):194–208, 1999. doi:10.1002/(SICI)1097-0193(1999)8:4<194::AID-HBM4>3.0.CO;2-C.

Ernesto Pereda Ricardo Bruña, Fernando Maestú. Phase locking value revisited: teaching new tricks to an old dog. Journal of Neural Engineering, 15(5):056011, 2018. doi:10.1088/1741-2552/aacfe4.

Cornelis J. Stam, Guido Nolte, and Andreas Daffertshofer. Phase lag index: assessment of functional connectivity from multi channel EEG and MEG with diminished bias from common sources. Human Brain Mapping, 28(11):1178–1193, 2007. doi:10.1002/hbm.20346.

Martin Vinck, Robert Oostenveld, Marijn van Wingerden, Franscesco Battaglia, and Cyriel M.A. Pennartz. An improved index of phase-synchronization for electrophysiological data in the presence of volume-conduction, noise and sample-size bias. NeuroImage, 55(4):1548–1565, 2011. doi:10.1016/j.neuroimage.2011.01.055.

Lionel Barnett and Anil K. Seth. Granger causality for state-space models. Physical Review E, 91(4):040101, 2015. doi:10.1103/PhysRevE.91.040101.

Irene Winkler, Danny Panknin, Daniel Bartz, Klaus-Robert Müller, and Stefan Haufe. Validity of time reversal for testing granger causality. IEEE Transactions on Signal Processing, 64(11):2746–2760, 2016. doi:10.1109/TSP.2016.2531628.

Stefan Haufe, Vadim V Nikulin, and Guido Nolte. Alleviating the influence of weak data asymmetries on granger-causal analyses. In Latent Variable Analysis and Signal Separation: 10th International Conference, LVA/ICA 2012, Tel Aviv, Israel, March 12-15, 2012. Proceedings 10, 25–33. Springer, 2012. doi:10.1007/978-3-642-28551-6_4.

Comparing spectral connectivity computed over time or over trials

mne_connectivity.spectral_connectivity_epochs

mne_connectivity.read_connectivity

---

## mne_connectivity.SpectroTemporalConnectivity#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.SpectroTemporalConnectivity.html

**Contents:**
- mne_connectivity.SpectroTemporalConnectivity#
- Examples using mne_connectivity.SpectroTemporalConnectivity#

Spectrotemporal connectivity class.

This class stores connectivity data that varies over both frequency and time. The temporal part describes sample-by-sample time-varying connectivity (usually on the order of milliseconds). Note the difference relative to Epochs.

The underlying data is an array of shape (n_connections, n_freqs, n_times), or (n_nodes, n_nodes, n_freqs, n_times).

The connectivity data that is a raveled array of (n_estimated_nodes, ...) shape. The n_estimated_nodes is equal to n_nodes_in * n_nodes_out if one is computing the full connectivity, or a subset of nodes equal to the length of indices passed in.

The frequencies at which the connectivity data is computed over. If the frequencies are “frequency bands” (i.e. gamma band), then these are the median of those bands.

The times at which the connectivity data is computed over.

The number of nodes in the dataset used to compute connectivity. This should be equal to the number of signals in the original dataset.

The names of the nodes of the dataset used to compute connectivity. If ‘None’ (default), then names will be a list of integers from 0 to n_nodes. If a list of names, then it must be equal in length to n_nodes.

The indices of relevant connectivity data. If 'all' (default), then data is connectivity between all nodes. If 'symmetric', then data is symmetric connectivity between all nodes. If a tuple, then the first list represents the “in nodes”, and the second list represents the “out nodes”. See “Notes” for more information.

The method name used to compute connectivity.

The type of method used to compute spectral analysis, by default None.

The number of epochs used in the computation of connectivity, by default None.

Extra connectivity parameters. These may include freqs for spectral connectivity, and/or times for connectivity over time. In addition, these may include extra parameters that are stored as xarray attrs.

Xarray attributes of connectivity.

Generate block companion matrix.

The coordinates of the xarray data.

The dimensions of the xarray data.

The frequency points of the connectivity data.

Indices of connectivity data.

The method used to compute connectivity.

The number of epochs the connectivity data varies over.

Number of epochs used in computation of connectivity.

The number of nodes in the original dataset.

Shape of raveled connectivity.

The time points of the connectivity data.

Xarray of the connectivity data.

Append another connectivity structure.

Combine connectivity data over epochs.

Get connectivity data as a numpy array.

plot_circle(**kwargs)

Visualize connectivity as a circular graph.

Predict samples on actual data.

rename_nodes(mapping)

Save connectivity data to disk.

simulate(n_samples[, noise_func, random_state])

Simulate vector autoregressive (VAR) model.

get_epoch_annotations

Append another connectivity structure.

The Epoched Connectivity class to append.

The altered Epoched Connectivity class.

Xarray attributes of connectivity.

Combine connectivity data over epochs.

How to combine correlation estimates across epochs. Default is ‘mean’. If callable, it must accept one positional input. For example:

The combined connectivity data structure.

Generate block companion matrix.

Returns the data matrix if the model is VAR(1).

The coordinates of the xarray data.

The dimensions of the xarray data.

The frequency points of the connectivity data.

If these are computed over a frequency band, it will be the median frequency of the frequency band.

Get connectivity data as a numpy array.

How to format the output, by default ‘raveled’, which will represent each connectivity matrix as a (n_nodes_in * n_nodes_out,) list. If ‘dense’, then will return each connectivity matrix as a 2D array. If ‘compact’ (default) then will return ‘raveled’ if indices were defined as a list of tuples, or dense if indices is ‘all’. Multivariate connectivity data cannot be returned in a dense form.

The output connectivity data.

Indices of connectivity data.

Either ‘all’ for all-to-all connectivity, ‘symmetric’ for symmetric all-to-all connectivity, or a tuple of lists representing the node-to-nodes that connectivity was computed.

The method used to compute connectivity.

The number of epochs the connectivity data varies over.

Number of epochs used in computation of connectivity.

Can be ‘None’, if there was no epochs used. This is equivalent to the number of epochs, if there is no combining of epochs.

The number of nodes in the original dataset.

Even if indices defines a subset of nodes that were computed, this should be the total number of nodes in the original dataset.

Visualize connectivity as a circular graph.

Node names. The order corresponds to the order in con.

Two arrays with indices of connections for which the connections strengths are defined in con. Only needed if con is a 1D array.

If not None, only the n_lines strongest connections (strength=abs(con)) are drawn.

Array with node positions in degrees. If None, the nodes are equally spaced on the circle. See mne.viz.circular_layout.

Width of each node in degrees. If None, the minimum angle between any two nodes is used as the width.

The relative height of the colored bar labeling each node. Default 1.0 is the standard height.

List with the color to use for each node. If fewer colors than nodes are provided, the colors will be repeated. Any color supported by matplotlib can be used, e.g., RGBA tuples, named colors.

Color to use for background. See matplotlib.colors.

Color to use for text. See matplotlib.colors.

Color to use for lines around nodes. See matplotlib.colors.

Line width to use for connections.

Colormap to use for coloring the connections.

Minimum value for colormap. If None, it is determined automatically.

Maximum value for colormap. If None, it is determined automatically.

Display a colorbar or not.

Size of the colorbar.

Position of the colorbar.

Font size to use for title.

Font size to use for node names.

Font size to use for colorbar.

Space to add around figure to accommodate long labels.

The axes to use to plot the connectivity circle.

The figure to use. If None, a new figure with the specified background color will be created.

Deprecated: will be removed in version 0.5.

Location of the subplot when creating figures with multiple plots. E.g. 121 or (1, 2, 1) for 1 row, 2 columns, plot 1. See matplotlib.pyplot.subplot.

Deprecated: will be removed in version 0.5.

When enabled, left-click on a node to show only connections to that node. Right-click shows all connections.

This code is based on a circle graph example by Nicolas P. Rougier

By default, matplotlib.pyplot.savefig() does not take facecolor into account when saving, even if set when a figure is generated. This can be addressed via, e.g.:

If facecolor is not set via matplotlib.pyplot.savefig(), the figure labels, title, and legend may be cut off in the output figure.

Predict samples on actual data.

The result of this function is used for calculating the residuals.

Epoched or continuous data set. Has shape (n_epochs, n_signals, n_times) or (n_signals, n_times).

Data as predicted by the VAR model of shape same as data.

Residuals are obtained by r = x - var.predict(x).

To compute residual covariances:

Mapping from original node names (keys) to new node names (values).

Save connectivity data to disk.

Can later be loaded using the function mne_connectivity.read_connectivity().

The filepath to save the data. Data is saved as netCDF files (.nc extension).

Shape of raveled connectivity.

Simulate vector autoregressive (VAR) model.

This function generates data from the VAR model.

Number of samples to generate.

This function is used to create the generating noise process. If set to None, Gaussian white noise with zero mean and unit variance is used.

If random_state is an int, it will be used as a seed for RandomState. If None, the seed will be obtained from the operating system (see RandomState for details). Default is None.

The time points of the connectivity data.

Xarray of the connectivity data.

Comparing spectral connectivity computed over time or over trials

Compute seed-based time-frequency connectivity in sensor space

Using the connectivity classes

mne_connectivity.SpectralConnectivity

mne_connectivity.EpochConnectivity

---

## mne_connectivity.symmetric_orth#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.symmetric_orth.html

**Contents:**
- mne_connectivity.symmetric_orth#
- Examples using mne_connectivity.symmetric_orth#

Perform symmetric orthogonalization.

Uses the method from [1] to jointly orthogonalize the time series.

The data to process. If a generator, it must return 2D arrays to process.

The maximum number of iterations to perform.

The relative tolerance for convergence.

Control verbosity of the logging output. If None, use the default verbosity level. See the logging documentation and mne.verbose() for details. Should only be passed as a keyword argument.

The orthogonalized data. If data is a generator, a generator is returned.

G. L. Colclough, M. J. Brookes, S. M. Smith, and M. W. Woolrich. A symmetric multivariate leakage correction for MEG connectomes. NeuroImage, 117:439–448, August 2015. doi:10.1016/j.neuroimage.2015.03.071.

Compute envelope correlations in source space

mne_connectivity.read_connectivity

mne_connectivity.degree

---

## mne_connectivity.TemporalConnectivity#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.TemporalConnectivity.html

**Contents:**
- mne_connectivity.TemporalConnectivity#
- Examples using mne_connectivity.TemporalConnectivity#

Temporal connectivity class.

This is an array of shape (n_connections, n_times), or (n_nodes, n_nodes, n_times). This describes how connectivity varies over time. It describes sample-by-sample time-varying connectivity (usually on the order of milliseconds). Here time (t=0) is the same for all connectivity measures.

The connectivity data that is a raveled array of (n_estimated_nodes, ...) shape. The n_estimated_nodes is equal to n_nodes_in * n_nodes_out if one is computing the full connectivity, or a subset of nodes equal to the length of indices passed in.

The times at which the connectivity data is computed over.

The number of nodes in the dataset used to compute connectivity. This should be equal to the number of signals in the original dataset.

The names of the nodes of the dataset used to compute connectivity. If ‘None’ (default), then names will be a list of integers from 0 to n_nodes. If a list of names, then it must be equal in length to n_nodes.

The indices of relevant connectivity data. If 'all' (default), then data is connectivity between all nodes. If 'symmetric', then data is symmetric connectivity between all nodes. If a tuple, then the first list represents the “in nodes”, and the second list represents the “out nodes”. See “Notes” for more information.

The method name used to compute connectivity.

The number of epochs used in the computation of connectivity, by default None.

Extra connectivity parameters. These may include freqs for spectral connectivity, and/or times for connectivity over time. In addition, these may include extra parameters that are stored as xarray attrs.

mne_connectivity.EpochConnectivity is a similar connectivity class to this one. However, that describes one connectivity snapshot for each epoch. These epochs might be chunks of time that have different meaning for time t=0. Epochs can mean separate trials, where the beginning of the trial implies t=0. These Epochs may also be discontiguous.

Xarray attributes of connectivity.

Generate block companion matrix.

The coordinates of the xarray data.

The dimensions of the xarray data.

Indices of connectivity data.

The method used to compute connectivity.

The number of epochs the connectivity data varies over.

Number of epochs used in computation of connectivity.

The number of nodes in the original dataset.

Shape of raveled connectivity.

The time points of the connectivity data.

Xarray of the connectivity data.

Append another connectivity structure.

Combine connectivity data over epochs.

Get connectivity data as a numpy array.

plot_circle(**kwargs)

Visualize connectivity as a circular graph.

Predict samples on actual data.

rename_nodes(mapping)

Save connectivity data to disk.

simulate(n_samples[, noise_func, random_state])

Simulate vector autoregressive (VAR) model.

get_epoch_annotations

Append another connectivity structure.

The Epoched Connectivity class to append.

The altered Epoched Connectivity class.

Xarray attributes of connectivity.

Combine connectivity data over epochs.

How to combine correlation estimates across epochs. Default is ‘mean’. If callable, it must accept one positional input. For example:

The combined connectivity data structure.

Generate block companion matrix.

Returns the data matrix if the model is VAR(1).

The coordinates of the xarray data.

The dimensions of the xarray data.

Get connectivity data as a numpy array.

How to format the output, by default ‘raveled’, which will represent each connectivity matrix as a (n_nodes_in * n_nodes_out,) list. If ‘dense’, then will return each connectivity matrix as a 2D array. If ‘compact’ (default) then will return ‘raveled’ if indices were defined as a list of tuples, or dense if indices is ‘all’. Multivariate connectivity data cannot be returned in a dense form.

The output connectivity data.

Indices of connectivity data.

Either ‘all’ for all-to-all connectivity, ‘symmetric’ for symmetric all-to-all connectivity, or a tuple of lists representing the node-to-nodes that connectivity was computed.

The method used to compute connectivity.

The number of epochs the connectivity data varies over.

Number of epochs used in computation of connectivity.

Can be ‘None’, if there was no epochs used. This is equivalent to the number of epochs, if there is no combining of epochs.

The number of nodes in the original dataset.

Even if indices defines a subset of nodes that were computed, this should be the total number of nodes in the original dataset.

Visualize connectivity as a circular graph.

Node names. The order corresponds to the order in con.

Two arrays with indices of connections for which the connections strengths are defined in con. Only needed if con is a 1D array.

If not None, only the n_lines strongest connections (strength=abs(con)) are drawn.

Array with node positions in degrees. If None, the nodes are equally spaced on the circle. See mne.viz.circular_layout.

Width of each node in degrees. If None, the minimum angle between any two nodes is used as the width.

The relative height of the colored bar labeling each node. Default 1.0 is the standard height.

List with the color to use for each node. If fewer colors than nodes are provided, the colors will be repeated. Any color supported by matplotlib can be used, e.g., RGBA tuples, named colors.

Color to use for background. See matplotlib.colors.

Color to use for text. See matplotlib.colors.

Color to use for lines around nodes. See matplotlib.colors.

Line width to use for connections.

Colormap to use for coloring the connections.

Minimum value for colormap. If None, it is determined automatically.

Maximum value for colormap. If None, it is determined automatically.

Display a colorbar or not.

Size of the colorbar.

Position of the colorbar.

Font size to use for title.

Font size to use for node names.

Font size to use for colorbar.

Space to add around figure to accommodate long labels.

The axes to use to plot the connectivity circle.

The figure to use. If None, a new figure with the specified background color will be created.

Deprecated: will be removed in version 0.5.

Location of the subplot when creating figures with multiple plots. E.g. 121 or (1, 2, 1) for 1 row, 2 columns, plot 1. See matplotlib.pyplot.subplot.

Deprecated: will be removed in version 0.5.

When enabled, left-click on a node to show only connections to that node. Right-click shows all connections.

This code is based on a circle graph example by Nicolas P. Rougier

By default, matplotlib.pyplot.savefig() does not take facecolor into account when saving, even if set when a figure is generated. This can be addressed via, e.g.:

If facecolor is not set via matplotlib.pyplot.savefig(), the figure labels, title, and legend may be cut off in the output figure.

Predict samples on actual data.

The result of this function is used for calculating the residuals.

Epoched or continuous data set. Has shape (n_epochs, n_signals, n_times) or (n_signals, n_times).

Data as predicted by the VAR model of shape same as data.

Residuals are obtained by r = x - var.predict(x).

To compute residual covariances:

Mapping from original node names (keys) to new node names (values).

Save connectivity data to disk.

Can later be loaded using the function mne_connectivity.read_connectivity().

The filepath to save the data. Data is saved as netCDF files (.nc extension).

Shape of raveled connectivity.

Simulate vector autoregressive (VAR) model.

This function generates data from the VAR model.

Number of samples to generate.

This function is used to create the generating noise process. If set to None, Gaussian white noise with zero mean and unit variance is used.

If random_state is an int, it will be used as a seed for RandomState. If None, the seed will be obtained from the operating system (see RandomState for details). Default is None.

The time points of the connectivity data.

Xarray of the connectivity data.

Compute envelope correlations in volume source space

mne_connectivity.Connectivity

mne_connectivity.SpectralConnectivity

---

## mne_connectivity.vector_auto_regression#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.vector_auto_regression.html

**Contents:**
- mne_connectivity.vector_auto_regression#
- Examples using mne_connectivity.vector_auto_regression#

Compute vector auto-regresssive (VAR) model.

The data from which to compute connectivity. The epochs dimension is interpreted differently, depending on 'output' argument.

(Optional) The time points used to construct the epoched data. If None, then times_used in the Connectivity will not be available.

The names of the nodes of the dataset used to compute connectivity. If ‘None’ (default), then names will be a list of integers from 0 to n_nodes. If a list of names, then it must be equal in length to n_nodes.

Autoregressive model order, by default 1.

Ridge penalty (l2-regularization) parameter, by default 0.0.

Whether to compute the backwards operator and average with the forward operator. Addresses bias in the least-square estimation [1].

Whether to compute one VAR model using all epochs as multiple samples of the same VAR model (‘avg-epochs’), or to compute a separate VAR model for each epoch (‘dynamic’), which results in a time-varying VAR model. See Notes.

The number of jobs to run in parallel (default 1). Requires the joblib package.

If not None, override default verbose level (see mne.verbose() for more info). If used, it should be passed as a keyword-argument only.

The connectivity data estimated.

Names can be passed in, which are then used to instantiate the nodes of the connectivity class. For example, they can be the electrode names of EEG.

For higher-order VAR models, there are n_order A matrices, representing the linear dynamics with respect to that lag. These are represented by vertically concatenated matrices. For example, if the input is data where n_signals is 3, then an order-1 VAR model will result in a 3x3 connectivity matrix. An order-2 VAR model will result in a 6x3 connectivity matrix, with two 3x3 matrices representing the dynamics at lag 1 and lag 2, respectively.

When computing a VAR model (i.e. linear dynamical system), we require the input to be a (n_epochs, n_signals, n_times) 3D array. There are two ways one can interpret the data in the model.

First, epochs can be treated as multiple samples observed for a single VAR model. That is, we have $X_1, X_2, …, X_n$, where each $X_i$ is a (n_signals, n_times) data array, with n epochs. We are interested in estimating the parameters, $(A_1, A_2, …, A_{order})$ from the following model over all epochs:

This results in one VAR model over all the epochs.

The second approach treats each epoch as a different VAR model, estimating a time-varying VAR model. Using the same data as above, we now are interested in estimating the parameters, $(A_1, A_2, …, A_{order})$ for each epoch. The model would be the following for each epoch:

This results in one VAR model for each epoch. This is done according to the model in [2].

b is of shape [m, m*p], with sub matrices arranged as follows:

Each sub matrix b_ij is a column vector of length p that contains the filter coefficients from channel j (source) to channel i (sink).

In order to optimize RAM usage, the estimating equations are set up by iterating over sample points. This assumes that there are in general more sample points then channels. You should not estimate a VAR model using less sample points then channels, unless you have good reason.

Scott T. M. Dawson, Maziar S. Hemati, Matthew O. Williams, and Clarence W. Rowley. Characterizing and correcting for the effect of sensor noise in the dynamic mode decomposition. Experiments in Fluids, Feb 2016. doi:10.1007/s00348-016-2127-7.

Adam Li, Kristin M. Gunnarsdottir, Sara Inati, Kareem Zaghloul, John Gale, Juan Bulacio, Jorge Martinez-Gonzalez, and Sridevi V. Sarma. Linear time-varying model characterizes invasive eeg signals generated from complex epileptic networks. In 2017 39th Annual International Conference of the IEEE Engineering in Medicine and Biology Society (EMBC), volume, 2802–2805. 2017. doi:10.1109/EMBC.2017.8037439.

Compute vector autoregressive model (linear system)

mne_connectivity.phase_slope_index

mne_connectivity.spectral_connectivity_epochs

---

## mne_connectivity.viz.plot_connectivity_circle#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.viz.plot_connectivity_circle.html

**Contents:**
- mne_connectivity.viz.plot_connectivity_circle#
- Examples using mne_connectivity.viz.plot_connectivity_circle#

Visualize connectivity as a circular graph.

Connectivity scores. Can be a square matrix, or a 1D array. If a 1D array is provided, “indices” has to be used to define the connection indices.

Node names. The order corresponds to the order in con.

Two arrays with indices of connections for which the connections strengths are defined in con. Only needed if con is a 1D array.

If not None, only the n_lines strongest connections (strength=abs(con)) are drawn.

Array with node positions in degrees. If None, the nodes are equally spaced on the circle. See mne.viz.circular_layout.

Width of each node in degrees. If None, the minimum angle between any two nodes is used as the width.

The relative height of the colored bar labeling each node. Default 1.0 is the standard height.

List with the color to use for each node. If fewer colors than nodes are provided, the colors will be repeated. Any color supported by matplotlib can be used, e.g., RGBA tuples, named colors.

Color to use for background. See matplotlib.colors.

Color to use for text. See matplotlib.colors.

Color to use for lines around nodes. See matplotlib.colors.

Line width to use for connections.

Colormap to use for coloring the connections.

Minimum value for colormap. If None, it is determined automatically.

Maximum value for colormap. If None, it is determined automatically.

Display a colorbar or not.

Size of the colorbar.

Position of the colorbar.

Font size to use for title.

Font size to use for node names.

Font size to use for colorbar.

Space to add around figure to accommodate long labels.

The axes to use to plot the connectivity circle.

The figure to use. If None, a new figure with the specified background color will be created.

Deprecated: will be removed in version 0.5.

Location of the subplot when creating figures with multiple plots. E.g. 121 or (1, 2, 1) for 1 row, 2 columns, plot 1. See matplotlib.pyplot.subplot.

Deprecated: will be removed in version 0.5.

When enabled, left-click on a node to show only connections to that node. Right-click shows all connections.

This code is based on a circle graph example by Nicolas P. Rougier

By default, matplotlib.pyplot.savefig() does not take facecolor into account when saving, even if set when a figure is generated. This can be addressed via, e.g.:

If facecolor is not set via matplotlib.pyplot.savefig(), the figure labels, title, and legend may be cut off in the output figure.

Compute mixed source space connectivity and visualize it using a circular graph

Compute source space connectivity and visualize it using a circular graph

mne_connectivity.viz.plot_sensors_connectivity

mne_connectivity.make_signals_in_freq_bands

---

## mne_connectivity.viz.plot_sensors_connectivity#

**URL:** https://mne.tools/mne-connectivity/stable/generated/mne_connectivity.viz.plot_sensors_connectivity.html

**Contents:**
- mne_connectivity.viz.plot_sensors_connectivity#
- Examples using mne_connectivity.viz.plot_sensors_connectivity#

Visualize the sensor connectivity in 3D.

The measurement info.

The computed connectivity measure(s).

Channels to include. Slices and lists of integers will be interpreted as channel indices. In lists, channel type strings (e.g., ['meg', 'eeg']) will pick channels of those types, channel name strings (e.g., ['MEG0111', 'MEG2623'] will pick the given channels. Can also be the string values 'all' to pick all channels, or 'data' to pick data channels. None (default) will pick good data channels. Note that channels in info['bads'] will be included if their names or indices are explicitly provided. Indices of selected channels.

Label for the colorbar.

Number of strongest connections shown. By default 20.

Colormap for coloring connections by strength. If str, must be a valid Matplotlib colormap (i.e. a valid key of matplotlib.colormaps). Default is "RdBu".

Comparing spectral connectivity computed over time or over trials

Compute all-to-all connectivity in sensor space

mne_connectivity.select_order

mne_connectivity.viz.plot_connectivity_circle

---

## MNE-Connectivity#

**URL:** https://mne.tools/mne-connectivity/stable/

**Contents:**
- MNE-Connectivity#

MNE-Connectivity is an open-source Python package for connectivity and related measures of MEG, EEG, or iEEG data built on top of the MNE-Python API. It includes modules for data input/output, visualization, common connectivity analysis, and post-hoc statistics and processing.

---

## Using the connectivity classes#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/connectivity_classes.html

**Contents:**
- Using the connectivity classes#

Go to the end to download the full example code.

Compute different connectivity measures and then demonstrate the utility of the class.

Here we compute the Phase Lag Index (PLI) between all gradiometers and showcase how we can interact with the connectivity class.

Now, we can look at different functionalities of the connectivity class returned by mne_connectivity.spectral_connectivity_epochs(). The following are some basic attributes of connectivity classes.

The underlying connectivity measure can be stored in two ways: i) raveled and ii) dense. Raveled storage will be a 1D column flattened array, similar to what one might expect when using numpy.ravel. However, if you ask for the dense data, then the shape will show the N by N connectivity. In general, you might prefer the raveled version if you specify a subset of indices (e.g. some subset of sources) for the computation of a bivariate connectivity measure or if you have a symmetric measure (e.g. coherence). The ‘dense’ output on the other hand provides an actual square matrix, which can be used for post-hoc analysis that expects a matrix shape.

The underlying data is stored as an xarray, so we have access to DataArray attributes. Each connectivity measure function automatically stores relevant metadata. For example, the method used in this example is the phase-lag index (‘pli’).

Other properties of the connectivity class, special to the spectro-temporal connectivity class.

Not all connectivity classes will have these properties.

Total running time of the script: (0 minutes 19.083 seconds)

Download Jupyter notebook: connectivity_classes.ipynb

Download Python source code: connectivity_classes.py

Download zipped: connectivity_classes.zip

Gallery generated by Sphinx-Gallery

Compute source space connectivity and visualize it using a circular graph

Working with ragged indices for multivariate connectivity

---

## Working with ragged indices for multivariate connectivity#

**URL:** https://mne.tools/mne-connectivity/stable/auto_examples/handling_ragged_arrays.html

**Contents:**
- Working with ragged indices for multivariate connectivity#
- Background#

Go to the end to download the full example code.

This example demonstrates how multivariate connectivity involving different numbers of seeds and targets can be handled in MNE-Connectivity.

With multivariate connectivity, interactions between multiple signals can be considered together, and the number of signals designated as seeds and targets does not have to be equal within or across connections. Issues can arise from this when storing information associated with connectivity in arrays.

Such arrays are ‘ragged’, and support for ragged arrays is limited in NumPy to the object datatype. Not only is working with ragged arrays cumbersome, but saving arrays with dtype='object' is not supported by the h5netcdf engine used to save connectivity objects.

The workaround used in MNE-Connectivity is to pad ragged arrays with some known values according to the largest number of entries in each dimension, such that there is an equal amount of information across and within connections for each dimension of the arrays.

As an example, consider we have 5 channels and want to compute 2 connections: the first between channels in indices 0 and 1 with those in indices 2, 3, and 4; and the second between channels 0, 1, 2, and 3 with channel 4. The seed and target indices can be written as such:

The indices parameter passed to spectral_connectivity_epochs() and spectral_connectivity_time() must be a tuple of array-likes, meaning that the indices can be passed as a tuple of: lists; tuples; or NumPy arrays. Examples of how indices can be formed are shown below:

N.B. Note that since NumPy v1.19.0, dtype=’object’ must be specified when forming ragged arrays.

Just as for bivariate connectivity, the length of indices[0] and indices[1] is equal (i.e. the number of connections), however information about the multiple channel indices for each connection is stored in a nested array.

Importantly, these indices are ragged, as the first connection will be computed between 2 seed and 3 target channels, and the second connection between 4 seed and 1 target channel(s). The connectivity functions will recognise the indices as being ragged, and pad them to a ‘full’ array by adding placeholder values which are masked accordingly. This makes the indices easier to work with, and also compatible with the engine used to save connectivity objects. For example, the above indices would become:

where -- are masked entries. These indices are what is stored in the returned connectivity objects.

For the connectivity results themselves, the methods available in MNE-Connectivity combine information across the different channels into a single (time-)frequency-resolved connectivity spectrum, regardless of the number of seed and target channels, so ragged arrays are not a concern here.

However, the maximised imaginary part of coherency (MIC) method also returns spatial patterns of connectivity, which show the contribution of each channel to the dimensionality-reduced connectivity estimate (explained in more detail in Compute multivariate measures of the imaginary part of coherency). Because these patterns are returned for each channel, their shape can vary depending on the number of seeds and targets in each connection, making them ragged.

To avoid this, the patterns are padded along the channel axis with the known and invalid entry np.nan, in line with that applied to indices. Extracting only the valid spatial patterns from the connectivity object is trivial, as shown below:

Total running time of the script: (0 minutes 0.018 seconds)

Download Jupyter notebook: handling_ragged_arrays.ipynb

Download Python source code: handling_ragged_arrays.py

Download zipped: handling_ragged_arrays.zip

Gallery generated by Sphinx-Gallery

Using the connectivity classes

Dynamic Connectivity Examples

---
