# Mne-Core - Installation

**Pages:** 13

---

## Advanced setup#

**URL:** https://mne.tools/stable/install/advanced.html

**Contents:**
- Advanced setup#
- Working with Jupyter Notebooks and JupyterLab#
- Installing to a headless Linux server#
- Using the development version#
- Choosing the Qt framework#
- Fixing dock icons on Linux#
- GPU acceleration with CUDA#
- Off-screen rendering with MESA#
- Troubleshooting 3D plots#
  - 3D plotting trouble after upgrade on macOS#

If you like using Jupyter notebooks, you should also update the “base” conda environment to include the nb_conda_kernels package; this will make it easier to use MNE-Python in Jupyter Notebooks launched from the Anaconda GUI:

When using MNE-Python within IPython or a Jupyter notebook, we strongly recommend using the Qt matplotlib backend for fast and correct rendering. On Linux, for example, Qt is the only matplotlib backend for which 3D rendering will work correctly. On macOS, certain matplotlib functions might not work as expected on backends other than Qt. Enabling Qt can be accomplished when starting IPython from a terminal:

or in a Jupyter Notebook, you can use the “magic” command:

This will create separate pop-up windows for each figure, and has the advantage that the 3D plots will retain rich interactivity (so, for example, you can click-and-drag to rotate cortical surface activation maps).

If you are creating a static notebook or simply prefer Jupyter’s inline plot display, MNE-Python will work with the standard “inline” magic:

but some functionality will be lost. For example, PyVista scenes will still pop-up a separate window, but only one window at a time is possible, and interactivity within the scene is limited in non-blocking plot calls.

If you are using MNE-Python on Windows through IPython or Jupyter, you might also have to use the IPython magic command %gui qt (see here). For example:

If you installed the nb_conda_kernels package into your base environment (as recommended), you should be able to launch mne-capable notebooks from within the Anaconda Navigator GUI without having to explicitly switch to the mne environment first; look for Python [conda env:mne] when choosing which notebook kernel to use. Otherwise, be sure to activate the mne environment before launching the notebook.

If you use another Python setup and you encounter some difficulties please report them on the MNE Forum or on the GitHub issues page to get assistance.

It is also possible to interact with the 3D plots without installing Qt by using the notebook 3d backend:

The notebook 3d backend requires PyVista to be installed along with other packages, please follow Install via pip or conda.

First, follow the standard installation instructions. Next, you can choose to install the osmesa (off-screen MESA) VTK variant, which avoids the need to use Xvfb to start a virtual display (and have a sufficiently updated MESA to render properly):

See Upgrading to the development version for how to do a one-time update to the latest development version of MNE-Python. If you plan to contribute to MNE-Python, or just prefer to use git rather than pip to make frequent updates, there are instructions for installing from a git clone in the Contributing guide.

The conda-forge version of MNE-Python ships with PyQt5. If you would like to use a different binding, you can instead install MNE-Python via pip:

On newer versions of Ubuntu (e.g., 24.04), applications must supply a .desktop file associated with them, otherwise a generic icon will be used like:

To fix this, you can create a .desktop file for MNE-Python. Here is an example file that you can save as ~/.local/share/applications/mne-python.desktop after fixing the path to the MNE-Python icon, which you can download here if needed:

It should make the icon appear correctly in the dock:

MNE-Python can utilize NVIDIA CUDA GPU processing to speed up some operations (e.g. FIR filtering) by roughly an order of magnitude. To use CUDA, first ensure that you are running the NVIDIA proprietary drivers on your operating system, and then do:

If you receive a message reporting the GPU’s available memory, CuPy is working properly. To permanently enable CUDA in MNE, you can do:

You can then test MNE CUDA support by running the associated test:

If the tests pass, then CUDA should work in MNE. You can use CUDA in methods that state that they allow passing n_jobs='cuda', such as mne.io.Raw.filter() and mne.io.Raw.resample(), and they should run faster than the CPU-based multithreading such as n_jobs=8.

On remote Linux systems, it might be possible to use MESA software rendering (such as llvmpipe or swr) for 3D visualization (with some tweaks). For example, on CentOS 7.5 you might be able to use an environment variable to force MESA to use modern OpenGL by using this before executing spyder or python:

Also, it’s possible that different software rending backends might perform better than others, such as using the llvmpipe backend rather than swr. In newer MESA (21+), rendering can be incorrect when using MSAA, so consider setting:

MESA also can have trouble with full-screen antialiasing, which you can disable with:

or by doing mne.viz.set_3d_options(antialias=False) within a given Python session.

Some hardware-accelerated graphics on linux (e.g., some Intel graphics cards) provide an insufficient implementation of OpenGL, and in those cases it can help to force software rendering instead with something like:

Another issue that may come up is that the MESA software itself may be out of date in certain operating systems, for example CentOS. This may lead to incomplete rendering of some 3D plots. A solution is described in this Github comment. It boils down to building a newer version (e.g., 18.3.6) locally following a variant of these instructions. If you have CentOS 7 or newer, you can also try some prebuilt binaries we made. After downloading the files, untar them and add them to the appropriate library paths using the following commands:

To check that everything went well, type the following:

Another way to check is to type:

and it should show the right version of MESA:

When upgrading MNE-Python from version 0.19 or lower, some macOS users may end up with conflicting versions of some of the 3D plotting dependencies. If you plot using the pyvista 3D backend and find that you can click-drag to rotate the brain, but cannot adjust any of the settings sliders, it is likely that your versions of VTK and/or QT are incompatible. This series of commands should fix it:

If you installed VTK using pip rather than conda, substitute the first line for pip uninstall -y vtk.

If you are having trouble with 3D plotting on Linux, one possibility is that you are using Wayland for graphics. To check, you can do:

If so, you will need to tell Qt to use X11 instead of Wayland. You can do this by setting export QT_QPA_PLATFORM=xcb in your terminal session. To make it permanent for your logins, you can set it for example in ~/.profile.

Install via pip or conda

Testing your installation

---

## IDE integration (VSCode, Spyder, etc.)#

**URL:** https://mne.tools/stable/install/ides.html

**Contents:**
- IDE integration (VSCode, Spyder, etc.)#

Most users find it convenient to write and run their code in an Integrated Development Environment (IDE). Some popular choices for scientific Python development are:

Visual Studio Code (often shortened to “VS Code” or “vscode”) is a development-focused text editor that supports many programming languages in addition to Python, includes an integrated terminal console, and has a rich extension ecosystem. Installing Microsoft’s Python Extension is enough to get most Python users up and running. VS Code is free and open-source.

Spyder is a free and open-source IDE developed by and for scientists who use Python. It can be installed via a standalone Spyder installer. To avoid dependency conflicts with Spyder, you should install mne in a separate environment, as explained in previous sections or using our dedicated installer. Then, instruct Spyder to use the MNE-Python interpreter by opening Spyder and navigating to Tools > Preferences > Python Interpreter > Use the following interpreter.

PyCharm is an IDE specifically for Python development that provides an all-in-one solution (no extension packages needed). PyCharm comes in a free and open-source Community edition as well as a paid Professional edition.

For these IDEs, you’ll need to provide the path to the Python interpreter you want it to use. If you’re using the MNE-Python installers, on Linux and macOS opening the Prompt will display several lines of information, including a line that will read something like:

Altertatively (or on Windows), you can find that path by opening the Python interpreter you want to use (e.g., the one from the MNE-Python installer, or a conda environment that you have activated) and running:

This should print something like C:\Program Files\MNE-Python\1.10.0_0\bin\python.exe (Windows) or /Users/user/Applications/MNE-Python/1.10.0_0/.mne-python/bin/python (macOS).

For Spyder, if the console cannot start because spyder-kernels is missing, install the required version in the conda environment. For example, with the environment you want to use activated, run conda install spyder-kernels.

MNE-Python installers

Install via pip or conda

---

## Installing FreeSurfer#

**URL:** https://mne.tools/stable/install/freesurfer.html

**Contents:**
- Installing FreeSurfer#

FreeSurfer is software for analysis and visualization of MRI data. In the MNE ecosystem, freesurfer is used to convert structural MRI scans into models of the scalp, inner/outer skull, and cortical surfaces, which are used to

model how changes in the electrical and magnetic field caused by neural activity propagate to the sensor locations (part of computing the “forward solution”), and

constrain the estimates of where brain activity may have occurred (in the “inverse imaging” step of source localization).

System requirements, setup instructions, and test scripts are provided on the FreeSurfer download page. Note that if you don’t already have it, you will need to install tcsh for FreeSurfer to work; tcsh is usually pre-installed with macOS, and is available in the package repositories for Linux-based systems (e.g., sudo apt install tcsh on Ubuntu-like systems).

Overview of the MNE tools suite

---

## Installing MNE-C#

**URL:** https://mne.tools/stable/install/mne_c.html

**Contents:**
- Installing MNE-C#
- System requirements#
- Downloading and Installing MNE-C#
- Configuring MNE-C#
- Testing MNE-C installation#
- Troubleshooting MNE-C installation#

MNE-C runs on macOS (version 10.5 “Leopard” or later) and Linux (kernel 2.6.9 or later). Both 32- and 64-bit operating systems are supported; a PowerPC version for macOS can be provided upon request. At least 2 GB of memory is required, 4 GB or more is recommended. The software requires at least 80 MB of disk space. MATLAB is an optional dependency; the free MATLAB runtime is sufficient. If MATLAB is not present, the utilities mne_convert_mne_data, mne_epochs2mat, mne_raw2mat, and mne_simu will not work.

For boundary-element model (BEM) mesh generation, and for accessing the tkmedit program from mne_analyze, MNE-C needs access to a working installation of FreeSurfer, including the environment variables FREESURFER_HOME, SUBJECTS_DIR, and SUBJECT.

For installation on macOS, you also need:

the XCode developer tools.

an X Window System such as XQuartz. Version 2.7.9 of XQuartz should work out of the box; the most current version (2.7.11, as of May 2019) may require these additional steps to work:

the netpbm library. The recommended way to get netpbm is to install Homebrew, and run brew install netpbm in the Terminal app. Alternatively, if you prefer to use MacPorts, you can run sudo port install netpbm in the Terminal app.

MNE-C is distributed as either a compressed tar archive (.tar.gz) or a macOS disk image (.dmg). The MNE-C download page requires registration with a valid email address. The current stable version is 2.7.3; “nightly” builds of the development version are also available on the download page.

To install from the compressed tar archive, change directory to the desired install location, and unpack the software using tar:

To install from the macOS disk image, double-click the downloaded .dmg file. In the window that opens, double-click the installer package file (.pkg) to launch the installer, and follow its instructions. In newer versions of macOS, if you see an error that the app is from an untrusted developer, you can override this warning by opening it anyway from the Security & Privacy pane within the computer’s System Preferences.

MNE-C requires two environment variables to be defined manually:

MNE_ROOT should give the path to the folder where MNE-C is installed

MATLAB_ROOT should give the path to your MATLAB binary (e.g., /opt/MATLAB/R2018b or similar). If you do not have MATLAB or the MATLAB runtime, leave MATLAB_ROOT undefined.

Other environment variables are defined by setup scripts provided with MNE-C. You may either run the setup script each time you use MNE-C, or (recommended) configure your shell to run it automatically each time you open a terminal. For bash compatible shells, e.g., sh/bash/zsh, the script to source is $MNE_ROOT/bin/mne_setup_sh. For C shells, e.g., csh/tcsh, the script to source is $MNE_ROOT/bin/mne_setup. If you don’t know what shell you are using, you can run the following command to find out:

To configure MNE-C automatically for bash or sh shells, add this to your .bashrc:

where <path_to_MNE> and <path_to_MATLAB> are replaced by the absolute paths to MNE-C and MATLAB, respectively. If you don’t have MATLAB, you should still include the export MATLAB_ROOT= statement, but leave <path_to_MATLAB> blank.

To configure MNE-C automatically for zsh, use the built-in emulate command in your .zshrc file:

To configure MNE-C automatically for csh or tcsh shells, the corresponding commands in the .cshrc / .tcshrc file are:

If you have done this correctly, the command ls $MNE_ROOT/bin/mne_setup_sh should succeed when run in a new terminal.

An easy way to verify whether your installation of MNE-C is working is to test the OpenGL graphics performance:

This will render an inflated brain surface repeatedly, rotating it by 5 degrees around the z-axis between redraws. The time spent for each full revolution is printed to the terminal window where mne_opengl_test was invoked. Switch focus to that terminal window and use the interrupt key (usually control-c) to halt the test.

The best graphics performance occurs when MNE-C renders to a local display on a computer with hardware acceleration enabled. The mne_analyze GUI has a menu item “On GLX…” in the Help menu; if the GLX dialog says “Direct rendering context” then hardware acceleration is in use. If you are rendering to a local display and see “Nondirect rendering context”, it is recommended that you enable hardware acceleration (consult a search engine or your local IT support staff for assistance). If you are rendering to a remote display or using a VNC connection, “Nondirect rendering context” is normal.

On the fastest graphics cards, the time per revolution in the mne_opengl_test is well below 1 second. If your time per revolution is longer than 10 seconds, either the graphics hardware acceleration is not in effect or you need a faster graphics adapter.

If MNE-C can’t find libxp.so.6, you will need to get the package from the original author (https://launchpad.net/%7Ezeehio/+archive/ubuntu/libxp) to install it:

If MNE-C can’t find libgfortran.so.1, you can probably safely link that filename to the current version of libfortran that came with your system. On a typical 64-bit Ubuntu-like system this would be accomplished by:

If you encounter other errors installing MNE-C, please post a message to the MNE Forum.

---

## Installing MNE-Python#

**URL:** https://mne.tools/stable/install/index.html

**Contents:**
- Installing MNE-Python#

Standalone installers

New to Python? Use our standalone installers that include everything to get you started!

Install via pip or conda

Already familiar with Python? Follow our advanced setup instructions for pip and conda!

MNE-Python installers

---

## Installing Python#

**URL:** https://mne.tools/stable/install/manual_install_python.html

**Contents:**
- Installing Python#
- Other Python distributions#

MNE-Python requires Python and several Python packages. MNE-Python version 1.11 requires Python version 3.10 or higher.

We recommend using a conda-based Python installation, such as Anaconda, Miniconda, or Miniforge. For new users we recommend our pre-built MNE-Python installers, which use conda environments under the hood.

Anaconda Inc., the company that develops the Anaconda and Miniconda Python distributions, changed their terms of service in March of 2024. If you’re unsure about whether your usage situation requires a paid license, we recommend using Miniforge or our pre-built installer instead. These options, by default, install packages only from the community-maintained conda-forge distribution channel, and avoid the distribution channels covered by Anaconda’s terms of service.

While conda-based CPython distributions provide many conveniences, other types of installation (pip / poetry, venv / system-level) and/or other Python distributions (PyPy) should also work with MNE-Python. Generally speaking, if you can install SciPy, getting MNE-Python to work should be unproblematic. Note however that we do not offer installation support for anything other than conda-based installations.

---

## Install via pip or conda#

**URL:** https://mne.tools/stable/install/manual_install.html

**Contents:**
- Install via pip or conda#
- Installing MNE-Python with all dependencies#
- Installing MNE-Python with core dependencies#
- Installing MNE-Python with HDF5 support#
- Installing MNE-Python for other scenarios#

If you’re unfamiliar with Python, we recommend using our MNE-Python installers instead.

MNE-Python requires Python version 3.10 or higher. If you need help installing Python, please refer to our Installing Python guide.

If you use Anaconda, we suggest installing MNE-Python into its own conda environment.

First, please ensure you’re using a recent version of conda. Run in your terminal:

The installed conda version should be 23.10.0 or newer.

Now, you can install MNE-Python:

This will create a new conda environment called mne (you can adjust this by passing a different name via --name) and install all dependencies into it.

If you need to convert structural MRI scans into models of the scalp, inner/outer skull, and cortical surfaces, you will also need to install FreeSurfer.

If you only need MNE-Python’s core functionality, which includes 2D plotting (but does not support 3D visualization), install via pip:

This will create a new conda environment called mne (you can adjust this by passing a different name via --name).

This minimal installation requires only a few dependencies. If you need additional functionality later on, you can install individual packages as needed.

If you plan to use MNE-Python’s functions that require HDF5 I/O (this includes mne.io.read_raw_eeglab(), mne.SourceMorph.save(), and others), you should run via pip:

This will create a new conda environment called mne (you can adjust this by passing a different name via --name).

If you have already installed MNE-Python with core dependencies (e.g. via pip install mne), you can install these two packages to unlock HDF5 support:

The Advanced setup page has additional tips and tricks for special situations (servers, notebooks, CUDA, installing the development version, etc). The Contributing guide has additional installation instructions for (future) contributors to MNE-Python (e.g, extra dependencies for running our tests and building our documentation).

IDE integration (VSCode, Spyder, etc.)

---

## mne.setup_source_space#

**URL:** https://mne.tools/stable/generated/mne.setup_source_space.html

**Contents:**
- mne.setup_source_space#
- Examples using mne.setup_source_space#

Set up bilateral hemisphere surface-based source space with subsampling.

The FreeSurfer subject name.

The spacing to use. Can be 'ico#' for a recursively subdivided icosahedron, 'oct#' for a recursively subdivided octahedron, 'all' for all points, or an integer to use approximate distance-based spacing (in mm).

Changed in version 0.18: Support for integers for distance-based spacing.

The path to the directory containing the FreeSurfer subjects reconstructions. If None, defaults to the SUBJECTS_DIR environment variable.

Add distance and patch information to the source space. This takes some time so precomputing it is recommended. Can also be ‘patch’ to only compute patch information.

Changed in version 0.20: Support for add_dist='patch'.

The number of jobs to run in parallel. If -1, it is set to the number of CPU cores. Requires the joblib package. None (default) is a marker for ‘unset’ that will be interpreted as n_jobs=1 (sequential execution) unless the call is performed under a joblib.parallel_config context manager that sets another value for n_jobs. Ignored if add_dist=='patch'.

Control verbosity of the logging output. If None, use the default verbosity level. See the logging documentation and mne.verbose() for details. Should only be passed as a keyword argument.

The source space for each hemisphere.

Generate a left cerebellum volume source space

Compute MNE inverse solution on evoked data with a mixed source space

Compute source power spectral density (PSD) of VectorView and OPM data

FreeSurfer MRI reconstruction

Head model and forward computation

The role of dipole orientations in distributed source localization

Working with CTF data: the Brainstorm auditory dataset

mne.setup_volume_source_space

---

## mne.setup_volume_source_space#

**URL:** https://mne.tools/stable/generated/mne.setup_volume_source_space.html

**Contents:**
- mne.setup_volume_source_space#
- Examples using mne.setup_volume_source_space#

Set up a volume source space with grid spacing or discrete source space.

Subject to process. If None, the path to the MRI volume must be absolute to get a volume source space. If a subject name is provided the T1.mgz file will be found automatically. Defaults to None.

Positions to use for sources. If float, a grid will be constructed with the spacing given by pos in mm, generating a volume source space. If dict, pos['rr'] and pos['nn'] will be used as the source space locations (in meters) and normals, respectively, creating a discrete source space.

For a discrete source space (pos is a dict), mri must be None.

The filename of an MRI volume (mgh or mgz) to create the interpolation matrix over. Source estimates obtained in the volume source space can then be morphed onto the MRI volume using this interpolator. If pos is a dict, this cannot be None. If subject name is provided, pos is a float or volume_label are not provided then the mri parameter will default to 'T1.mgz' or aseg.mgz, respectively, else it will stay None.

Define spherical source space bounds using origin and radius given by (Ox, Oy, Oz, rad) in sphere_units. Only used if bem and surface are both None. Can also be a spherical ConductorModel, which will use the origin and radius. None (the default) uses a head-digitization fit.

Define source space bounds using a BEM file (specifically the inner skull surface) or a ConductorModel for a 1-layer of 3-layers BEM. See make_bem_model() and make_bem_solution() to create a ConductorModel. If provided, surface must be None.

Define source space bounds using a FreeSurfer surface file. Can also be a dictionary with entries 'rr' and 'tris', such as those returned by mne.read_surface(). If provided, bem must be None.

Exclude points closer than this distance (mm) to the bounding surface.

Exclude points closer than this distance (mm) from the center of mass of the bounding surface.

The path to the directory containing the FreeSurfer subjects reconstructions. If None, defaults to the SUBJECTS_DIR environment variable.

Region(s) of interest to use. None (default) will create a single whole-brain source space. Otherwise, a separate source space will be created for each entry in the list or dict (str will be turned into a single-element list). If list of str, standard Freesurfer labels are assumed. If dict, should be a mapping of region names to atlas id numbers, allowing the use of other atlases.

Changed in version 0.21.0: Support for dict added.

If True and mri is not None, then an interpolation matrix will be produced.

If True, multiple values of volume_label will be merged into a a single source space instead of occupying multiple source spaces (one for each sub-volume), i.e., len(src) will be 1 instead of len(volume_label). This can help conserve memory and disk space when many labels are used.

The number of jobs to run in parallel. If -1, it is set to the number of CPU cores. Requires the joblib package. None (default) is a marker for ‘unset’ that will be interpreted as n_jobs=1 (sequential execution) unless the call is performed under a joblib.parallel_config context manager that sets another value for n_jobs.

Control verbosity of the logging output. If None, use the default verbosity level. See the logging documentation and mne.verbose() for details. Should only be passed as a keyword argument.

A SourceSpaces object containing one source space for each entry of volume_labels, or a single source space if volume_labels was not specified.

Volume source spaces are related to an MRI image such as T1 and allow to visualize source estimates overlaid on MRIs and to morph estimates to a template brain for group analysis. Discrete source spaces don’t allow this. If you provide a subject name the T1 MRI will be used by default.

When you work with a source space formed from a grid you need to specify the domain in which the grid will be defined. There are three ways of specifying this: (i) sphere, (ii) bem model, and (iii) surface. The default behavior is to use sphere model (sphere=(0.0, 0.0, 0.0, 90.0)) if bem or surface is not None then sphere is ignored. If you’re going to use a BEM conductor model for forward model it is recommended to pass it here.

To create a discrete source space, pos must be a dict, mri must be None, and volume_label must be None. To create a whole brain volume source space, pos must be a float and ‘mri’ must be provided.

To create a volume source space from label, pos must be a float, volume_label must be provided, and ‘mri’ must refer to a .mgh or .mgz file with values corresponding to the freesurfer lookup-table (typically aseg.mgz).

Generate a left cerebellum volume source space

Compute MNE inverse solution on evoked data with a mixed source space

Plot point-spread functions (PSFs) for a volume

Source alignment and coordinate frames

Head model and forward computation

Setting the EEG reference

mne.setup_source_space

mne.surface.complete_surface_info

---

## MNE-Python installers#

**URL:** https://mne.tools/stable/install/installers.html

**Contents:**
- MNE-Python installers#
- Platform-specific installers#
- First steps#
- Uninstallation#

MNE-Python installers are the easiest way to install MNE-Python and all dependencies. They also provide many additional Python packages and tools. Got any questions? Let us know on the MNE Forum!

Supported platforms: Ubuntu 18.04 (Bionic Beaver) and newer

Run the installer in a terminal via:

Download for macOS (Intel)

Supported platforms: macOS 10.15 (Catalina) and newer

Download for macOS (Apple Silicon)

Supported platforms: macOS 10.15 (Catalina) and newer

Supported platforms: Windows 10 and newer

Once installation completes, set up your IDE!

The installer adds menu entries on Linux and Windows, and several application bundles to the Applications folder on macOS.

Set up Visual Studio Code or another IDE (instructions here) to start writing your own analysis scripts right away, or to run one of our examples from this website.

With System Info, list the versions of all installed MNE-Python-related packages.

The Prompt drops you into a command line interface with a properly activated MNE-Python environment.

Depending on your system, it may take a little while for these applications to start, especially on the very first run – which may take particularly long on Apple Silicon-based computers. Subsequent runs should usually be much faster.

To remove the MNE-Python distribution provided by our installers above:

Remove relevant lines from your shell initialization scripts if you added them at installation time. To do this, you can run from the MNE Prompt:

Or you can manually edit shell initialization scripts, e.g., ~/.bashrc or ~/.bash_profile.

Follow the instructions below to remove the MNE-Python conda installation for your platform:

In a BASH terminal you can do:

You can simply drag the MNE-Python folder to the trash in the Finder.

Alternatively, you can do something like:

To uninstall MNE-Python, you can remove the application using the Windows Control Panel.

Installing MNE-Python

IDE integration (VSCode, Spyder, etc.)

---

## Overview of the MNE tools suite#

**URL:** https://mne.tools/stable/install/mne_tools_suite.html

**Contents:**
- Overview of the MNE tools suite#
- Related software#
- What should I install?#
- Getting help#

MNE-Python is an open-source Python module for processing, analysis, and visualization of functional neuroimaging data (EEG, MEG, sEEG, ECoG, and fNIRS). There are several related or interoperable software packages that you may also want to install, depending on your analysis needs.

MNE-C was the initial stage of this project, providing a set of interrelated command-line and GUI programs focused on computing cortically constrained Minimum Norm Estimates from MEG and EEG data. These tools were written in C by Matti Hämäläinen, and are documented here. See Installing MNE-C for installation instructions.

MNE-Python reimplements the functionality of MNE-C, extends considerably the analysis and visualization capabilities, and adds support for additional data types like functional near-infrared spectroscopy (fNIRS). MNE-Python is collaboratively developed and has more than 200 contributors.

MNE-MATLAB provides a MATLAB interface to the .fif file format and other MNE data structures, and provides example MATLAB implementations of some of the core analysis functionality of MNE-C. It is distributed alongside MNE-C, and can also be downloaded from the MNE-MATLAB GitHub repository.

MNE-CPP provides core MNE functionality implemented in C++ and is primarily intended for embedded and real-time applications.

There is also a growing ecosystem of other Python packages that work alongside MNE-Python, including:

If you know of a package that is related but not listed here, feel free to to add it to this list by making a pull request to update doc/sphinxext/related_software.py.

alphacsc: Convolutional dictionary learning for noisy signals.

antio: Python package to handle I/O with the CNT format from ANT Neuro.

autoreject: Automated rejection and repair of epochs in M/EEG.

best-python: The goal of this project is to provide a way to use the best-brainstorm Matlab solvers in Python, compatible with MNE-Python.

bycycle: Cycle-by-cycle analyses of neural oscillations.

conpy: Functions and classes for performing connectivity analysis on MEG data.

cross-domain-saliency-maps: Pytorch/Tensorflow package for generating saliency maps for time-series models using Cross-Domain Integrated Gradients.

curryreader: File reader for Compumedics Neuroscan data formats (.cdt, .dat).

dcm2niix: DCM2NIIX Python package

dipy: Diffusion MRI Imaging in Python

edfio: Read and write EDF/EDF+C/BDF/BDF+C files.

eeg_positions: Compute and plot standard EEG electrode positions.

eeglabio: I/O support for EEGLAB files in Python

eelbrain: Open-source Python toolkit for MEG and EEG data analysis.

emd: Empirical Mode Decomposition

fooof: fitting oscillations & one-over f

fsleyes: FSLeyes, the FSL image viewer

meegkit: M/EEG denoising in Python

meggie: User-friendly graphical user interface to do M/EEG analysis

mffpy: Reader and Writer for Philips’ MFF file format.

mne-ari: All-Resolutions Inference for M/EEG

mne-bids: MNE-BIDS: Organizing MEG, EEG, and iEEG data according to the BIDS specification and facilitating their analysis with MNE-Python

mne-bids-pipeline: A full-flegded processing pipeline for your MEG and EEG data

mne-connectivity: mne-connectivity: A module for connectivity data analysis with MNE.

mne-faster: MNE-FASTER: automatic bad channel/epoch/component detection

mne-features: MNE-Features software for extracting features from multivariate time series

mne-gui-addons: MNE-Python GUI addons.

mne-hcp: We provide Python tools for seamless integration of MEG data from the Human Connectome Project into the Python ecosystem

mne-icalabel: MNE-ICALabel: Automatic labeling of ICA components from MEG, EEG and iEEG data with MNE.

mne-kit-gui: A module for KIT MEG coregistration.

mne-lsl: Real-time framework integrated with MNE-Python for online neuroscience research through LSL-compatible devices.

mne-microstates: Code for microstate analysis, in combination with MNE-Python.

mne-nirs: An MNE compatible package for processing near-infrared spectroscopy data

mne-qt-browser: PyQtGraph-based backend for MNE-Python’s raw data browser

mne-rsa: Code for performing Representational Similarity Analysis on MNE-Python data structures.

mnelab: A graphical user interface for MNE

neurodsp: Digital signal processing for neural time series.

neurokit2: The Python Toolbox for Neurophysiological Signal Processing.

nilearn: Statistical learning for neuroimaging in Python

niseq: Group sequential tests for neuroimaging

nitime: Nitime: timeseries analysis for neuroscience data

openmeeg: Forward problems solver in the field of EEG and MEG.

openneuro-py: A Python client for OpenNeuro.

pactools: Estimation of phase-amplitude coupling (PAC) in neural time series, including with driven auto-regressive (DAR) models.

posthoc: post-hoc modification of linear models

pybv: pybv - a lightweight I/O utility for the BrainVision data format

pycrostates: A simple open source Python package for EEG microstate segmentation.

pyprep: PyPREP: A Python implementation of the preprocessing pipeline (PREP) for EEG data.

pyriemann: Machine learning for multivariate data with Riemannian geometry

neo: Neo is a package for representing electrophysiology data in Python, together with support for reading a wide range of neurophysiology file formats

python-picard: Preconditoned ICA for Real Data

sesameeg: Sequential Monte Carlo algorithm for multi dipolar source modeling in MEEG.

sleepecg: A package for sleep stage classification using ECG data

snirf: Interface and validator for SNIRF files

tensorpac: Tensor-based Phase-Amplitude Coupling

wfdb: The WFDB Python package: tools for reading, writing, and processing physiologic signals and annotations.

yasa: YASA: Analysis of polysomnography recordings.

If you intend only to perform ERP, ERF, or other sensor-level analyses, MNE-Python is all you need. If you prefer to work with shell scripts and the Unix command line, or prefer MATLAB over Python, probably all you need is MNE-C — the MNE MATLAB toolbox is distributed with it — although note that the C tools and the MATLAB toolbox are less actively developed than the MNE-Python module, and hence are considerably less feature-complete.

If you want to transform sensor recordings into estimates of localized brain activity, you will need MNE-Python, plus FreeSurfer to convert structural MRI scans into models of the scalp, inner/outer skull, and cortical surfaces (specifically, for command-line functions mne flash_bem, mne watershed_bem, and mne make_scalp_surfaces).

Help with installation is available through the MNE Forum. See the Getting help page for more information.

Installing FreeSurfer

Documentation overview

---

## Testing your installation#

**URL:** https://mne.tools/stable/install/check_installation.html

**Contents:**
- Testing your installation#

To make sure MNE-Python was installed correctly, type the following command in a terminal:

If you installed MNE-Python using one of our installers, enter the above command in the Prompt.

This should display some system information along with the versions of MNE-Python and its dependencies. Typical output looks like this:

If you see an error like:

This suggests that your environment containing MNE-Python is not active. If you followed the setup for 3D plotting/source analysis (i.e., you installed to a new mne environment instead of the base environment) try running conda activate mne first, and try again. If this works, you might want to set your terminal to automatically activate the mne environment each time you open a terminal:

If something else went wrong during installation and you can’t figure it out, check out the Advanced setup instructions to see if your problem is discussed there. If not, the MNE Forum is a good resources for troubleshooting installation problems.

---

## Updating MNE-Python#

**URL:** https://mne.tools/stable/install/updating.html

**Contents:**
- Updating MNE-Python#
- Upgrading MNE-Python only#
- Upgrading all packages#
- Upgrading to the development version#

If you want to update MNE-Python to a newer version, there are a few different options, depending on how you originally installed it.

To update via the MNE-Python installers, simply download and run the latest installer for your platform. MNE-Python will be installed in parallel to your existing installation, which you may uninstall or delete if you don’t need it anymore.

If you’re not using the MNE-Python installers, keep reading.

If you wish to update MNE-Python only and leave other packages in their current state, you can usually safely do this with pip, even if you originally installed via conda. With the mne environment active (conda activate name_of_environment), do:

Generally speaking, if you want to upgrade your whole software stack including all the dependencies, the best approach is to re-create it as a new virtual environment, because neither conda nor pip are fool-proof at making sure all packages remain compatible with one another during upgrades.

Here we’ll demonstrate renaming the old environment first, as a safety measure. We’ll assume that the existing environment is called mne and you want to rename the old one so that the new, upgraded environment can be called mne instead.

Before running the below command, ensure that your existing MNE conda environment is not activated. Run conda deactivate if in doubt.

Then, just follow our regular installation instructions, Install via pip or conda.

If you installed extra packages into your old mne environment, you’ll need to repeat that process after re-creating the updated environment. Comparing the output of conda list --name old_mne versus conda list --name mne will show you what is missing from the new environment. On Linux, you can automate that comparison like this:

In between releases, function and class APIs can change without warning.

Sometimes, new features or bugfixes become available that are important to your research and you just can’t wait for the next official release of MNE-Python to start taking advantage of them. In such cases, you can use pip to install the development version of MNE-Python. Ensure to activate the MNE conda environment first by running conda activate mne.

Testing your installation

Installing FreeSurfer

---
