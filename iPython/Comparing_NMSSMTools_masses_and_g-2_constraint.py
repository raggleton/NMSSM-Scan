
# coding: utf-8

# This workbook is designed to show the effect when NMSSMTools calculates the Higgs mass with loop corrections. The two sets of parameter points were generated with exactly the same parameter ranges and masses. The only change was in option I4: 0 for "default" and 1 for "Full 1 + 2 loop". From the README:
# 
# ```
# BLOCK MODSEL
# 
# 	8       0               # Precision for Higgs masses (default 0: as before,
# #                                 1: full 1 loop + full 2 loop from top/bot Yukawas
# 
# I4=0: Precision of the CP-even/odd/charged Higgs masses:
#       1-loop: complete contributions ~ top/bottom Yukawas
# 	      contributions ~ g1, g2, lambda and kappa to LLA
# 	      for the SM-like CP-even Higgs only
#       2-loop: top/bottom Yukawa contributions to LLA
# I4=1: as in G. Degrassi, P. Slavich, Nucl.Phys.B825:119-150,2010, 
#       arXiv:0907.4682 (with special thanks to P. Slavich);
#       corrections to the charged Higgs mass from K.H.Phan and P. Slavich:
#       1-loop: complete contributions ~ top/bottom Yukawas
# 	      complete contributions ~g1, g2, lambda and kappa
# 	      (except for pole masses)
#       2-loop: complete contributions ~ top/bottom Yukawas
# 
# ```

# We will require points to pass all constraints, except for the g-2 requirement on $\Delta a_{\mu}$, where we only require $\Delta a_{\mu} > 0$. (see discussion later)
# 
# Range of parameters for these plots:
# 
# - $\tan \beta \in [1.5, 50]$
# 
# - $\mu_{eff} \in [100, 300] ~\mathrm{GeV}$
# 
# - $\lambda \in [0, 0.7]$
# 
# - $\kappa \in [0, 0.7]$
# 
# - $A_{\lambda} \in [-1000, 4000]~\mathrm{GeV}$
# 
# - $A_{\kappa} \in [-30, 2.5]~\mathrm{GeV}$
# 
# 
# And the various masses:
# ```
#  	1	150.D0		# M1 (If =/= M2/2)
# 	2	300.D0		# M2
# 	3	1000.D0		# M3 (If =/= 3*M2)
# 	11	2500.D0		# AU3
# 	12	2500.D0		# AD3
# 	13	2500.D0		# AE3
# 	33	1000.D0		# ML3
# 	36	1000.D0		# ME3
# 	43	1000.D0		# MQ3
# 	46	1000.D0		# MU3
# 	49	1000.D0		# MD3
# ```

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
matplotlib.rcParams.update({'font.size': 24})
matplotlib.rcParams['text.usetex'] = True
matplotlib.rcParams['xtick.major.size'] = 8
matplotlib.rcParams['xtick.major.width'] = 1.5
matplotlib.rcParams['xtick.minor.size'] = 5
matplotlib.rcParams['xtick.minor.width'] = 1.5
matplotlib.rcParams['ytick.minor.size'] = 2
matplotlib.rcParams['ytick.minor.width'] = 1.1
matplotlib.rcParams['ytick.major.size'] = 5
matplotlib.rcParams['ytick.major.width'] = 1.5
matplotlib.rcParams['xtick.labelsize'] = 24
matplotlib.rcParams['ytick.labelsize'] = 24

# latex for axes values
matplotlib.rcParams.update({'font.size': 24, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})

# common plotting variables
scat = "scatter"
latex_size = 25
s_size = 30
alp = 0.3


# In[2]:

# NMSSMTools calculates Higgs mass at LO
folders_LOMass = [
"jobs_50_MICRO_LOMASS_17_Apr_15_0835",
"jobs_50_MICRO_LOMASS_17_Apr_15_0836",
"jobs_50_MICRO_LOMASS_17_Apr_15_0837",
"jobs_50_MICRO_LOMASS_17_Apr_15_0840",
"jobs_50_MICRO_LOMASS_17_Apr_15_0841",
"jobs_50_MICRO_LOMASS_17_Apr_15_0842",
"jobs_50_MICRO_LOMASS_17_Apr_15_2318",
"jobs_50_MICRO_LOMASS_17_Apr_15_2319",
"jobs_50_MICRO_LOMASS_17_Apr_15_2320",
"jobs_50_MICRO_LOMASS_17_Apr_15_2321",
"jobs_50_MICRO_LOMASS_17_Apr_15_2322",
"jobs_50_MICRO_LOMASS_17_Apr_15_2323",
"jobs_50_MICRO_LOMASS_18_Apr_15_0957",
"jobs_50_MICRO_LOMASS_18_Apr_15_0958",
"jobs_50_MICRO_LOMASS_18_Apr_15_0959",
"jobs_50_MICRO_LOMASS_18_Apr_15_1000",
"jobs_50_MICRO_LOMASS_18_Apr_15_1001",
"jobs_50_MICRO_LOMASS_18_Apr_15_1002",
"jobs_50_MICRO_LOMASS_18_Apr_15_1211",
"jobs_50_MICRO_LOMASS_18_Apr_15_1212",
"jobs_50_MICRO_LOMASS_18_Apr_15_1213",
"jobs_50_MICRO_LOMASS_18_Apr_15_1214",
"jobs_50_MICRO_LOMASS_18_Apr_15_1215",
"jobs_50_MICRO_LOMASS_18_Apr_15_1216"
# "jobs_50_MICRO_LOMASS_17_Apr_15_1814",
# "jobs_50_MICRO_LOMASS_17_Apr_15_1815",
# "jobs_50_MICRO_LOMASS_17_Apr_15_1816",
# "jobs_50_MICRO_LOMASS_17_Apr_15_1817",
# "jobs_50_MICRO_LOMASS_17_Apr_15_1818",
# "jobs_50_MICRO_LOMASS_17_Apr_15_1819",
# "jobs_50_MICRO_LOMASS_17_Apr_15_2116",
# "jobs_50_MICRO_LOMASS_17_Apr_15_2117",
# "jobs_50_MICRO_LOMASS_17_Apr_15_2118",
# "jobs_50_MICRO_LOMASS_17_Apr_15_2119",
# "jobs_50_MICRO_LOMASS_17_Apr_15_2120",
# "jobs_50_MICRO_LOMASS_17_Apr_15_2121"
]

# NMSSMTools calculates Higgs mass with corrections
folders = [
# "jobs_50_MICRO_11_Apr_15_0005",
# "jobs_50_MICRO_11_Apr_15_0006",
# "jobs_50_MICRO_11_Apr_15_0007",
# "jobs_50_MICRO_11_Apr_15_0008",
# "jobs_50_MICRO_11_Apr_15_0009",
# "jobs_50_MICRO_11_Apr_15_0010",
# "jobs_50_MICRO_11_Apr_15_0952",
# "jobs_50_MICRO_11_Apr_15_0953",
# "jobs_50_MICRO_11_Apr_15_0957",
# "jobs_50_MICRO_11_Apr_15_1009",
"jobs_50_MICRO_11_Apr_15_1036",
"jobs_50_MICRO_11_Apr_15_1038",
"jobs_50_MICRO_11_Apr_15_1157",
"jobs_50_MICRO_11_Apr_15_1158",
"jobs_50_MICRO_11_Apr_15_1203",
"jobs_50_MICRO_09_Apr_15_2049",
"jobs_50_MICRO_09_Apr_15_2046",
"jobs_50_MICRO_09_Apr_15_2340",
"jobs_50_MICRO_09_Apr_15_2048",
"jobs_50_MICRO_09_Apr_15_1857",
"jobs_50_MICRO_09_Apr_15_1856",
"jobs_50_MICRO_09_Apr_15_2047",
"jobs_50_MICRO_09_Apr_15_1500",
"jobs_50_MICRO_09_Apr_15_1458",
"jobs_50_MICRO_09_Apr_15_1457",
"jobs_50_MICRO_09_Apr_15_1446",
"jobs_50_MICRO_09_Apr_15_1443",
"jobs_50_MICRO_09_Apr_15_2050",
"jobs_50_MICRO_09_Apr_15_2108",
"jobs_50_MICRO_09_Apr_15_2333",
"jobs_50_MICRO_09_Apr_15_2335",
"jobs_50_MICRO_09_Apr_15_2337",
"jobs_50_MICRO_09_Apr_15_2338"
]


# Load files into Panda data frame
def load_df(folders):
    """Load data frame with CSV files from several folders"""
    df_list = []
    df_orig = None
    for fo in folders:
#         print fo
        for fi in glob.glob("/users/robina/Dropbox/4Tau/NMSSM-Scan/data/" + fo + "/output_good*.dat"):
            df_temp = pd.read_csv(fi, delimiter=",")#, keep_default_na=True, na_values="")
            if not df_orig:
                df_orig = df_temp
            else:
                
            df_list.append(df_temp)
    df_orig = pd.concat(df_list)
    return df_orig

df_orig = load_df(folders)
n_orig = len(df_orig.index)

df_orig_loMass = load_df(folders_LOMass)
n_orig_loMass = len(df_orig_loMass.index)

# Fix the constraints column, such that the ones that pass have NaN replaced by something more sensible
df_orig.fillna({"constraints":""}, axis=0, inplace=True)
df_orig_loMass.fillna({"constraints":""}, axis=0, inplace=True)

# Load up the glu-glu cross sections for 13 TeV
cs = pd.read_csv("/Users/robina/Dropbox/4Tau/NMSSM-Scan/iPython/parton_lumi_ratio.csv")
masses = cs["MH [GeV]"].tolist()
xsec_ggf13 = cs["ggF 13TeV cross section [pb]"].tolist()

def find_xsec(mass):
    m = min(range(len(masses)), key=lambda x: abs(masses[x]-mass))
    return xsec_ggf13[m]

# Store SM cross section for gg fusion at 13 TeV for production of m1 and m2
df_orig["xsec_ggf13_h1"] = df_orig.apply(lambda row: find_xsec(row['mh1']), axis=1)
df_orig["xsec_ggf13_h2"] = df_orig.apply(lambda row: find_xsec(row['mh2']), axis=1)
df_orig_loMass["xsec_ggf13_h1"] = df_orig_loMass.apply(lambda row: find_xsec(row['mh1']), axis=1)
df_orig_loMass["xsec_ggf13_h2"] = df_orig_loMass.apply(lambda row: find_xsec(row['mh2']), axis=1)


def store_xsec(df):
    """
    Calculate total cross-section & scaled cross-sections 
    for gg->h1->a1a1, gg->h2->a1a1, gg->h2->h1h1, 
    with final states 4tau, 2b2tau, 4b. 
    Denoted as gg -> X -> YY ->f1f1f2f2
    """
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
                # store scaled total XS * BR
                process_scaled.append(name) 
                df[name] = df[x+"ggrc2"] * df["Br"+x+y+y] * df["Br"+y+f1] * df["Br"+y+f2] * factor
                # store actual XS * BR
                name = name.replace("_scaled", "")
                process.append(name)
                df[name] = df["xsec_ggf13_"+x] * df[x+"ggrc2"] * df["Br"+x+y+y] * df["Br"+y+f1] * df["Br"+y+f2] * factor


store_xsec(df_orig)
store_xsec(df_orig_loMass)
# df_orig[0:5]["constraints"]


# In[5]:

# Make some subsets here:

# subset based on passing all constraints
def pass_all(df):
    """
    return dataframe where points pass all constraints,
     or fail g-2, but have +ve contribution
    """
    pass_all_str = df["constraints"] == ""
    del_a_mu_str = df["constraints"] == r"Muon magn. mom. more than 2 sigma away"
    pass_del_a_mu = df["Del_a_mu"] > 0

    return df[pass_all_str | (del_a_mu_str & pass_del_a_mu)]

df = pass_all(df_orig)
df_loMass = pass_all(df_orig_loMass)
n_total = len(df.index)
n_total_loMass = len(df_loMass.index)


def subset_mass(df, min_mass, max_mass, mass):
    """Make subset based on range of object mass"""
    mass_max = df[mass] < max_mass
    mass_min = df[mass] > min_mass
    return df[mass_min & mass_max]

# subset with 2m_tau < ma1 < 10
df_ma1Lt10 = subset_mass(df, 3.554, 10, "ma1")
df_loMass_ma1Lt10 = subset_mass(df_loMass, 3.554, 10, "ma1")

mhmin = 122.1
mhmax = 128.1

# subset with h1 as h_SM
df_h1SM = subset_mass(df, mhmin, mhmax, "mh1")
df_loMass_h1SM = subset_mass(df_loMass, mhmin, mhmax, "mh1")

# subset with h2 as h_SM
df_h2SM = subset_mass(df, mhmin, mhmax, "mh2")
df_loMass_h2SM = subset_mass(df_loMass, mhmin, mhmax, "mh2")

print "MASS WITH FULL 1+2 LOOPS:"
print "Running over", n_orig, "points"
print n_total, "points passing all constraints (=", 100*n_total/float(n_orig), "%)"
print len(df_ma1Lt10.index), "of these have 2m_tau < ma1 < 10 GeV (=",100*len(df_ma1Lt10.index)/float(n_total), "%)"
print len(df_h1SM.index), "points in the h1 = h(125) subset (=", 100*len(df_h1SM.index)/float(n_total), "%)"
print len(df_h2SM.index), "points in the h2 = h(125) subset (=", 100*len(df_h2SM.index)/float(n_total), "%)"
print ""
print "DEFAULT MASS:"
print "Running over", n_orig_loMass, "points"
print n_total_loMass, "points passing all constraints (=", 100*n_total_loMass/float(n_orig_loMass), "%)"
print len(df_loMass_ma1Lt10.index), "of these have 2m_tau < ma1 < 10 GeV (=",100*len(df_loMass_ma1Lt10.index)/float(n_total_loMass), "%)"
print len(df_loMass_h1SM.index), "points in the h1 = h(125) subset (=", 100*len(df_loMass_h1SM.index)/float(n_total_loMass), "%)"
print len(df_loMass_h2SM.index), "points in the h2 = h(125) subset (=", 100*len(df_loMass_h2SM.index)/float(n_total_loMass), "%)"

# check constraints
# df[10:15].T


# In[6]:

store = pd.HDFStore('store.h5')
store.put('full12loop', df, format='table', data_columns=True)
store.put('default', df_loMass, format='table', data_columns=True)


# In[14]:

def plot_two_hists(var, df1, df2, title1, title2, xlabel, ylabel, same_y=True, **kwargs):
    """function to make 2 side-by-side hists to compare 2 dataframes"""
    fig2, ax2 = plt.subplots(nrows=1, ncols=2)
    fig2.set_size_inches(24, 8)
    plt.subplots_adjust(wspace=0.2)
    
    df1[var].plot(kind="hist", ax=ax2[0], title=title1, **kwargs)
    ax2[0].set_xlabel(xlabel)
    ax2[0].set_ylabel(ylabel)

    df2[var].plot(kind="hist", ax=ax2[1], title=title2, **kwargs)
    ax2[1].set_xlabel(xlabel)
    ax2[1].set_ylabel(ylabel)

    # set range of both y axis to cover smallest minimum, largest maximum
    if same_y:
        miny = min(ax2[0].get_ylim()[0], ax2[1].get_ylim()[0])
        maxy = max(ax2[0].get_ylim()[1], ax2[1].get_ylim()[1])
        for ax in ax2:
            ax.set_ylim([miny, maxy])

    return fig2, ax2


# In[10]:

def plot_two_scatters(varx, vary, df1, df2, title1, title2, xlabel, ylabel, **kwargs):
    """function to make 2 side-by-side scatter plots to compare 2 dataframes"""
    fig2, ax2 = plt.subplots(nrows=1, ncols=2)
    fig2.set_size_inches(24, 8)
    plt.subplots_adjust(wspace=0.2)
    
    df1.plot(kind=scat, x=varx, y=vary, ax=ax2[0], title=title1, **kwargs)
    ax2[0].set_xlabel(xlabel)
    ax2[0].set_ylabel(ylabel)

    df2.plot(kind=scat, x=varx, y=vary, ax=ax2[1], title=title2, **kwargs)
    ax2[1].set_xlabel(xlabel)
    ax2[1].set_ylabel(ylabel)

    return fig2, ax2


# # $m_{h_i}$ distributions

# Note that in the folloing plots, to pass experimental constraints, there is *a* higgs with mass $m_{h} \in [122.1, 128.1] ~\mathrm{GeV}$, however this could be $h_1$ or $h_2$.

# ## $m_{h_1}$

# In[45]:

fig2, ax2 = plot_two_hists("mh1", df_orig, df_orig_loMass, "Full 1+2 loop", "Default", 
               r"$m_{h_1}~\mathrm{[GeV]}$", r"p.d.f.", 
               range=[122,128], bins=30, normed=True, cumulative=False, logy=False)


# Can clearly see that the distributions are very different:
# 
# - __With loop corrections:__ generally prefers a larger higgs mass, although there are only $\sim \frac{1}{5}$ fewer points for $m=122~\mathrm{GeV}$ than $m=128~\mathrm{GeV}$, indicating a reasonable potential for all masses in the range [122, 128]
# 
# - __Without loop corrections:__ prefers a smaller mass, in the range [122, 124], with far fewer points $\gtrsim 124~\mathrm{GeV}$. As mass increases, number of parameter points decreases - the supression is $\mathcal{O}(10^{1}) - \mathcal{O}(10^{2})$.

# ## $m_{h_2}$

# In[46]:

plot_two_hists("mh2", df, df_loMass, "Full 1+2 loop", "Default",
               r"$m_{h_1}~\mathrm{[GeV]}$", ylabel=r"$N$", same_y=False,
               range=[0,2000], bins=30, normed=False, cumulative=False, logy=False, color='green')


# Unlike the distribution of $m_{h_1}$, the distribution of $m_{h_2}$ is far more similar even when including full loop corrections to the mass. 
# 
# 
# __Similarities:__
# 
# - both distriubtions cover a large mass range, up to 2 TeV and beyond
# 
# - both distributions prefer a lower mass $h_2$, around 400 - 500 GeV
# 
# 
# __Differences:__
# 
# - including loop corrections focusses this 'preference' for a $\sim 400 ~\mathrm{GeV}~h_2$ slightly more than in the case without loop corrections 
# 
# - without loop corrections, there is a stronger preference for $h_2 = h_{125}$ (about 3x as much)

# What about in the mass range [122,128]:

# In[72]:

fig, ax = plot_two_hists("mh2", df, df_loMass, "Full 1+2 loop", "Default", 
                       r"$m_{h_1}~\mathrm{[GeV]}$", r"$N$", same_y=False,
                       range=[122,128], bins=30, normed=False, cumulative=False, logy=False, color='green')
fig.suptitle(r"$h_{SM} = h_1\mathrm{~or~}h_2$", )


# ## $m_{a_1}$

# In[48]:

fig2, ax2 = plot_two_hists("ma1", df, df_loMass, "Full 1+2 loop", "Default", 
               r"$m_{h_1}~\mathrm{[GeV]}$", r"$N$", same_y=False,
               range=[0,100], bins=20, normed=False, cumulative=False, logy=False, color='purple')


# Again, there are few differences in the distribution of $m_{a_1}$, with both scenarios prefering a heavier $a_1$, especially above 60 GeV.

# Let's look at the low mass region in more detail:

# In[49]:

plot_two_hists("ma1", df, df_loMass, "Full 1+2 loop", "Default",
               r"$m_{a_1}~\mathrm{[GeV]}$", r"p.d.f. per 0.5 GeV bin", 
               range=[0,10], bins=20, cumulative=False, normed=True, color='purple')


# Note that, while it appears that running with loop corrections gives a larger fraction of $m_{a_1} \in [3.5, 10]~\mathrm{GeV}$ range, the statistical errors here are large - of order $\sqrt{40} \simeq 6 - 7$ points.

# # Replicate Bomark/Moretti/et al plots

# Figure 2 from the paper (arxiv 1409.8393): case where $h_1 = h_{SM}$

# In[50]:

fig4, ax4 = plt.subplots(nrows=2, ncols=2)
fig4.set_size_inches(24, 14)
plt.subplots_adjust(wspace=0.3)

import matplotlib as mpl

fig4.suptitle(r"$h_{SM} = h_1$", fontsize=30)
df_h1SM.plot(kind="scatter", x="ma1", y="mh1", marker="+", ax=ax4[0][0], c=df_h1SM.tgbeta, 
             cmap=mpl.cm.cool, vmin=0, vmax=50, title="Full 1+2 loop corrections")
ax4[0][0].set_xlim([0, 150])
ax4[0][0].set_ylim([122,129])
ax4[0][0].set_xlabel(r"$m_{a_1}\mathrm{~[GeV]}$")
ax4[0][0].set_ylabel(r"$m_{h_1}\mathrm{~[GeV]}$")

df_h1SM.plot(kind="scatter", x="kappa", y="mh1", marker="+", ax=ax4[0][1], c=df_h1SM["lambda"], 
             cmap=mpl.cm.cool, vmin=0, vmax=0.7, title="Full 1+2 loop corrections")
ax4[0][1].set_xlim([0, 0.7])
ax4[0][1].set_ylim([122,129])
ax4[0][1].set_xlabel(r"$\kappa$")
ax4[0][1].set_ylabel(r"$m_{h_1}\mathrm{~[GeV]}$")

df_loMass_h1SM.plot(kind="scatter", x="ma1", y="mh1", marker="+", ax=ax4[1][0], c=df_loMass_h1SM.tgbeta, 
                    cmap=mpl.cm.cool, vmin=0, vmax=50, title="Default")
ax4[1][0].set_xlim([0, 150])
ax4[1][0].set_ylim([122,129])
ax4[1][0].set_xlabel(r"$m_{a_1}\mathrm{~[GeV]}$")
ax4[1][0].set_ylabel(r"$m_{h_1}\mathrm{~[GeV]}$")

df_loMass_h1SM.plot(kind="scatter", x="kappa", y="mh1", marker="+", ax=ax4[1][1], c=df_loMass_h1SM["lambda"], 
                    cmap=mpl.cm.cool, vmin=0, vmax=0.7, title="Default")
ax4[1][1].set_xlim([0, 0.7])
ax4[1][1].set_ylim([122,129])
ax4[0][1].set_xlabel(r"$\kappa$")
ax4[1][1].set_ylabel(r"$m_{h_1}\mathrm{~[GeV]}$")


# In[51]:

from IPython.display import Image

fig = Image(filename=('bm_fig2.png'))
fig


# We can expand our requirement on $h_{125}$ to include the points where $h_{125} = h_2$ as well.

# In[76]:

fig4, ax4 = plt.subplots(nrows=2, ncols=2)
fig4.set_size_inches(24, 14)
plt.subplots_adjust(wspace=0.3, hspace=0.5)

import matplotlib as mpl

fig4.suptitle(r"$h_{SM} = h_1 \mathrm{~or~} h_2$", fontsize=30)
df.plot(kind="scatter", x="ma1", y="mh1", marker="+", ax=ax4[0][0], c=df.tgbeta, 
             cmap=mpl.cm.cool, vmin=0, vmax=50, title="Full 1+2 loop corrections")
ax4[0][0].set_xlim([0, 150])
ax4[0][0].set_ylim([20,130])
ax4[0][0].set_xlabel(r"$m_{a_1}\mathrm{~[GeV]}$")
ax4[0][0].set_ylabel(r"$m_{h_1}\mathrm{~[GeV]}$")

df.plot(kind="scatter", x="kappa", y="mh1", marker="+", ax=ax4[0][1], c=df["lambda"], 
             cmap=mpl.cm.cool, vmin=0, vmax=0.7, title="Full 1+2 loop corrections")
ax4[0][1].set_xlim([0, 0.7])
ax4[0][1].set_ylim([20,130])
ax4[0][1].set_xlabel(r"$\kappa$")
ax4[0][1].set_ylabel(r"$m_{h_1}\mathrm{~[GeV]}$")

df_loMass.plot(kind="scatter", x="ma1", y="mh1", marker="+", ax=ax4[1][0], c=df_loMass.tgbeta, 
                    cmap=mpl.cm.cool, vmin=0, vmax=50, title="Default")
ax4[1][0].set_xlim([0, 150])
ax4[1][0].set_ylim([20,130])
ax4[1][0].set_xlabel(r"$m_{a_1}\mathrm{~[GeV]}$")
ax4[1][0].set_ylabel(r"$m_{h_1}\mathrm{~[GeV]}$")

df_loMass.plot(kind="scatter", x="kappa", y="mh1", marker="+", ax=ax4[1][1], c=df_loMass["lambda"], 
                    cmap=mpl.cm.cool, vmin=0, vmax=0.7, title="Default")
ax4[1][1].set_xlim([0, 0.7])
ax4[1][1].set_ylim([20,130])
ax4[0][1].set_xlabel(r"$\kappa$")
ax4[1][1].set_ylabel(r"$m_{h_1}\mathrm{~[GeV]}$")


# # $\tan\beta$ distributions & the g-2 constraint

# The reference paper has a lot of points with small $\tan\beta$, whilst my previous scans did not. After discussion, it was noted that my previous scans constrained the g-2 contribution to be within a certain set of values, whilst the reference paper includes all points that make a +ve contribution to g-2. From literature, it has been noted that there is a strong connection between value of $\tan \beta$ and the 2-loop contribution to $a_{\mu}$. Below we can see that by requiring the contribution to be within certain bounds, we effectively remove all $\tan\beta$ values below $\sim 17$. 
# 
# 
# Note that points satisfy all other experimenta constraints (incl. relic density as calcualted by MicrOMEGAs), and thus there is a Higgs with mass in the range [122, 128] GeV. The $a_1$ mass is not constrained.

# The NMSSM contribution can be important at 2-loop level, with the main contribution from the "Bar-Zee" diagram:

# In[68]:

Image(url='https://inspirehep.net/record/1085333/files/Barr-Zee-3.png')


# Literature on g-2 wrt NMSSM:
# 
# - http://arxiv.org/abs/0808.2509
# - http://arxiv.org/abs/hep-ph/0208076
# - http://arxiv.org/abs/hep-ph/0103183
# - http://arxiv.org/abs/hep-ph/0009292
# - http://arxiv.org/abs/hep-ph/0609168

# In[53]:

plot_two_hists("tgbeta", df, df[df.constraints == ""], 
               r"$\Delta a_{\mu} > 0$", 
               r"$\Delta a_{\mu} \in [8.77\cdot 10^{-10}, 4.61\cdot 10^{-9}] $", 
               r"$\tan\beta$", r"$N$", range=[0,50], bins=25, cumulative=False, normed=False)


# In[54]:

fig2, ax2 = plot_two_scatters("ma1", "tgbeta", df, df[df.constraints == ""], 
                              r"$\Delta a_{\mu} > 0$", 
                              r"$\Delta a_{\mu} \in [8.77\cdot 10^{-10}, 4.61\cdot 10^{-9}] $", 
                              r"$m_{a_1}~\mathrm{[GeV]}$", r"$\tan \beta$",
                              color='purple', alpha=0.3)
fig2.suptitle("Full 1+2 loop corrections", fontsize=30)
for ax in ax2:
    ax.set_ylim(bottom=0)
    ax.set_xlim(left=0, right=100)


# We'll plot points that have $\Delta a_{\mu}$ but where it isn't large enough (or too large)

# In[55]:

ax = df[df.constraints != ""].plot(kind=scat, color='purple', alpha=0.3, x="ma1", y="tgbeta", 
                                   title=r"$\Delta a_{\mu} > 0$ but outside $[8.77\cdot 10^{-10}, 4.61\cdot 10^{-9}]$")
ax.set_xlabel(r"$m_{a_1}~\mathrm{[GeV]}$")
ax.set_ylabel(r"$\tan \beta$")
ax.set_ylim(bottom=0, top=50)
ax.set_xlim(left=0, right=105)


# We can repeat these plots when we don't include extra loop mass corrections, however the changes are minimal.

# In[56]:

fig2, ax2 = plot_two_scatters("ma1", "tgbeta", df_loMass, df_loMass[df_loMass.constraints == ""], 
                              r"$\Delta a_{\mu} > 0$", 
                              r"$\Delta a_{\mu} \in [8.77\cdot 10^{-10}, 4.61\cdot 10^{-9}] $", 
                              r"$m_{a_1}~\mathrm{[GeV]}$", r"$\tan \beta$",
                              alpha=0.3)
fig2.suptitle("Default", fontsize=30)
for ax in ax2:
    ax.set_ylim(bottom=0, top=50)
    ax.set_xlim(left=0, right=105)


# In[57]:

ax = df_loMass[df_loMass.constraints != ""].plot(kind=scat, alpha=0.3, x="ma1", y="tgbeta", 
                                    title=r"$\Delta a_{\mu} > 0$ but outside $[8.77\cdot 10^{-10}, 4.61\cdot 10^{-9}]$")
ax.set_xlabel(r"$m_{a_1}~\mathrm{[GeV]}$")
ax.set_ylabel(r"$\tan \beta$")
ax.set_ylim(bottom=0, top=50)
ax.set_xlim(left=0, right=105)


# We can see how the other input parameters affect the passing of this constraint:

# In[58]:

fig2, ax2 = plot_two_scatters("ma1", "mueff", df, df[df.constraints == ""], 
                              r"$\Delta a_{\mu} > 0$", 
                              r"$\Delta a_{\mu} \in [8.77\cdot 10^{-10}, 4.61\cdot 10^{-9}] $", 
                              r"$m_{a_1}~\mathrm{[GeV]}$", 
                              r"$\mu_{eff}$",
                              color='orange', alpha=0.3)
fig2.suptitle("Full 1+2 loop corrections", fontsize=30)
for ax in ax2:
    ax.set_ylim(top=300)
    ax.set_xlim(left=0, right=105)


# Note that the strong 'bands' here are due to the relic density constraint - in previous scans without running MicrOMEGAs, I got a continuum of points in the range [100,300]

# In[59]:

fig2, ax2 = plot_two_scatters("ma1", "kappa", df, df[df.constraints == ""], 
                              r"$\Delta a_{\mu} > 0$", 
                              r"$\Delta a_{\mu} \in [8.77\cdot 10^{-10}, 4.61\cdot 10^{-9}] $", 
                              r"$m_{a_1}~\mathrm{[GeV]}$", 
                              r"$\kappa$",
                              color='salmon', alpha=0.3)
fig2.suptitle("Full 1+2 loop corrections", fontsize=30)
for ax in ax2:
    ax.set_ylim(bottom=0)
    ax.set_xlim(left=0, right=105)


# In[60]:

fig2, ax2 = plot_two_scatters("ma1", "lambda", df, df[df.constraints == ""], 
                              r"$\Delta a_{\mu} > 0$", 
                              r"$\Delta a_{\mu} \in [8.77\cdot 10^{-10}, 4.61\cdot 10^{-9}] $", 
                              r"$m_{a_1}~\mathrm{[GeV]}$", 
                              r"$\lambda$",
                              color='royalblue', alpha=0.3)
fig2.suptitle("Full 1+2 loop corrections", fontsize=30)
for ax in ax2:
    ax.set_ylim(bottom=0, top=0.7)
    ax.set_xlim(left=0, right=105)


# In[61]:

fig2, ax2 = plot_two_scatters("ma1", "akappa", df, df[df.constraints == ""], 
                              r"$\Delta a_{\mu} > 0$", 
                              r"$\Delta a_{\mu} \in [8.77\cdot 10^{-10}, 4.61\cdot 10^{-9}] $", 
                              r"$m_{a_1}~\mathrm{[GeV]}$", 
                              r"$A_{\kappa}$",
                              color='orchid', alpha=0.3)
fig2.suptitle("Full 1+2 loop corrections", fontsize=30)
for ax in ax2:
#     ax.set_ylim(bottom=0)
    ax.set_xlim(left=0, right=105)


# In[62]:

fig2, ax2 = plot_two_scatters("ma1", "alambda", df, df[df.constraints == ""], 
                              r"$\Delta a_{\mu} > 0$", 
                              r"$\Delta a_{\mu} \in [8.77\cdot 10^{-10}, 4.61\cdot 10^{-9}] $", 
                              r"$m_{a_1}~\mathrm{[GeV]}$", 
                              r"$A_{\lambda}$",
                              color='coral', alpha=0.3)
fig2.suptitle("Full 1+2 loop corrections", fontsize=30)
for ax in ax2:
    ax.set_ylim(top=4000, bottom=-1000)
    ax.set_xlim(left=0, right=105)


# Perhaps $A_{\lambda}$ is correlated with the size of $\Delta a_{\mu}$?

# In[63]:

ax = df[df.constraints != ""].plot(kind=scat, color='coral', alpha=0.3, x="ma1", y="alambda", 
                                   title=r"$\Delta a_{\mu} > 0$ but outside $[8.77\cdot 10^{-10}, 4.61\cdot 10^{-9}]$")
ax.set_xlabel(r"$m_{a_1}~\mathrm{[GeV]}$")
ax.set_ylabel(r"$A_{\lambda}$")
ax.set_ylim(top=4000, bottom=-1000)
ax.set_xlim(left=0, right=105)


# So it appears that $A_{\lambda}$ isn't directly correlated with the size of $\Delta a_{\mu}$

# In[63]:




# In[ ]:



