#!/usr/bin/env python

"""
Make exclusion plots using NMSSM scan points.
"""

import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib as mpl
# import matplotlib.patches as patches
# from itertools import izip, product
import commonPlot as plotr

# pd.set_option('precision',7)
# mpl.rcParams['figure.figsize'] = (9.0, 5.0)  # default size of plots
# mpl.rcParams['font.size'] = 16
# mpl.rcParams['axes.labelsize'] = 16

# mpl.rcParams['xtick.labelsize'] = 14
# mpl.rcParams['ytick.labelsize'] = 14
# mpl.rcParams['xtick.major.size'] = 10
# mpl.rcParams['ytick.major.size'] = 10
# mpl.rcParams['xtick.minor.size'] = 5
# mpl.rcParams['ytick.minor.size'] = 5

# mpl.rcParams['legend.fontsize'] = 16
# mpl.rcParams['legend.framealpha'] = 0.75
# mpl.rcParams['legend.scatterpoints'] = 1
# mpl.rcParams['legend.numpoints'] = 1

# mpl.rcParams.update({'font.size': 24, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})


def make_all_NMSSM_plots():
    # h = h(125)
    df_2hdm_type2_h125 = pd.read_csv("Daniele_Plots/sigma_4tau_mh125_type2.dat",
                                     sep="\t", names=["m_a", "xsec_br_4tau"])
    print len(df_2hdm_type2_h125.index)


    # Scan contributions to put on plot
    scan_dicts = []
    #     {'df': df_2hdm_type2_h125,
    #      'label': r"$h_{125}$",
    #      'color': 'dodgerblue'},
    #     {'df': df_2hdm_type2_H125,
    #      'label': r"$H_{125}$",
    #      'color': 'indigo'},
    # ]

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
    title = 'Observed exclusion limits ' + r'$\left(\sqrt{s}\ =\ 8\ \mathrm{TeV}\right)$'
    common_text = 'NMSSM'
    str_ma = r'$m_a\ \mathrm{[GeV]}$'
    str_xsec_4tau = r'$\sigma\ \times\ BR\ (h_i\ \to\ 2a\ \to\ 4\tau)\ \mathrm{[pb]}$'
    str_br_4tau = r'$\frac{\sigma}{\sigma_{SM}} \times BR\ (h\ \to\ 2a\ \to\ 4\tau)$'

    plotr.save_scan_exclusions_xsec("NMSSM_Plots/xsec_br_4tau", ["eps", "svg", "pdf", "png"],
                                    scan_dicts, experimental_dicts,
                                    y_var='xsec_br_4tau',
                                    x_label=str_ma, y_label=str_xsec_4tau,
                                    x_range=[2, 12], y_range=[0.05, 5E2],
                                    title=title, text=common_text, text_coords=[0.8, 0.1])

    plotr.save_scan_exclusions_br("NMSSM_Plots/br_4tau", ["eps", "svg", "pdf", "png"],
                                  scan_dicts, experimental_dicts,
                                  y_var='br_4tau',
                                  x_label=str_ma, y_label=str_br_4tau,
                                  x_range=[2, 12],
                                  title=title, text=common_text, text_coords=[0.8, 0.1])


if __name__ == "__main__":
    make_all_NMSSM_plots()
