
# coding: utf-8

# ## Difference to results shown on 24/2/15 - now includes checks on $\chi^2 (H\to gg/ZZ/bb)$

# ### Previous results *DID NOT* include checks on $\chi^2(H \to \gamma\gamma/ZZ/bb)$ - note very different plots for rates for $h_1 \to a_1a_1$!

# Let's plot input paramaters against various interesting quantities.
# 
# **Input params:**
# 
# Reminder that our SUSY-invariant superpotential is (without the normal Yukawa interactions that are the same as in the MSSM)
# $$\mathcal{W}_{NMSSM} = \lambda \hat{S} \hat{H}_u \cdot \hat{H}_d + \frac{\kappa}{3}\hat{S}^3$$
# where the hats denote superfields, $\hat{H}_{u/d}$ are the Higgs superfields, $\hat{S}$ is the singlet superfield, and $\lambda$ and $\kappa$ are dimensionless coupling parameters.
# 
# Our input parameters for NMSSM Tools are:
# 
# $\tan\beta$ (ratio of vevs, $\tan\beta = \frac{v_u}{v_d}$)
# 
# $\mu_{eff}$ (the "effective" $\mu$ from the MSSM, $\mu_{eff} = \lambda\times \langle S \rangle$)
# 
# $\kappa$ 
# 
# $\lambda$
# 
# $A_{\kappa}$ (soft susy-breaking term)
# 
# $A_{\lambda}$ (soft susy-breaking term)
# 
# For these scans, we constrained:
# 
# $$1.5 < \tan \beta < 50$$
# $$100 < \mu_{eff}< 300\mathrm{~GeV}$$
# $$0 < \lambda < 1$$
# $$0 < \kappa < 1$$
# $$ -4000 < A_{\lambda} < 4000\mathrm{~GeV}$$
# $$ -30 < A_{\kappa} < 10 \mathrm{~GeV}$$
# where only events with $0 < m_{a_1} < 100~\mathrm{GeV}$ have been selected. In addition, other mass parameters were set:
# $$M_1 = 150 \mathrm{~GeV,~} M_2 = 300\mathrm{~GeV,~} M_3 = 1 \mathrm{~TeV}$$
# 
# Note that in NMSSM Tools 4.5.0, we require that points must pass all experimental constraints (see list at end, replica of nmhdecay.f), except:
# 
# - Excluded by sparticle searches at the LHC
# 
# - Excluded by ggF/bb->H/A->tautau at the LHC
# 
# - Excluded H_125->AA->4mu (CMS)
# 
# **Interesting quantities:**
# 
# $m_{a_1}$
# 
# $BR(a_1 \to \tau\tau)$
# 
# $BR(h_1 \to \tau\tau)$
# 
# $g_{ggh_i}/g_{{ggh_i}_{SM}}$
# 
# $BR(h_i\to a_1a_1)$
# 
# $BR(h_i~\to~a_1a_1)$ Vs $m_{a_1}$
# 
# $BR(h_2\to h_1h_1)$
# 
# $\mu_{eff}\kappa/\lambda$
# 
# $\mathrm{Total~scaled~} \sigma\times BR$
# 
# $\mathrm{Total~} \sigma\times BR \mathrm{~at~} \sqrt{s}=13\mathrm{~TeV}$
# 
# $m_{a_1}$ Vs $m_{h_i}$
# 
# 
# 

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob

# to show plots:
get_ipython().magic(u'pylab inline')

pylab.rcParams['figure.figsize'] = (9.0, 6.0)  # default size of plots
matplotlib.rcParams.update({'font.size': 20})
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
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# common plotting variables
scat = "scatter"
latex_size = 25
s_size = 60
alp = 0.3


# In[2]:

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
"jobs_50_MICRO_08_Mar_15_2237",
"jobs_50_MICRO_08_Mar_15_2234"
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

# Calculate total cross-section & scaled cross-sections for gg->h1->a1a1->4tau, gg->h2->a1a1->4tau, gg->h2->h1h1->4tau 
# (no constraint on if h2 is hSM)
df_orig["xsec_scaled_h1_2a1_4tau"] = df_orig.h1ggrc2 * df_orig.Brh1a1a1 * df_orig.Bra1tautau * df_orig.Bra1tautau
df_orig["xsec_scaled_h2_2a1_4tau"] = df_orig.h2ggrc2 * df_orig.Brh2a1a1 * df_orig.Bra1tautau * df_orig.Bra1tautau
df_orig["xsec_scaled_h2_2h1_4tau"] = df_orig.h2ggrc2 * df_orig.Brh2h1h1 * df_orig.Bra1tautau * df_orig.Bra1tautau

df_orig["xsec_h1_2a1_4tau"] = df_orig.xsec_ggf13_h1 * df_orig.h1ggrc2 * df_orig.Brh1a1a1 * df_orig.Bra1tautau * df_orig.Bra1tautau
df_orig["xsec_h2_2a1_4tau"] = df_orig.xsec_ggf13_h2 * df_orig.h2ggrc2 * df_orig.Brh2a1a1 * df_orig.Bra1tautau * df_orig.Bra1tautau
df_orig["xsec_h2_2h1_4tau"] = df_orig.xsec_ggf13_h2 * df_orig.h2ggrc2 * df_orig.Brh2h1h1 * df_orig.Bra1tautau * df_orig.Bra1tautau



# In[7]:

# Make some subsets here:

# subset based on constraints
def check_constraint(con_list, constraint):
    return constraint in con_list

# pass_all_str = df_orig["constraints"] == ""
# df = df_orig[pass_all_str] # passes all constraints
# n_total = len(df.index)
# subset based on passing all constraints
pass_all_str = df_orig["constraints"] == ""
del_a_mu_str = df_orig["constraints"] == r"Muon magn. mom. more than 2 sigma away"
pass_del_a_mu = df_orig["Del_a_mu"] > 0
# pass_DMlarge_str = (df_orig["constraints"].str.match(r"Relic density too large \(Planck\)\Z"))
# pass_DMsmall_str = (df_orig["constraints"].str.match(r"Relic density too small \(Planck\)\Z"))
# df = df_orig[pass_DMlarge_str | pass_DMsmall_str] 
df = df_orig[pass_all_str | (del_a_mu_str & pass_del_a_mu)]
n_total = len(df.index)

# subset with 2m_tau < ma1 < 10
ma10 = df["ma1"] < 10
ma2tau = df["ma1"] > (2*df["mtau"].mean())
df_ma10 = df[ma10 & ma2tau]
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
print len(df_ma10.index), "of these have 2m_tau < ma1 < 10 GeV (=",100*len(df_ma10.index)/float(n_total), "%)"
print len(df_h1SM.index), "points in the h1 = h(125) subset (=", 100*len(df_h1SM.index)/float(n_total), "%)"
print len(df_h2SM.index), "points in the h2 = h(125) subset (=", 100*len(df_h2SM.index)/float(n_total), "%)"

df[10:15].T


# In[8]:

# NMSSM params with latex equivalents for axis labels
params = {"lambda":r"$\lambda$", "mueff":r"$\mu_{eff} \mathrm{~[GeV]}$", "kappa":r"$\kappa$", 
          "alambda":r"$A_{\lambda} \mathrm{~[GeV]}$", "akappa":r"$A_{\kappa} \mathrm{~[GeV]}$", "tgbeta":r"$\tan\beta$"}


# # $m_{a_1}$

# In[9]:

fig6, ax6 = plt.subplots(ncols=3, nrows=2)
fig6.set_size_inches(24, 14)
plt.subplots_adjust(wspace=0.3, hspace=0.1)

for i, a in enumerate(ax6.reshape(-1)):
    k = params.keys()[i]
    v = params[k]
    
    df.plot(kind=scat, x="ma1", y=k, s=s_size, color="Tomato", alpha=alp*0.5, ax=a)
    a.set_xlabel(r"$m_{a_1}\mathrm{~[GeV]}$", fontsize=latex_size)
    a.set_ylabel(v, fontsize=latex_size)


# We can see that for light $m_{a_1}$, we require a small $A_{\kappa}$ (somewhere in the interval -5 to 0). $A_{\lambda}$ can also be limited to the range [-1000, 3000], However the rest of the parameters are not strongly correlated with $m_{a_1}$, with satisfactory masses occurring over a wide range of parameter space.

# # $BR(a_1/h_1 \to \tau\tau)$

# In[10]:

fig6, ax6 = plt.subplots(ncols=3, nrows=2)
fig6.set_size_inches(24, 14)
plt.subplots_adjust(wspace=0.3, hspace=0.1)

for i, a in enumerate(ax6.reshape(-1)):
    k = params.keys()[i]
    v = params[k]
    
    df.plot(kind=scat, x="Bra1tautau", y=k, s=s_size, color="darkorange", alpha=alp, ax=a, label=r"$X = a_1$")
    df.plot(kind=scat, x="Brh1tautau", y=k, s=s_size, color="firebrick", alpha=alp, ax=a, label=r"$X = h_1$")
    a.set_xlabel(r"$BR(X \to \tau\tau)$", fontsize=latex_size)
    a.set_ylabel(v, fontsize=latex_size)
    
    # redo legend so points actually visible
    marker_a1 = plt.Line2D((0, 0), (0, 0), markeredgecolor="darkorange", markerfacecolor='darkorange', linestyle='', marker='o', markeredgewidth=2, markersize=5)
    marker_h1 = plt.Line2D((0, 0), (0, 0), markeredgecolor="firebrick", markerfacecolor='firebrick', linestyle='', marker='o', markeredgewidth=2, markersize=5)
    a.legend([marker_a1, marker_h1], [r"$X = a_1$", r"$X = h_1$"], numpoints=1, loc='best', bbox_to_anchor=(1, 1))


# We can see that BRs are available over most of the parameter space scanned. Note that the BR (without any constraints on $m_{a_1}$) only inhabits 2 range of values: 0 - 0.15 (more common), and 0.8 - 0.95. If we ony restrict ourselves to $2m_{\tau} < m_{a_1} < 10\mathrm{~GeV}$, then the points inhabit the later region (as expected in that mass window). Also of note is that the $BR(h_1 \to \tau\tau) \lesssim 0.15$, since $h_1$ is most often $h_{SM}$.

# We can also plot the BR as a function of $m_{a_1/h_1}$:

# In[11]:

fig4, ax4 = plt.subplots(nrows=1, ncols=3)
fig4.set_size_inches(24, 8)
plt.subplots_adjust(wspace=0.3)

for a in ax4:
    df.plot(kind="scatter", x="ma1", y="Bra1tautau", s=90, color="darkorange", alpha=0.5, ax=a, label=r"$X = a_1$")
    df.plot(kind="scatter", x="mh1", y="Brh1tautau", s=90, color="firebrick", alpha=1, ax=a, label=r"X = $h_1$")
    a.set_xlabel(r"$m_{X}~\mathrm{[GeV]}$", fontsize=latex_size)
    a.set_ylabel(r"$BR(X\to\/\tau\tau)$", fontsize=latex_size)    
    
# Overall plot on left
# ax4[0].set_xlim([0, 100])
ax4[0].set_ylim([-0.05, 1.1])
# ax4[0].set_yscale("log")

# Zoomed in center plot
ax4[1].set_xlim([2, 12])
ax4[1].set_ylim([0.75, 1.0])

# Zoomed in right plot
ax4[2].set_xlim([8, 130])
ax4[2].set_ylim([0, 0.15])


# This shows us that there are 2 distinct regions for $a_1 \to \tau\tau$ decays:
# - for $2m_{\tau} < m_{a_1} < 10$ GeV, this is the dominant decay, as expected, with BR ~ 0.8 - 0.95
# - for $m_{a_1} > 10$ GeV, the BR generally ranges from ~0.06 to ~0.14, with a strong **slightly positive?!** correlation between $m_{a_1}$ and $BR(a_1\to\tau\tau)$

# # $gg\to h_i \mathrm{~reduced~coupling^2}$

# In[12]:

fig6, ax6 = plt.subplots(ncols=3, nrows=2)
fig6.set_size_inches(24, 14)
plt.subplots_adjust(wspace=0.3, hspace=0.1)

for i, a in enumerate(ax6.reshape(-1)):
    k = params.keys()[i]
    v = params[k]
# If you want only the scenario when h(125) = h1 or h2, use these two lines
#     df_h1SM.plot(kind=scat, x="h1ggrc2", y=k, s=s_size, color="deepskyblue", alpha=alp, ax=a, label=r"$h_1$")
#     df_h2SM.plot(kind=scat, x="h2ggrc2", y=k, s=s_size, color="mediumpurple", alpha=1, ax=a, label=r"$h_2$")

    df.plot(kind=scat, x="h1ggrc2", y=k, s=s_size, color="deepskyblue", alpha=alp, ax=a, label=r"$h_1$")
    df.plot(kind=scat, x="h2ggrc2", y=k, s=s_size, color="mediumpurple", alpha=alp, ax=a, label=r"$h_2$")

    a.set_xlabel(r"$g^2_{ggh_i}/g^2_{{ggh_i}_{SM}}$", fontsize=latex_size)
    a.set_ylabel(v, fontsize=latex_size)

    # redo legend so points actually visible
    marker_h2 = plt.Line2D((0, 0), (0, 0), markeredgecolor="mediumpurple", markerfacecolor='mediumpurple', linestyle='', marker='o', markeredgewidth=2, markersize=5)
    marker_h1 = plt.Line2D((0, 0), (0, 0), markeredgecolor="deepskyblue", markerfacecolor='deepskyblue', linestyle='', marker='o', markeredgewidth=2, markersize=5)
    a.legend([marker_h2, marker_h1], [r"$h_2$", r'$h_1$'], numpoints=1, loc='best', bbox_to_anchor=(1, 1))


# "Reduced coupling" is the coupling relative to a CP-even Higgs boson of the same mass as the boson under question. Thus the squared reduced coupling is the factor by which $\sigma_{SM}$ scales.

# # $BR(h_i\to a_1a_1)$

# In[13]:

fig6, ax6 = plt.subplots(ncols=3, nrows=2)
fig6.set_size_inches(24, 14)
plt.subplots_adjust(wspace=0.3, hspace=0.1)

for i, a in enumerate(ax6.reshape(-1)):
    k = params.keys()[i]
    v = params[k]

    # If you want the scanerio where h_i = h(125) use these 2 lines:
#     df_h1SM[df_h1SM["Brh1a1a1"]>0].plot(kind=scat, x="Brh1a1a1", y=k, s=s_size, color="deepskyblue", alpha=alp*0.5, ax=a, label=r"$h_1$")
#     df_h2SM[df_h2SM["Brh2a1a1"]>0].plot(kind=scat, x="Brh2a1a1", y=k, s=s_size, color="mediumpurple", alpha=1, ax=a, label=r"$h_2$")

    df[df["Brh2a1a1"]>0].plot(kind=scat, x="Brh2a1a1", y=k, s=s_size, color="mediumpurple", alpha=alp*0.2, ax=a, label=r"$h_2$")
    df[df["Brh1a1a1"]>0].plot(kind=scat, x="Brh1a1a1", y=k, s=s_size, color="deepskyblue", alpha=alp*0.35, ax=a, label=r"$h_1$")

    a.set_xlabel(r"$BR(h_i\to a_1a_1)$", fontsize=latex_size)
    a.set_ylabel(v, fontsize=latex_size)

    # redo legend so points actually visible
    marker_h2 = plt.Line2D((0, 0), (0, 0), markeredgecolor="mediumpurple", markerfacecolor='mediumpurple', linestyle='', marker='o', markeredgewidth=2, markersize=5)
    marker_h1 = plt.Line2D((0, 0), (0, 0), markeredgecolor="deepskyblue", markerfacecolor='deepskyblue', linestyle='', marker='o', markeredgewidth=2, markersize=5)
    a.legend([marker_h2, marker_h1], [r"$h_2", r'$h_1$'], numpoints=1, loc='best', bbox_to_anchor=(1, 1))


# From these plots, $h_2$ appears to generally have a larger BR to $a_1a_1$ than $h_1$. We can clearly see here that $h_1$, usually the $h_{SM}$ has a limited BR to fit with measurements of visible decay channels.

# # $BR(h_i \to a_1a_1)$ Vs $m_{a_1}$

# Let's have a look at how $BR(h_i \to a_1a_1)$ responds with $m_{a_1}$ for different scalar Higgs bosons, again zooming in on the low mass range for $a_1$.

# In[14]:

fig2, ax2 = plt.subplots(ncols=2, nrows=1)
fig2.set_size_inches(20, 9)
plt.subplots_adjust(wspace=0.2)

# left plot - all ma1
df.plot(kind="scatter", x="ma1", y="Brh2a1a1", s=df.mh2*0.25, label=r"$BR(h_2 \to a_1a_1)$", color="Green", alpha=0.2, ax=ax2[0])
df.plot(kind="scatter", x="ma1", y="Brh1a1a1", s=df.mh1*0.5, label=r"$BR(h_1 \to a_1a_1)$", color="Blue", alpha=0.5, ax=ax2[0])
ax2[0].set_ylim([0, 1.3])
ax2[0].set_xlim([0, 100])

# right plot - ma1 < 10
df_ma10.plot(kind="scatter", x="ma1", y="Brh1a1a1", s=df.mh1*0.5, label=r"$BR(h_1 \to a_1a_1)$", color="Blue", alpha=0.5, ax=ax2[1])
df_ma10.plot(kind="scatter", x="ma1", y="Brh2a1a1", s=df.mh2*0.55, label=r"$BR(h_2 \to a_1a_1)$", color="Green", alpha=0.5, ax=ax2[1])
ax2[1].set_ylim([0, 1.2])
ax2[1].set_xlim([2, 10])

for a in ax2:
    a.set_title(r"$\mathrm{Scatter~point~size~\propto~}m_{h_i}$", fontsize=latex_size, va="bottom")
    a.set_xlabel(r"$m_{a_{1}}~\mathrm{[GeV]}$", fontsize=latex_size)
    a.set_ylabel(r"$BR (h_i\/\to\/a_1a_1)$", fontsize=latex_size)


# Note that in these plots, the size of the point is proprotional to the mass of $h_i$. It appears that $BR(h_1 \to a_1a_1)$ has a very restricted range for $h_1 \to a_1a_1$ as $h_1$ is often $h(125)$ and thus must fit with current limits on visible chennels including $H \to ZZ/bb/gg$. For $h_2$, which often has $m \gg 125$ GeV, the BR is much larger and more consistent ($\sim 0.7$), for a wide range of $m_{h_2}$. (*Impact on kinematics - larger h2 -> larger boost, more collimated a1 decay products.*)

# # $BR(h_2 \to h_1h_1)$

# In[15]:

fig6, ax6 = plt.subplots(ncols=3, nrows=2)
fig6.set_size_inches(24, 14)
plt.subplots_adjust(wspace=0.3, hspace=0.1)

for i, a in enumerate(ax6.reshape(-1)):
    k = params.keys()[i]
    v = params[k]
    
    df[df["Brh2h1h1"] > 0.0].plot(kind=scat, x="Brh2h1h1", y=k, s=s_size, color="orchid", alpha=0.5*alp, ax=a)
    a.set_xlabel(r"$BR(h_2\to h_1h_1)$", fontsize=latex_size)
    a.set_ylabel(v, fontsize=latex_size)


# Often favours small BR, with maximum being BR ~ 0.25.

# # $\mu_{eff}\kappa/\lambda$

# From arXiv:1002.1956 : relationship between $\mu\kappa/\lambda$ and whether $h_1$ or $h_2$ is $h_{SM}$. This is a cross-check, to make sure that my scans seem reasonable.

# In[16]:

df["mukappaOvlambda"] = df["mueff"] * df["kappa"] / df["lambda"]

# Use these if you only want 2m_tau < m_a < 10
# df[ma10 & ma2tau]. instead of df.
ma10 = df["ma1"] < 10
ma2tau = df["ma1"] > 2*df["mtau"].mean()

ax = df.plot(kind=scat, x="mukappaOvlambda", y="mh1", color="deepskyblue", alpha=alp, s=s_size, label=r"$m_{h_1}$")
df.plot(kind=scat, x="mukappaOvlambda", y="mh2", color="orchid", alpha=alp, s=s_size, ax=ax, label=r"$m_{h_2}$")
ax.set_xlabel(r"$\mu\kappa/\lambda\mathrm{~[GeV]}$")
ax.set_ylabel(r"$m_{h_i}\mathrm{~[GeV]}")
ax.set_xlim(left=0, right=120)
ax.set_ylim(bottom=0, top=250)


# This exhibits the same behaviour as seen in the paper:

# In[17]:

from IPython.display import Image

fig = Image(filename=('sasha4mu.png'))
fig


# # Total scaled $\sigma \times BR$

# i.e. relative to $\sigma_{SM}$

# In[18]:

fig6, ax6 = plt.subplots(ncols=3, nrows=2)
fig6.set_size_inches(24, 17)
plt.subplots_adjust(wspace=0.3, hspace=0.1)

for i, a in enumerate(ax6.reshape(-1)):
    k = params.keys()[i]
    v = params[k]
    # For the scenario where your first Higgs = h(125), use these 4 lines:
#     df_h1SM[df_h1SM["totalScaled_h1_2a1_4tau"] > 0].plot(kind=scat, x="totalScaled_h1_2a1_4tau", y=k, s=s_size, color="deepskyblue", alpha=alp, ax=a, label=r"$X_{125} = h_1, Y = a_1$")
#     df_h2SM[df_h2SM["totalScaled_h2_2a1_4tau"] > 0].plot(kind=scat, x="totalScaled_h2_2a1_4tau", y=k, s=s_size, color="darkmagenta", alpha=1, ax=a, label=r"$X_{125} = h_2, Y = a_1$")
#     df_h2SM[df_h2SM["totalScaled_h2_2h1_4tau"] > 0].plot(kind=scat, x="totalScaled_h2_2h1_4tau", y=k, s=s_size, color="fuchsia", alpha=1, ax=a, label=r"$X_{125} = h_2, Y = h_1$")
#     a.set_xlabel(r"$\frac{\sigma(gg \to X_{125})}{\sigma_{SM}(gg \to X_{125})} \cdot BR(X_{125}\to YY) \cdot BR(Y\to \tau\tau)^2$", fontsize=latex_size)

    # For any mass of your first Higgs use these 4:
    df[df["xsec_scaled_h1_2a1_4tau"] > 0].plot(kind=scat, x="xsec_scaled_h1_2a1_4tau", y=k, s=s_size, color="deepskyblue", alpha=alp, ax=a, label=r"$X = h_1, Y = a_1$")
    df[df["xsec_scaled_h2_2a1_4tau"] > 0].plot(kind=scat, x="xsec_scaled_h2_2a1_4tau", y=k, s=s_size, color="darkmagenta", alpha=alp*0.5, ax=a, label=r"$X = h_2, Y = a_1$")
    df[df["xsec_scaled_h2_2h1_4tau"] > 0].plot(kind=scat, x="xsec_scaled_h2_2h1_4tau", y=k, s=s_size, color="fuchsia", alpha=alp*0.25, ax=a, label=r"$X = h_2, Y = h_1$")
    a.set_xlabel(r"$\frac{\sigma(gg \to X)}{\sigma_{SM}(gg \to X)} \cdot BR(X\to YY) \cdot BR(Y\to \tau\tau)^2$", fontsize=latex_size)
    
    a.set_ylabel(v, fontsize=latex_size)
    a.set_xscale("log")
    a.set_xlim(left=1E-7)
    a.set_ylim(top=a.get_ylim()[1]*1.3) # bit more space for legend

    # redo legend    
    marker_h1_a1 = plt.Line2D((0, 0), (0, 0), markeredgecolor="deepskyblue", markerfacecolor='deepskyblue', linestyle='', marker='o', markeredgewidth=2, markersize=5)
    marker_h2_a1 = plt.Line2D((0, 0), (0, 0), markeredgecolor="darkmagenta", markerfacecolor='darkmagenta', linestyle='', marker='o', markeredgewidth=2, markersize=5)
    marker_h2_h1 = plt.Line2D((0, 0), (0, 0), markeredgecolor="fuchsia", markerfacecolor='fuchsia', linestyle='', marker='o', markeredgewidth=2, markersize=5)
    a.legend([marker_h1_a1, marker_h2_a1, marker_h2_h1], [r"$X = h_1, Y = a_1$", r"$X = h_2, Y = a_1$", r"$X = h_2, Y = h_1$"], numpoints=1, loc='best', bbox_to_anchor=(1, 1))


# Note that here, we've included points where X is **not** the SM Higgs at 125 GeV. We can scan again, this time requiring X = h(125):

# In[19]:

fig6, ax6 = plt.subplots(ncols=3, nrows=2)
fig6.set_size_inches(24, 17)
plt.subplots_adjust(wspace=0.3, hspace=0.1)

for i, a in enumerate(ax6.reshape(-1)):
    k = params.keys()[i]
    v = params[k]
    # For the scenario where your first Higgs = h(125), use these 4 lines:
    df_h1SM[df_h1SM["xsec_scaled_h1_2a1_4tau"] > 0].plot(kind=scat, x="xsec_scaled_h1_2a1_4tau", y=k, s=s_size, color="deepskyblue", alpha=alp, ax=a, label=r"$X_{125} = h_1, Y = a_1$")
    df_h2SM[df_h2SM["xsec_scaled_h2_2a1_4tau"] > 0].plot(kind=scat, x="xsec_scaled_h2_2a1_4tau", y=k, s=s_size, color="darkmagenta", alpha=1, ax=a, label=r"$X_{125} = h_2, Y = a_1$")
    df_h2SM[df_h2SM["xsec_scaled_h2_2h1_4tau"] > 0].plot(kind=scat, x="xsec_scaled_h2_2h1_4tau", y=k, s=s_size, color="fuchsia", alpha=1, ax=a, label=r"$X_{125} = h_2, Y = h_1$")
    a.set_xlabel(r"$\frac{\sigma(gg \to X_{125})}{\sigma_{SM}(gg \to X_{125})} \cdot BR(X_{125}\to YY) \cdot BR(Y\to \tau\tau)^2$", fontsize=latex_size)

    a.set_ylabel(v, fontsize=latex_size)
    a.set_xscale("log")
    a.set_xlim(left=1E-7)
    a.set_ylim(top=a.get_ylim()[1]*1.3) # bit more space for legend


# # Total $\sigma \times BR$ at $\sqrt{s}=13\mathrm{~TeV}$

# These are the full cross sections. They are calculated as follows:
# 
# For the process $gg \to X \to YY \to 4\tau$, where the combinations are:
# 
# $$X = h_1, Y= a_1$$
# $$X = h_2, Y= a_1$$
# $$X = h_2, Y= h_1$$
# 
# the total $\sigma \times BR$ is computed as 
# 
# $$\sigma_{SM}^{ggX,~13TeV} \times g^2_{ggX}/g^2_{ggX_{SM}} \times BR(X \to YY) \times BR^2(Y\to \tau\tau)$$
# 
# where $\sigma_{SM}^{ggX,~13TeV}$ is taken from the LHC Higgs Cross Section Working Group, obtained by scaling the 8TeV cross-sections by the parton luminosity ratio for 13 TeV compared to 8TeV. https://twiki.cern.ch/twiki/bin/view/LHCPhysics/CERNYellowReportPageAt1314TeV#Higgs_cross_section_estimation_v
# 

# In[20]:

fig6, ax6 = plt.subplots(ncols=3, nrows=2)
fig6.set_size_inches(24, 17)
plt.subplots_adjust(wspace=0.3, hspace=0.1)

for i, a in enumerate(ax6.reshape(-1)):
    k = params.keys()[i]
    v = params[k]

    # For any mass of your first Higgs use these 4:
    df[df["xsec_h1_2a1_4tau"] > 0].plot(kind=scat, x="xsec_h1_2a1_4tau", y=k, s=s_size, color="deepskyblue", alpha=alp, ax=a, label=r"$X = h_1, Y = a_1$")
    df[df["xsec_h2_2a1_4tau"] > 0].plot(kind=scat, x="xsec_h2_2a1_4tau", y=k, s=s_size, color="darkmagenta", alpha=alp*0.5, ax=a, label=r"$X = h_2, Y = a_1$")
    df[df["xsec_h2_2h1_4tau"] > 0].plot(kind=scat, x="xsec_h2_2h1_4tau", y=k, s=s_size, color="fuchsia", alpha=alp*0.25, ax=a, label=r"$X = h_2, Y = h_1$")
    a.set_xlabel(r"$\sigma \times BR \mathrm{~[pb]}$", fontsize=latex_size)
    
    a.set_ylabel(v, fontsize=latex_size)
    a.set_xscale("log")
    a.set_xlim(left=1E-7)
    a.set_ylim(top=a.get_ylim()[1]*1.3) # bit more space for legend
    
    # redo legend    
    marker_h1_a1 = plt.Line2D((0, 0), (0, 0), markeredgecolor="deepskyblue", markerfacecolor='deepskyblue', linestyle='', marker='o', markeredgewidth=2, markersize=5)
    marker_h2_a1 = plt.Line2D((0, 0), (0, 0), markeredgecolor="darkmagenta", markerfacecolor='darkmagenta', linestyle='', marker='o', markeredgewidth=2, markersize=5)
    marker_h2_h1 = plt.Line2D((0, 0), (0, 0), markeredgecolor="fuchsia", markerfacecolor='fuchsia', linestyle='', marker='o', markeredgewidth=2, markersize=5)
    a.legend([marker_h1_a1, marker_h2_a1, marker_h2_h1], [r"$X = h_1, Y = a_1$", r"$X = h_2, Y = a_1$", r"$X = h_2, Y = h_1$"], numpoints=1, loc='best', bbox_to_anchor=(1, 1))


# And again, this time constraining $X = h(125)$

# In[21]:

fig6, ax6 = plt.subplots(ncols=3, nrows=2)
fig6.set_size_inches(24, 17)
plt.subplots_adjust(wspace=0.3, hspace=0.1)

for i, a in enumerate(ax6.reshape(-1)):
    k = params.keys()[i]
    v = params[k]
    # For the scenario where your first Higgs = h(125), use these 4 lines:
    df_h1SM[df_h1SM["xsec_h1_2a1_4tau"] > 0].plot(kind=scat, x="xsec_h1_2a1_4tau", y=k, s=s_size, color="deepskyblue", alpha=alp*2, ax=a, label=r"$X_{125} = h_1, Y = a_1$")
    df_h2SM[df_h2SM["xsec_h2_2a1_4tau"] > 0].plot(kind=scat, x="xsec_h2_2a1_4tau", y=k, s=s_size, color="darkmagenta", alpha=1, ax=a, label=r"$X_{125} = h_2, Y = a_1$")
    df_h2SM[df_h2SM["xsec_h2_2h1_4tau"] > 0].plot(kind=scat, x="xsec_h2_2h1_4tau", y=k, s=s_size, color="fuchsia", alpha=1, ax=a, label=r"$X_{125} = h_2, Y = h_1$")

    a.set_xlabel(r"$\sigma \times BR \mathrm{~[pb]}$", fontsize=latex_size)
    
    a.set_ylabel(v, fontsize=latex_size)
    a.set_xscale("log")
    a.set_xlim(left=1E-7)
    a.set_ylim(top=a.get_ylim()[1]*1.3) # bit more space for legend


# In the above plots, we can see that a whole variety of total production cross-sections are possible, ranging from $\mathrm{ab}$ to several $\mathrm{pb}$, with some points of $\mathcal{O}(10 \mathrm{~pb})$. Having $h_2 = h(125)$ tends to cause a reduction in possible cross-sections, with very few points exceeding $\sigma \times BR \sim \mathcal{O} (\mathrm{fb})$

# # $m_{a_1}$ Vs $m_{h_i}$

# Also of interest is possible masses for our CP-even and CP-odd bosons. We plot $m_{a_1}$ against $m_{h_i}$, for $i = 1, 2, 3$, and zoom in on the mass range $2m_{\tau} < m_{a_1} < 10$ GeV

# In[22]:

fig1, ax1 = plt.subplots(ncols=2, nrows=1)
fig1.set_size_inches(20, 9)
plt.subplots_adjust(wspace=0.2)

for i, a in enumerate(ax1):
    df.plot(kind="scatter", x="ma1", y="mh1", s=50, color="Blue", label=r"$m_{h_1}$", alpha=0.3*(2*i+1), ax=a)
    df.plot(kind="scatter", x="ma1", y="mh2", s=50, color='Green', label=r"$m_{h_2}$", alpha=0.3*(2*i+1), ax=a)
    df.plot(kind="scatter", x="ma1", y="mh3", s=50, color='Red', label=r"$m_{h_3}$", alpha=0.3*(2*i+1), ax=a)    
    a.set_xlabel(r"$m_{a_{1}}~\mathrm{[GeV]}$", fontsize=latex_size)
    a.set_ylabel(r"$m_{h_{i}}~\mathrm{[GeV]}$", fontsize=latex_size)
    a.set_yscale("log")

# all ma1
ax1[0].set_xlim(left=0, right=100)
ax1[0].set_ylim(bottom=60, top=5000)

# ma1 < 10
ax1[1].set_xlim(left=2, right=10)
ax1[1].set_ylim(bottom=100, top=10000)


# We can see that for the most part:
# - $m_{h_1} \sim 125$ GeV
# - $300 \lesssim m_{h_2} \lesssim  700$ GeV 
# - $1.75 \lesssim m_{h_3} \lesssim 3$ TeV
# - $m_{a_1}$ tends to favour higher values
# 
# So it appears that often, $h_1 = h(125)$, and only very rarely is $h_2 = h(125)$. The limit on $m_{a_{1}} < 100$ is artifical (done when selecting good param points). 
# 
# More param points lie at higher $m_{a_1}$, although points still exist for small $m_{a_{1}}$.

# # Replicating one of Daniele's plots

# In[23]:

a = df_h1SM[df_h1SM["xsec_h1_2a1_4tau"] > 0].plot(kind=scat, y=r"xsec_h1_2a1_4tau", x="h1ggrc2", s=s_size, color="royalblue", alpha=1, label=r"$X_{125} = h_1, Y = a_1$")
df_h2SM[df_h2SM["xsec_h2_2a1_4tau"] > 0].plot(kind=scat, y=r"xsec_h2_2a1_4tau", x="h2ggrc2", s=s_size, color="deepskyblue", alpha=1, label=r"$X_{125} = h_2, Y = a_1$", ax=a)
a.set_xlabel(r"$g^2_{ggh_i}/g^2_{{ggh_i}_{SM}}$")
a.set_ylabel(r"$\sigma [\mathrm{~pb}]$")
a.set_xlim(left=0.8, right=0.98)
a.set_ylim(bottom=1E-3, top=1E2)
a.set_yscale("log")


# Daniele's plot:

# In[24]:

fig = Image(filename=('daniele14tev.png'))
fig


# Note that my plot is for 13 TeV, Daniele is at 14 TeV. Also that my x-axis is the reduced coupling squared, whereas Daniele's is just the reduced coupling?? Shapes look fairly similar, however the lack of $h_2=h_{SM}$ is a worry. Also my cross-sections are about an order of magnitude lower.

# # Take away notes/TODO:

# (in no particular order):
# 
# - Investigate parallel co-ordinate plotting, ask Benjamin
# - Experimental constraints - what regions of phase space do they affect?
# - Rate for 4tau/2b2tau/4b signal when $m_{a_{1}} > 10 \mathrm{~GeV}$
# - How does NMSSMTools do the b mass for the yukawa coupling and the phase space calculations - ask Daniele
# - Run some more points to check $BR(X \to \tau\tau)$ for low mass X
# - Try and udnerstand the $BR(h_i \to aa)$ plots a bit better - why such a separation? Why does it stay $\sim0.6$ for $h_2$? Find expression for $g_{haa}$
# - Replot without constraints on $122 < m_h < 128$ and $\chi^2$ for gg/zz/bb
# - Check with Stefano/Bomark paper - $h_2$ there gievs largest rate for whole process, whereas in mine it's $h_1$

# In[ ]:



