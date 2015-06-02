
# coding: utf-8

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


# In[2]:

from common_plots import *


# In[31]:

store = pd.HDFStore("points_daniele_more.h5")
df_orig = store.full12loop_all
df_pass_all = store.full12loop_good_posMuMagMom_planckUpperOnly
store.close()


# In[130]:

store = pd.HDFStore("../daniele_points/points_daniele.h5")
df_orig_orig = store.full12loop_all
df_orig_pass_all = store.full12loop_good_posMuMagMom_planckUpperOnly
store.close()


# In[141]:

df_orig_strict = df_orig_pass_all[df_orig_pass_all.constraints == ""]
df_orig_strict = subset_mass(df_orig_strict, 124, 126, 'mh1')
df_orig_strict = subset_mass(df_orig_strict, 2, 5, 'xsec_h1_2a1_4tau')
# print len(df_orig_strict.index)
print df_orig_strict.T


# In[42]:

from make_hdf5 import subset_mass
df_pass_all_h1 = subset_mass(df_pass_all, 122.1, 128.1, 'mh1')
df_pass_all_h2 = subset_mass(df_pass_all, 122.1, 128.1, 'mh2')
df_pass_all_strict = df_pass_all[df_pass_all.constraints == ""]


# In[33]:

print 'Original points (no constraints):', len(df_orig.index) 
print 'With relaxed constraints (on g-2, relic density & some LHC constraints):', len(df_pass_all.index)
print 'Strictly enforcing all constraints in NMSSMTools 4.6.0:',len(df_pass_all_strict.index)


# In[128]:

# df_pass_all.ma1.describe()


# In[129]:

# df_pass_all.columns


# In[127]:

pd.set_option('display.max_rows', 500)
# The magic reference point:
df_ref = subset_mass(df_pass_all_strict, 124.2, 125.5, 'mh1')
df_ref = subset_mass(df_ref, 8, 9, 'ma1')
df_ref = df_ref[df_ref.xsec_h1_2a1_4tau>3]
# df_ref = df_ref.loc[42772]
df_ref.T
# jobs_100_MICRO_SCAN_DANIELLE_29_May_15_1002/output_ma1Lt1145.dat


# In[144]:

fig = generate_fig(size=[8,6])
ax1 = fig.add_subplot(1,1,1)

path_all = plot_scatter(ax1, xvar='ma1', yvar='xsec_h1_2a1_4tau', df=df_pass_all,
             xlabel=r'$m_{a_1}\ \mathrm{[GeV]}$', 
             ylabel=r'$\sigma\times BR\ \mathrm{[pb]}$',
             label=r'Relaxed constraints',
             title=r'$\sigma_{13}(ggh_1)\times BR(h_1\to a_1 a_1)\times BR(a_1\to\tau \tau)^2$',
             color='blue')
path_strict = plot_scatter(ax1, xvar='ma1', yvar='xsec_h1_2a1_4tau', df=df_pass_all_strict, 
             xlabel=r'$m_{a_1}\ \mathrm{[GeV]}$', 
             ylabel=r'$\sigma\times BR\ \mathrm{[pb]}$',
             label='Strict constraints',
             title=r'$\sigma_{13}(ggh_1)\times BR(h_1\to a_1 a_1)\times BR(a_1\to\tau \tau)^2$',
             color='red')
plot_scatter(ax1, xvar='ma1', yvar='xsec_h1_2a1_4tau', df=df_ref,
             xlabel=r'$m_{a_1}\ \mathrm{[GeV]}$', 
             ylabel=r'$\sigma\times BR\ \mathrm{[pb]}$',
             label='Benchmark point',
             title=r'$\sigma_{13}(ggh_1)\times BR(h_1\to a_1 a_1)\times BR(a_1\to\tau \tau)^2$',
             color='gold', marker="*", s=200, lw=2)

plot_scatter(ax1, xvar='ma1', yvar='xsec_h1_2a1_4tau', df=df_orig_strict,
             xlabel=r'$m_{a_1}\ \mathrm{[GeV]}$', 
             ylabel=r'$\sigma\times BR\ \mathrm{[pb]}$',
             label='Benchmark point',
             title=r'$\sigma_{13}(ggh_1)\times BR(h_1\to a_1 a_1)\times BR(a_1\to\tau \tau)^2$',
             color='gold', marker="*", s=200, lw=2)
plt.ylim(bottom=0, top=10)

plt.axvline(x=9.460, label=r'$\Upsilon(1S/2S/3S)$', ls='-', color='fuchsia', lw=2)
plt.axvline(x=10.023, ls='-', color='fuchsia', lw=2)
plt.axvline(x=10.355, ls='-', color='fuchsia', lw=2)
plt.legend(loc=0, fontsize=18)
# plt.axhline(y=3)
# plt.figtext(0.74, 0.73, r"$h_{125}\ =\ h_1$", bbox={'facecolor':'white', 'alpha':0.5, 'boxstyle': 'round'})


# In[142]:

fig = generate_fig(size=[8,6])
ax1 = fig.add_subplot(1,1,1)

plot_scatter(ax1, xvar='tgbeta', yvar='xsec_h1_2a1_4tau', df=df_pass_all_h1, 
             xlabel=r'$\tan \beta$', 
             ylabel=r'$\sigma\times BR\ \mathrm{[pb]}$',
             label=r"Relaxed constraints",
             title=r'$\sigma_{13}(ggh_1)\times BR(h_1\to a_1 a_1)\times BR(a_1\to\tau \tau)^2$',
             color='blue')
plot_scatter(ax1, xvar='tgbeta', yvar='xsec_h1_2a1_4tau', df=df_pass_all_strict, 
             xlabel=r'$\tan \beta$', 
             ylabel=r'$\sigma\times BR\ \mathrm{[pb]}$',
             label=r"Strict constraints",
             title=r'$\sigma_{13}(ggh_1)\times BR(h_1\to a_1 a_1)\times BR(a_1\to\tau \tau)^2$',
             color='red')
plot_scatter(ax1, xvar='tgbeta', yvar='xsec_h1_2a1_4tau', df=df_ref, 
             xlabel=r'$\tan \beta$', 
             ylabel=r'$\sigma\times BR\ \mathrm{[pb]}$',
             label=r"Benchmark point",
             title=r'$\sigma_{13}(ggh_1)\times BR(h_1\to a_1 a_1)\times BR(a_1\to\tau \tau)^2$',
             color='gold', marker="*", s=200, lw=2)
plot_scatter(ax1, xvar='tgbeta', yvar='xsec_h1_2a1_4tau', df=df_orig_strict, 
             xlabel=r'$\tan \beta$', 
             ylabel=r'$\sigma\times BR\ \mathrm{[pb]}$',
             label=r"Benchmark point",
             title=r'$\sigma_{13}(ggh_1)\times BR(h_1\to a_1 a_1)\times BR(a_1\to\tau \tau)^2$',
             color='gold', marker="*", s=200, lw=2)
plt.ylim(bottom=0, top=10)
plt.xlim(right=50)
plt.legend(fontsize=18)
# plt.figtext(0.74, 0.73, r"$h_{125}\ =\ h_1$", bbox={'facecolor':'white', 'alpha':0.5, 'boxstyle': 'round'})


# In[123]:

fig = generate_fig()
ax1 = fig.add_subplot(1,2,1)

plot_scatter(ax1, xvar='ma1', yvar='Bra1tautau', df=df_pass_all_h1, 
             color='blue', xlabel=r'$m_{a_1}\ \mathrm{[GeV]}$', ylabel=r'$BR(a_1\to\tau\tau)$', 
             label='Relaxed constraints')
plot_scatter(ax1, xvar='ma1', yvar='Bra1tautau', df=df_pass_all_strict, 
             color='red', xlabel=r'$m_{a_1}\ \mathrm{[GeV]}$', ylabel=r'$BR(a_1\to\tau\tau)$',
             label='Strict constraints')
plot_scatter(ax1, xvar='ma1', yvar='Bra1tautau', df=df_ref, 
             xlabel=r'$m_{a_1}\ \mathrm{[GeV]}$', ylabel=r'$BR(a_1\to\tau\tau)$',
             label='Benchmark point', color='gold', marker="*", s=200, lw=2)
plt.ylim(bottom=0)
plt.legend(fontsize=18, loc=4)


# In[124]:

nrows = math.ceil(len(param_dict)/3.)
fig = generate_fig(size=[20,6*nrows])
xvar='xsec_h1_2a1_4tau'
for i, (var, label) in enumerate(param_dict.iteritems(), 1):
    ax1 = fig.add_subplot(nrows,3,i)
    plot_scatter(ax1, xvar=xvar, yvar=var, df=df_orig, color='green', label='No constraints', alpha=0.5)
    plot_scatter(ax1, xvar=xvar, yvar=var, df=df_pass_all, color='blue', label='Relaxed constraints', alpha=0.6)
    plot_scatter(ax1, xvar=xvar, yvar=var, df=df_pass_all_strict, color='red', label='Strict constraints')    
    plot_scatter(ax1, xvar=xvar, yvar=var, df=df_ref, label='Benchmark point', color='gold', marker="*", s=200, lw=2)    
    plt.legend(fontsize=14, loc='best')
    plt.xlim(left=0.1)
    plt.xlabel(r'$\sigma_{13}(ggh_1)\times BR(h_1\to a_1 a_1)\times BR(a_1\to\tau \tau)^2\ \mathrm{[pb]}$', fontsize=18)
    plt.ylabel(label)
    plt.xscale('log')


# In[125]:

nrows = math.ceil(len(param_dict)/3.)
fig = generate_fig(size=[20,6*nrows])
xvar='ma1'
for i, (var, label) in enumerate(param_dict.iteritems(), 1):
    ax1 = fig.add_subplot(nrows,3,i)
    plot_scatter(ax1, xvar=xvar, yvar=var, df=df_orig, color='green', label='No constraints')
    plot_scatter(ax1, xvar=xvar, yvar=var, df=df_pass_all, color='blue', label='Relaxed constraints')
    plot_scatter(ax1, xvar=xvar, yvar=var, df=df_pass_all_strict, color='red', label='Strict constraints')    
    plot_scatter(ax1, xvar=xvar, yvar=var, df=df_ref, label='Benchmark point', color='gold', marker="*", s=200, lw=2)    
    plt.xlim(left=0)
    plt.xlabel(r'$m_{a_1}\ \mathrm{[GeV]}$', fontsize=18)
    plt.ylabel(label)
    plt.axvline(x=9.460, label=r'$\Upsilon(1S/2S/3S)$', ls='-', color='fuchsia', lw=2)
    plt.axvline(x=10.023, ls='-', color='fuchsia', lw=2)
    plt.axvline(x=10.355, ls='-', color='fuchsia', lw=2)
#     plt.xscale('log')
    plt.legend(fontsize=14, loc='best')


# In[ ]:



