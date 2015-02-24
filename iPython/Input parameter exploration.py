
# coding: utf-8

# Let's plot input paramaters against various interesting quantities.
# 
# **Input params:**
# 
# Reminder that our SUSY-invariant superpotential is
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
# $$0 < \kappa < 1 ???$$
# $$ -4000 < A_{\lambda} < 4000\mathrm{~GeV}$$
# $$ -30 < A_{\kappa} < 10 \mathrm{~GeV}$$
# where only events with $0 < m_{a_1} < 100~\mathrm{GeV}$ have been selected. In addition, other mass parameters were set:
# $$M_1 = 150 \mathrm{~GeV,~} M_2 = 300\mathrm{~GeV,~} M_3 = 1 \mathrm{~TeV}$$
# 
# Note that in NMSSM Tools 4.5.0, we require that points must pass all experimental constraints (see nmhdecay.f), except:
#     - Excluded by sparticle searches at the LHC
#     - Excluded by ggF/bb->H/A->tautau at the LHC
#     - Excluded H_125->AA->4mu (CMS)
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
# $BR(h_2\to h_1h_1)$
# 
# $\mu_{eff}\kappa/\lambda$
# 
# $\mathrm{Total~scaled~} \sigma\times BR$
# 

# In[286]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# to show plots:
get_ipython().magic(u'pylab inline')

pylab.rcParams['figure.figsize'] = (9.0, 6.0)  # default size of plots
matplotlib.rcParams.update({'font.size': 16})
matplotlib.rcParams['xtick.major.size'] = 8
matplotlib.rcParams['xtick.major.width'] = 1.5
matplotlib.rcParams['xtick.minor.size'] = 5
matplotlib.rcParams['xtick.minor.width'] = 1.5
matplotlib.rcParams['ytick.minor.size'] = 2
matplotlib.rcParams['ytick.minor.width'] = 1.1
matplotlib.rcParams['ytick.major.size'] = 5
matplotlib.rcParams['ytick.major.width'] = 1.5
# latex for axes values
plt.rc('text', usetex=True)
plt.rc('font', family='serif')

# common plotting variables
scat = "scatter"
latex_size = 25
s_size = 60
alp = 0.3


# In[379]:

dep_kappa = True # for alternate set with kappa set by 0 < mueff*kappa/lambda < 200

files = []
if dep_kappa:
    files = [
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
    files = [
            "output_jobs_50_20_Feb_15_1256.dat",
            "output_jobs_50_20_Feb_15_1520.dat",
            "output_jobs_50_20_Feb_15_1613.dat",
            "output_jobs_50_20_Feb_15_1739.dat",
            "output_jobs_50_23_Feb_15_1738.dat",
            "output_jobs_50_23_Feb_15_2023.dat",
            "output_jobs_50_23_Feb_15_2027.dat",
            "output_jobs_50_23_Feb_15_2059.dat"
            ]
    
# Load files into Panda data frame
df_list = []
for fi in files:
    df_temp = pd.read_csv(fi, delim_whitespace=True)
    df_list.append(df_temp)
df = pd.concat(df_list)
n_total = len(df.index)

# Calculate total scaled cross-section for gg->h1->a1a1->4tau, gg->h2->a1a1->4tau, gg->h2->h1h1->4tau 
# (no constraint on if h2 is hSM)
df["totalScaled_h1_2a1_4tau"] = df.h1ggrc2 * df.Brh1a1a1 * df.Bra1tautau * df.Bra1tautau
df["totalScaled_h2_2a1_4tau"] = df.h2ggrc2 * df.Brh2a1a1 * df.Bra1tautau * df.Bra1tautau
df["totalScaled_h2_2h1_4tau"] = df.h2ggrc2 * df.Brh2h1h1 * df.Bra1tautau * df.Bra1tautau

# Make some subsets here:

# subset with 2m_tau < ma1 < 10
ma10 = df["ma1"] < 10
ma2tau = df["ma1"] > 2*df["mtau"].mean()
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

print "Running over", n_total, "points overall"
print len(df_ma10.index), "in the subset of 2m_tau < ma1 < 10 GeV (=",100*len(df_ma10.index)/float(n_total), "%)"
print len(df_h1SM.index), "points in the h1 = h125 subset (=", 100*len(df_h1SM.index)/float(n_total), "%)"
print len(df_h2SM.index), "points in the h2 = h125 subset (=", 100*len(df_h2SM.index)/float(n_total), "%)"


# In[380]:

# NMSSM params with latex equivalents for axis labels
params = {"lambda":r"$\lambda$", "mueff":r"$\mu_{eff} \mathrm{~[GeV]}$", "kappa":r"$\kappa$", 
          "alambda":r"$A_{\lambda} \mathrm{~[GeV]}$", "akappa":r"$A_{\kappa} \mathrm{~[GeV]}$", "tgbeta":r"$\tan\beta$"}


## First, $m_{a_1}$

# In[381]:

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

## $BR(a_1/h_1 \to \tau\tau)$

# In[382]:

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


# We can see that BRs are available over most of the parameter space scanned. Note that the BR (without any constraints on $m_{a_1}$) only inhabits 2 range of values: 0 - 0.15 (more common), and 0.8 - 0.95. If we ony restrict ourselves to $2m_{\tau} < m_{a_1} < 10\mathrm{~GeV}$, then the points inhabit the later region (as expected in that mass window). Also of note is that the $BR(h_1 \to \tau\tau) \lesssim 0.15$, since $h_1$ is most often $h_{SM}$.

## $gg\to h_i \mathrm{~reduced~coupling^2}$

# In[383]:

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


# "Reduced coupling" is the coupling relative to a CP-even Higgs boson of the same mass as the boson under question. Thus the squared reduced coupling is the factor by which $\sigma_{SM}$ scales.

## $BR(h_i\to a_1a_1)$

# In[384]:

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


# From these plots, $h_2$ appears to generally have a larger BR to $a_1a_1$ than $h_1$. However it should be noted that for both $h_2 \to a_1 a_1$ and $h_1 \to a_1 a_1$, the whole range of BRs are possible.

## $BR(h_2 \to h_1h_1)$

# In[385]:

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

## $\mu_{eff}\kappa/\lambda$

# From arXiv:1002.1956 : relationship between $\mu\kappa/\lambda$ and whether $h_1$ or $h_2$ is $h_{SM}$

# In[386]:

df["mukappaOvlambda"] = df["mueff"] * df["kappa"] / df["lambda"]

# Use these if you only want 2m_tau < m_a < 10
# df[ma10 & ma2tau]. instead of df.
ma10 = df["ma1"] < 10
ma2tau = df["ma1"] > 2*df["mtau"].mean()

ax = df.plot(kind=scat, x="mukappaOvlambda", y="mh1", color="deepskyblue", alpha=alp, s=s_size, label=r"$m_{h_1}$")
df.plot(kind=scat, x="mukappaOvlambda", y="mh2", color="orchid", alpha=alp, s=s_size, ax=ax, label=r"$m_{h_2}$")
ax.set_xlabel(r"$\mu\kappa/\lambda\mathrm{~[GeV]}$")
ax.set_ylabel(r"$m_{h_i}\mathrm{~[GeV]}")
ax.set_xlim(left=0, right=200)
ax.set_ylim(bottom=0, top=500)


## Total scaled $\sigma \times BR$

# In[387]:

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
    df[df["totalScaled_h1_2a1_4tau"] > 0].plot(kind=scat, x="totalScaled_h1_2a1_4tau", y=k, s=s_size, color="deepskyblue", alpha=alp, ax=a, label=r"$X = h_1, Y = a_1$")
    df[df["totalScaled_h2_2a1_4tau"] > 0].plot(kind=scat, x="totalScaled_h2_2a1_4tau", y=k, s=s_size, color="darkmagenta", alpha=alp*0.5, ax=a, label=r"$X = h_2, Y = a_1$")
    df[df["totalScaled_h2_2h1_4tau"] > 0].plot(kind=scat, x="totalScaled_h2_2h1_4tau", y=k, s=s_size, color="fuchsia", alpha=alp*0.5, ax=a, label=r"$X = h_2, Y = h_1$")
    a.set_xlabel(r"$\frac{\sigma(gg \to X)}{\sigma_{SM}(gg \to X)} \cdot BR(X\to YY) \cdot BR(Y\to \tau\tau)^2$", fontsize=latex_size)
    
    a.set_ylabel(v, fontsize=latex_size)
    a.set_xscale("log")
    a.set_xlim(left=1E-7)
    a.set_ylim(top=a.get_ylim()[1]*1.3) # bit more space for legend


# Note that here, we've contrained points to those where X (produced by gluon-gluon fusion) is the discovered higgs boson with mass in the range [122.1, 128.1] GeV
