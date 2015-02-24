#NMSSM-Scan

Files to do parameter scans using [NMSSMTools](http://www.th.u-psud.fr/NMHDECAY/nmssmtools.html). Based on Daniele Barducci's code.

##Setup & Running

###NMSSMTools
- Download latest version from website: http://www.th.u-psud.fr/NMHDECAY/nmssmtools.html
- Extract with `tar -xvzf NMSSMTools_x.y.z.tgz`
- Clone `NMSSM-Scan` into `NMSSMTools_x.y.z` folder (or clone it somewhere else and sym-link it incase you want to update in future):
```
git clone git@github.com:raggleton/NMSSM-Scan.git
```
- Compile NMSMTools (can take a little while):
```shell
make init
make
```
- Look at `README` in NMSSMTools folder
- Also look at [README_Daniele](README_Daniele)

###Running batch jobs (on HTCondor)
- We will run NMSSMTools lot of times, for single points in parameter space. To do this, each paramter point requires a separate input file, to specify all the value sof the paramters at that point.
    - Don't use the grip scan options for now... more info in `spectr_*.dat` files than from grid output
- We will run this on the HTCondor batch system at Bristol. To run batch jobs on HTCondor, we need to export NMSSMTools to worker node because it's not installed centrally. Tar up the compiled NMSSMTools (worker node uses same architecture as submission node):
```shell
cd NMSSMTools_*
tar -cvzf NMSSMTOOLS.tgz --exclude="NMSSM-Scan" --exclude="*DS_Store" --exclude="*.tgz" --exclude="SAMPLES" .
cp NMSSMTOOLS.tgz <wherever you cloned NMSSM-Scan >
```
- Running batch jobs requires 2 files: a job file, and a script file.
    - **job file**: gives instructions to HTcondor about input/output files, how much RAM/cpus to use, etc. This is [Proto_files/runScan.condor](Proto_files/runScan.condor)
    - **setup script file**: setup NMSSMTools and run the input file(s) on the worker node. This is [Proto_files/setupRun.sh](Proto_files/setupRun.sh).
- Since making and copying the input files for NMSSMTools is time consuming and results in lots of large files, it's easier to make them on the worker node as part of the batch system.
- So if you want to run over a set of parameter points, do the following:
    1. Edit [NMSSM_scan.pl](NMSSM_scan.pl). This is the script that generates input files (using [Proto_files/inp_PROTO.dat](Proto_files/inp_PROTO.dat) as a template) for paramter space points, and runs NMSSMTools on them. Edit the boundaries for parameters, and the number of points to run over (for 1 job). Can also choose to have dependant parameters, e.g. set kappa based on mu and lambda.
    2. Edit [runScan.sh](runScan.sh). Set the number of jobs you want to run in parallel, and optionally a description for this set of jobs.
    3. Edit [Proto_files/runScan.condor](Proto_files/runScan.condor), changing the paths of `NMSSMTOOLS.tgz`, `NMSSM_scan.pl`, `setupRun.sh` and `inp_PROTO.dat`
    4. Can now submit jobs by doing `./runScan.sh`. This will create a directory, `jobs_<DESCRIPTION>_<date>_<month>_<year>_<hour><min>`, where all your spectrum files will be placed, along with a copy of your input parameter scan range, and the log files from HTCondor (in subdirectory `logFiles`).
- Check status of your jobs with
```
condor_queue `whoami`
```

###Analysis of spectrum files
- First untar all the spectrum tarballs (**warning**, output will be large!):
```
cd <dir>
for f in *.tgz; do tar -xvzf $f; done
```
- To analyse the output `spectr_*.dat` files, we first run over them and find all parameter points that pass experimental constraints, then pull the relevant masses/BRs/couplings, etc. and put them into a file. This is done by [Analyse_scans.pl](Analyse_scans.pl), which you can run with:
```
perl Analyse_scans.pl <dir with spectr_* files>
```
- If you want to do this to several folders simultaneously, there's a script [analyse.sh](analyse.sh) to do so:
```
./analyse.sh <dir 1> <dir 2> ...
```
- The `Analyse_scans.pl` will create a CSV file with space-delimited values of interesting masses, BRs, parameters, etc, for all parameter points passing experimental constraints. To see what constraints we check against, see the function `passExpCheck` in [Analyse_scans.pl](Analyse_scans.pl). These are pulled from `nmhdecay.f`.
- This output file is created in the job directory with all the `spectr_*` files, and copied to the directory `NMSSM-Scan/output`. This directory will be created if it doesn't already exist. Note that the output files will have unique names, based on the folder they were run on.

###Plotting
- At the moment, plotting and tinkering is done via iPython + pandas + matplotlib + numpy. Make sure these are installed first using `pip`. You may also need to install `texlive-latex-extra` via MacPorts (or similar in TexLive utility?) for latex fonts.
- This may change in future to ROOT (bluergh), but for now it's a handy way to play around with settings, without having to re-run everything necessarily. See the [iPython](iPython) folder for some iPython scripts.
- Easiest to copy the output*.dat files locally, then run iPython on them.

## Notes:

- NMSSMTools contains NMHDECAY, NMSPEC, NMGMSB and NMSDECAY. From the website:

__NMHDECAY__:

> computes the masses, couplings and decay widths of all Higgs bosons of the NMSSM, and the masses of all sparticles, in terms of its parameters at the electroweak (or susy breaking) scale: the Yukawa couplings lambda and kappa, the soft trilinear terms A_lambda and A_kappa, and tan(beta) and mu_eff = lambda*S. (Instead of A_lambda, the MSSM-like parameter M_A can also be used as input.) The computation of the Higgs spectrum includes leading electroweak corrections, two loop terms and propagator corrections. The computation of the decay widths is carried out as in HDECAY, but momentarily without three body decays. Each point in parameter space is checked against negative Higgs boson searches at LEP, and negative sparticle searches at LEP and the Tevatron, including unconventional channels relevant for the NMSSM. B physics constraints from b -> s gamma, Delta M_q, B -> mu+mu- and B+ -> tau+ nu_tau are included as in ref. [4] below. The dark matter relic density can be computed via a link to a NMSSM version of the MicrOMEGAs code [3]. SLHA conventions for input and output are used.

__NMSPEC__

> compute the sparticle and Higgs masses, Higgs decay widths and couplings in the NMSSM, with soft Susy breaking terms specified at the GUT scale. Exceptions are the soft singlet mass and kappa, that are both determined in terms of the other parameters through the minimization equations of the Higgs potential. The soft Higgs and gaugino masses at the GUT scale can be chosen as non-universal, if desired.

__NMGMSB__:

> compute the sparticle and Higgs masses, Higgs decay widths and couplings in the NMSSM, where soft Susy breaking terms are specified at by gauge mediated supersymmetry breaking, plus terms originating from couplings of the Singlet to messengers. The boundary conditions at the messenger scale are taken from the paper below, and described in the file README. Either the soft Singlet mass or a Susy tadpole term XIS are determined in terms of the other parameters through the minimization equations of the Higgs potential. Sample input- and output files are included.

__NMSDECAY__

> compute sparticle widths and branching ratios (not yet for NMGMSB). It is based on a generalization of SDECAY, including the corresponding QCD corrections and 3-body decay modes. Slepton 3-body decays, possibly relevant in case of a singlino-like LSP, have been added.
