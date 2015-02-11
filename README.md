#NMSSM-Scan

Files to do parameter scans using [NMSSMTools](http://www.th.u-psud.fr/NMHDECAY/nmssmtools.html). Based on Daniele Barducci's code (see [README_Daniele](README_Daniele) for instructions).

##Setup

###NMSSMTools
- Download latest version from website: http://www.th.u-psud.fr/NMHDECAY/nmssmtools.html
- Extract with `tar -xvzf NMSSMTools_x.y.z.tgz`
- Clone `NMSSM-Scan` into `NMSSMTools_x.y.z` folder (or clone it somewhere else and sym-link it incase you want to update in future):
```
git clone git@github.com:raggleton/NMSSM-Scan.git
```
- Compile:
```shell
make init
make
```
- Look at `README` in NMSSMTools folder
- Also look at [README_Daniele](README_Daniele)

###Running batch jobs (on HTCondor)
- We will run NMSSMTools lot of times, for single points in parameter space
    - Don't use the grip scan options for now... more info in `spectr_*.dat` files than from grid output
- To run batch jobs on HTCondor, we need to export NMSSMTools to worker node. Tar up the compiled NMSSMTools (worker node uses same architecture as submission node):
```shell
cd NMSSMTools_*
tar -cvzf NMSSMTOOLS.tgz --exclude="NMSSM-Scan" --exclude="*DS_Store" --exclude="*.tgz" --exclude="SAMPLES" .
cp NMSSMTOOLS.tgz NMSSM-Scan/
```
- Edit the `transfer_input_files` line in [Proto_files/runScan.condor](Proto_files/runScan.condor) to the path of your tgz (don't delete the `SED_INPUT`)
- Running batch jobs requires 2 files: a job file, and a script file.
    - **job file**: gives instructions to HTcondor about input/output files, how much RAM/cpus to use, etc
    - **setup script file**: setup NMSSMTools and run the input file(s) on the worker node
- [NMSSM_scan.pl](NMSSM_scan.pl) will setup input files for NMSSMTools to use, as well as the job and script files
    + it will output everything needed in a new directory, `job_<description>_<date>_<time>`
    + this will contain all the `inp_*.dat` files, a job file (`runScan.condor`) and a setup script file (`setupRun.sh`).
- Run with `perl NMSSM_scan.pl`
- Submit jobs with `condor_submit <job dir>/runScan.condor`

###Analysis
- To analyse the output `spectr_*.dat` files, we first run over them and find all parameter points that pass experimental constraints, then pull the relevant masses/BRs/couplings, etc. This is done by [Analyse_scans.pl](Analyse_scans.pl):
```
perl Analyse_scans.pl <dir with spectr_* files>
```
- TODO: plotting

## Notes:

- NMSSMTools contains NMHDECAY, NMSPEC, NMGMSB and NMSDECAY. From the webiste:

__NMHDECAY__:

> computes the masses, couplings and decay widths of all Higgs bosons of the NMSSM, and the masses of all sparticles, in terms of its parameters at the electroweak (or susy breaking) scale: the Yukawa couplings lambda and kappa, the soft trilinear terms A_lambda and A_kappa, and tan(beta) and mu_eff = lambda*S. (Instead of A_lambda, the MSSM-like parameter M_A can also be used as input.) The computation of the Higgs spectrum includes leading electroweak corrections, two loop terms and propagator corrections. The computation of the decay widths is carried out as in HDECAY, but momentarily without three body decays. Each point in parameter space is checked against negative Higgs boson searches at LEP, and negative sparticle searches at LEP and the Tevatron, including unconventional channels relevant for the NMSSM. B physics constraints from b -> s gamma, Delta M_q, B -> mu+mu- and B+ -> tau+ nu_tau are included as in ref. [4] below. The dark matter relic density can be computed via a link to a NMSSM version of the MicrOMEGAs code [3]. SLHA conventions for input and output are used.

__NMSPEC__

> compute the sparticle and Higgs masses, Higgs decay widths and couplings in the NMSSM, with soft Susy breaking terms specified at the GUT scale. Exceptions are the soft singlet mass and kappa, that are both determined in terms of the other parameters through the minimization equations of the Higgs potential. The soft Higgs and gaugino masses at the GUT scale can be chosen as non-universal, if desired.

__NMGMSB__:

> compute the sparticle and Higgs masses, Higgs decay widths and couplings in the NMSSM, where soft Susy breaking terms are specified at by gauge mediated supersymmetry breaking, plus terms originating from couplings of the Singlet to messengers. The boundary conditions at the messenger scale are taken from the paper below, and described in the file README. Either the soft Singlet mass or a Susy tadpole term XIS are determined in terms of the other parameters through the minimization equations of the Higgs potential. Sample input- and output files are included.

__NMSDECAY__

> compute sparticle widths and branching ratios (not yet for NMGMSB). It is based on a generalization of SDECAY, including the corresponding QCD corrections and 3-body decay modes. Slepton 3-body decays, possibly relevant in case of a singlino-like LSP, have been added.
