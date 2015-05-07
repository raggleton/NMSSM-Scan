
# coding: utf-8

# In[2]:

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

# In[3]:

dep_kappa = False # for alternate set with kappa set by 0 < mueff*kappa/lambda < 200

folders = []
if dep_kappa:
    folders = [
"jobs_50_MICRO_depKappa_13_Mar_15_1016",
"jobs_50_MICRO_depKappa_13_Mar_15_1019",
"jobs_50_MICRO_depKappa_13_Mar_15_1020",
"jobs_50_MICRO_depKappa_13_Mar_15_1048",
"jobs_50_MICRO_depKappa_13_Mar_15_1055",
"jobs_50_MICRO_depKappa_13_Mar_15_1115",
"jobs_50_MICRO_depKappa_13_Mar_15_1233",
"jobs_50_MICRO_depKappa_13_Mar_15_1352",
"jobs_50_MICRO_depKappa_13_Mar_15_1356",
"jobs_50_MICRO_depKappa_13_Mar_15_1357"
            ]
else:
    # default set with 0 < kappa < 1
    folders = [
"jobs_50_MICRO_08_Mar_15_0946",
"jobs_50_MICRO_08_Mar_15_1037",
"jobs_50_MICRO_08_Mar_15_1044",
"jobs_50_MICRO_08_Mar_15_1114",
"jobs_50_MICRO_08_Mar_15_1151",
"jobs_50_MICRO_08_Mar_15_1221",
"jobs_50_MICRO_08_Mar_15_1308",
"jobs_50_MICRO_08_Mar_15_1419",
"jobs_50_MICRO_08_Mar_15_1421",
"jobs_50_MICRO_08_Mar_15_1852",
"jobs_50_MICRO_08_Mar_15_2153",
"jobs_50_MICRO_08_Mar_15_2234",
"jobs_50_MICRO_08_Mar_15_2237",
"jobs_50_MICRO_09_Apr_15_1443",
"jobs_50_MICRO_09_Apr_15_1446",
"jobs_50_MICRO_09_Apr_15_1448",
"jobs_50_MICRO_09_Apr_15_1457",
"jobs_50_MICRO_09_Apr_15_1458",
"jobs_50_MICRO_09_Apr_15_1500",
"jobs_50_MICRO_09_Apr_15_1854",
"jobs_50_MICRO_09_Apr_15_1856",
"jobs_50_MICRO_09_Apr_15_1857",
"jobs_50_MICRO_09_Apr_15_1902",
"jobs_50_MICRO_09_Apr_15_1903",
"jobs_50_MICRO_09_Apr_15_1904",
"jobs_50_MICRO_09_Apr_15_2046",
"jobs_50_MICRO_09_Apr_15_2047",
"jobs_50_MICRO_09_Apr_15_2048",
"jobs_50_MICRO_09_Apr_15_2049",
"jobs_50_MICRO_09_Apr_15_2050",
"jobs_50_MICRO_09_Apr_15_2108",
"jobs_50_MICRO_09_Apr_15_2333",
"jobs_50_MICRO_09_Apr_15_2335",
"jobs_50_MICRO_09_Apr_15_2337",
"jobs_50_MICRO_09_Apr_15_2338",
"jobs_50_MICRO_09_Apr_15_2340",
"jobs_50_MICRO_09_Apr_15_2341"

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


# In[4]:

# Make some subsets here:

# subset based on passing all constraints
pass_all_str = df_orig["constraints"] == ""
del_a_mu_str = df_orig["constraints"] == r"Muon magn. mom. more than 2 sigma away"
pass_del_a_mu = df_orig["Del_a_mu"] > 0
# pass_DMlarge_str = (df_orig["constraints"].str.match(r"Relic density too large \(Planck\)\Z"))
# pass_DMsmall_str = (df_orig["constraints"].str.match(r"Relic density too small \(Planck\)\Z"))
# df = df_orig[pass_DMlarge_str | pass_DMsmall_str] 
df = df_orig[pass_all_str | (del_a_mu_str & pass_del_a_mu)]
n_total = len(df.index)
df[0:12].T


# In[5]:

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
df[10:15].T


# In[6]:

# NMSSM params with latex equivalents for axis labels
params = {"lambda":r"$\lambda$", "mueff":r"$\mu_{eff} \mathrm{~[GeV]}$", "kappa":r"$\kappa$", 
          "alambda":r"$A_{\lambda} \mathrm{~[GeV]}$", "akappa":r"$A_{\kappa} \mathrm{~[GeV]}$", "tgbeta":r"$\tan\beta$"}


# # $BR(h_1/a_1 \to f\bar{f})$ Vs $m_{a_1}$

# Let's look at the BR for several final states - $\tau\tau$, $\mu\mu$, $bb$.

# In[26]:

finals = {#"mumu": dict(shape="o", label=r"$,~f\bar{f} = \mu^-\mu^+$", color="forestgreen"), 
          "bb": dict(shape="s", label=r"$,~f\bar{f} = b\bar{b}$", color="crimson"),
          "tautau": dict(shape="p", label=r"$,~f\bar{f} = \tau^-\tau^+$", color="dodgerblue") 
          }

fig4, ax4 = plt.subplots(nrows=1, ncols=3)
fig4.set_size_inches(24, 10)
plt.subplots_adjust(wspace=0.3)

for i, a in enumerate(ax4.reshape(-1)):
    for fin in finals:
        df.plot(kind="scatter", x="ma1", y="Bra1"+fin, s=70, alpha=0.5, ax=a, label=r"$X = a_1$"+finals[fin]["label"], color=finals[fin]["color"], marker="s")
        df.plot(kind="scatter", x="mh1", y="Brh1"+fin, s=90, alpha=1, ax=a, label=r"$X = h_1$"+finals[fin]["label"], color=finals[fin]["color"], marker="p")
    a.set_xlabel(r"$m_{X}~\mathrm{[GeV]}$", fontsize=latex_size)
    a.set_ylabel(r"$BR(X\to\/f\bar{f})$", fontsize=latex_size)    
    
# Overall plot on left
ax4[0].set_xlim([0, 100])
ax4[0].set_ylim([-0.05, 1.4])
# ax4[0].set_yscale("log")

# Zoomed in center plot
ax4[1].set_xlim([2, 12])
ax4[1].set_ylim([0.75, 1.02])
# ax4[1].set_ylim(bottom=0, top=1.4)

# Zoomed in right plot
ax4[2].set_xlim([20, 60])
ax4[2].set_ylim([0, 1.3])


# # Experimental Constraints

# Let's look at what constraints are the most common, and how they affect several interesting observeables. First, all points altogether:

# In[8]:

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
                p = p.replace(r"->gg", r"->\gamma\gamma")
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
                p = p.replace(r"tautau", r"\tau\tau")
                cons.append(p)

    # use Counter?
#     from collections import Counter
#     count = Counter(cons)

    # use Series
    s = pd.Series(cons)
    vc = s.value_counts(normalize=True)
    vc_cum = vc.cumsum()
    # find out how many points make up the top X%
    limit = 0.9
    last_i = next(x[0] for x in enumerate(vc_cum) if x[1] > limit) 

    fig, ax = plt.subplots(nrows=1, ncols=1)
    fig.set_size_inches(8, 6)
    vc[:last_i].plot(kind="barh")
    ax.set_xlabel("Fraction of failing points that fail given experimental constraint\n(encompassing " + str(limit*100) + " \% of all failing points)", multialignment='center')
    ax.set_title(title)
    return ax

plot_constraints(df_orig, "All scanned points")


# Now for the subset where $h_2 = h_{SM}$ (i.e. why aren't there more points with $h_2 = h_{SM}$. Note that even *prior* to applying experimental constraints, a very small fraction of generated points have $h_2 = h_{SM}, \sim 0.4\%$, so there is more to investigate.

# In[ ]:

# subset where h2 = hSM (no experimental constraints applied)
df_h2SM_all = df_orig[(df_orig["mh2"] < mhmax) & (df_orig["mh2"] > mhmin)]
print len(df_h2SM_all.index), "=", 100*len(df_h2SM_all.index)/float(n_orig), "% of ALL points"

plot_constraints(df_h2SM_all, r"Subset where $h_2 = h_{SM}$")


# And same for $h_1 = h_{SM}$:

# In[ ]:

# subset where h1 = hSM (no experimental constraints applied)
df_h1SM_all = df_orig[(df_orig["mh1"] < mhmax) & (df_orig["mh1"] > mhmin)]
print len(df_h1SM_all.index), "=", 100*len(df_h1SM_all.index)/float(n_orig), "% of ALL points"
plot_constraints(df_h1SM_all, r"Subset where $h_1 = h_{SM}$")


# Out of curiosity, why do points with $2m_{\tau} < m_{a_1} < 2m_b$ fail?

# In[ ]:

# subset where 3.5 < ma1 < 10
plot_constraints(df_ma1Lt10_all, r"Subset where $2m_{\tau} < m_{a_1} < 10$")


# What we would like to do is see how the different classes of constraint (excluded by ee -> Zh, b-physics, etc) affect various parameters (both input one, and physical ones). Let's start by doing our plots of the 6 input var, for various stage of constraint.

# In[94]:




# # Rates for $4\tau/2b2\tau/4b$ at $\sqrt{s} = 13\mathrm{~TeV}$

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

# In[10]:

# make a subset where m_a1 > 10 GeV
df_ma1Gt10 = df[df.ma1 > 10.]
print len(df_ma1Gt10.index), "points where m_a1 > 10 GeV (=", 100*len(df_ma1Gt10.index)/float(n_total), "%)"


# ## Passing all experimental constraints

# In[11]:

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


# In[12]:

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


# ## Passing all experimental constraints AND requiring $X = h_{SM}$

# In[13]:

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


# In[14]:

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


# ## No requirement of a Higgs in the mass range [122,128] GeV ( & fail $\chi^2 (h\to \gamma\gamma/bb/ZZ) > 6.18$)

# Make the correct subset and check:

# In[15]:

# find subset where on constraint failing is No Higgs in the 122.1-128.1 GeV mass range and no chi2 on H->bb/gg/ZZ
dd = df_orig
chi2_test = (dd["constraints"].str.match("chi2\(H->[bgZ]{2}\) >   6.18"))
higgs_test = (dd["constraints"].str.match("No Higgs in the 122.1-128.1 GeV mass range"))
dd = dd[higgs_test | chi2_test]
print len(dd.index), "points failing No Higgs in the 122.1-128.1 GeV mass range/chi2(H->gg/bb/ZZ) constraints (=", 100*len(dd.index)/float(n_orig) ,"% of ALL points)"
pd.set_option("display.colheader_justify", "left")
dd[0:10]["constraints"] # check matches worked


# In[16]:

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


# In[17]:

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

# In[ ]:

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


# # Investigating $BR(h_i \to a_1a_1)$

# Let's look at that BR in more depth, trying to identify reasons for the massive difference in rate for $h_1$ Vs $h_2$. The rate for $h_1\to a_1a_1$ is not unexpected - too high a rate would comflict with existing measurements for Sm decay channels, so we expect something ~10%. But $h_2$ is suspicously localised ~ 0.7. First, look at experimental constraints:

# In[18]:

df.plot(kind=scat, x="ma1", y="Brh2a1a1")
plt.xlabel(r"$m_{a_1}\mathrm{~[GeV]}$")
plt.ylabel(r"$BR(h_2 \to a_1 a_1)$")


# In[19]:

# subset where h2 has BR(h2 ->a1a1) < 0.6
df_h2_Bh2a1a1Lt0p6_orig = df_orig[(df_orig["Brh2a1a1"] < 0.6)]
print len(df_h2_Bh2a1a1Lt0p6_orig.index), "=", 100*len(df_h2_Bh2a1a1Lt0p6_orig.index)/float(n_orig), "% of ALL points"
plot_constraints(df_h2_Bh2a1a1Lt0p6_orig, r"Subset where $BR(h_2 \to a_1a_1) < 0.6$")


# One consideration is: irrespective of experimental constraints, given the range of input parameters scanned, do we even have many points with $BR(h_2 \to a_1a_1)$?

# In[ ]:

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

# 
# 
# We can do the same thing for $BR(h_1 \to a_1a_1) > 0.25$ out of curiosity:

# In[20]:

# subset where h2 has BR(h2 ->a1a1) >0.2
df_h1_Bh1a1a1Gt0p2 = df_orig[df_orig["Brh1a1a1"] > 0.25]
print len(df_h1_Bh1a1a1Gt0p2.index), "=", 100*len(df_h1_Bh1a1a1Gt0p2.index)/float(n_orig), "% of ALL points"

plot_constraints(df_h1_Bh1a1a1Gt0p2, r"Subset where $BR(h_1 \to a_1a_1) > 0.25$")


# In[21]:


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
    


# # Replicate Bomark/Moretti/et al plots

# Figure 2 from the paper (arxiv 1409.8393): case where $h_1 = h_{SM}$

# In[22]:

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

# In[111]:

df_tanbetaLt15 = df_orig[df_orig.tgbeta < 17]
print len(df_tanbetaLt15.index), "=", 100*len(df_tanbetaLt15.index)/float(n_orig), "% of ALL points"
plot_constraints(df_tanbetaLt15, r"$\tan\beta < 17$")


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
#     - MicrOMEGAs v 2.4.5: DM relic density < 0.131 (assumes +-10% error on 0.191)
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

# # More $h_2$ stuff

# In[24]:

# fig2, ax2 = plt.subplots(nrows=1, ncols=2)
# fig2.set_size_inches(24, 6)
# plt.subplots_adjust(wspace=0.3)

# df_orig.plot(kind="hexbin", x="Brh2a1a1", y="kappa", alpha=1, ax=ax2[0], gridsize=30, cmap=mpl.cm.hot)
# df_orig.plot(kind="hexbin", x="Brh2a1a1", y="lambda", alpha=1, ax=ax2[1], gridsize=30, cmap=mpl.cm.hot)

fig6, ax6 = plt.subplots(ncols=3, nrows=2)
fig6.set_size_inches(24, 12)
fig6.suptitle(r"Passing experimental constraints", fontsize=24)
plt.subplots_adjust(wspace=0.5)

for i, a in enumerate(ax6.reshape(-1)):
    k = params.keys()[i]
    v = params[k]
    
#     df.plot(kind="hexbin", x="mh2", y=k, gridsize=35, cmap=mpl.cm.jet, ax=a)
    df.plot(kind=scat, x="mh2", y=k, ax=a)
#     a.set_xlabel(r"$BR(h_2\to a_1a_1)$")
    a.set_xlim(left=0, right=2000)
    a.set_ylabel(v, fontsize=latex_size)


# In[121]:

fig6, ax6 = plt.subplots(ncols=3, nrows=2)
fig6.set_size_inches(24, 12)

plt.subplots_adjust(wspace=0.5)

df_diff = df.copy()
df_diff["mh2mh1"] = df.mh2-df.mh1
max_mh2 = 200
for i, a in enumerate(ax6.reshape(-1)):
    k = params.keys()[i]
    v = params[k]
    
#     df.plot(kind="hexbin", x="mh2", y=k, gridsize=35, cmap=mpl.cm.jet, ax=a, bins=None)
    df_diff[df.mh2 < max_mh2].plot(kind=scat, x="mh2mh1", y=k, alpha=0.5, ax=a)
    a.set_xlabel(r"$m_{h_2} - m_{h_1}$")
    a.set_xlim([0,100])
    a.set_ylabel(v, fontsize=latex_size)
#     a.set_xscale("log")
fig6.suptitle(r"With experimental constraints, $m_{h_2} < %g GeV$" % max_mh2, fontsize=24)


# In[ ]:



