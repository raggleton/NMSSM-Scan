
# coding: utf-8

# Let's start by importing necessary modules. We're gonna use pandas with matplotlib to do plotting

# In[89]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
# to show plots
get_ipython().magic(u'pylab inline')
pylab.rcParams['figure.figsize'] = (9.0, 6.0)  # default size of plots
matplotlib.rcParams.update({'font.size': 16})
matplotlib.rcParams['xtick.major.size'] = 5
matplotlib.rcParams['xtick.major.width'] = 1.5
matplotlib.rcParams['ytick.minor.size'] = 2
matplotlib.rcParams['ytick.minor.width'] = 1.1
matplotlib.rcParams['ytick.major.size'] = 5
matplotlib.rcParams['ytick.major.width'] = 1.5
plt.rc('text', usetex=True)
plt.rc('font', family='serif')
latex_size = 25


# Open our output file here as a panda data frame, see what's in it

# In[154]:

dep_kappa = False

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


# In[155]:

df.describe().T


# Range of parameters scanned:
# **never get tan beta < 15??**
# $$1.5 < \tan \beta < 50$$
# $$100 < \mu_{eff}< 300$$
# $$0 < \lambda < 1$$
# $$0 < \kappa < 1$$
# $$ -4000 < A_{\lambda} < 4000$$
# $$ -30 < A_{\kappa} < 10$$
# where only events with $$0 < m_{a_1} < 100~\mathrm{GeV}$$ have been selected

# We also make a subset of points where $m_{a_1} < 10$ GeV:

# In[156]:

ma10 = df["ma1"] < 10
ma2tau = df["ma1"] > 2*df["mtau"].mean()
df_ma10 = df[ma10 & ma2tau]
df_ma10.describe().T


# Let's plot a few things:

# In[157]:

fig1, ax1 = plt.subplots(ncols=2, nrows=1)
fig1.set_size_inches(20, 9)
plt.subplots_adjust(wspace=0.2)

for i, a in enumerate(ax1):
    df.plot(kind="scatter", x="ma1", y="mh1", s=50, color="Blue", label=r"$m_{h_1}$", alpha=0.3*(i+1), ax=a)
    df.plot(kind="scatter", x="ma1", y="mh2", s=50, color='Green', label=r"$m_{h_2}$", alpha=0.3*(i+1), ax=a)
    df.plot(kind="scatter", x="ma1", y="mh3", s=50, color='Red', label=r"$m_{h_3}$", alpha=0.3*(i+1), ax=a)    
    a.set_xlabel(r"$m_{a_{1}}~\mathrm{[GeV]}$", fontsize=latex_size)
    a.set_ylabel(r"$m_{h_{i}}~\mathrm{[GeV]}$", fontsize=latex_size)
    a.set_yscale("log")

# all ma1
ax1[0].set_xlim(left=0, right=100)
ax1[0].set_ylim(bottom=100, top=5000)

# ma1 < 10
ax1[1].set_xlim(left=2, right=10)
ax1[1].set_ylim(bottom=100, top=10000)


# We can see that for the most part:
# - $m_{h_1} \sim 125$ GeV
# - $300 \lesssim m_{h_2} \lesssim  700$ GeV 
# - $1.75 \lesssim m_{h_3} \lesssim 3$ TeV
# - $m_{a_1}$ tends to favour higher values
# 
# So it appears that often, $h_1 = h(125)$, and only very rarely is $h_2 = h(125)$ (implying that the masses of $h_1$ and $h_2$ are very close). The limit on $m_{a_{1}} < 100$ is artifical (done when selecting good param points). 
# 
# More param points lie at higher $m_{a_1}$, although points still exist for small $m_{a_{1}}$.

# Let's have a look at how the $BR(h_i~\to~a_1a_1)$ responds with $m_{a_1}$ for different scalar Higgs bosons.

# In[158]:

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


# So it appears that $BR(h_1 \to a_1a_1)$ is generally small, where $m_{h_1} \sim 125$ GeV. But for $h_2$, which has $m \gg 125$ GeV, the BR is much larger and more consistent ($\sim 0.7$), for a range of $m_{h_2}$. (*Impact on kinematics - larger h2 -> larger boost, more collimated a1 decay products.*)

# Let's plot a histogram of $m_{a_1}$ to see what's most popular

# In[159]:

axh = df['ma1'].plot(kind="hist", bins=25, color="Purple")
plt.xlabel(r"$m_{a_1}~\mathrm{[GeV]}$", fontsize=latex_size)
plt.ylabel(r"$N$", fontsize=latex_size)


# In[160]:

axh2 = df['mh1'].plot(kind="hist", bins=50, color="Blue")
# axh2.set_xlim([120, 130])
plt.xlabel(r"$m_{h_1}~\mathrm{[GeV]}$", fontsize=latex_size)
plt.ylabel(r"$N$", fontsize=latex_size)
axh2.set_yscale("log")


# In[161]:

axh2 = df['mh2'].plot(kind="hist", bins=75, color="Green")
axh2.set_xlim([100, 400]) if def_kappa else axh2.set_xlim([100, 1000])
plt.xlabel(r"$m_{h_2}~\mathrm{[GeV]}$", fontsize=latex_size)
plt.ylabel(r"$N$", fontsize=latex_size)


# Let's look at $BR(a_1 \to \tau\tau)$ by itself, and as a function of $m_{a_1}$

# In[162]:

axh3 = df['Bra1tautau'].plot(kind="hist", bins=40, color="purple")
# axh3.set_xlim([0, 0.2])
plt.xlabel(r"$BR(a_1 \to \tau\tau)$", fontsize=latex_size)
plt.ylabel(r"$N$", fontsize=latex_size)
axh3.set_yscale("log")


# In[163]:

fig4, ax4 = plt.subplots(nrows=1, ncols=3)
fig4.set_size_inches(24, 8)
plt.subplots_adjust(wspace=0.3)

for a in ax4:
    df.plot(kind="scatter", x="ma1", y="Bra1tautau", s=90, color="Purple", alpha=0.5, ax=a)
    a.set_xlabel(r"$m_{a_1}~\mathrm{[GeV]}$", fontsize=latex_size)
    a.set_ylabel(r"$BR(a_1\to\/\tau\tau)$", fontsize=latex_size)    
    
# Overall plot on left
ax4[0].set_xlim([0, 100])
ax4[0].set_ylim([-0.05, 1.1])
# ax4[0].set_yscale("log")

# Zoomed in center plot
ax4[1].set_xlim([2, 12])
ax4[1].set_ylim([0.75, 1.0])

# Zoomed in right plot
ax4[2].set_xlim([8, 102])
ax4[2].set_ylim([0, 0.15])


# This shows us that there are 2 distinct regions:
# - for $2m_{\tau} < m_{a_1} < 10$ GeV, this is the dominant decay, as expected, with BR ~ 0.8 - 0.95
# - for $m_{a_1} > 10$ GeV, the BR only reaches ~0.1, with a strong **slightly positive?!** correlation between $m_{a_1}$ and $BR(a_1\to\tau\tau)$
