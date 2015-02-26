
# coding: utf-8

# In[111]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
from itertools import product as itprod

# to show plots:
get_ipython().magic(u'pylab inline')

pd.set_option('display.max_colwidth', 100) # stop putting in the ...

pylab.rcParams['figure.figsize'] = (9.0, 6.0)  # default size of plots
# matplotlib.rcParams.update({'font.size': 20})
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
matplotlib.rcParams.update({'font.size': 20, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})

# common plotting variables
scat = "scatter"
latex_size = 25
s_size = 30
alp = 0.3


# In[46]:

dep_kappa = False # for alternate set with kappa set by 0 < mueff*kappa/lambda < 200

folders = []
if dep_kappa:
    folders = [
            "output_jobs_depKappa_21_Feb_15_1326.dat",
            "output_jobs_depKappa_21_Feb_15_1327.dat",
            "output_jobs_depKappa_21_Feb_15_1349.dat",
            "output_jobs_depKappa_23_Feb_15_1550.dat",
            "output_jobs_depKappa_23_Feb_15_1554.dat",
            "output_jobs_depKappa_23_Feb_15_2150.dat",
            "output_jobs_depKappa_23_Feb_15_2151.dat"
            ]
else:
    # default set with 0 < kappa < 1
    folders = [
            "jobs_50_20_Feb_15_1256",
            "jobs_50_20_Feb_15_1520",
            "jobs_50_20_Feb_15_1613",
            "jobs_50_20_Feb_15_1739",
            "jobs_50_23_Feb_15_1738",
            "jobs_50_23_Feb_15_2023",
            "jobs_50_23_Feb_15_2027",
            "jobs_50_23_Feb_15_2059",
            "jobs_50_25_Feb_15_1010",
            "jobs_50_25_Feb_15_1706"
#             "jobs_50_25_Feb_15_1710"
#             "jobs_50_25_Feb_15_1008"
            ]
    
# Load files into Panda data frame
df_list = []
for fo in folders:
    print fo
    for fi in glob.glob("/users/robina/Dropbox/4Tau/NMSSM-Scan/" + fo + "/output*.dat"):
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


# In[47]:

# Make some subsets here:

# subset based on passing all constraints
pass_all_str = df_orig["constraints"] == ""
df = df_orig[pass_all_str] # passes all constraints
n_total = len(df.index)

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

# check constraints are empty
# df[10:15].T


# In[5]:

# NMSSM params with latex equivalents for axis labels
params = {"lambda":r"$\lambda$", "mueff":r"$\mu_{eff} \mathrm{~[GeV]}$", "kappa":r"$\kappa$", 
          "alambda":r"$A_{\lambda} \mathrm{~[GeV]}$", "akappa":r"$A_{\kappa} \mathrm{~[GeV]}$", "tgbeta":r"$\tan\beta$"}


## $BR(h_1/a_1 \to f\bar{f})$ Vs $m_{a_1}$

# Let's look at the BR for several final states - $\tau\tau$, $\mu\mu$, $bb$.

# In[70]:

finals = {"mumu": dict(shape="o", label=r"$,~f\bar{f} = \mu^-\mu^+$", color="forestgreen"), 
          "bb": dict(shape="s", label=r"$,~f\bar{f} = b\bar{b}$", color="crimson"),
          "tautau": dict(shape="p", label=r"$,~f\bar{f} = \tau^-\tau^+$", color="dodgerblue") 
          }

fig4, ax4 = plt.subplots(nrows=1, ncols=3)
fig4.set_size_inches(24, 10)
plt.subplots_adjust(wspace=0.3)

for i, a in enumerate(ax4.reshape(-1)):
    for fin in finals:
        df.plot(kind="scatter", x="ma1", y="Bra1"+fin, s=70, alpha=0.5, ax=a, label=r"$X = a_1$"+finals[fin]["label"], color=finals[fin]["color"], marker=finals[fin]["shape"])
#         df.plot(kind="scatter", x="mh1", y="Brh1"+fin, s=90, alpha=1, ax=a, label=r"$X = h_1$"+finals[fin]["label"], color=finals[fin]["color"], marker=finals[fin]["shape"])
    a.set_xlabel(r"$m_{X}~\mathrm{[GeV]}$", fontsize=latex_size)
    a.set_ylabel(r"$BR(X\to\/f\bar{f})$", fontsize=latex_size)    
    
# Overall plot on left
ax4[0].set_xlim([0, 100])
ax4[0].set_ylim([-0.05, 1.4])
# ax4[0].set_yscale("log")

# Zoomed in center plot
ax4[1].set_xlim([2, 12])
ax4[1].set_ylim([0.75, 1.02])

# Zoomed in right plot
ax4[2].set_xlim([20, 60])
ax4[2].set_ylim([0, 1.3])


## Experimental Constraints

# Let's look at what constraints are the most common, and how they affect several interesting observeables. First, all points altogether:

# In[198]:

def plot_constraints(df, title):
    # This plots a bar chart of the most popular reasons 
    # for points failing experimental constraints, in a given DataFrame.
    # It will plot the top X% of reasons (see below)
    
    c = df["constraints"].tolist()
    cons = []
    for cc in c:
        if cc:
            for p in cc.split("/"):
                p = "$\mathrm{"+p+"}$"
                p = p.replace(r"_", r"\_")
                p = p.replace(r"_s", r"\_{s}")
                p = p.replace(r"_d", r"\_{d}")
                p = p.replace(r">>", r"\gg")
                p = p.replace(r"->", r"\to")
#                 p = p.replace(r">", r"\gt")
                p = p.replace(r" ", r"~")
                p = p.replace(r"~~~", r"~")
                p = p.replace(r"~~", r"~")
                p = p.replace(r"to", r"to ")
                p = p.replace(r"chi2", r"}\chi^2 \mathrm{")
                p = p.replace(r"Delta", r"}\Delta \mathrm{")
                p = p.replace(r"Msusy", r"M_{SUSY}")
                p = p.replace(r"MGUT", r"M_{GUT}")
                cons.append(p)

    # use Counter?
#     from collections import Counter
#     count = Counter(cons)

    # use Series
    s = pd.Series(cons)
    vc = s.value_counts(normalize=True)
    vc_cum = vc.cumsum()
    # find out how many points make up the top X%
    last_i = next(x[0] for x in enumerate(vc_cum) if x[1] > 0.9) 

    fig, ax = plt.subplots(nrows=1, ncols=1)
    fig.set_size_inches(8, 6)
    vc[:last_i].plot(kind="barh")
    ax.set_xlabel(r"Fraction of failing points that fail given experimental constraint")
    ax.set_title(title)
    return ax

plot_constraints(df_orig, "All scanned points")


# Now for the subset where $h_2 = h_{SM}$ (i.e. why aren't there more points with $h_2 = h_{SM}$. Note that even *prior* to applying experimental constraints, a very small fraction of generated points have $h_2 = h_{SM}, \sim 0.4\%$, so there is more to investigate.

# In[50]:

# subset where h2 = hSM (no experimental constraints applied)
df_h2SM_all = df_orig[(df_orig["mh2"] < mhmax) & (df_orig["mh2"] > mhmin)]
print len(df_h2SM_all.index), "=", 100*len(df_h2SM_all.index)/float(n_orig), "% of ALL points"

plot_constraints(df_h2SM_all, r"Subset where $h_2 = h_{SM}$")


# And same for $h_1 = h_{SM}$:

# In[72]:

# subset where h1 = hSM (no experimental constraints applied)
df_h1SM_all = df_orig[(df_orig["mh1"] < mhmax) & (df_orig["mh1"] > mhmin)]
print len(df_h1SM_all.index), "=", 100*len(df_h1SM_all.index)/float(n_orig), "% of ALL points"
plot_constraints(df_h1SM_all, r"Subset where $h_1 = h_{SM}$")


# Out of curiosity, why do points with $2m_{\tau} < m_{a_1} < 2m_b$ fail?

# In[73]:

# subset where 3.5 < ma1 < 10
plot_constraints(df_ma1Lt10_all, r"Subset where $2m_{\tau} < m_{a_1} < 10$")


## Rates for $4\tau/2b2\tau/4b$ at $\sqrt{s} = 13\mathrm{~TeV}$

# Here we look at the total reduced $\sigma \times BR$ and absolute $\sigma \times BR$ for $X\to YY\ \to 4\tau / 2\tau2b / 4b$ for several scenarios:
# 
# - passing all experimental constraints
# 
# - passing all experimental constraints AND requiring $X=h_{SM}$
# 
# - no requirement that there must be a Higgs in mass range [122,128] GeV
# 
# Note that in the calulation of the $2b2\tau$ final state, there is an additional factor of 2 from combinatorics.
# 

# In[11]:

# make a subset where m_a1 > 10 GeV
df_ma1Gt10 = df[df.ma1 > 10.]
print len(df_ma1Gt10.index), "points where m_a1 > 10 GeV (=", 100*len(df_ma1Gt10.index)/float(n_total), "%)"


### Passing all experimental constraints

# In[74]:

fig3, ax3 = plt.subplots(nrows=1, ncols=3)
fig3.set_size_inches(24, 8)
plt.subplots_adjust(wspace=0.3)

final_states = ["4tau", "2b2tau", "4b"]
dd = df
for i,a in enumerate(ax3):
    dd.plot(kind="scatter", y=r"xsec_scaled_h2_2a1_"+final_states[i], x="ma1", s=s_size, alpha=0.5, ax=a, color="blueviolet", label=r"$X = h_2, Y = a_1$")
    dd.plot(kind="scatter", y=r"xsec_scaled_h1_2a1_"+final_states[i], x="ma1", s=s_size, alpha=0.5, ax=a, color="deepskyblue", label=r"$X = h_1, Y = a_1$")
    dd.plot(kind="scatter", y=r"xsec_scaled_h2_2h1_"+final_states[i], x="mh1", s=s_size, ax=a, color="fuchsia", label=r"$X = h_2, Y = h_1$")
    if final_states[i] == "4tau":
        fs = r"BR(YY \to 4\tau)$"
    elif final_states[i] == "2b2tau":
        fs = r"BR(YY \to 2b2\tau)$"
    else:
        fs = r"BR(YY \to 4b)$"
    a.set_ylabel(r"$\frac{\sigma(gg \to X)}{\sigma_{SM}(gg \to X)} \cdot BR(X\to YY) \cdot "+fs, fontsize=latex_size)
    a.set_xlabel(r"$m_Y \mathrm{~[GeV]}$", fontsize=latex_size)
    a.set_yscale("log")
    a.set_ylim(bottom=1E-7, top=75)
    a.set_xlim([2,135])
    a.legend(loc='best', fancybox=True, framealpha=0.5)


# In[75]:

fig3, ax3 = plt.subplots(nrows=1, ncols=3)
fig3.set_size_inches(24, 8)
plt.subplots_adjust(wspace=0.3)

final_states = ["4tau", "2b2tau", "4b"]
dd = df
for i,a in enumerate(ax3):
    dd.plot(kind="scatter", y=r"xsec_h2_2a1_"+final_states[i], x="ma1", s=s_size, alpha=0.5, ax=a, color="blueviolet", label=r"$X = h_2, Y = a_1$")
    dd.plot(kind="scatter", y=r"xsec_h1_2a1_"+final_states[i], x="ma1", s=s_size, alpha=0.5, ax=a, color="deepskyblue", label=r"$X = h_1, Y = a_1$")
    dd.plot(kind="scatter", y=r"xsec_h2_2h1_"+final_states[i], x="mh1", s=s_size, ax=a, color="fuchsia", label=r"$X = h_2, Y = h_1$")
    if final_states[i] == "4tau":
        fs = r"BR(YY \to 4\tau)\mathrm{~[pb]}$"
    elif final_states[i] == "2b2tau":
        fs = r"BR(YY \to 2b2\tau)\mathrm{~[pb]}$"
    else:
        fs = r"BR(YY \to 4b) \mathrm{~[pb]}$"
    a.set_ylabel(r"$\sigma(gg \to X) \cdot BR(X\to YY) \cdot "+fs, fontsize=latex_size)
    a.set_xlabel(r"$m_Y \mathrm{~[GeV]}$", fontsize=latex_size)
    a.set_yscale("log")
    a.set_ylim(bottom=1E-7, top=5E2)
    a.set_xlim([2,135])
    a.legend(loc='best', fancybox=True, framealpha=0.7)


### Passing all experimental constraints AND requiring $X = h_{SM}$

# In[85]:

fig3, ax3 = plt.subplots(nrows=1, ncols=3)
fig3.set_size_inches(24, 8)
plt.subplots_adjust(wspace=0.3)

final_states = ["4tau", "2b2tau", "4b"]
dd = df
for i,a in enumerate(ax3):
    dd[(dd.mh1 < mhmax) & (dd.mh1> mhmin)].plot(kind="scatter", y=r"xsec_scaled_h1_2a1_"+final_states[i], x="ma1", s=s_size, alpha=1, ax=a, color="deepskyblue", label=r"$X_{125} = h_1, Y = a_1$")
    dd[(dd.mh2 < mhmax) & (dd.mh2 > mhmin)].plot(kind="scatter", y=r"xsec_scaled_h2_2a1_"+final_states[i], x="ma1", s=s_size, alpha=1, ax=a, color="blueviolet", label=r"$X_{125} = h_2, Y = a_1$")
    dd[(dd.mh2 < mhmax) & (dd.mh2 > mhmin)].plot(kind="scatter", y=r"xsec_scaled_h2_2h1_"+final_states[i], x="mh1", s=s_size, ax=a, color="fuchsia", label=r"$X_{125} = h_2, Y = h_1$")
    if final_states[i] == "4tau":
        fs = r"BR(YY \to 4\tau)$"
    elif final_states[i] == "2b2tau":
        fs = r"BR(YY \to 2b2\tau)$"
    else:
        fs = r"BR(YY \to 4b)$"
    a.set_ylabel(r"$\frac{\sigma(gg \to X_{125})}{\sigma_{SM}(gg \to X_{125})} \cdot BR(X_{125}\to YY) \cdot "+fs, fontsize=latex_size)
    a.set_xlabel(r"$m_Y \mathrm{~[GeV]}$", fontsize=latex_size)
    a.set_yscale("log")
    a.set_ylim(bottom=1E-7, top=75)
    a.set_xlim([2,135])
    a.legend(loc='best', fancybox=True, framealpha=0.5)


# In[86]:

fig3, ax3 = plt.subplots(nrows=1, ncols=3)
fig3.set_size_inches(24, 8)
plt.subplots_adjust(wspace=0.3)

final_states = ["4tau", "2b2tau", "4b"]
dd = df
for i,a in enumerate(ax3):
    dd[(dd.mh1 < mhmax) & (dd.mh1> mhmin)].plot(kind="scatter", y=r"xsec_h1_2a1_"+final_states[i], x="ma1", s=s_size, ax=a, color="deepskyblue", label=r"$X_{125} = h_1, Y = a_1$")
    dd[(dd.mh2 < mhmax) & (dd.mh2 > mhmin)].plot(kind="scatter", y=r"xsec_h2_2a1_"+final_states[i], x="ma1", s=s_size, ax=a, color="blueviolet", label=r"$X_{125} = h_2, Y = a_1$")
    dd[(dd.mh2 < mhmax) & (dd.mh2 > mhmin)].plot(kind="scatter", y=r"xsec_h2_2h1_"+final_states[i], x="mh1", s=s_size, ax=a, color="fuchsia", label=r"$X_{125} = h_2, Y = h_1$")
    if final_states[i] == "4tau":
        fs = r"BR(YY \to 4\tau)\mathrm{~[pb]}$"
    elif final_states[i] == "2b2tau":
        fs = r"BR(YY \to 2b2\tau)\mathrm{~[pb]}$"
    else:
        fs = r"BR(YY \to 4b) \mathrm{~[pb]}$"
    a.set_ylabel(r"$\sigma(gg \to X_{125}) \cdot BR(X_{125}\to YY) \cdot "+fs, fontsize=latex_size)
    a.set_xlabel(r"$m_Y \mathrm{~[GeV]}$", fontsize=latex_size)
    a.set_yscale("log")
    a.set_ylim(bottom=1E-7, top=5E2)
    a.set_xlim([2,135])
    a.legend(loc='best', fancybox=True, framealpha=0.7)


### No requirement of a Higgs in the mass range [122,128] GeV ( & fail $\chi^2 (h\to gg/bb/ZZ) > 6.18$)

# Make the correct subset and check:

# In[78]:

# find subset where on constraint failing is No Higgs in the 122.1-128.1 GeV mass range and no chi2 on H->bb/gg/ZZ
dd = df_orig
chi2_test = (dd["constraints"].str.match("chi2\(H->[bgZ]{2}\) >   6.18"))
higgs_test = (dd["constraints"].str.match("No Higgs in the 122.1-128.1 GeV mass range"))
dd = dd[higgs_test | chi2_test]
print len(dd.index), "points failing No Higgs in the 122.1-128.1 GeV mass range/chi2(H->gg/bb/ZZ) constraints (=", 100*len(dd.index)/float(n_orig) ,"% of ALL points)"
pd.set_option("display.colheader_justify", "left")
# dd[0:10]["constraints"] # check matches worked


# In[79]:

fig3, ax3 = plt.subplots(nrows=1, ncols=3)
fig3.set_size_inches(24, 8)
plt.subplots_adjust(wspace=0.3)

final_states = ["4tau", "2b2tau", "4b"]

for i,a in enumerate(ax3):
    dd.plot(kind="scatter", y=r"xsec_scaled_h1_2a1_"+final_states[i], x="ma1", s=s_size, alpha=1, ax=a, color="deepskyblue", label=r"$X = h_1, Y = a_1$")
    dd.plot(kind="scatter", y=r"xsec_scaled_h2_2a1_"+final_states[i], x="ma1", s=s_size, alpha=0.6, ax=a, color="blueviolet", label=r"$X = h_2, Y = a_1$")
    dd.plot(kind="scatter", y=r"xsec_scaled_h2_2h1_"+final_states[i], x="mh1", s=s_size, ax=a, color="fuchsia", label=r"$X = h_2, Y = h_1$")
    if final_states[i] == "4tau":
        fs = r"BR(YY \to 4\tau)$"
    elif final_states[i] == "2b2tau":
        fs = r"BR(YY \to 2b2\tau)$"
    else:
        fs = r"BR(YY \to 4b)$"
    a.set_ylabel(r"$\frac{\sigma(gg \to X)}{\sigma_{SM}(gg \to X)} \cdot BR(X\to YY) \cdot "+fs, fontsize=latex_size)
    a.set_xlabel(r"$m_Y \mathrm{~[GeV]}$", fontsize=latex_size)
    a.set_yscale("log")
    a.set_ylim(bottom=1E-7, top=75)
    a.set_xlim([2,135])
    a.legend(loc='best', fancybox=True, framealpha=0.6)


# In[199]:

fig3, ax3 = plt.subplots(nrows=1, ncols=3)
fig3.set_size_inches(24, 8)
plt.subplots_adjust(wspace=0.3)

final_states = ["4tau", "2b2tau", "4b"]

for i,a in enumerate(ax3):
    dd.plot(kind="scatter", y=r"xsec_h1_2a1_"+final_states[i], x="ma1", s=s_size, ax=a, color="deepskyblue", label=r"$X = h_1, Y = a_1$")
    dd.plot(kind="scatter", y=r"xsec_h2_2a1_"+final_states[i], x="ma1", s=s_size, ax=a, color="blueviolet", label=r"$X = h_2, Y = a_1$")
    dd.plot(kind="scatter", y=r"xsec_h2_2h1_"+final_states[i], x="mh1", s=s_size, ax=a, color="fuchsia", label=r"$X = h_2, Y = h_1$")
    if final_states[i] == "4tau":
        fs = r"BR(YY \to 4\tau)\mathrm{~[pb]}$"
    elif final_states[i] == "2b2tau":
        fs = r"BR(YY \to 2b2\tau)\mathrm{~[pb]}$"
    else:
        fs = r"BR(YY \to 4b) \mathrm{~[pb]}$"
    a.set_ylabel(r"$\sigma(gg \to X) \cdot BR(X\to YY) \cdot "+fs, fontsize=latex_size)
    a.set_xlabel(r"$m_Y \mathrm{~[GeV]}$", fontsize=latex_size)
    a.set_yscale("log")
    a.set_ylim(bottom=1E-7, top=5E2)
    a.set_xlim([2,135])
    a.legend(loc='best', fancybox=True, framealpha=0.8)


# Note that there is an odd cutoff at around $m_Y \sim 128.5\mathrm{~GeV}$, implying some limit on $m_X$. Plot rate vs $m_X$ instead::

# In[80]:

fig3, ax3 = plt.subplots(nrows=1, ncols=3)
fig3.set_size_inches(24, 8)
plt.subplots_adjust(wspace=0.3)

final_states = ["4tau", "2b2tau", "4b"]

for i,a in enumerate(ax3):
    dd.plot(kind="scatter", y=r"xsec_scaled_h1_2a1_"+final_states[i], x="mh1", s=s_size, alpha=1, ax=a, color="deepskyblue", label=r"$X = h_1, Y = a_1$")
    dd.plot(kind="scatter", y=r"xsec_scaled_h2_2a1_"+final_states[i], x="mh2", s=s_size, alpha=0.6, ax=a, color="blueviolet", label=r"$X = h_2, Y = a_1$")
    dd.plot(kind="scatter", y=r"xsec_scaled_h2_2h1_"+final_states[i], x="mh2", s=s_size, ax=a, color="fuchsia", label=r"$X = h_2, Y = h_1$")
    if final_states[i] == "4tau":
        fs = r"BR(YY \to 4\tau)$"
    elif final_states[i] == "2b2tau":
        fs = r"BR(YY \to 2b2\tau)$"
    else:
        fs = r"BR(YY \to 4b)$"
    a.set_ylabel(r"$\frac{\sigma(gg \to X)}{\sigma_{SM}(gg \to X)} \cdot BR(X\to YY) \cdot "+fs, fontsize=latex_size)
    a.set_xlabel(r"$m_X \mathrm{~[GeV]}$", fontsize=latex_size)
    a.set_yscale("log")
    a.set_ylim(bottom=1E-7, top=75)
    a.set_xlim([20,300])
    a.legend(loc='best', fancybox=True, framealpha=0.6)


## Investigating $BR(h_i \to a_1a_1)$

# Let's look at that BR in more depth, trying to identify reasons for the massive difference in rate for $h_1$ Vs $h_2$. The rate for $h_1\to a_1a_1$ is not unexpected - too high a rate would comflict with existing measurements for Sm decay channels, so we expect something ~10%. But $h_2$ is suspicously localised ~ 0.7. First, look at experimental constraints:

# In[196]:

# subset where h2 has BR(h2 ->a1a1) < 0.6
df_h2_Bh2a1a1Lt0p6_orig = df_orig[(df_orig["Brh2a1a1"] < 0.6)]
print len(df_h2_Bh2a1a1Lt0p6_orig.index), "=", 100*len(df_h2_Bh2a1a1Lt0p6_orig.index)/float(n_orig), "% of ALL points"
plot_constraints(df_h2_Bh2a1a1Lt0p6_orig, r"Subset where $BR(h_2 \to a_1a_1) < 0.6$")


# One consideration is: irrespective of experimental constraints, given the range of input parameters scanned, do we even have many points with $BR(h_2 \to a_1a_1)$?

# In[255]:

fig2, ax2 = plt.subplots(nrows=1, ncols=2)
fig2.set_size_inches(18, 8)
plt.subplots_adjust(wspace=0.3)

pd.set_option("display.float_format", '{:.20f}'.format)
df_orig[(df_orig.Brh2a1a1 < 1E-8) & (df_orig.Brh2a1a1 > 0.)].Brh2a1a1[0:5]

# plot without constraints on left
min_br = 5E-4
max_br = 1
df_orig[(df_orig.Brh2a1a1 > min_br) & (df_orig.Brh2a1a1 < max_br)]["Brh2a1a1"].plot(kind="hist", ax=ax2[0], bins=20, color="green")
ax2[0].set_title("No exp. constraints")
# with all constraints on right
df[(df.Brh2a1a1 > min_br) & (df.Brh2a1a1 < max_br)]["Brh2a1a1"].plot(kind="hist", ax=ax2[1], bins=20, color="green")
ax2[1].set_title("All exp. constraints")
                 
for a in ax2:
#     a.set_xlim([0,0.1])
    a.set_xlabel(r"$BR(h_2\to a_1a_1)$")
    a.set_ylabel(r"$N$")
    


# So we can see that, indeed there are far more points occupying the region < 0.6. However, there is still a clear peak at ~ 0.6. The lump at ~ 0 is I *think* is a rounding error, but needs checking.

# We can look at the masses on $h_1, h_2$ for BR < 0.6 with no experimental constraints, and applying the most common constraints one at a time:

# In[239]:

ddd = df_h2_Bh2a1a1Lt0p6_orig
filters = ["Excluded by", "Landau", "Muon", "Neutralinos", "No Higgs"]
titles = ["No exp. constraints", r"+ excluded by ee $\to$ hZ...", r"+ Landau pole below $M_{GUT}$", "+ Muon mag. mom." , "+ Neutralinos too light", "No Higgs in [122,128]"]
fig6, ax6 = plt.subplots(nrows=2, ncols=3)
fig6.set_size_inches(24, 14)
fig6.suptitle(r"$BR(h_2 \to a_1a_1) < 0.6$", fontsize=24)
plt.subplots_adjust(wspace=0.5)
dd = ddd
for i,a in enumerate(ax6.reshape(-1)):
    if i != 0:
        dd = dd[(~dd.constraints.str.contains(filters[i-1]))]
    dd.plot(kind="scatter", x="mh1", y="mh2", color="seagreen", alpha=0.5, ax=a)
    a.set_xlabel(r"$m_{h_1}\mathrm{~[GeV]}$")
    a.set_xlim([0,140])
    a.set_ylabel(r"$m_{h_2}\mathrm{~[GeV]}$")
    a.set_ylim([1E2,200])
    # ax.set_yscale("log")
    a.set_title(titles[i])

    # mark out acceptable Higgs masses
    a.vlines([mhmin, mhmax], a.get_ylim()[0], a.get_ylim()[1], linewidths=3, linestyles="dashed")
    a.hlines([mhmin,mhmax], a.get_xlim()[0], a.get_xlim()[1], linewidths=3, linestyles="dashed")


# 
# 
# We can do the same thing for $BR(h_1 \to a_1a_1) > 0.25$ out of curiosity:

# In[90]:

# subset where h2 has BR(h2 ->a1a1) >0.2
df_h1_Bh1a1a1Gt0p2 = df_orig[df_orig["Brh1a1a1"] > 0.25]
print len(df_h1_Bh1a1a1Gt0p2.index), "=", 100*len(df_h1_Bh1a1a1Gt0p2.index)/float(n_orig), "% of ALL points"

plot_constraints(df_h1_Bh1a1a1Gt0p2, r"Subset where $BR(h_1 \to a_1a_1) > 0.25$")


# In[94]:


fig2, ax2 = plt.subplots(nrows=1, ncols=2)
fig2.set_size_inches(18, 8)
plt.subplots_adjust(wspace=0.3)

# plot without constraints on left
min_br = 5E-4
max_br = 1
df_orig[(df_orig.Brh1a1a1 > min_br) & (df_orig.Brh1a1a1 < max_br)]["Brh1a1a1"].plot(kind="hist", ax=ax2[0], bins=20)
ax2[0].set_title("No exp. constraints")
# with all constraints on right
df[(df.Brh1a1a1 > min_br) & (df.Brh1a1a1 < max_br)]["Brh1a1a1"].plot(kind="hist", ax=ax2[1], bins=20)
ax2[1].set_title("All exp. constraints")
                 
for a in ax2:
#     a.set_xlim([0,0.1])
    a.set_xlabel(r"$BR(h_1\to a_1a_1)$")
    a.set_ylabel(r"$N$")
    


## Replicate Bomark/Moretti/et al plots

# Figure 2 from the paper (arxiv 1409.8393): case where $h_1 = h_{SM}$

# In[134]:

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


# In[135]:

from IPython.display import Image

fig = Image(filename=('moretti_fig2.png'))
fig


# Clearly these distributions are completely different:
# 
# - No low $\tan \beta$ points in LH plot.
# 
# - No sudden spike as $m_{a_1} > 60$
# 
# - Mine favours large $m_{h_1}$, whereas Figure 2 favours smaller $m_{h_1}$
# 
# - RH plot - no sharp rise at $\kappa \sim 0.35$
# 
# - $\lambda$ fairly constant over range of $\kappa$ in Figure 2, but mine preferes larger $\lambda$ for larger $\kappa$

# One of the many differences is that I have no points below $\tan\beta\sim17$. Is this due to experimental constraints?

# In[142]:

df_tanbetaLt15 = df_orig[df_orig.tgbeta < 17]
print len(df_tanbetaLt15.index), "=", 100*len(df_tanbetaLt15.index)/float(n_orig), "% of ALL points"
plot_constraints(df_tanbetaLt15, r"$\tan\beta < 17$")


# Since the range of $\tan\beta$ scanned is [1.5, 50], and [1.5, 17] ~ 32% of that range, then if we assume points are distributed roughly equally in $\tan\beta$, we are therefore generating enough points in the range [1.5,17], but they fail the experimental constraints, primarily Muon magnetic moment and lack of suitable $h_{125}$

# Differences in scanning:
# 
# - I set IMOD = 0 => general NMSSM, whereas I think BM uses mSUGRA boundary conditions
# 
# - As a result, they also scan over range of $m_0$ (universal scalar mass), $m_{1/2}$ (common gaugino mass), trilinear coupling $A_0$, all specified at the SUSY-breaking scale, $M_{SUSY}$. This is in addtion to the 6 that I scan over ($\tan\beta, \lambda, \kappa, \mu_{eff}, A_{\lambda}, A_{\kappa}$)
# 
# - Choice of experimental constraints: BM require
#     
#     - NMSSMTools v4.2.1: only experimental constraints related to Higgs. No g-2 check then?
#     
#     - HiggsBounds v4.1.3: LEP & LHC exclusion limits applicable on the non-SM-like Higgs bosons 
#     
#     - MicrOMEGAs v 2.4.5: DM relic density < 0.131 (assumes $\pm10%$ error on 0.191)
#     
#     - SuperIso v3.3: limits on $BR(B_s \to \mu\mu)$, $BR(B_u \to \tau\nu)$, $BR(\bar{B}\to X_s\gamma)$
#     
#     - Require $h_1$ or $h_2$ to have mass in the range [122,129] GeV
#     
#     - Also require SM-like signal rates in $\gamma\gamma$ and $ZZ$ channels
#     
# - Whereas I require all experimental constraints in NMSSTools v4.5.0 except 
# 
#     - Excluded by sparticle searches at the LHC
#     - Excluded by ggF/bb->H/A->tautau at the LHC
#     - Excluded H_125->AA->4mu (CMS)
#     - ** Don't calculate relic density or check against MicrOMEGAs**
#     - Don't check with HiggsBounds
#     - Do check several B-physics limits (b -> s gamma more than 2 sigma away, Delta M_s more than 2 sigma away, Delta M_d more than 2 sigma away, B_s -> mu+ mu- more than 2 sigma away, B+ -> tau nu_tau more than 2 sigma away"
# 
# - In addition, there are differences between the different versions of NMSSMTools. Changes include:
# 
#     - Correction of the two loop term in the MSbar-DRbar transition of h_top
#     
#     - The light Higgs contribution to the transition from the top pole mass to the running top mass is expressed in terms of h_top at m_top and not M_SUSY; increases the SM-like Higgs mass by 0.2-0.3 GeV
#     
#     - Constraints from B-physics are updated using values from the HFAG web page
#     
#     - Constraints on signal strengths are updated,
#     
#     - Regularisation of some IR logarithms for a very light pseudoscalar
#     
#     - Hadronic parameters for B-physics are updated
#     
#     - Contributions of two distinct Higgs bosons to the gammagamma/ZZ signal rates are summed only if the mass difference is below 3 GeV. 
#     
#     - Constraint on the invisible Z-width reduced to 0.5 MeV 

## $haa$ tree-level coupling term in the NMSSM

# From Ulrich's paper, Appendix A:

# In[129]:

fig = Image(filename=('haa_coupling_2.png'))
fig


# In[128]:

fig2 = Image(filename=('haa_coupling_1.png'))
fig2

