
# coding: utf-8

# In[52]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.special import zetac

get_ipython().magic(u'matplotlib inline')


# In[200]:

pd.set_option('precision',7)
mpl.rcParams['figure.figsize'] = (9.0, 5.0)  # default size of plots
mpl.rcParams['font.size'] = 16
mpl.rcParams['axes.labelsize'] = 16

mpl.rcParams['xtick.labelsize'] = 14
mpl.rcParams['ytick.labelsize'] = 14
mpl.rcParams['xtick.major.size'] = 10
mpl.rcParams['ytick.major.size'] = 10
mpl.rcParams['xtick.minor.size'] = 5
mpl.rcParams['ytick.minor.size'] = 5

mpl.rcParams['legend.fontsize'] = 16
mpl.rcParams['legend.framealpha'] = 0.6
mpl.rcParams['legend.scatterpoints'] = 1
mpl.rcParams['legend.numpoints'] = 1

mpl.rcParams.update({'font.size': 24, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})


# In[3]:

get_ipython().magic(u"config InlineBackend.figure_format='svg'")
# %config InlineBackend.figure_format='retina'


# # Importing CSV data 

# In[4]:

get_ipython().system(u'ls *.csv')


# In[5]:

def make_all_cols_floats(df):
    for c in df.columns:
        df[c] = df[c].astype(float)


# ## CMS HIG-14-019 (4tau)

# In[6]:

df_hig_14_019 = pd.read_csv("4tau experimental limits - HIG-14-019.csv").dropna()
make_all_cols_floats(df_hig_14_019)
df_hig_14_019


# ## CMS HIG-14-022 (4tau)

# In[7]:

df_hig_14_022 = pd.read_csv("4tau experimental limits - HIG-14-022- Combined.csv").dropna()
make_all_cols_floats(df_hig_14_022)


# In[8]:

df_hig_14_022


# ## CMS HIG-15-011 (2tau2mu)

# In[9]:

df_hig_15_011 = pd.read_csv("4tau experimental limits - HIG-15-011 (mumutautau).csv").dropna()
make_all_cols_floats(df_hig_15_011)


# In[10]:

df_hig_15_011.head()


# ## ATLAS HIGG-2014-02 (2tau2mu)

# In[11]:

df_atlas_higg_2014_02 = pd.read_csv("4tau experimental limits - ATLAS mumutautau.csv").dropna()
make_all_cols_floats(df_atlas_higg_2014_02)


# In[12]:

df_atlas_higg_2014_02.head()


# ## CMS HIG-14-041 (2mu2b)

# In[13]:

df_hig_14_041 = pd.read_csv("4tau experimental limits - HIG-14-041 bbmumu xsec limit.csv")
make_all_cols_floats(df_hig_14_041)


# In[14]:

df_hig_14_041.head()


# # Tidying up

# Every Dataframe should have, for each m_a:
# 
# - xsec * BR(4tau) [pb] (`xsec_br_4tau`)
# 
# - above / xsec(SM) (`br_4tau`)
# 
# - xsec * BR(2tau2mu) [pb] (`xsec_br_2tau2mu`)
# 
# - above / xsec(SM) (`br_2tau2mu`)
# 
# - xsec * BR(4mu) [pb] (`xsec_br_4mu`)
# 
# - above / xsec(SM) (`br_4mu`)
# 

# We need a function to convert between the various branching ratios, as well as a function to convert between xsec * BR to just BR

# In[15]:

# Some common masses in GeV
M_TAU = 1.776
M_MU = 0.106
M_B = 4.18


# In[16]:

def convert_BR_final_states(m_new, m_old, m_a):
    """Get ratio of widths (ie BR) of a -> 2m_new / a -> 2m_old
    
    Uses tree-level equation A3 in 1312.4992v5 
    (note, older versions miss a sqrt in phase factor!)
    """
    return m_new**2 * np.sqrt(1 - (2*m_new/m_a)**2) / (m_old**2 * np.sqrt(1 - (2*m_old/m_a)**2))


# In[17]:

def convert_4tau_to_2tau_2mu(df, xsec=True):
    """Convert from 4 tau final state to 2tau 2mu final state.

    xsec: bool. If True, uses xsec column, otherwise uses BR column.
    """
    pre = 'xsec_' if xsec else ''
    return 2. * df['%sbr_4tau' % pre].values * convert_BR_final_states(M_MU, M_TAU, df['m_a'].values)


# In[18]:

def convert_4tau_to_4mu(df, xsec=True):
    """Convert from 4 tau final state to 4mu final state.

    xsec: bool. If True, uses xsec column, otherwise uses BR column.
    """
    pre = 'xsec_' if xsec else ''
    return df['%sbr_4tau' % pre].values * convert_BR_final_states(M_MU, M_TAU, df['m_a'].values)**2


# In[19]:

def convert_xsec_to_br(xsec):
    """Convert from xsec * BR to just BR, assuming SM xsec."""
    return xsec / 19.27


# In[20]:

def calc_other_final_states(df):
    """Do all necessary mappings from 4tau final state to other final states."""

    # Do xsec * BR
    if 'xsec_br_4tau' in df.columns:
        df['xsec_br_2tau2mu'] = convert_4tau_to_2tau_2mu(df, xsec=True)
        df['xsec_br_4mu'] = convert_4tau_to_4mu(df, xsec=True)
    else:
        print 'Cannot calculate other final state xsec - no xsec_br_4tau field'

    # Do BR
    if 'br_4tau' in df.columns:
        df['br_2tau2mu'] = convert_4tau_to_2tau_2mu(df, xsec=False)
        df['br_4mu'] = convert_4tau_to_4mu(df, xsec=False)
    else:
        print 'Cannot calculate other final state BR - no br_4tau field'


# ## CMS HIG-14-019

# In[21]:

df_hig_14_019.columns


# In[22]:

df_hig_14_019.rename(columns={'xsec*BR limit (xsec = xsec_SM_125)': 'xsec_br_4tau', 
                              'BR(h->aa->4tau) limit': 'br_4tau'}, 
                     inplace=True)

calc_other_final_states(df_hig_14_019)


# In[23]:

df_hig_14_019


# ## CMS HIG-14-022 (4tau)

# In[24]:

df_hig_14_022.columns


# In[25]:

df_hig_14_022.rename(columns={'xsec*BR limit (xsec = xsec_SM_125)': 'xsec_br_4tau', 
                              'BR(h->aa->4tau) limit': 'br_4tau'}, 
                     inplace=True)
calc_other_final_states(df_hig_14_022)


# In[26]:

df_hig_14_022


# ## CMS HIG-15-011 (2tau2mu)

# In[27]:

df_hig_15_011.columns


# In[28]:

df_hig_15_011.rename(columns={'m_a (rounded)': 'm_a',
                              'xsec * BR(h ->aa ->4tau) [pb]': 'xsec_br_4tau', 
                              'BR (h -> aa ->4tau)': 'br_4tau'}, 
                     inplace=True)
df_hig_15_011.drop('m_a (scraped)', 1, inplace=True)
calc_other_final_states(df_hig_15_011)


# In[29]:

df_hig_15_011.head()


# ## ATLAS HIGG-2014-02 (2tau2mu)

# In[30]:

df_atlas_higg_2014_02.columns


# In[31]:

df_atlas_higg_2014_02.rename(columns={'BR': 'br_4tau', 
                                       'xsec * BR': 'xsec_br_4tau'},
                              inplace=True)
calc_other_final_states(df_atlas_higg_2014_02)


# In[32]:

df_atlas_higg_2014_02.head()


# ## CMS HIG-14-041 (2mu2b)

# In[33]:

df_hig_14_041.columns


# In[34]:

df_hig_14_041.rename(columns={'m_a (scraped)': 'm_a',
                              ' xsec*BR(h->aa->bbmumu) [fb] ': 'xsec_br_2b2mu'},
                    inplace=True)


# In[35]:

df_hig_14_041.head()


# #  Plotting

# In Type1/2 models, the bottom and tau/mu both have the same relative coupling strength to a. Therefore we can convert easily, without any $\tan(\beta)$ dependence.

# In[36]:

dfs_dict = [
    {'df': df_hig_14_019, 'label': 'CMS HIG-14-019 '+r'$(h\ \to\ 2a\ \to\ 4\tau)$', 'color': 'blue'},
    {'df': df_hig_14_022, 'label': 'CMS HIG-14-022 '+r'$(h\ \to\ 2a\ \to\ 4\tau)$', 'color': 'green'},
    {'df': df_hig_15_011, 'label': 'CMS HIG-15-011 '+r'$(h \to\ 2a\ \to\ 2\tau2\mu)$', 'color': 'orange'},
    {'df': df_atlas_higg_2014_02, 'label': 'ATLAS HIGG-2014-02 '+r'$(h\ \to\ 2a\ \to\ 2\tau2\mu)$', 'color': 'red'},
]


# In[37]:

def plot_exclusion_regions(dfs_dict, y_var, y_label, x_range=None, y_range=None, 
                           title=None, shade=True, text=None, text_coords=[0.6, 0.1]):
    """Make a plot of exclusion regions.

    Parameters
    ----------
    dfs_dict : list
        List of dictionaries, one for each dataframe to be plotted. 
        Must contain fields for dataframe (df), label, color.
    
    y_var : str
        Variable to plot on y axis. Must correspond to column name in dataframe.

    y_label : str
        Label for y axis
        
    x_range : list/tuple, Optional
        Limits for x axis range
        
    y_range : list/tuple, Optional
        Limits for y axis range
    
    title : str, Optional
        Title for plot
        
    shade : bool, Optional
        If True, shades exclusion region in semi-transparent color.
        
    text : str, Optional
        Text to put on plot.
    """
    for entry in dfs_dict:
        df = entry['df']
        plt.plot(df['m_a'].values, df[y_var].values, 
                 label=entry['label'], 
                 color=entry['color'], linewidth=2)
    
    if x_range:
        plt.xlim(*x_range)
    if y_range:
        plt.ylim(*y_range)

    plt.yscale('log')
    
    if shade:
        y_top = plt.ylim()[1]
        for entry in dfs_dict:
            df = entry['df']
            upper_edge = np.ones_like(df[y_var]) * y_top
            plt.fill_between(df['m_a'], df[y_var], 
                             y2=upper_edge,
                             color=entry['color'],
                             alpha=0.2)
            
    plt.minorticks_on()
    plt.xlabel(r'$m_a\ \mathrm{[GeV]}$', fontsize=20)
    plt.ylabel(y_label, fontsize=20)
    plt.legend(loc=0, fontsize=14)
#     plt.xscale('log')

    if title:
        plt.suptitle(title)

    if text:
        plt.text(*text_coords, s=text, transform=plt.gca().transAxes)
    
    # line for mh/2    
    mh = 125.
    plt.vlines(mh/2, *plt.ylim(), linestyle='dotted', color='dimgrey', linewidth=2)
    plt.annotate(r'$m_h/2$', xy=(mh/2, plt.ylim()[0]), 
                 xytext=(5, 20), xycoords='data', 
                 textcoords='offset points', 
                 fontsize=16, color='dimgrey')


# In[38]:

def draw_xsec_sm():
    """Draw a horizontal line at xsec_SM"""
    xlim = plt.xlim()
    plt.hlines(19.27, *xlim, linestyle='dashed')
    plt.annotate(r'$\sigma_{SM}$', xy=(xlim[0], 19.27),
                 xytext=(5, 5), xycoords='data', 
                 textcoords='offset points', fontsize=16)
    
def draw_hline_1():
#     xlim = plt.xlim()
    plt.hlines(1, *plt.xlim(), linestyle='dashed')


# ## 4tau

# In[39]:

plot_exclusion_regions(dfs_dict, 
                       y_var='xsec_br_4tau', 
                       y_label=r'$\sigma\ \times\ BR\ (h\ \to\ 2a\ \to\ 4\tau)\ \mathrm{[pb]}$', 
                       y_range=[0.1, 1E3],
                       title='Observed exclusion limits '+r'$\left(\sqrt{s}\ =\ 8\ \mathrm{TeV}\right)$',
                       text='Type I/II', text_coords=[0.65, 0.1])
draw_xsec_sm()


# In[40]:

plot_exclusion_regions(dfs_dict, 
                       y_var='br_4tau', 
                       y_label=r'$\frac{\sigma}{\sigma_{SM}} \times BR\ (h\ \to\ 2a\ \to\ 4\tau)$', 
#                        y_range=[1E-7, 1E-2],
                       title='Observed exclusion limits '+r'$\left(\sqrt{s}\ =\ 8\ \mathrm{TeV}\right)$',
                       text='Type I/II', text_coords=[0.65, 0.1])
draw_hline_1()


# ## 2tau 2mu

# In[41]:

plot_exclusion_regions(dfs_dict, 
                       y_var='xsec_br_2tau2mu', 
                       y_label=r'$\sigma\ \times\ BR\ (h\ \to\ 2a\ \to\ 2\tau2\mu)\ \mathrm{[pb]}$', 
                       y_range=[1E-3, 10],
                       title='Observed exclusion limits '+r'$\left(\sqrt{s}\ =\ 8\ \mathrm{TeV}\right)$',
                       text='Type I/II', text_coords=[0.65, 0.1])
draw_xsec_sm()


# In[42]:

plot_exclusion_regions(dfs_dict, 
                       y_var='br_2tau2mu', 
                       y_label=r'$\frac{\sigma}{\sigma_{SM}} \times BR\ (h\ \to\ 2a\ \to\ 2\tau2\mu)$', 
                       y_range=[5E-5, 1],
                       title='Observed exclusion limits '+r'$\left(\sqrt{s}\ =\ 8\ \mathrm{TeV}\right)$',
                       text='Type I/II', text_coords=[0.65, 0.1])


# ## 4 mu

# In[43]:

plot_exclusion_regions(dfs_dict, 
                       y_var='xsec_br_4mu', 
                       y_label=r'$\sigma\ \times\ BR\ (h\ \to\ 2a\ \to\ 4\mu)\ \mathrm{[pb]}$', 
                       y_range=[1E-6, 1E-1],
                       title='Observed exclusion limits '+r'$\left(\sqrt{s}\ =\ 8\ \mathrm{TeV}\right)$',
                       text='Type I/II', text_coords=[0.65, 0.1])


# In[44]:

plot_exclusion_regions(dfs_dict, 
                       y_var='br_4mu', 
                       y_label=r'$\frac{\sigma}{\sigma_{SM}} \times BR\ (h\ \to\ 2a\ \to\ 4\mu)$', 
                       y_range=[5E-8, 1E-2],
                       title='Observed exclusion limits '+r'$\left(\sqrt{s}\ =\ 8\ \mathrm{TeV}\right)$',
                       text='Type I/II', text_coords=[0.65, 0.1])


# # Adding in $a\to bb$ & tan($\beta$) dependence - Type III/IV models

# We need some functions to calculate the various BR ratios for b<=>tau/mu, for various m_a, for various tan(beta). Remember, we **observe** a limit on a particular process independent of the model. But to recast that limit **in another channel** we need the correct transfer factors.
# 
# We use formulae A3 - A8 in 1312.4992v5.
# 
# \begin{equation}
# \Gamma(a\to \ell\ell) = \frac{G_F}{4\sqrt{2}\pi}g_{a\ell\ell}^2 m_a m_{\ell}^2\sqrt{1-\left(\frac{2m_{\ell}}{m_a}\right)^2}
# \\
# \Gamma(a\to q\bar{q}) = \frac{3 G_F}{4\sqrt{2}\pi}g_{aqq}^2 m_a m_q^2\sqrt{1-\left(\frac{2\bar{m}_q}{m_a}\right)^2} \left(1 + \Delta_{q\bar{q}} + \Delta_a^2\right)
# \\
# \mathrm{where\ the\ corrections\ are}
# \\
# \Delta_{q\bar{q}} = 5.67\frac{\bar{\alpha}_s}{\pi} +(35.64 -1.35N_f)\left(\frac{\bar{\alpha}_s}{\pi}\right)^2
# \\
# \Delta_a^2 = \left(\frac{\bar{\alpha}_s}{\pi}\right)^2 \left(3.83 - \ln\frac{m_a^2}{m_t^2} + \frac{1}{6}\ln^2\frac{\bar{m}_q^2}{m_a^2} \right)
# \end{equation}
# 
# Where $N_f$ is the number of active light quarks, $\bar{\alpha}_s$ is the running strong coupling constant, and $\bar{m}_q$ is the running quark mass in the $\overline{MS}$ scheme. The latter two are at renormalisation scale $\mu = m_a$.
# 
# Therefore we need to calculate:
# 
# - running of $\bar{\alpha}_s$
# 
# - running of $\bar{m}_b$
# 
# For Type III, $\frac{g_{aqq}}{g_{a\tau\tau}} = \frac{1}{\tan^2\beta}$. For Type IV, it is the inverse.
# 
# (So in Type III, large $\tan\beta$ = larger $BR(a\to\tau\tau)$)

# ## Running of $\alpha_s$

# References: 
# 
# - http://pdg.lbl.gov/2015/reviews/rpp2015-rev-qcd.pdf
# 
# - QCDNUM: https://www.nikhef.nl/~h24/qcdnum-files/doc/qcdnum170007.pdf
# 
# - A. Djouadi: Anatomy of EWSB I and II, arxiv:0503172, arxiv:0503173 
# 
# - Exotic Decays of the 125GeV Higgs Boson (Strassler et al), arxiv:1312.4992v5

# Working in petrubative QCD (pQCD), the running of the coupling constant is determined by the renormalisation group equation (RGE) (PDG eq9.3):
# 
# \begin{equation}
# \mu_R^2\frac{d\alpha_s^{(N_f)}}{d\mu_R^2} = \frac{d\alpha_s^{(N_f)}}{d\ln\mu_R^2} = \beta(\alpha_s^{(N_f)}) = -\sum_{i=0}^{\infty}b_i {\alpha_s^{(N_f)}}^{i+2}
# \end{equation}
# 
# where the factors $b_i$ up to 3-loop are given by (b3 from 9701390v1):
# 
# \begin{align}
# b_0 &= (33 - 2N_f)/(12\pi)
# \\
# b_1 &= (153 - 19N_f)/(24\pi^2)
# \\
# b_2 &= (2857 - \frac{5033}{9}N_f + \frac{325}{27}N_f^2)/(128\pi^3)
# \\
# b_3 &= \left( \left(\frac{149753}{6} + 3564N_f \right) - \left( \frac{1078361}{162} + \frac{6508}{27}\zeta(3)\right)N_f + \left( \frac{50065}{162} + \frac{6472}{81}\zeta(3) \right) N_f^2 + \frac{1093}{729}N_f^3 \right) / (\pi^4)
# \end{align}
# 
# where $N_f$ is the number of "light" flavours $(m_q \ll \mu_R)$. The remaining flavours decouple from the theory.
# 
# Note that the - sign is crucial for asymptotic freedom: higher scale = weaker coupling.
# 
# $b_i$ = "i+1 loop $\beta$-function coeff."
# 
# Note that the expressions for $b_i$ are scheme-dependent. Here we always work in the $\overline{MS}$ scheme.

# Note that if one only considers $b_0$, a simple analytic solution exists:
# 
# \begin{equation}
# \alpha_s(\mu_R^2) = \frac{1}{b_0\ln\left(\mu_R^2/\Lambda^2\right)}
# \end{equation}
# 
# where $\Lambda$ is a constant, representing the limit to which pQCD can be applied before non-perturbative effectes render the approach invalid.

# Considering higher orders, an approximate analytic solution exists up to 3-loop order (PDG eq9.5):
# 
# \begin{equation}
# \alpha_s(\mu_R^2) \simeq \frac{1}{b_0t}\left(1 - \frac{b_1}{b_0^2}\frac{\ln t}{t} + \frac{b_1^2\left(\ln^2 t- \ln t - 1 \right)+b_0 b_2}{b_0^4 t^2} - \frac{b_1^3 \left( \ln^3t -\frac{5}{2}\ln^2t -2\ln t + \frac{1}{2} \right) + 3b_0 b_1 b_2\ln t - \frac{1}{2}b_0^2 b_3}{b_0^6 t^3} \right)
# \end{equation}
# 
# where
# 
# \begin{equation}
# t = \ln \frac{\mu_R^2}{\Lambda^2}
# \end{equation}

# Another subtelty enters when one considers the number of quarks contributing to $N_f$. When $\mu$ exceeds a heavier quark mass, it must be included. To relate the coupling for $N_F+1$ to $N_f$, the following formula is used (PDG eq9.4):
# 
# \begin{equation}
# \alpha_s^{(N_f+1)}(\mu_R^2) = \alpha_s^{(N_f)}\left( 1 + \sum_{n=1}^\infty \sum_{\ell=0}^n c_{n\ell} \left[  \alpha_s^{(N_f)}\left( \mu_R^2 \right)\right]^n \ln^\ell \frac{\mu_R^2}{m_Q} \right)
# \end{equation}
# 
# where $m_Q$ is the flavour of the $(N_f+1)$ quark. The first few constants $c_{n\ell}$ are:
# 
# \begin{align}
# c_{10} &= 0
# \\
# c_{11} &= 1/6\pi
# \\
# c_{20} &= -11/(72\pi^2)
# \\
# c_{21} &= 19/(24\pi^2)
# \\
# c_{22} &= 1/(36\pi^2)
# \end{align}
# 
# These are valid when $m_Q$ is the $\overline{MS}$ mass at scale $m_Q$. If the pole mass is used, the only difference is now $c_{20} = 7/(24\pi^2)$

# So there are 2 approaches that can be used to calculate $\alpha_s$ at any scale, starting from a reference value at a given scale $\mu_{ref}$ with a given $N_f$. Typically $\alpha_s(M_Z^2) = 0.1181$ is used
# 
# 1) Determine $\Lambda$ via the approximate analytic solution. From there, one can determine $\alpha_s$ at any other scale.
# 
# 2) Solve the RGE using $\alpha_s(\mu^2)|_{\mu = \mu_{ref}} = \alpha_s(\mu_{ref}^2)$

# Handily, the PDG has calcualted $\Lambda^{(N_f)}_{\overline{MS}}$ for the above reference value of $\alpha_s$ using the approximate analytic expression to 4-loop, and 3-loop matching at pole masses 1.3 (c), 4.2 (b), and 173 (t) GeV.
# 
# **Note** that these are only valid down to a few GeV - below that the analystic expression isn't very accurate, and one must solve the RGE.
# 
# \begin{align}
# \Lambda_{\overline{MS}}^{(6)} &= 89\ \mathrm{MeV}
# \\
# \Lambda_{\overline{MS}}^{(5)} &= 210\ \mathrm{MeV}
# \\
# \Lambda_{\overline{MS}}^{(4)} &= 291\ \mathrm{MeV}
# \\
# \Lambda_{\overline{MS}}^{(3)} &= 332\ \mathrm{MeV}
# \end{align}

# In[202]:

zeta3 = zetac(3)+1

def alpha_s(mu, n_flav, simple=False):
    """Calculate strong coupling constant at any scale.

    simple : bool. Do 1-loop only. Overly large at small mu, but faster.
    """
    lambda_ = 0  # use underscore to avoid clashing with python builtin
    if n_flav == 3:
        lambda_ = 0.332
    elif n_flav == 4:
        lambda_ = 0.291
    elif n_flav == 5:
        lambda_ = 0.210
    elif n_flav == 6:
        lambda_ = 0.089
    else:
        raise RuntimeError('n_flav no in range [3, 6] for alpha_s')
        
    # RGE constants, using PDG convention
    b0 = (33. - 2.*n_flav) / (12. * np.pi)
    
    if simple:
        return 1. / (b0 * np.log(mu**2/lambda_**2))

    b1 = (153 - 19*n_flav) / (24. * np.pi**2)
    
    b2 = (2857 - (5033. * n_flav / 9.) + (325. * n_flav**2 / 27.)) / (128. * np.pi**3)
    
    
    b3_0 = ((149753/6.) + (3564.*zeta3))
    b3_1 = ((1078361./162.) + (6508.*zeta3/27.)) * n_flav
    b3_2 = ((50065./162.) + (6472.*zeta3/81.)) * n_flav**2 
    b3_3 = (1093./729.) * n_flav**3
    b3 = (b3_0 - b3_1 + b3_2 + b3_3) / (256. * np.pi**4)
   
    # calculate the analytic approximation, using PDG convention
    t = np.log((mu**2) / (lambda_**2))
    lnt = np.log(t)
    
    part1 = 1
    part2 = ((b1 * lnt) / (b0**2 * t))
    part3 = ((b1**2 * (lnt**2 - lnt - 1)) + (b0*b2)) / (b0**4 * t**2)
    part4 = (b1**3 * (lnt**3 - (2.5*lnt**2) - (2*lnt) + 0.5) + (3*b0*b1*b2*lnt) - (0.5 * b0**2 * b3)) / (b0**6 * t**3)
    return (part1 - part2 + part3 - part4) / (b0*t)

print 'MZ', alpha_s(91.1882, 5), 'should be 0.118'


# In[224]:

# Calculate a_s for variosu scales, covering 1 GeV to 2 TeV,
# comparing 4 loop with 1 loop

# For lin x scale:
# Q_ranges = [np.linspace(1, 1.3, 100), np.linspace(1.3, 4.2, 100), 
#             np.linspace(4.2, 173, 100), np.linspace(173, 2000, 100)]

# For log x scale:
Q_ranges = [np.logspace(0, np.log10(1.3), 20), np.logspace(np.log10(1.3), np.log10(4.2), 20), 
            np.logspace(np.log10(4.2), np.log10(173), 50), np.logspace(np.log10(173), np.log10(2000), 100)]
Q = np.concatenate(Q_ranges)

a_s = np.concatenate([alpha_s(qr, i+3) for i, qr in enumerate(Q_ranges)])
a_s_1loop = np.concatenate([alpha_s(qr, i+3, True) for i, qr in enumerate(Q_ranges)])


# In[225]:

plt.plot(Q, a_s, label='4-loop', linewidth=2)
plt.plot(Q, a_s_1loop, label='1-loop', linestyle='dashed', linewidth=2)
plt.plot([91.1876], [0.1181], 'dr', label=r'$\alpha_s(M_Z^2)\ =\ 0.1181$', markersize=10)
plt.xlim(1, 2000)
plt.xscale('log')
plt.xlabel('Q [GeV]', fontsize=20)
# plt.ylim(0.05, 0.4)
plt.ylabel(r'$\alpha_s(Q^2)$', fontsize=20)
plt.legend(fontsize=16, loc=0)
plt.minorticks_on()
plt.grid()


# ## Running of quark masses 

# 

# In[46]:

def m_b(mu):
    return 4.18


# # Absolute values of BR(a -> ff)

# To plot BR(h->aa), we need the absolute values of BR(a->ff). This is not trivial, and depends on $\tan(\beta)$...

# In[ ]:



