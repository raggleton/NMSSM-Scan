#!/usr/bin/env python

"""
Make exclusion plots using Nils-Eriks's GUT NMSSM scan points.
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd

mpl.rcParams['font.size'] = 26
mpl.rcParams['figure.figsize'] = (7.0, 4.0)  # default size of plots
mpl.rcParams['axes.labelsize'] = 26
mpl.rcParams['xtick.labelsize'] = 22
mpl.rcParams['ytick.labelsize'] = 22
mpl.rcParams['xtick.major.size'] = 12
mpl.rcParams['xtick.major.width'] = 2
mpl.rcParams['ytick.major.size'] = 12
mpl.rcParams['ytick.major.width'] = 2
mpl.rcParams['xtick.minor.size'] = 6
mpl.rcParams['xtick.minor.width'] = 1
mpl.rcParams['ytick.minor.size'] = 6
mpl.rcParams['ytick.minor.width'] = 1
mpl.rcParams['legend.framealpha'] = 0.9
mpl.rcParams['legend.scatterpoints'] = 1
mpl.rcParams['legend.numpoints'] = 1
mpl.rcParams.update({'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})
pd.set_option('display.max_colwidth', 120)
pd.set_option('display.max_columns', 200)
pd.set_option('display.max_rows', 500)

import commonPlot as plotr

mpl.rcParams['xtick.major.pad'] = 8
mpl.rcParams['ytick.major.pad'] = 8
mpl.rcParams['savefig.dpi'] = 300


def load_dataframe(filename):
    col_map = {0: 'mh1', 1: 'mh2', 2: 'mh3',  3: 'ma1', 69: 'Brh1a1a1', 70: 'Brh2a1a1', 106: 'Bra1tautau', 48: 'ggh1rc', 52: 'ggh2rc'}
    print col_map
    print col_map.keys()
    print col_map.values()
    return pd.read_csv(filename, delim_whitespace=True,
                       usecols=col_map.keys(), header=None,
                       names=col_map.values())


def make_all_GUT_plots():
    # df_gut_h1 = load_dataframe("NE_GUT_NMSSM/head.out")
    df_gut_h1 = load_dataframe("NE_GUT_NMSSM/Goodh1.out")
    df_gut_h2 = load_dataframe("NE_GUT_NMSSM/Goodh2.out")
    df_gut_h1 = df_gut_h1.query('ma1<60')
    df_gut_h2 = df_gut_h2.query('ma1<60')

    print df_gut_h1.head()
    print 'df_gut_h1', df_gut_h1.describe()
    print 'df_gut_h2', df_gut_h2.describe()

    df_gut_h1['xsec_br_4tau_h1'] = 19.27 * df_gut_h1['ggh1rc'] * df_gut_h1['ggh1rc'] * df_gut_h1['Brh1a1a1'] * df_gut_h1['Bra1tautau'] * df_gut_h1['Bra1tautau']
    # df_gut_h1['xsec_br_4tau_h2'] = 19.27 * df_gut_h1['ggh2rc'] * df_gut_h1['ggh2rc'] * df_gut_h1['Brh2a1a1'] * df_gut_h1['Bra1tautau'] * df_gut_h1['Bra1tautau']
    df_gut_h2['xsec_br_4tau_h2'] = 19.27 * df_gut_h2['ggh2rc'] * df_gut_h2['ggh2rc'] * df_gut_h2['Brh2a1a1'] * df_gut_h2['Bra1tautau'] * df_gut_h2['Bra1tautau']
    # df_gut_h2['xsec_br_4tau_h1'] = 19.27 * df_gut_h2['ggh1rc'] * df_gut_h2['ggh1rc'] * df_gut_h2['Brh1a1a1'] * df_gut_h2['Bra1tautau'] * df_gut_h2['Bra1tautau']


    # Scan contributions to put on plot
    scan_dicts = [
        {'df': df_gut_h1, 'label': r"$h_i =\ h_1$", 'color': 'lawngreen', 'shape': '^', 'yvar': 'xsec_br_4tau_h1'},
        # {'df': df_gut_h1, 'label': None, 'color': 'lawngreen', 'shape': '^', 'yvar': 'xsec_br_4tau_h2'},

        # {'df': df_gut_h1, 'label': r"$h_i =\ h_1 =\ h_{125}$", 'color': 'lawngreen', 'shape': '^', 'yvar': 'xsec_br_4tau_h1'},
        # {'df': df_gut_h1, 'label': r"$h_i =\ h_1 \neq\ h_{125}$", 'color': 'green', 'shape': '^', 'yvar': 'xsec_br_4tau_h2'},

        {'df': df_gut_h2, 'label': r"$h_i =\ h_2$", 'color': 'dodgerblue', 'shape': 'v', 'yvar': 'xsec_br_4tau_h2'},
        # {'df': df_gut_h2, 'label': None, 'color': 'dodgerblue', 'shape': 'v', 'yvar': 'xsec_br_4tau_h1'},

        # {'df': df_gut_h2, 'label': r"$h_i =\ h_2 =\ h_{125}$", 'color': 'dodgerblue', 'shape': 'v', 'yvar': 'xsec_br_4tau_h2'},
        # {'df': df_gut_h2, 'label': r"$h_i =\ h_2 \neq\ h_{125}$", 'color': 'blue', 'shape': 'v', 'yvar': 'xsec_br_4tau_h1'},
    ]



    # Get experimental limits
    with pd.HDFStore('exp_limits.h5') as store:
        df_hig_14_019 = store['CMS_HIG_14_019']
        df_hig_14_022 = store['CMS_HIG_14_022']
        df_atlas_higg_2014_02 = store['ATLAS_HIGG_2014_02']
        df_hig_14_041 = store['CMS_HIG_14_041']
        df_hig_15_011 = store['CMS_HIG_15_011']

    # Experimental contributions to put on plot
    experimental_dicts = [
        {'df': df_hig_14_019, 'label': 'CMS HIG-14-019 ' + r'$(4\tau)$', 'color': 'blue'},
        {'df': df_hig_14_022, 'label': 'CMS HIG-14-022 ' + r'$(4\tau)$', 'color': 'turquoise'},
        {'df': df_hig_14_041, 'label': 'CMS HIG-14-041 ' + r'$(2b2\mu)$', 'color': 'fuchsia', 'yvar': 'xsec_br_4tau_type1_tb1'},
        {'df': df_hig_15_011, 'label': 'CMS HIG-15-011 ' + r'$(2\tau2\mu)$', 'color': 'orange'},
        {'df': df_atlas_higg_2014_02, 'label': 'ATLAS HIGG-2014-02 ' + r'$(2\tau2\mu)$', 'color': 'red'},
    ]

    # Make plots
    # title = 'Observed exclusion limits ' + r'$\left(\sqrt{s}\ =\ 8\ \mathrm{TeV}\right)$'
    title = 'Observed exclusion limits ' + r'$( \sqrt{s}\ =\ 8\ \mathrm{TeV} )$'
    common_text = 'GUT-NMSSM\nRelaxed constraints'
    str_ma = r'$m_{a_1}\ \mathrm{[GeV]}$'
    str_xsec_4tau = r'$\sigma\ \times\ BR\ (h_i\ \to\ 2a_1\ \to\ 4\tau)\ \mathrm{[pb]}$'

    # plotr.plot_scan_exclusions(scan_dicts, experimental_dicts,
    plotr.save_scan_exclusions_xsec('NE_GUT_NMSSM/xsec_br_4tau_gut', ['pdf'],
                                    scan_dicts, experimental_dicts,
                                    # x_var='m_a',
                                    y_var='xsec_br_4tau',
                                    x_label=str_ma,
                                    y_label=str_xsec_4tau,
                                    x_range=[2, 60],
                                    y_range=[5E-3, 5E1],
                                    title=title, leg_loc=1,
                                    text=common_text, text_coords=[0.56, 0.05], rasterized=True)


if __name__ == "__main__":
    make_all_GUT_plots()
