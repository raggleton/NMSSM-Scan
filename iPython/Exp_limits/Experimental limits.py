
# coding: utf-8

# In[1]:

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

get_ipython().magic(u'matplotlib inline')


# In[256]:

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

mpl.rcParams.update({'font.size': 24, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})


# In[226]:

get_ipython().magic(u"config InlineBackend.figure_format='svg'")
# %config InlineBackend.figure_format='retina'


# # Importing CSV data 

# In[4]:

get_ipython().system(u'ls *.csv')


# In[72]:

def make_all_cols_floats(df):
    for c in df.columns:
        df[c] = df[c].astype(float)


# ## CMS HIG-14-019 (4tau)

# In[74]:

df_hig_14_019 = pd.read_csv("4tau experimental limits - HIG-14-019.csv").dropna()
make_all_cols_floats(df_hig_14_019)
df_hig_14_019


# ## CMS HIG-14-022 (4tau)

# In[75]:

df_hig_14_022 = pd.read_csv("4tau experimental limits - HIG-14-022- Combined.csv").dropna()
make_all_cols_floats(df_hig_14_022)


# In[76]:

df_hig_14_022


# ## CMS HIG-15-011 (2tau2mu)

# In[135]:

df_hig_15_011 = pd.read_csv("4tau experimental limits - HIG-15-011 (mumutautau).csv").dropna()
make_all_cols_floats(df_hig_15_011)


# In[136]:

df_hig_15_011.head()


# ## ATLAS HIGG-2014-02 (2tau2mu)

# In[214]:

df_atlas_higg_2014_02 = pd.read_csv("4tau experimental limits - ATLAS mumutautau.csv").dropna()
make_all_cols_floats(df_atlas_higg_2014_02)


# In[215]:

df_atlas_higg_2014_02.head()


# ## CMS HIG-14-041 (2mu2b)

# In[139]:

df_hig_14_041 = pd.read_csv("4tau experimental limits - HIG-14-041 bbmumu xsec limit.csv")
make_all_cols_floats(df_hig_14_041)


# In[140]:

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

# In[141]:

# Some common masses in GeV
M_TAU = 1.776
M_MU = 0.106
M_B = 4.18


# In[142]:

def convert_BR_final_states(m_new, m_old, m_a):
    """Get ratio of widths (ie BR) of a -> 2m_new / a -> 2m_old
    
    Uses tree-level equation A3 in 1312.4992v5 
    (note, older versions miss a sqrt in phase factor!)
    """
    return m_new**2 * np.sqrt(1 - (2*m_new/m_a)**2) / (m_old**2 * np.sqrt(1 - (2*m_old/m_a)**2))


# In[143]:

def convert_4tau_to_2tau_2mu(df, xsec=True):
    """Convert from 4 tau final state to 2tau 2mu final state.

    xsec: bool. If True, uses xsec column, otherwise uses BR column.
    """
    pre = 'xsec_' if xsec else ''
    return 2. * df['%sbr_4tau' % pre].values * convert_BR_final_states(M_MU, M_TAU, df['m_a'].values)


# In[144]:

def convert_4tau_to_4mu(df, xsec=True):
    """Convert from 4 tau final state to 4mu final state.

    xsec: bool. If True, uses xsec column, otherwise uses BR column.
    """
    pre = 'xsec_' if xsec else ''
    return df['%sbr_4tau' % pre].values * convert_BR_final_states(M_MU, M_TAU, df['m_a'].values)**2


# In[145]:

def convert_xsec_to_br(xsec):
    """Convert from xsec * BR to just BR, assuming SM xsec."""
    return xsec / 19.27


# In[146]:

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

# In[147]:

df_hig_14_019.columns


# In[148]:

df_hig_14_019.rename(columns={'xsec*BR limit (xsec = xsec_SM_125)': 'xsec_br_4tau', 
                              'BR(h->aa->4tau) limit': 'br_4tau'}, 
                     inplace=True)

calc_other_final_states(df_hig_14_019)


# In[149]:

df_hig_14_019


# ## CMS HIG-14-022 (4tau)

# In[150]:

df_hig_14_022.columns


# In[151]:

df_hig_14_022.rename(columns={'xsec*BR limit (xsec = xsec_SM_125)': 'xsec_br_4tau', 
                              'BR(h->aa->4tau) limit': 'br_4tau'}, 
                     inplace=True)
calc_other_final_states(df_hig_14_022)


# In[152]:

df_hig_14_022


# ## CMS HIG-15-011 (2tau2mu)

# In[153]:

df_hig_15_011.columns


# In[154]:

df_hig_15_011.rename(columns={'m_a (rounded)': 'm_a',
                              'xsec * BR(h ->aa ->4tau) [pb]': 'xsec_br_4tau', 
                              'BR (h -> aa ->4tau)': 'br_4tau'}, 
                     inplace=True)
df_hig_15_011.drop('m_a (scraped)', 1, inplace=True)
calc_other_final_states(df_hig_15_011)


# In[155]:

df_hig_15_011.head()


# ## ATLAS HIGG-2014-02 (2tau2mu)

# In[156]:

df_atlas_higg_2014_02.columns


# In[216]:

df_atlas_higg_2014_02.rename(columns={'BR': 'br_4tau', 
                                       'xsec * BR': 'xsec_br_4tau'},
                              inplace=True)
calc_other_final_states(df_atlas_higg_2014_02)


# In[217]:

df_atlas_higg_2014_02.head()


# ## CMS HIG-14-041 (2mu2b)

# In[323]:

df_hig_14_041.columns


# In[325]:

df_hig_14_041.rename(columns={'m_a (scraped)': 'm_a',
                              ' xsec*BR(h->aa->bbmumu) [fb] ': 'xsec_br_2b2mu'},
                    inplace=True)


# In[326]:

df_hig_14_041.head()


# #  Plotting

# In[260]:

dfs_dict = [
    {'df': df_hig_14_019, 'label': 'CMS HIG-14-019 '+r'$(h\ \to\ 2a\ \to\ 4\tau)$', 'color': 'blue'},
    {'df': df_hig_14_022, 'label': 'CMS HIG-14-022 '+r'$(h\ \to\ 2a\ \to\ 4\tau)$', 'color': 'green'},
    {'df': df_hig_15_011, 'label': 'CMS HIG-15-011 '+r'$(h \to\ 2a\ \to\ 2\tau2\mu)$', 'color': 'orange'},
    {'df': df_atlas_higg_2014_02, 'label': 'ATLAS HIGG-2014-02 '+r'$(h\ \to\ 2a\ \to\ 2\tau2\mu)$', 'color': 'red'},
]


# In[402]:

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


# In[360]:

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

# In[403]:

plot_exclusion_regions(dfs_dict, 
                       y_var='xsec_br_4tau', 
                       y_label=r'$\sigma\ \times\ BR\ (h\ \to\ 2a\ \to\ 4\tau)\ \mathrm{[pb]}$', 
                       y_range=[0.1, 1E3],
                       title='Observed exclusion limits '+r'$\left(\sqrt{s}\ =\ 8\ \mathrm{TeV}\right)$',
                       text='Type XXX', text_coords=[0.65, 0.1])
draw_xsec_sm()


# In[404]:

plot_exclusion_regions(dfs_dict, 
                       y_var='br_4tau', 
                       y_label=r'$\frac{\sigma}{\sigma_{SM}} \times BR\ (h\ \to\ 2a\ \to\ 4\tau)$', 
#                        y_range=[1E-7, 1E-2],
                       title='Observed exclusion limits '+r'$\left(\sqrt{s}\ =\ 8\ \mathrm{TeV}\right)$',
                       text='Type XXX', text_coords=[0.65, 0.1])
draw_hline_1()


# ## 2tau 2mu

# In[405]:

plot_exclusion_regions(dfs_dict, 
                       y_var='xsec_br_2tau2mu', 
                       y_label=r'$\sigma\ \times\ BR\ (h\ \to\ 2a\ \to\ 2\tau2\mu)\ \mathrm{[pb]}$', 
                       y_range=[1E-3, 10],
                       title='Observed exclusion limits '+r'$\left(\sqrt{s}\ =\ 8\ \mathrm{TeV}\right)$',
                       text='Type XXX', text_coords=[0.65, 0.1])
draw_xsec_sm()


# In[409]:

plot_exclusion_regions(dfs_dict, 
                       y_var='br_2tau2mu', 
                       y_label=r'$\frac{\sigma}{\sigma_{SM}} \times BR\ (h\ \to\ 2a\ \to\ 2\tau2\mu)$', 
#                        y_range=[1E-7, 1E-2],
                       title='Observed exclusion limits '+r'$\left(\sqrt{s}\ =\ 8\ \mathrm{TeV}\right)$',
                       text='Type XXX', text_coords=[0.65, 0.1])


# ## 4 mu

# In[407]:

plot_exclusion_regions(dfs_dict, 
                       y_var='xsec_br_4mu', 
                       y_label=r'$\sigma\ \times\ BR\ (h\ \to\ 2a\ \to\ 4\mu)\ \mathrm{[pb]}$', 
                       y_range=[1E-6, 1E-1],
                       title='Observed exclusion limits '+r'$\left(\sqrt{s}\ =\ 8\ \mathrm{TeV}\right)$',
                       text='Type XXX', text_coords=[0.65, 0.1])


# In[408]:

plot_exclusion_regions(dfs_dict, 
                       y_var='br_4mu', 
                       y_label=r'$\frac{\sigma}{\sigma_{SM}} \times BR\ (h\ \to\ 2a\ \to\ 4\mu)$', 
                       y_range=[1E-7, 1E-2],
                       title='Observed exclusion limits '+r'$\left(\sqrt{s}\ =\ 8\ \mathrm{TeV}\right)$',
                       text='Type XXX', text_coords=[0.65, 0.1])


# # tan($\beta$) dependence - Type 3/4 models

# In[ ]:




# In[ ]:



