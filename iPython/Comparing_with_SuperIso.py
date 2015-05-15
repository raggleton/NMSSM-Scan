
# coding: utf-8

# In this workbook, we compare flavour observables calculated using NMSSMTools v4.5.1 with those calculated using SuperIso v3.4. Unfortunately, NMSSMTools only calculates a handful of flavour physics results. 2 $\sigma$ valid ranges as applied in NMSSMTools are listed in brackets:
# 
# - $BR(b \to s \gamma)$ - $[2.99, 3.87]\times 10^{-4}$
# 
# - $BR(B_s \to \mu\mu)$ - $[1.2, 5.2]\times 10^{-9}$ - **NEW MAY 2015 LIMIT** $[1.6, 4.2]\times 10^{-9}$
# 
# - $BR(B^+ \to \tau^+ \nu_{\tau})$ - $[0.70, 1.58]\times 10^{-4}$
# 
# - $\Delta M_d$ - $[5.04, 5.16]\times 10^{-1}\ \mathrm{ps}^{-1}$ - **_Not calculated by SuperIso_**
# 
# - $\Delta M_s$ - $[1.7717, 1.7805]\times 10^{1}\ \mathrm{ps}^{-1}$ - **_Not calculated by SuperIso_**
# 
# whereas SuperIso calculates a much larger range of observables. Thus, we will only compare those 3 common observables listed above. One could also add in additional experimental constraints based on the extra observables SuperIso calculates, this is on the TODO list, although will takes some time to find references for all the experimental measurements.
# 
# 
# For the plots below, the following parameter space was scanned:
# 
# - $500 < M3 < 2000 $ GeV 
# 
# - $500 < MU3, MQ3 < 2500$ GeV
# 
# - $500 < AU3 < 3000$ GeV
# 
# - $M1$ = 150 GeV, $M2$ = 300 GeV
# 
# - $MD3$ = 1 TeV
# 
# - $AD3$ = 2.5 TeV
# 
# - $\tan \beta \in [1.5, 50]$
# 
# - $\mu_{eff} \in [100, 300]\ \mathrm{GeV}$
# 
# - $\kappa,\lambda \in [0, 0.7]$
# 
# - $A_{\kappa} \in [-30, 2.5]\ \mathrm{GeV}$
# 
# - $A_{\lambda} \in [-1000, 4000]\ \mathrm{GeV}$
# 
# Note also that:
# 
# - All constraints checked against except the LHC ones, and in addition we require 1) $\Delta a_{\mu} > 0$ and 2) $\Omega h^2 < 0.131$
# 
# - Plots that are labelled 'without experimental constraints' have points that are only required to pass: 
#     - $m_h^2 > 1$
#     - $m_a^2 >1$
#     - $m_{H^\pm}^2 >1$
#     - $m_{a_1} < 100\ \mathrm{GeV}$
#     
# 
# On a practical note, some notes about running with SuperIso:
# 
# - Easy to compile and run, pass the SLHA `spectr*.dat` output file from NMSSMTools to the SuperIso SLHA program:
# 
# ```
# make slha
# ./slha.x spectr1.dat
# ```
# 
# - SuperIso outputs a SLHA file and also outputs info to STDOUT. Unfortunately you can't set the SLHA filename, and doesn't include the relic density as calculated by SuperIso.
# 
# - Since SuperIso requires the outptu SLHA from NMSSMTools, it is not possible to run SUperIso and NMSSMTools in parallel. This can slow generation & analysis significantly. e.g it takes approx. 45 min to generate 10K poitns with NMSSMTools, and just over 1 hour to run over them with SuperIso, thereby doubling total time.

# In[1]:

import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from itertools import izip

# to show plots:
get_ipython().magic(u'pylab inline')

get_ipython().magic(u'load_ext autoreload')
get_ipython().magic(u'autoreload 2')

mpl.rcParams['figure.figsize'] = (7.0, 4.0)  # default size of plots
mpl.rcParams['axes.labelsize'] = 30
mpl.rcParams['xtick.labelsize'] = 20
mpl.rcParams['ytick.labelsize'] = 20
mpl.rcParams['xtick.major.size'] = 10
mpl.rcParams['ytick.major.size'] = 10
mpl.rcParams['xtick.minor.size'] = 5
mpl.rcParams['ytick.minor.size'] = 5
mpl.rcParams.update({'font.size': 24, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})


# In[265]:

from common_plots import *


# In[6]:

# Unpack dataframes from hdf5 binaries
# I4 = 1 dataset, scanning over M3,MU3,MQ3,AU3 
store_M3MU3MQ3AU3_scan = pd.HDFStore("points_I41_scan_M3MQ3MU3AU3.h5")
# store_M3MU3MQ3AU3_scan
df_M3MU3MQ3AU3_orig = store_M3MU3MQ3AU3_scan.full12loop_all
df_M3MU3MQ3AU3_pass_all = store_M3MU3MQ3AU3_scan.full12loop_good_posMuMagMom_planckUpperOnly
# df_M3MU3MQ3AU3_ma1Lt10 = store_M3MU3MQ3AU3_scan.full12loop_good_posMuMagMom_planckUpperOnly_maLt10
df_M3MU3MQ3AU3_h1SM = store_M3MU3MQ3AU3_scan.full12loop_good_posMuMagMom_planckUpperOnly_h1SM
# df_M3MU3MQ3AU3_h2SM = store_M3MU3MQ3AU3_scan.full12loop_good_posMuMagMom_planckUpperOnly_h2SM
store_M3MU3MQ3AU3_scan.close()


# In[80]:

print 'Without exp. constraints:', len(df_M3MU3MQ3AU3_orig.index), ', with exp. constraints:', len(df_M3MU3MQ3AU3_pass_all.index)


# #$BR(b\to s\gamma)$

# In[184]:

# central experimental value +- 2 sigma
bsgamma_lim = [2.99E-4, 3.87E-4]


# Summary of the BRs, comparing NMSSMTools (`bsgamma`) and SuperIso (`bsgamma_si`) without experimental constraints:

# In[79]:

df_M3MU3MQ3AU3_orig.loc[:, ['bsgamma', 'bsgamma_si']].describe()


# First we plot the distributions of each value:

# In[266]:

fig = plt.figure()
fig.set_size_inches(14,6)
title = r"Without exp. constraints"
xlabel = r"$BR(b\to s \gamma)$"
bins = 25
br_range = [3E-4, 6.5E-4]

# Lin y axis
ax1 = fig.add_subplot(1,2,1)
y11, bins11, patches11 = plot_histogram(ax1, 'bsgamma', df_M3MU3MQ3AU3_orig, "NMSSMTools", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='red', range=br_range, bins=bins, histtype="step", linewidth=1.5)
y21, bins21, patches21 = plot_histogram(ax1, 'bsgamma_si', df_M3MU3MQ3AU3_orig, "SuperIso", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='green', range=br_range, bins=bins, histtype="step", linewidth=1.5)
ax1.add_patch(make_highlight_region(ax=ax1, limits=bsgamma_lim, axis='x', 
                               label=r"Exp. $\pm 2\sigma$", alpha=0.2, facecolor='grey'))
ax1.set_xlim(br_range)
ax1.legend(fontsize=20)
ax1.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# log y axis
ax2 = fig.add_subplot(1,2,2)
y12, bins12, patches12 = plot_histogram(ax2, 'bsgamma', df_M3MU3MQ3AU3_orig, "NMSSMTools", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='red', range=br_range, bins=bins, histtype="step", linewidth=1.5, log=True)
y22, bins22, patches22 = plot_histogram(ax2, 'bsgamma_si', df_M3MU3MQ3AU3_orig, "SuperIso", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='green', range=br_range, bins=bins, histtype="step", linewidth=1.5, log=True)
ax2.add_patch(make_highlight_region(ax=ax2, limits=bsgamma_lim, axis='x', 
                               label=r"Exp. $\pm 2\sigma$", alpha=0.2, facecolor='grey'))
ax2.set_xlim(br_range)
ax2.set_ylim(bottom=1E-4)
ax2.legend(fontsize=20)
ax2.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
fig.tight_layout()

# print df_M3MU3MQ3AU3_pass_all[df_M3MU3MQ3AU3_pass_all.constraints.str.contains(r"b \-> s")].constraints


# So we can see that in general NMSSMTools tends to provide slightly smaller values of BR than SuperIso. Therefore, on the whole, the difference is fairly small, i.e. $\langle {BR}_{\mathrm{NMSSMTools}}\rangle - \langle {BR}_{\mathrm{SuperIso}}\rangle \ll \langle {BR}_{NMSSMTools}\rangle$ (mean diff is about 3%)

# We can also look at the difference on a point-by-point basis, i.e. for each parameter point calculate BR using both NMSSMTools and SuperIso, and compare:

# In[135]:

# Make new series with diff between NMSSMTools and SuperIso without exp. con
bsgamma_without = df_M3MU3MQ3AU3_orig.bsgamma.copy(deep=True)
bsgamma_si_without = df_M3MU3MQ3AU3_orig.bsgamma_si
bsgamma_without = bsgamma_without.subtract(bsgamma_si_without)
bsgamma_without.describe()


# In[250]:

fig = plt.figure()
fig.set_size_inches(14,6)
title = r"$b \to s \gamma$ without exp. constraints"
br_range = [-4.8E-4, 0.2E-4]

bsgamma_val = bsgamma_without.values
weights = np.ones_like(bsgamma_val)/len(bsgamma_val)
y, bins, patches = plt.hist(bsgamma_val, weights=weights, bins=60, 
                            range=br_range, log=True, color='cornflowerblue', alpha=0.8)
plt.xlabel(r"${BR}_{NMSSMTools} - {BR}_{SuperIso}$")
plt.ylabel("p.d.f.")
plt.xlim(br_range)
plt.title(title)
plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
plt.minorticks_on()


# So we can see that even on a point-by-point basis NMSSMTools tends to provide slightly smaller values of BR than SuperIso. The mean difference, -1.1E-5, is about 3% of the NMSSMTools mean value (if one takes the median, then that difference is about 1.5% of the NMSSMTools median value). So the difference between NMSSMTools and SuperIso per point is fairly small, i.e. $\langle {BR}_{\mathrm{NMSSMTools}} - {BR}_{\mathrm{SuperIso}}\rangle \ll \langle {BR}_{NMSSMTools}\rangle$. (Aside: sometimes there are some _very_ large differences)

# One should note that NMSSMTools tends to assign a large theoretical uncertainty to the BR, $\delta_{theoretical}^{BR}$, such that even if the BR falls above the upper limit (3.87E-4), $BR-\delta_{theoretical}^{BR}$ can easily bring it below the upper limit. This can be seen when we plot the BR with and without the BR constraint (taking the BR from NMSSMTools and ignoring all other experimental constraints).

# In[257]:

fig = plt.figure()
fig.set_size_inches(14,6)
title = r"With & without BR exp. constraint"
xlabel = r"$BR(b\to s \gamma)$"
bins = 25
br_range = [3E-4, 6.5E-4]

# Subset of points that pass the b->sgamma constraint (ignoring all other constraints)
df_pass_bsgamma = df_M3MU3MQ3AU3_orig[~ df_M3MU3MQ3AU3_orig.constraints.str.contains(r"b \-> s gamma")]
# print df_pass_bsgamma.constraints

# Lin y axis
ax1 = fig.add_subplot(1,2,1)
y11, bins11, patches11 = plot_histogram(ax1, 'bsgamma', df_M3MU3MQ3AU3_orig, "Without BR exp. con.", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='red', range=br_range, bins=bins, histtype="step", linewidth=1.5)
y21, bins21, patches21 = plot_histogram(ax1, 'bsgamma', df_pass_bsgamma, "With BR exp. con.", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='purple', range=br_range, bins=bins, histtype="step", linewidth=1.5)
ax1.add_patch(make_highlight_region(ax=ax1, limits=bsgamma_lim, axis='x', 
                               label=r"Exp. $\pm 2\sigma$", alpha=0.2, facecolor='grey'))
ax1.set_xlim(br_range)
ax1.legend(fontsize=20)
ax1.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# log y axis
ax2 = fig.add_subplot(1,2,2)
y12, bins12, patches12 = plot_histogram(ax2, 'bsgamma', df_M3MU3MQ3AU3_orig, "Without BR exp. con.", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='red', range=br_range, bins=bins, histtype="step", linewidth=1.5, log=True)
y22, bins22, patches22 = plot_histogram(ax2, 'bsgamma', df_pass_bsgamma, "With BR exp. con.", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='purple', range=br_range, bins=bins, histtype="step", linewidth=1.5, log=True)
ax2.add_patch(make_highlight_region(ax=ax2, limits=bsgamma_lim, axis='x', 
                               label=r"Exp. $\pm 2\sigma$", alpha=0.2, facecolor='grey'))
ax2.set_xlim(br_range)
ax2.set_ylim(bottom=1E-4)
ax2.legend(fontsize=20)
ax2.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
fig.tight_layout()

# print df_M3MU3MQ3AU3_pass_all[df_M3MU3MQ3AU3_pass_all.constraints.str.contains(r"b \-> s")].constraints
print 'Max value of BR(b->s gamma) passing BR constraint:', max(df_pass_bsgamma.bsgamma)


# Thus, the theoretical uncertainty is as large as (5.776 - 3.87)E-4 = 1.9E-4 $\sim 50\%$ of the $BR+2\sigma$ constraint! 
# 
# 
# **Conclusion**: changing to the SuperIso value won't really affect the number of points passing the constraint, since:
# 
# 1) $\langle {BR}_{\mathrm{NMSSMTools}}\rangle - \langle{BR}_{\mathrm{SuperIso}}\rangle \ll \langle {BR}_{NMSSMTools}\rangle$
# 
# 2) $\langle {BR}_{\mathrm{NMSSMTools}} - {BR}_{\mathrm{SuperIso}}\rangle \ll \langle {BR}_{NMSSMTools}\rangle$
# 
# 
# 3) $\langle {BR}_{\mathrm{NMSSMTools}} - {BR}_{\mathrm{SuperIso}} \rangle \ll \delta_{theoretical}^{BR}$ 

# #$BR(B_s \to \mu \mu)$

# In[217]:

# central experimental value +- 2 sigma
bsmumu_lim = [1.2E-9, 5.2E-9]
bsmumu_lim_new = [1.6E-9, 4.2E-9] # may 2015 combined value http://www.nature.com/nature/journal/vaop/ncurrent/pdf/nature14474.pdf
# SM prediction, ±2 sigma bands
bsmumu_sm_central = 3.66E-9
bsmumu_sm_lim = [3.2E-9 ,4.12E-9]


# Summary of the BRs, comparing NMSSMTools (`bsmumu`) and SuperIso (`bsmumu_si`) without experimental constraints:

# In[141]:

df_M3MU3MQ3AU3_orig.loc[:, ['bsmumu', 'bsmumu_si']].describe()


# We should look at the median, rather than the mean here, since some **very** large values of BR completely distort the mean.

# First we plot the distributions of each value:

# In[273]:

fig = plt.figure()
fig.set_size_inches(14,6)
title = r"Without exp. constraints"
xlabel = r"$BR(B_s\to \mu\mu)$"
bins = 50
br_range = [0, 10E-9]

# Lin y axis
ax1 = fig.add_subplot(1,2,1)
y11, bins11, patches11 = plot_histogram(ax1, 'bsmumu', df_M3MU3MQ3AU3_orig, "NMSSMTools", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='red', range=br_range, bins=bins, histtype="step", linewidth=1.5)
y21, bins21, patches21 = plot_histogram(ax1, 'bsmumu_si', df_M3MU3MQ3AU3_orig, "SuperIso", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='green', range=br_range, bins=bins, histtype="step", linewidth=1.5)

ax1.add_patch(make_highlight_region(ax=ax1, limits=bsmumu_lim, axis='x', 
                               label=r"Exp. $\pm 2\sigma$", alpha=0.2, facecolor='grey'))
# new limit from 14/5!
ax1.add_patch(make_highlight_region(ax=ax1, limits=bsmumu_lim_new, axis='x', 
                               label=r"Exp. $\pm 2\sigma$ (new)", alpha=0.2, facecolor='cornflowerblue'))
# SM range
ax1.add_patch(make_highlight_region(ax=ax1, limits=bsmumu_sm_lim, axis='x', 
                               label=r"SM. $\pm 2\sigma$ (new)", alpha=0.3, facecolor='palegreen'))
ax1.set_xlim(br_range)
ax1.legend(fontsize=18)
ax1.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# log y axis
ax2 = fig.add_subplot(1,2,2)
y12, bins12, patches12 = plot_histogram(ax2, 'bsmumu', df_M3MU3MQ3AU3_orig, "NMSSMTools", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='red', range=br_range, bins=bins, histtype="step", linewidth=1.5, log=True)
y22, bins22, patches22 = plot_histogram(ax2, 'bsmumu_si', df_M3MU3MQ3AU3_orig, "SuperIso", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='green', range=br_range, bins=bins, histtype="step", linewidth=1.5, log=True)

ax2.add_patch(make_highlight_region(ax=ax2, limits=bsmumu_lim, axis='x', 
                               label=r"Exp. $\pm 2\sigma$", alpha=0.2, facecolor='grey'))
# new limit
ax2.add_patch(make_highlight_region(ax=ax2, limits=bsmumu_lim_new, axis='x', 
                               label=r"Exp. $\pm 2\sigma$ (new)", alpha=0.2, facecolor='cornflowerblue'))
# SM range
ax2.add_patch(make_highlight_region(ax=ax2, limits=bsmumu_sm_lim, axis='x', 
                               label=r"SM. $\pm 2\sigma$ (new)", alpha=0.3, facecolor='palegreen'))
ax2.set_xlim(br_range)
ax2.set_ylim(bottom=5E-5)
ax2.legend(fontsize=18)
ax2.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
fig.tight_layout()

# print df_M3MU3MQ3AU3_pass_all[df_M3MU3MQ3AU3_pass_all.constraints.str.contains(r"b \-> s")].constraints


# On the whole, NMSSMTools gives slightly larger values of the BR than SuperIso, with the NMSSMTools distribution skewed towards larger BR and the SuperIso distribution skewed towards smaller values, and the peaks in the same bin. The slight difference makes almost no difference when comparing against the experimental constraint. Interestingly, the most common scenario (*before* experimental constraints applied) is for a BR slightly lower than that predicted in the SM.

# Let's look at the distributions on a point-by-point basis like before:

# In[189]:

# Make new series with diff between NMSSMTools and SuperIso without exp. con
bsmumu_without = df_M3MU3MQ3AU3_orig.bsmumu.copy(deep=True)
bsmumu_si_without = df_M3MU3MQ3AU3_orig.bsmumu_si
bsmumu_without = bsmumu_without.subtract(bsmumu_si_without)
bsmumu_without.describe()


# In[243]:

fig = plt.figure()
fig.set_size_inches(14,6)

# lin y axis
ax2 = fig.add_subplot(1,2,1)
title = r"$B_s \to \mu\mu$ without exp. constraints"
br_range = [-2E-10, 4E-10]

bsmumu_val = bsmumu_without.values
weights = np.ones_like(bsmumu_val)/len(bsmumu_val)
y, bins, patches = ax2.hist(bsmumu_val, weights=weights, bins=30, 
                            range=br_range, log=False, color='cornflowerblue', alpha=0.8)
ax2.set_xlabel(r"${BR}_{NMSSMTools} - {BR}_{SuperIso}$")
ax2.set_ylabel("p.d.f.")
ax2.set_xlim(br_range)
ax2.set_title(title, y=1.02)
ax2.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
ax2.minorticks_on()
plt.tight_layout()

# log y axis
ax = fig.add_subplot(1,2,2)
title = r"$B_s \to \mu\mu$ without exp. constraints"
br_range = [-2E-5, 4E-5]

# bsmumu_val = bsmumu_without.values
# weights = np.ones_like(bsmumu_val)/len(bsmumu_val)
y, bins, patches = ax.hist(bsmumu_val, weights=weights, bins=30, 
                            range=br_range, log=True, color='cornflowerblue', alpha=0.8)
ax.set_xlabel(r"${BR}_{NMSSMTools} - {BR}_{SuperIso}$")
ax.set_ylabel("p.d.f.")
ax.set_xlim(br_range)
ax.set_title(title, y=1.02)
ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
ax.minorticks_on()
plt.tight_layout()


# Note the **very** different scales on the x axes - the plot on the left is essentially the largest 2 bins on the RH plot. 
# 
# **Conclusion**:
# 
# _WRITE SOMETHING HERE_

# #$B^+ \to \tau^+ \nu_{\tau}$ 

# In[252]:

# central experimental value +- 2 sigma
btaunu_lim = [0.7E-4, 1.58E-4]
# SM prediction, ±2 sigma bands
btaunu_sm_central = 3.66E-9
btaunu_sm_lim = [3.2E-9 ,4.12E-9]


# Summary of the BRs, comparing NMSSMTools (`btaunu`) and SuperIso (`btaunu_si`) without experimental constraints:

# In[282]:

df_M3MU3MQ3AU3_orig.loc[:, ['btaunu', 'btaunu_si']].describe()


# First we plot the distributions of each value:

# In[342]:

fig = plt.figure()
fig.set_size_inches(14,6)
title = r"Without exp. constraints"
xlabel = r"$BR(B^+\to \tau^+\nu_{\tau})$"
bins = 100
br_range = [0.4E-4, 1.2E-4]

# Lin y axis
ax1 = fig.add_subplot(1,2,1)
y11, bins11, patches11 = plot_histogram(ax1, 'btaunu', df_M3MU3MQ3AU3_orig, "NMSSMTools", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='red', range=br_range, bins=bins, histtype="step", linewidth=1.5)
y21, bins21, patches21 = plot_histogram(ax1, 'btaunu_si', df_M3MU3MQ3AU3_orig, "SuperIso", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='green', range=br_range, bins=bins, histtype="step", linewidth=1.5)

ax1.add_patch(make_highlight_region(ax=ax1, limits=btaunu_lim, axis='x', 
                               label=r"Exp. $\pm 2\sigma$", alpha=0.2, facecolor='grey'))
# SM range
# ax1.add_patch(make_highlight_region(ax=ax1, limits=btaunu_sm_lim, axis='x', 
#                                label=r"SM. $\pm 2\sigma$ (new)", alpha=0.3, facecolor='palegreen'))
ax1.set_xlim(br_range)
ax1.legend(fontsize=20, loc=2)
ax1.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# log y axis
ax2 = fig.add_subplot(1,2,2)
y12, bins12, patches12 = plot_histogram(ax2, 'btaunu', df_M3MU3MQ3AU3_orig, "NMSSMTools", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='red', range=br_range, bins=bins, histtype="step", linewidth=1.5, log=True)
y22, bins22, patches22 = plot_histogram(ax2, 'btaunu_si', df_M3MU3MQ3AU3_orig, "SuperIso", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='green', range=br_range, bins=bins, histtype="step", linewidth=1.5, log=True)

ax2.add_patch(make_highlight_region(ax=ax2, limits=btaunu_lim, axis='x', 
                               label=r"Exp. $\pm 2\sigma$", alpha=0.2, facecolor='grey'))
# SM range
# ax2.add_patch(make_highlight_region(ax=ax2, limits=btaunu_sm_lim, axis='x', 
#                                label=r"SM. $\pm 2\sigma$ (new)", alpha=0.3, facecolor='palegreen'))
ax2.set_xlim(br_range)
ax2.set_ylim(bottom=5E-5)
ax2.legend(fontsize=20, loc=2)
ax2.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
fig.tight_layout()


# We can see that the overall distributions are very different. The shapes are similar, with both having a sharp dropoff (although there are a handful of points above this sharp dropoff). However the dropoff is at 0.8E-4 for SuperIso, and at 1.1E-4 for NMSSMTools. Is this important when considering the experimental constraint?

# In[334]:

tot = len(df_M3MU3MQ3AU3_orig.index)
print 'Percentage of points failing lower bound: NMSSMTools: %.3f%%  SuperIso: %.3f%%' % (100.0*len(df_M3MU3MQ3AU3_orig[df_M3MU3MQ3AU3_orig.btaunu < btaunu_lim[0]].index)/tot, 100.*len(df_M3MU3MQ3AU3_orig[df_M3MU3MQ3AU3_orig.btaunu_si < btaunu_lim[0]].index)/tot)


# In[320]:

fig = plt.figure()
fig.set_size_inches(14,6)
title = r"With exp. constraints"
xlabel = r"$BR(B^+\to \tau^+\nu_{\tau})$"
bins = 50
br_range = [0, 1.4E-4]

# Lin y axis
ax1 = fig.add_subplot(1,2,1)
y11, bins11, patches11 = plot_histogram(ax1, 'btaunu', df_M3MU3MQ3AU3_pass_all, "NMSSMTools", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='red', range=br_range, bins=bins, histtype="step", linewidth=1.5)
y21, bins21, patches21 = plot_histogram(ax1, 'btaunu_si', df_M3MU3MQ3AU3_pass_all, "SuperIso", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='green', range=br_range, bins=bins, histtype="step", linewidth=1.5)

ax1.add_patch(make_highlight_region(ax=ax1, limits=btaunu_lim, axis='x', 
                               label=r"Exp. $\pm 2\sigma$", alpha=0.2, facecolor='grey'))
# SM range
# ax1.add_patch(make_highlight_region(ax=ax1, limits=btaunu_sm_lim, axis='x', 
#                                label=r"SM. $\pm 2\sigma$ (new)", alpha=0.3, facecolor='palegreen'))
ax1.set_xlim(br_range)
ax1.legend(fontsize=20, loc=2)
ax1.ticklabel_format(style='sci', axis='x', scilimits=(0,0))

# log y axis
ax2 = fig.add_subplot(1,2,2)
y12, bins12, patches12 = plot_histogram(ax2, 'btaunu', df_M3MU3MQ3AU3_pass_all, "NMSSMTools", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='red', range=br_range, bins=bins, histtype="step", linewidth=1.5, log=True)
y22, bins22, patches22 = plot_histogram(ax2, 'btaunu_si', df_M3MU3MQ3AU3_pass_all, "SuperIso", 
                                     xlabel, "p.d.f", title, errorbars=False, normed=True, 
                                     color='green', range=br_range, bins=bins, histtype="step", linewidth=1.5, log=True)

ax2.add_patch(make_highlight_region(ax=ax2, limits=btaunu_lim, axis='x', 
                               label=r"Exp. $\pm 2\sigma$", alpha=0.2, facecolor='grey'))
# SM range
# ax2.add_patch(make_highlight_region(ax=ax2, limits=btaunu_sm_lim, axis='x', 
#                                label=r"SM. $\pm 2\sigma$ (new)", alpha=0.3, facecolor='palegreen'))
ax2.set_xlim(br_range)
ax2.set_ylim(bottom=5E-5)
ax2.legend(fontsize=20, loc=2)
ax2.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
fig.tight_layout()


# Let's look at the distributions on a point-by-point basis like before:

# In[300]:

# Make new series with diff between NMSSMTools and SuperIso without exp. con
btaunu_without = df_M3MU3MQ3AU3_orig.btaunu.copy(deep=True)
btaunu_si_without = df_M3MU3MQ3AU3_orig.btaunu_si
btaunu_without = btaunu_without.subtract(btaunu_si_without)
btaunu_without.describe()


# In[317]:

fig = plt.figure()
fig.set_size_inches(14,6)

# lin y axis
ax2 = fig.add_subplot(1,2,1)
title = r"$B^+ \to \tau^+\nu_{\tau}$ without exp. constraints"
br_range = [2E-5, 2.8E-5]

btaunu_val = btaunu_without.values
weights = np.ones_like(btaunu_val)/len(btaunu_val)
y, bins, patches = ax2.hist(btaunu_val, weights=weights, bins=25, 
                            range=br_range, log=False, color='cornflowerblue', alpha=0.8)
ax2.set_xlabel(r"${BR}_{NMSSMTools} - {BR}_{SuperIso}$")
ax2.set_ylabel("p.d.f.")
ax2.set_xlim(br_range)
ax2.set_title(title, y=1.05)
ax2.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
ax2.minorticks_on()
plt.tight_layout()

# log y axis
ax = fig.add_subplot(1,2,2)
br_range = [2E-5, 2.8E-5]
y, bins, patches = ax.hist(btaunu_val, weights=weights, bins=28, 
                            range=br_range, log=True, color='cornflowerblue', alpha=0.8)
ax.set_xlabel(r"${BR}_{NMSSMTools} - {BR}_{SuperIso}$")
ax.set_ylabel("p.d.f.")
ax.set_xlim(br_range)
ax.set_title(title, y=1.05)
ax.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
ax.minorticks_on()
plt.tight_layout()


# In[339]:

btaunu_mean = btaunu_without.mean()
print "Mean difference: %.3e, and as a percentage of central exp. constraint: %.3f%%" %(btaunu_mean, 100.*(btaunu_mean/(0.5*sum(btaunu_lim))))


# So it is a fairly big difference on a point-by-point basis. However, we should also consider the fact that this is without any experimental constraints - how does it actually affect the parameter space we're interested in?
