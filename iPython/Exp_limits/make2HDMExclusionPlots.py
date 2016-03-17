#!/usr/bin/env python

"""
Make exclusion plots using Daniele's 2HDM Type 2 scan points.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


pd.set_option('precision',7)
mpl.rcParams['figure.figsize'] = (9.0, 5.0)  # default size of plots
mpl.rcParams['font.size'] = 16
mpl.rcParams['axes.labelsize'] = 16

mpl.rcParams['xtick.labelsize'] = 14
mpl.rcParams['ytick.labelsize'] = 14
mpl.rcParams['xtick.major.size'] = 12
mpl.rcParams['ytick.major.size'] = 12
mpl.rcParams['xtick.minor.size'] = 6
mpl.rcParams['ytick.minor.size'] = 6

mpl.rcParams['legend.fontsize'] = 16
mpl.rcParams['legend.framealpha'] = 0.8
mpl.rcParams['legend.scatterpoints'] = 1
mpl.rcParams['legend.numpoints'] = 1

mpl.rcParams.update({'font.size': 24, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})


def plot_scan_exclusions(scan_dicts, experimental_dicts, y_var, y_label, x_range=None, y_range=None,
                         title=None, shade=True, text=None, text_coords=[0.6, 0.1]):
    """Make a plot of exclusion regions on top of scan points.

    Parameters
    ----------
    scan_dicts : list[dict]
        List of dictionaries, one for each scan dataframe to be plotted.

    experimental_dicts : list[dict]
        List of dictionaries, one for each experimental dataframe to be plotted.
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
    for entry in scan_dicts:
        df = entry['df']
        plt.plot(df['m_a'].values, df[y_var].values, 'o',
                 label=entry['label'],
                 color=entry['color'], alpha=0.7)

    for entry in experimental_dicts:
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
        for entry in experimental_dicts:
            df = entry['df']
            upper_edge = np.ones_like(df[y_var]) * y_top
            plt.fill_between(df['m_a'], df[y_var],
                             y2=upper_edge,
                             color=entry['color'],
                             alpha=0.2)

    plt.minorticks_on()
    plt.xlabel(r'$m_A\ \mathrm{[GeV]}$', fontsize=20, labelpad=1)
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


def draw_xsec_sm():
    """Draw a horizontal line at xsec_SM"""
    xlim = plt.xlim()
    plt.hlines(19.27, *xlim, linestyle='dashed')
    plt.annotate(r'$\sigma_{SM}$', xy=(xlim[0], 19.27),
                 xytext=(5, 5), xycoords='data',
                 textcoords='offset points', fontsize=16)


def make_all_2HDM_plots():
    # h = h(125)
    df_2hdm_type2_h125 = pd.read_csv("Daniele_Points/sigma_4tau_mh125_type2.dat",
                                     sep="\t", names=["m_a", "xsec_br_4tau"])
    print len(df_2hdm_type2_h125.index)

    # H = h(125)
    df_2hdm_type2_H125 = pd.read_csv("Daniele_Points/sigma_4tau_mH125_type2-2.dat",
                                     sep="\t", names=["m_a", "xsec_br_4tau"])
    print len(df_2hdm_type2_H125.index)

    # Scan contributions to put on plot
    scan_dicts = [
        {'df': df_2hdm_type2_h125,
         'label': r"$h_{125}$",
         'color': 'dodgerblue'},
        {'df': df_2hdm_type2_H125,
         'label': r"$H_{125}$",
         'color': 'indigo'},
    ]

    # Get experimental limits
    with pd.HDFStore('exp_limits.h5') as store:
        df_hig_14_019 = store['CMS_HIG_14_019']
        df_hig_14_022 = store['CMS_HIG_14_022']
        df_atlas_higg_2014_02 = store['ATLAS_HIGG_2014_02']

    # Experimental contributions to put on plot
    experimental_dicts = [
        {'df': df_hig_14_019,
         'label': 'CMS HIG-14-019 ' + r'$(4\tau)$',
         'color': 'blue'},
        {'df': df_hig_14_022,
         'label': 'CMS HIG-14-022 ' + r'$(4\tau)$',
         'color': 'green'},
        {'df': df_atlas_higg_2014_02,
         'label': 'ATLAS HIGG-2014-02 ' + r'$(2\tau2\mu)$',
         'color': 'red'},
    ]

    # Make plots
    plot_scan_exclusions(scan_dicts, experimental_dicts,
                         y_var='xsec_br_4tau',
                         y_label=r'$\sigma\ \times\ BR\ (h_i\ \to\ 2A\ \to\ 4\tau)\ \mathrm{[pb]}$',
                         x_range=[2, 12],
                         y_range=[0.05, 5E2],
                         title='Observed exclusion limits ' + r'$\left(\sqrt{s}\ =\ 8\ \mathrm{TeV}\right)$',
                         text='2HDM\nType II', text_coords=[0.82, 0.1])
    draw_xsec_sm()
    plt.savefig("Daniele_Points/xsec_br_4tau_type2.svg")
    plt.savefig("Daniele_Points/xsec_br_4tau_type2.pdf")


if __name__ == "__main__":
    make_all_2HDM_plots()
