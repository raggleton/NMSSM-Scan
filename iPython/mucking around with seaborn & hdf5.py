
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from itertools import product as itprod
# import seaborn as sns
from pandas.tools.plotting import scatter_matrix
# pd.options.display.mpl_style = 'default'
pd.options.display.mpl_style = False
pd.options.display.precision = 3

# to show plots:
get_ipython().magic(u'pylab inline')

pylab.rcParams['figure.figsize'] = (9.0, 6.0)  # default size of plots
pylab.rcParams['axes.labelsize'] = 30
pylab.rcParams['xtick.labelsize'] = 20
pylab.rcParams['ytick.labelsize'] = 20
pylab.rcParams['xtick.major.size'] = 10
pylab.rcParams['ytick.major.size'] = 10
pylab.rcParams['xtick.minor.size'] = 5
pylab.rcParams['ytick.minor.size'] = 5
# pylab.rcParams['ytick.major.width'] = 2
# pylab.rcParams['ytick.minor.width'] = 2
# pylab.rcParams['xtick.major.width'] = 2
# pylab.rcParams['xtick.minor.width'] = 2
matplotlib.rcParams.update({'font.size': 24, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})


# In[2]:

store = pd.HDFStore("store.h5")
# print store
df = store.full12loop
df_loMass = store.default
len(df.index)


# In[ ]:

store_new = pd.HDFStore("points_store_small.h5")
df = store_new.full12loop_all
df_pass = store_new.full12loop_good_posMuMagMom_planckUpperOnly
df_ma1Lt10 = store_new.full12loop_good_posMuMagMom_planckUpperOnly_maLt10
print store_new
len(df.index)
len(df_ma1Lt10.index)
df = df_pass


# In[ ]:

df_pass.ma1.describe()


# In[ ]:

df_pass[0:5].T


# In[ ]:

ax = df.mh1.plot(kind="hist", normed=False, range=[122,128], bins=30, logy=False, alpha=0.8)
ax.set_xlabel(r"$m_{h_1}\mathrm{[GeV]}$")
ax.set_ylabel(r"$N$")
plt.suptitle("Full 1 + 2 loop")
plt.minorticks_on()
plt.savefig("mh1.pdf")


# In[ ]:

df.plot(kind="scatter", x="ma1", y="Del_a_mu", alpha=1, c="tgbeta", cmap=plt.get_cmap("YlOrRd"))
plt.ylabel(r"$\Delta a_{\mu}$")
plt.xlabel(r"$m_{a_1}\mathrm{[GeV]}$")
plt.minorticks_on()
plt.yscale("log")
plt.ylim([5E-11, 2E-9])
plt.xlim([0,30])


# In[ ]:

df.plot(kind="scatter", x="ma1", y="kappa", alpha=1, color="orange")
# fig = plt.figure()
from matplotlib.colors import LogNorm
# counts, xedges, yedges, im = plt.hist2d(df["ma1"], df["kappa"], bins=[40,35], range=[[0,30],[0, 0.7]], 
#                                         norm=LogNorm(), cmap=plt.get_cmap("YlOrRd"))
plt.ylabel(r"$\kappa$")
plt.xlabel(r"$m_{a_1}\mathrm{[GeV]}$")
plt.minorticks_on()
plt.xlim([0, 30])
plt.ylim([0, 0.7])
# plt.colorbar(im)
# plt.savefig("ma1_kappa.pdf")


# In[142]:

df.plot(kind="scatter", x="ma1", y="mstop1", alpha=1, color="purple")
# fig = plt.figure()
from matplotlib.colors import LogNorm
# counts, xedges, yedges, im = plt.hist2d(df["ma1"], df["kappa"], bins=[40,35], range=[[0,30],[0, 0.7]], 
#                                         norm=LogNorm(), cmap=plt.get_cmap("YlOrRd"))
plt.ylabel(r"$m_{\tilde{t_1}}\mathrm{[GeV]}$")
plt.xlabel(r"$m_{a_1}\mathrm{[GeV]}$")
plt.minorticks_on()
plt.xlim([0, 30])
plt.ylim([856, 862])


# In[140]:

df.plot(kind="scatter", x="mstop1", y="tgbeta", alpha=0.7, c="purple")
# fig = plt.figure()
from matplotlib.colors import LogNorm
# counts, xedges, yedges, im = plt.hist2d(df["ma1"], df["kappa"], bins=[40,35], range=[[0,30],[0, 0.7]], 
#                                         norm=LogNorm(), cmap=plt.get_cmap("YlOrRd"))
plt.xlabel(r"$m_{\tilde{t_1}}\mathrm{[GeV]}$")
plt.ylabel(r"$\tan\beta$")
plt.minorticks_on()
plt.ylim([0, 50])
plt.xlim([855, 865])


# In[143]:

df.plot(kind="scatter", x="mstop2", y="tgbeta", alpha=0.7, c="purple")
# fig = plt.figure()
from matplotlib.colors import LogNorm
# counts, xedges, yedges, im = plt.hist2d(df["ma1"], df["kappa"], bins=[40,35], range=[[0,30],[0, 0.7]], 
#                                         norm=LogNorm(), cmap=plt.get_cmap("YlOrRd"))
plt.xlabel(r"$m_{\tilde{t_2}}\mathrm{[GeV]}$")
plt.ylabel(r"$\tan\beta$")
plt.minorticks_on()
plt.ylim([0, 50])
# plt.xlim([855, 865])


# In[24]:

df.tgbeta.plot(kind="hist", bins=50)


# In[10]:

df_ma1 = df[df.ma1<10.5]
df_ma1 = df_ma1.loc[:,['ma1', "tgbeta", "mueff", "lambda", "kappa", "alambda", "akappa", "Bra1tautau", "Brh1a1a1"]]
scatter_matrix(df_ma1, alpha=0.5, figsize=(24, 24), diagonal='hist', color="blue", marker="x")


# $\gamma$

# In[9]:

ddf = df.loc[:,["mh1", "mh2", "ma1", "ma2", "tgbeta", "mueff", "lambda", "kappa", "alambda", "akappa", "Brh1gg", "Brh1tautau", "Brh1bb", "Brh1a1a1", "Brh2gg", "Brh2tautau", "Brh2bb", "Brh2a1a1", "Brh2h1h1", "Bra1tautau", "Bra1bb", "omega", "Del_a_mu"]]
scatter_matrix(ddf, alpha=0.2, figsize=(50, 50), diagonal='hist', color="blue")
plt.savefig("scatter_matrix.png")

