
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from itertools import product as itprod

# to show plots:
get_ipython().magic(u'pylab inline')

pd.set_option('display.max_colwidth', 100) # stop putting in the ...
pd.set_option('display.max_rows', 50)
pylab.rcParams['figure.figsize'] = (9.0, 6.0)  # default size of plots
matplotlib.rcParams.update({'font.size': 20})
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['xtick.major.size'] = 8
matplotlib.rcParams['xtick.major.width'] = 1.5
matplotlib.rcParams['xtick.minor.size'] = 5
matplotlib.rcParams['xtick.minor.width'] = 1.5
matplotlib.rcParams['ytick.minor.size'] = 2
matplotlib.rcParams['ytick.minor.width'] = 1.1
matplotlib.rcParams['ytick.major.size'] = 5
matplotlib.rcParams['ytick.major.width'] = 1.5
matplotlib.rcParams['xtick.labelsize'] = 20
matplotlib.rcParams['ytick.labelsize'] = 20

# latex for axes values
# matplotlib.rcParams.update({'font.size': 20, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})

# common plotting variables
scat = "scatter"
latex_size = 25
s_size = 30
alp = 0.3


# We will require points to pass all constraint, except for $\Delta a_{\mu}$, where we only require $\Delta a_{\mu} > 0$.

# In[2]:

# NMSSMTools calculates Higgs mass at LO
folders_LOMass = [
"jobs_50_MICRO_LOMASS_17_Apr_15_0835",
"jobs_50_MICRO_LOMASS_17_Apr_15_0836",
"jobs_50_MICRO_LOMASS_17_Apr_15_0837",
"jobs_50_MICRO_LOMASS_17_Apr_15_0840",
"jobs_50_MICRO_LOMASS_17_Apr_15_0841",
"jobs_50_MICRO_LOMASS_17_Apr_15_0842"
]

# NMSSMTools calculates Higgs mass with corrections
folders = [
"jobs_50_MICRO_11_Apr_15_1009",
"jobs_50_MICRO_11_Apr_15_1036",
"jobs_50_MICRO_11_Apr_15_1038",
"jobs_50_MICRO_11_Apr_15_1157",
"jobs_50_MICRO_11_Apr_15_1158",
"jobs_50_MICRO_11_Apr_15_1203"
]


# Load "good" files into Panda data frame
df_list = []
for fo in folders:
    print fo
    for fi in glob.glob("/users/robina/Dropbox/4Tau/NMSSM-Scan/" + fo + "/output_good*.dat"):
        df_temp = pd.read_csv(fi, delimiter=",")#, keep_default_na=True, na_values="")
        df_list.append(df_temp)
df_orig = pd.concat(df_list)
n_orig = len(df_orig.index)

# Fix the constraints column, such that the ones that pass have NaN replaced by something more sensible
df_orig.fillna({"constraints":""}, axis=0, inplace=True)

# Load up the glu-glu cross sections for 13 TeV
cs = pd.read_csv("/Users/robina/Dropbox/4Tau/NMSSM-Scan/iPython/parton_lumi_ratio.csv")
cs[cs["MH [GeV]"] == 125]
masses = cs["MH [GeV]"].tolist()
xsec_ggf13 = cs["ggF 13TeV cross section [pb]"].tolist()

def find_xsec(mass):
    m = min(range(len(masses)), key=lambda x: abs(masses[x]-mass))
    return xsec_ggf13[m]

# Store SM cross section for gg fusion at 13 TeV for production of m1 and m2
df_orig["xsec_ggf13_h1"] = df_orig.apply(lambda row: find_xsec(row['mh1']), axis=1)
df_orig["xsec_ggf13_h2"] = df_orig.apply(lambda row: find_xsec(row['mh2']), axis=1)

# Calculate total cross-section & scaled cross-sections for gg->h1->a1a1, gg->h2->a1a1, gg->h2->h1h1, 
# with final states 4tau, 2b2tau, 4b. 
# Denoted as gg -> X -> YY ->f1f1f2f2

process_scaled = [] # Store them for later
process = []

# (no constraint on if ggh is hSM)
X = ["h1", "h2"]
Y = ["a1", "h1"]
F = ["tautau", "bb"]

for x,y in itprod(X,Y):
    if x == y:
        continue
    for f1, f2 in itprod(F,F):
        ff = ""
        factor = 1
        if f1 == f2 == "tautau":
            ff = "4tau"
        elif f1 == f2 == "bb":
            ff = "4b"
        else:
            factor = 2
            ff = "2b2tau"    
        name = "xsec_scaled_"+x+"_"+"2"+y+"_"+ff
        if not name in process_scaled:
            process_scaled.append(name) 
            df_orig[name] = df_orig[x+"ggrc2"] * df_orig["Br"+x+y+y] * df_orig["Br"+y+f1] * df_orig["Br"+y+f2] * factor

            name = name.replace("_scaled", "")
            process.append(name)
            df_orig[name] = df_orig["xsec_ggf13_"+x] * df_orig[x+"ggrc2"] * df_orig["Br"+x+y+y] * df_orig["Br"+y+f1] * df_orig["Br"+y+f2] * factor

# df_orig[0:5]["constraints"]


# In[3]:

# Make some subsets here:

# subset based on passing all constraints
pass_all_str = df_orig["constraints"] == ""
del_a_mu_str = df_orig["constraints"] == r"Muon magn. mom. more than 2 sigma away"
pass_del_a_mu = df_orig["Del_a_mu"] > 0

df = df_orig[pass_all_str | (del_a_mu_str & pass_del_a_mu)]
n_total = len(df.index)
df[0:12].T


# In[19]:

# subset with 2m_tau < ma1 < 10
ma10 = df["ma1"] < 10
ma2tau = df["ma1"] > (2*df["mtau"].mean())
df_ma1Lt10 = df[ma10 & ma2tau]
df_ma1Lt10_all = df_orig[(df_orig["ma1"]<10) & (df_orig["ma1"]> (2*df_orig["mtau"].mean()))]
# df = df_ma10; alp *= 2 # comment out to run over all masses

mhmin = 122.1
mhmax = 128.1

# subset with h1 as h_SM
h1SMu = df["mh1"] < mhmax
h1SMl = df["mh1"] > mhmin
df_h1SM = df[h1SMu & h1SMl]
# df = df_h1SM

# subset with h2 as h_SM
h2SMu = df["mh2"] < mhmax
h2SMl = df["mh2"] > mhmin
df_h2SM = df[h2SMu & h2SMl]
# df = df_h2SM

print "Running over", n_orig, "points without checking experimental constraints"
print n_total, "points passing all constraints (=", 100*n_total/float(n_orig), "%)"
print len(df_ma1Lt10.index), "of these have 2m_tau < ma1 < 10 GeV (=",100*len(df_ma1Lt10.index)/float(n_total), "%)"
print len(df_h1SM.index), "points in the h1 = h(125) subset (=", 100*len(df_h1SM.index)/float(n_total), "%)"
print len(df_h2SM.index), "points in the h2 = h(125) subset (=", 100*len(df_h2SM.index)/float(n_total), "%)"

# check constraints
# df[10:15].T


# In[22]:

df["mh1"].plot(kind="hist", range=[120,130], bins=50, normed=True, cumulative=False, logy=True)
plt.xlabel(r"$m_{h_1}~\mathrm{[GeV]}$")
plt.ylabel(r"p.d.f.")
# ax2[0].set_title(r"Passing all constraints ($\Delta a_{\mu} > 0$)")


# # Replicate Bomark/Moretti/et al plots

# Figure 2 from the paper (arxiv 1409.8393): case where $h_1 = h_{SM}$

# In[21]:

fig2, ax2 = plt.subplots(nrows=1, ncols=2)
fig2.set_size_inches(24, 6)
plt.subplots_adjust(wspace=0.3)

import matplotlib as mpl


df_h1SM.plot(kind="scatter", x="ma1", y="mh1", marker="+", ax=ax2[0], c=df_h1SM.tgbeta, cmap=mpl.cm.CMRmap, vmin=0, vmax=40)
ax2[0].set_xlabel(r"$m_{a_1}\mathrm{~[GeV]}$")
ax2[0].set_xlim([0, 150])
ax2[0].set_ylim([122,129])
ax2[0].set_ylabel(r"$m_{h_1}\mathrm{~[GeV]}$")

df_h1SM.plot(kind="scatter", x="kappa", y="mh1", marker="+", ax=ax2[1], c=df_h1SM["lambda"], cmap=mpl.cm.CMRmap, vmin=0, vmax=0.7)
ax2[1].set_xlabel(r"$\kappa$")
ax2[1].set_xlim([0, 0.7])
ax2[1].set_ylim([122,129])
ax2[1].set_ylabel(r"$m_{h_1}\mathrm{~[GeV]}$")


# In[110]:

from IPython.display import Image

fig = Image(filename=('bm_fig2.png'))
fig


# In[23]:

# plot tan beta values
fig2, ax2 = plt.subplots(nrows=1, ncols=2)
fig2.set_size_inches(24, 6)
plt.subplots_adjust(wspace=0.3)

df["tgbeta"].plot(kind="hist", range=[0,50], bins=50, normed=True, cumulative=False, ax=ax2[0])
ax2[0].set_xlabel(r"$\tan \beta$")
ax2[0].set_ylabel(r"p.d.f.")
ax2[0].set_title(r"Passing all constraints ($\Delta a_{\mu} > 0$)")

df[df.constraints == ""]["tgbeta"].plot(kind="hist", range=[0,50], bins=50, normed=True, cumulative=False, ax=ax2[1])
ax2[1].set_xlabel(r"$\tan \beta$")
ax2[1].set_ylabel(r"p.d.f.")
ax2[1].set_title(r"Passing all constraints ($\Delta a_{\mu} \in [8.77\cdot 10^{-10}, 4.61\cdot 10^{-9}] $)")


# # More $h_2$ stuff

# In[17]:

fig6, ax6 = plt.subplots(ncols=3, nrows=2)
fig6.set_size_inches(24, 12)
fig6.suptitle(r"Passing experimental constraints", fontsize=24)
plt.subplots_adjust(wspace=0.5)

for i, a in enumerate(ax6.reshape(-1)):
    k = params.keys()[i]
    v = params[k]
    
    df.plot(kind=scat, x="mh2", y=k, ax=a)
    a.set_xlim(left=0, right=2000)
    a.set_ylabel(v, fontsize=latex_size)

