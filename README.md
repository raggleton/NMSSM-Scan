#NMSSM-Scan

Files to do parameter scans using [NMSSMTools](http://www.th.u-psud.fr/NMHDECAY/nmssmtools.html).
Originally based on Daniele Barducci's code.

**Full instructions on the wiki:** [NMSSM-Scan Wiki](https://github.com/raggleton/NMSSM-Scan/wiki)

There are 4 parts to running this code:

1) parameter point generation

2) converting spectrum files (SLHA) into CSV

3) converting CSV into HDF5 binary files

4) use the HDF5 binaries to make lots of interesting plots

Steps 1, 2, and 3 are done on HTCondor (but can also be done locally if desired).
Step 4 is done locally (although watch this space for doing it on Soolin Mk2...).

Plotting is done using the `pandas` (which can read HDF5 files) + `matplotlib` packages, in jupyter workbooks.
