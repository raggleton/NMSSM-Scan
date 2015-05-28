
# coding: utf-8

# In this notebook, we will compare the output from NMSSMTools 4.5.1 and NMSSMCALC (as downloaded from last website update on 11.2.15).
# 
# **CAVEAT: not checked all inputs are the same (e.g. SM masses, mixing angles etc)**
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
# - The switch `I4 = 1` was used in NMSSMTools
# 
# - The following results contain plots for both 1-loop and 2-loop masses for NMSSMCALC
# 

# In[51]:

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

get_ipython().magic(u"config InlineBackend.figure_formats = 'png', ")

mpl.rcParams['figure.figsize'] = (7.0, 4.0)  # default size of plots
mpl.rcParams['axes.labelsize'] = 30
mpl.rcParams['xtick.labelsize'] = 20
mpl.rcParams['ytick.labelsize'] = 20
mpl.rcParams['xtick.major.size'] = 10
mpl.rcParams['ytick.major.size'] = 10
mpl.rcParams['xtick.minor.size'] = 5
mpl.rcParams['ytick.minor.size'] = 5
mpl.rcParams['legend.framealpha'] = 0.6
mpl.rcParams.update({'font.size': 24, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})


# In[74]:

from common_plots import *


# In[4]:

# Unpack dataframes from hdf5 binaries
# I4 = 1 dataset, NMSSMCALC 1 Loop, scanning over M3,MU3,MQ3,AU3 
store_M3MU3MQ3AU3_1LOOP_scan = pd.HDFStore("points_scan_M3MQ3MU3AU3_NMSSMCALC_1LOOP.h5")
df_M3MU3MQ3AU3_1LOOP_orig = store_M3MU3MQ3AU3_1LOOP_scan.full12loop_all
df_M3MU3MQ3AU3_1LOOP_pass_all = store_M3MU3MQ3AU3_1LOOP_scan.full12loop_good_posMuMagMom_planckUpperOnly
# df_M3MU3MQ3AU3_ma1Lt10 = store_M3MU3MQ3AU3_scan.full12loop_good_posMuMagMom_planckUpperOnly_maLt10
# df_M3MU3MQ3AU3_1LOOP_h1SM = store_M3MU3MQ3AU3_1LOOP_scan.full12loop_good_posMuMagMom_planckUpperOnly_h1SM
# df_M3MU3MQ3AU3_h2SM = store_M3MU3MQ3AU3_scan.full12loop_good_posMuMagMom_planckUpperOnly_h2SM
store_M3MU3MQ3AU3_1LOOP_scan.close()


# In[6]:

# Unpack dataframes from hdf5 binaries
# I4 = 1 dataset, NMSSMCALC 2 Loop, scanning over M3,MU3,MQ3,AU3 
store_M3MU3MQ3AU3_2LOOP_scan = pd.HDFStore("points_scan_M3MQ3MU3AU3_NMSSMCALC_2LOOP.h5")
df_M3MU3MQ3AU3_2LOOP_orig = store_M3MU3MQ3AU3_2LOOP_scan.full12loop_all
df_M3MU3MQ3AU3_2LOOP_pass_all = store_M3MU3MQ3AU3_2LOOP_scan.full12loop_good_posMuMagMom_planckUpperOnly
# df_M3MU3MQ3AU3_ma1Lt10 = store_M3MU3MQ3AU3_scan.full12loop_good_posMuMagMom_planckUpperOnly_maLt10
# df_M3MU3MQ3AU3_2LOOP_h1SM = store_M3MU3MQ3AU3_2LOOP_scan.full12loop_good_posMuMagMom_planckUpperOnly_h1SM
# df_M3MU3MQ3AU3_h2SM = store_M3MU3MQ3AU3_scan.full12loop_good_posMuMagMom_planckUpperOnly_h2SM
store_M3MU3MQ3AU3_2LOOP_scan.close()


# In[9]:

# print len(df_M3MU3MQ3AU3_1LOOP_pass_all.index), len(df_M3MU3MQ3AU3_2LOOP_pass_all.index)


# In[33]:

# experimental constraint on higgs mass 
mh_range = [122.1,128.1] 


# #$m_{h_1}$ 

# Let's start by looking at the mass of the lightest scalar. Here, `mh1` is from NMSSMTools, `mh1_nc` is from NMSSMCALC.

# In[18]:

print 'To 1-loop in NMSSMCALC:'
df_M3MU3MQ3AU3_1LOOP_pass_all.loc[:, ['mh1', 'mh1_nc']].describe(percentiles=[.05, .25, .75, .95])


# In[19]:

print 'To 2-loop in NMSSMCALC:'
df_M3MU3MQ3AU3_2LOOP_pass_all.loc[:, ['mh1', 'mh1_nc']].describe(percentiles=[.05, .25, .75, .95])


# First, let's plot distributions of each:

# In[56]:

get_ipython().magic(u"config InlineBackend.figure_formats = 'png', 'pdf'")

fig = plt.figure()
fig.set_size_inches(14,6)
title='With exp. constraints'
xlabel=r'$m_{h_1}\ \mathrm{[GeV]}$'
bins = 40
m_range = [110,130]

# Lin y axis
ax1 = fig.add_subplot(1,2,1)
# NMSSMTools
y11, bins11, patches11 = plot_histogram(ax1, var='mh1', df=df_M3MU3MQ3AU3_1LOOP_pass_all, label='NMSSMTools',
                                       xlabel=xlabel, ylabel='p.d.f.', title=title, errorbars=False, normed=True,
                                       color='red', range=m_range, bins=bins, histtype="step", linewidth=1.5)
add_median_line(df_M3MU3MQ3AU3_1LOOP_pass_all, var='mh1', c='red', ls='--', lw=1.5, label='NMSSMTools median')
# NMSSMCALC 1 LOOP
y12, bins12, patches12 = plot_histogram(ax1, var='mh1_nc', df=df_M3MU3MQ3AU3_1LOOP_pass_all, label='NMSSMCALC (1 loop)',
                                       xlabel=xlabel, ylabel='p.d.f.', title=title, errorbars=False, normed=True,
                                       color='green', range=m_range, bins=bins, histtype="step", linewidth=1.5)
add_median_line(df_M3MU3MQ3AU3_1LOOP_pass_all, var='mh1_nc', c='green', ls='--', lw=1.5, label='NMSSMCALC (1 loop) median')
# NMSSMCALC 2 LOOP
y13, bins13, patches13 = plot_histogram(ax1, var='mh1_nc', df=df_M3MU3MQ3AU3_2LOOP_pass_all, label='NMSSMCALC (2 loop)',
                                       xlabel=xlabel, ylabel='p.d.f.', title=title, errorbars=False, normed=True,
                                       color='blue', range=m_range, bins=bins, histtype="step", linewidth=1.5)
add_median_line(df_M3MU3MQ3AU3_2LOOP_pass_all, var='mh1_nc', c='blue', ls='--', lw=1.5, label='NMSSMCALC (2 loop) median')

# plt.ylim(top=max(y11+y12+y13))
make_highlight_region(ax1, mh_range, 'x', color='grey', alpha=0.3, label=r'$m_{h}$ exp. constraint $\pm 2 \sigma$')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize=20)


# Let's look at this on a point-by-point basis:

# In[126]:

print 'Comparison with NMSSMCALC, 1 loop:'
mh1_1loop_diff = df_M3MU3MQ3AU3_1LOOP_pass_all.mh1.subtract(df_M3MU3MQ3AU3_1LOOP_pass_all.mh1_nc)
mh1_1loop_diff.describe(percentiles=[.05, .25, .75, .95])


# In[127]:

print 'Comparison with NMSSMCALC, 2 loop:'
mh1_2loop_diff = df_M3MU3MQ3AU3_2LOOP_pass_all.mh1.subtract(df_M3MU3MQ3AU3_2LOOP_pass_all.mh1_nc)
mh1_2loop_diff.describe(percentiles=[.05, .25, .75, .95])


# In[152]:

fig = plt.figure()
fig.set_size_inches(14,6)
ax = fig.add_subplot(1,2,1)
bins = 30
m_range = [0,15]
log = False

y11, bins11, patches11 = plot_histogram(ax, array=mh1_1loop_diff.values, label='1 loop', 
                                  xlabel=r'$m_{h_1}^{\mathrm{NMSSMTools}}-m_{h_1}^{\mathrm{NMSSMCALC}}\ \ \mathrm{[GeV]}$', ylabel='p.d.f',
                                  normed=True, color='purple', range=m_range, bins=bins, histtype="step", 
                                  linewidth=1.5, log=log)
y12, bins12, patches12 = plot_histogram(ax, array=mh1_2loop_diff.values, label='2 loop', 
                                  xlabel=r'$m_{h_1}^{\mathrm{NMSSMTools}}-m_{h_1}^{\mathrm{NMSSMCALC}}\ \ \mathrm{[GeV]}$', ylabel='p.d.f',
                                  normed=True, color='red', range=m_range, bins=bins, histtype="step", 
                                  linewidth=1.5, log=log)
plt.ylim(bottom=0)
plt.legend(fontsize=18)

ax = fig.add_subplot(1,2,2)
# bins = 40
# m_range = [0,20]
log = True

y21, bins21, patches21 = plot_histogram(ax, array=mh1_1loop_diff.values, label='1 loop', 
                                  xlabel=r'$m_{h_1}^{\mathrm{NMSSMTools}}-m_{h_1}^{\mathrm{NMSSMCALC}}\ \ \mathrm{[GeV]}$', ylabel='p.d.f',
                                  normed=True, color='purple', range=m_range, bins=bins, histtype="step", 
                                  linewidth=1.5, log=log)
y22, bins22, patches22 = plot_histogram(ax, array=mh1_2loop_diff.values, label='2 loop', 
                                  xlabel=r'$m_{h_1}^{\mathrm{NMSSMTools}}-m_{h_1}^{\mathrm{NMSSMCALC}}\ \ \mathrm{[GeV]}$', ylabel='p.d.f',
                                  normed=True, color='red', range=m_range, bins=bins, histtype="step", 
                                  linewidth=1.5, log=log)
plt.suptitle(r"With exp. constraints, $m_{h_1}^{\mathrm{NMSSMTools}} \in [122, 128]\ \mathrm{GeV}$", y=1.04)
plt.ylim(bottom=1E-4)
plt.legend(fontsize=18)


# #$m_{h_2}$ 

# We can do the same thing for the second scalar.

# In[58]:

print 'To 1-loop in NMSSMCALC:'
df_M3MU3MQ3AU3_1LOOP_pass_all.loc[:, ['mh2', 'mh2_nc']].describe(percentiles=[.05, .25, .75, .95])


# In[57]:

print 'To 2-loop in NMSSMCALC:'
df_M3MU3MQ3AU3_2LOOP_pass_all.loc[:, ['mh2', 'mh2_nc']].describe(percentiles=[.05, .25, .75, .95])


# In[83]:

## get_ipython().magic(u"config InlineBackend.figure_formats = 'png', 'pdf'")

fig = plt.figure()
fig.set_size_inches(14,6)
title='With exp. constraints'
xlabel=r'$m_{h_2}\ \mathrm{[GeV]}$'
bins = 25
m_range = [100,1000]

# Lin y axis
ax1 = fig.add_subplot(1,2,1)
# NMSSMTools
y11, bins11, patches11 = plot_histogram(ax1, var='mh2', df=df_M3MU3MQ3AU3_1LOOP_pass_all, label='NMSSMTools',
                                       xlabel=xlabel, ylabel='p.d.f.', title=title, errorbars=False, normed=True,
                                       color='red', range=m_range, bins=bins, histtype="step", linewidth=1.5)
add_median_line(df_M3MU3MQ3AU3_1LOOP_pass_all, var='mh2', c='red', ls='--', lw=1.5, label='NMSSMTools median')
# NMSSMCALC 1 LOOP
y12, bins12, patches12 = plot_histogram(ax1, var='mh2_nc', df=df_M3MU3MQ3AU3_1LOOP_pass_all, label='NMSSMCALC (1 loop)',
                                       xlabel=xlabel, ylabel='p.d.f.', title=title, errorbars=False, normed=True,
                                       color='green', range=m_range, bins=bins, histtype="step", linewidth=1.5)
add_median_line(df_M3MU3MQ3AU3_1LOOP_pass_all, var='mh2_nc', c='green', ls='--', lw=1.5, label='NMSSMCALC (1 loop) median')
# NMSSMCALC 2 LOOP
y13, bins13, patches13 = plot_histogram(ax1, var='mh2_nc', df=df_M3MU3MQ3AU3_2LOOP_pass_all, label='NMSSMCALC (2 loop)',
                                       xlabel=xlabel, ylabel='p.d.f.', title=title, errorbars=False, normed=True,
                                       color='blue', range=m_range, bins=bins, histtype="step", linewidth=1.5)
add_median_line(df_M3MU3MQ3AU3_2LOOP_pass_all, var='mh2_nc', c='blue', ls='--', lw=1.5, label='NMSSMCALC (2 loop) median')
plt.xlim(m_range)
plt.ylim(top=1.1*max(np.concatenate([y11, y12, y13])))
# print max(np.concatenate([y11, y12, y13])
# make_highlight_region(ax1, mh_range, 'x', color='grey', alpha=0.3, label=r'$m_{h}$ exp. constraint $\pm 2 \sigma$')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize=20)


# And in the h(125) region, where we consider points that have $m_{h_2} \in [110, 130]$ GeV to compare with the above $m_{h_1}$ plot (limited by v.small stats):

# In[104]:

## get_ipython().magic(u"config InlineBackend.figure_formats = 'png', 'pdf'")

fig = plt.figure()
fig.set_size_inches(14,6)
title=''

xlabel=r'$m_{h_2}\ \mathrm{[GeV]}$'
bins = 20
m_range = [110,130]

# Lin y axis
ax1 = fig.add_subplot(1,2,1)
# NMSSMTools
y11, bins11, patches11 = plot_histogram(ax1, var='mh2', df=df_M3MU3MQ3AU3_1LOOP_pass_all, label='NMSSMTools',
                                       xlabel=xlabel, ylabel='p.d.f.', title=title, errorbars=True, normed=True,
                                       color='red', range=m_range, bins=bins, histtype="step", linewidth=1.5)
add_median_line(df_M3MU3MQ3AU3_1LOOP_pass_all, var='mh2', c='red', ls='--', lw=1.5, label='NMSSMTools median')
# NMSSMCALC 1 LOOP
y12, bins12, patches12 = plot_histogram(ax1, var='mh2_nc', df=df_M3MU3MQ3AU3_1LOOP_pass_all, label='NMSSMCALC (1 loop)',
                                       xlabel=xlabel, ylabel='p.d.f.', title=title, errorbars=True, normed=True,
                                       color='green', range=m_range, bins=bins, histtype="step", linewidth=1.5)
add_median_line(df_M3MU3MQ3AU3_1LOOP_pass_all, var='mh2_nc', c='green', ls='--', lw=1.5, label='NMSSMCALC (1 loop) median')
# NMSSMCALC 2 LOOP
y13, bins13, patches13 = plot_histogram(ax1, var='mh2_nc', df=df_M3MU3MQ3AU3_2LOOP_pass_all, label='NMSSMCALC (2 loop)',
                                       xlabel=xlabel, ylabel='p.d.f.', title=title, errorbars=True, normed=True,
                                       color='blue', range=m_range, bins=bins, histtype="step", linewidth=1.5)
add_median_line(df_M3MU3MQ3AU3_2LOOP_pass_all, var='mh2_nc', c='blue', ls='--', lw=1.5, label='NMSSMCALC (2 loop) median')
plt.xlim(m_range)
ymax = max(np.concatenate([y11, y12, y13]))
plt.ylim(top=1.3*ymax, bottom=0)
# print max(np.concatenate([y11, y12, y13])
# make_highlight_region(ax1, mh_range, 'x', color='grey', alpha=0.3, label=r'$m_{h}$ exp. constraint $\pm 2 \sigma$')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize=20)
plt.suptitle(r'With exp. constraints, $m_{h_2} \in [110, 130]\ \mathrm{GeV}$', fontsize=24, y=1.02)


# So we see the same effect here, with the masses as correspondingly smaller for NMSSMCALC.

# #$m_{a_1}$ 

# In[122]:

print 'To 1-loop in NMSSMCALC:'
df_M3MU3MQ3AU3_1LOOP_pass_all.loc[:, ['ma1', 'ma1_nc']].describe(percentiles=[.05, .25, .75, .95])


# In[123]:

print 'To 2-loop in NMSSMCALC:'
df_M3MU3MQ3AU3_2LOOP_pass_all.loc[:, ['ma2', 'ma1_nc']].describe(percentiles=[.05, .25, .75, .95])


# In[107]:

## get_ipython().magic(u"config InlineBackend.figure_formats = 'png', 'pdf'")

fig = plt.figure()
fig.set_size_inches(14,6)
title='With exp. constraints'
xlabel=r'$m_{a_1}\ \mathrm{[GeV]}$'
bins = 25
m_range = [0,100]

# Lin y axis
ax1 = fig.add_subplot(1,2,1)
# NMSSMTools
y11, bins11, patches11 = plot_histogram(ax1, var='ma1', df=df_M3MU3MQ3AU3_1LOOP_pass_all, label='NMSSMTools',
                                       xlabel=xlabel, ylabel='p.d.f.', title=title, errorbars=False, normed=True,
                                       color='red', range=m_range, bins=bins, histtype="step", linewidth=1.5)
add_median_line(df_M3MU3MQ3AU3_1LOOP_pass_all, var='ma1', c='red', ls='--', lw=1.5, label='NMSSMTools median')
# NMSSMCALC 1 LOOP
y12, bins12, patches12 = plot_histogram(ax1, var='ma1_nc', df=df_M3MU3MQ3AU3_1LOOP_pass_all, label='NMSSMCALC (1 loop)',
                                       xlabel=xlabel, ylabel='p.d.f.', title=title, errorbars=False, normed=True,
                                       color='green', range=m_range, bins=bins, histtype="step", linewidth=1.5)
add_median_line(df_M3MU3MQ3AU3_1LOOP_pass_all, var='ma1_nc', c='green', ls='--', lw=1.5, label='NMSSMCALC (1 loop) median')
# NMSSMCALC 2 LOOP
y13, bins13, patches13 = plot_histogram(ax1, var='ma1_nc', df=df_M3MU3MQ3AU3_2LOOP_pass_all, label='NMSSMCALC (2 loop)',
                                       xlabel=xlabel, ylabel='p.d.f.', title=title, errorbars=False, normed=True,
                                       color='blue', range=m_range, bins=bins, histtype="step", linewidth=1.5)
add_median_line(df_M3MU3MQ3AU3_2LOOP_pass_all, var='ma1_nc', c='blue', ls='--', lw=1.5, label='NMSSMCALC (2 loop) median')
plt.xlim(m_range)
plt.ylim(top=1.1*max(np.concatenate([y11, y12, y13])))
# print max(np.concatenate([y11, y12, y13])
# make_highlight_region(ax1, mh_range, 'x', color='grey', alpha=0.3, label=r'$m_{h}$ exp. constraint $\pm 2 \sigma$')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize=20)


# Note that the distributions look very similar, however there is glut of point at m = 0. This is from NMSSMCALC (in my analysis script, it defaults to 0 if no suitable nmssmcalc output found) - sometimes it fails to calcualte masses correctly that NMSSMTools has no trouble with (I believe). This requires further investigation.

# Let's focus on the low mass region, as that is what we're primarily interested in.

# In[121]:

## get_ipython().magic(u"config InlineBackend.figure_formats = 'png', 'pdf'")

fig = plt.figure()
fig.set_size_inches(14,6)
title='With exp. constraints'
xlabel=r'$m_{a_1}\ \mathrm{[GeV]}$'
bins = 10
m_range = [0,20]

# Lin y axis
ax1 = fig.add_subplot(1,2,1)
errors = False
log = True
# NMSSMTools
y11, bins11, patches11 = plot_histogram(ax1, var='ma1', df=df_M3MU3MQ3AU3_1LOOP_pass_all, label='NMSSMTools',
                                       xlabel=xlabel, ylabel='p.d.f.', title=title, errorbars=errors, normed=True,
                                       color='red', range=m_range, bins=bins, histtype="step", linewidth=1.5, log=log)
add_median_line(df_M3MU3MQ3AU3_1LOOP_pass_all, var='ma1', c='red', ls='--', lw=1.5, label='NMSSMTools median')
# NMSSMCALC 1 LOOP
y12, bins12, patches12 = plot_histogram(ax1, var='ma1_nc', df=df_M3MU3MQ3AU3_1LOOP_pass_all, label='NMSSMCALC (1 loop)',
                                       xlabel=xlabel, ylabel='p.d.f.', title=title, errorbars=errors, normed=True,
                                       color='green', range=m_range, bins=bins, histtype="step", linewidth=1.5, log=log)
add_median_line(df_M3MU3MQ3AU3_1LOOP_pass_all, var='ma1_nc', c='green', ls='--', lw=1.5, label='NMSSMCALC (1 loop) median')
# NMSSMCALC 2 LOOP
y13, bins13, patches13 = plot_histogram(ax1, var='ma1_nc', df=df_M3MU3MQ3AU3_2LOOP_pass_all, label='NMSSMCALC (2 loop)',
                                       xlabel=xlabel, ylabel='p.d.f.', title=title, errorbars=errors, normed=True,
                                       color='blue', range=m_range, bins=bins, histtype="step", linewidth=1.5, log=log)
add_median_line(df_M3MU3MQ3AU3_2LOOP_pass_all, var='ma1_nc', c='blue', ls='--', lw=1.5, label='NMSSMCALC (2 loop) median')
plt.xlim(m_range)
plt.ylim(top=0.02, bottom=3E-5)
# make_highlight_region(ax1, mh_range, 'x', color='grey', alpha=0.3, label=r'$m_{h}$ exp. constraint $\pm 2 \sigma$')
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize=20)


# In[ ]:



