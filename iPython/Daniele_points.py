
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


# In[42]:

from make_hdf5 import subset_mass
df_pass_all_h1 = subset_mass(df_pass_all, 122.1, 128.1, 'mh1')
df_pass_all_h2 = subset_mass(df_pass_all, 122.1, 128.1, 'mh2')
df_pass_all_strict = df_pass_all[df_pass_all.constraints == ""]


# In[33]:

print 'Original points (no constraints):', len(df_orig.index) 
print 'With relaxed constraints (on g-2, relic density & some LHC constraints):', len(df_pass_all.index)
print 'Strictly enforcing all constraints in NMSSMTools 4.6.0:',len(df_pass_all_strict.index)


# In[34]:

df_pass_all.ma1.describe()


# In[35]:

df_pass_all.columns


# In[36]:

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
plt.ylim(bottom=0, top=10)
plt.legend(loc=0, fontsize=18)
# plt.figtext(0.74, 0.73, r"$h_{125}\ =\ h_1$", bbox={'facecolor':'white', 'alpha':0.5, 'boxstyle': 'round'})


# In[37]:

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
plt.ylim(bottom=0, top=10)
plt.xlim(right=50)
plt.legend(fontsize=18)
# plt.figtext(0.74, 0.73, r"$h_{125}\ =\ h_1$", bbox={'facecolor':'white', 'alpha':0.5, 'boxstyle': 'round'})


# In[38]:

fig = generate_fig()
ax1 = fig.add_subplot(1,2,1)

plot_scatter(ax1, xvar='ma1', yvar='Bra1tautau', df=df_pass_all_h1, 
             color='blue', xlabel=r'$m_{a_1}\ \mathrm{[GeV]}$', ylabel=r'$BR(a_1\to\tau\tau)$', 
             label='Relaxed constraints')
plot_scatter(ax1, xvar='ma1', yvar='Bra1tautau', df=df_pass_all_strict, 
             color='red', xlabel=r'$m_{a_1}\ \mathrm{[GeV]}$', ylabel=r'$BR(a_1\to\tau\tau)$',
             label='Strict constraints')
plt.ylim(bottom=0)
plt.legend(fontsize=18, loc=4)


# In[39]:

nrows = math.ceil(len(param_dict)/3.)
fig = generate_fig(size=[20,6*nrows])
xvar='xsec_h1_2a1_4tau'
for i, (var, label) in enumerate(param_dict.iteritems(), 1):
    ax1 = fig.add_subplot(nrows,3,i)
    plot_scatter(ax1, xvar=xvar, yvar=var, df=df_orig, color='green', label='No constraints')
    plot_scatter(ax1, xvar=xvar, yvar=var, df=df_pass_all, color='blue', label='Relaxed constraints')
    plot_scatter(ax1, xvar=xvar, yvar=var, df=df_pass_all_strict, color='red', label='Strict constraints')    
    plt.legend(fontsize=14, loc='best')
    plt.xlim(left=0.1)
    plt.xlabel(r'$\sigma_{13}(ggh_1)\times BR(h_1\to a_1 a_1)\times BR(a_1\to\tau \tau)^2\ \mathrm{[pb]}$', fontsize=18)
    plt.ylabel(label)
    plt.xscale('log')


# In[40]:

nrows = math.ceil(len(param_dict)/3.)
fig = generate_fig(size=[20,6*nrows])
xvar='ma1'
for i, (var, label) in enumerate(param_dict.iteritems(), 1):
    ax1 = fig.add_subplot(nrows,3,i)
    plot_scatter(ax1, xvar=xvar, yvar=var, df=df_orig, color='green', label='No constraints')
    plot_scatter(ax1, xvar=xvar, yvar=var, df=df_pass_all, color='blue', label='Relaxed constraints')
    plot_scatter(ax1, xvar=xvar, yvar=var, df=df_pass_all_strict, color='red', label='Strict constraints')    
    plt.legend(fontsize=14, loc='best')
    plt.xlim(left=0)
    plt.xlabel(r'$m_{a_1}\ \mathrm{[GeV]}$', fontsize=18)
    plt.ylabel(label)
#     plt.xscale('log')


# In[ ]:



