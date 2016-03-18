#!/usr/bin/env python

"""
Make exclusion plots using Daniele's 2HDM Type 2 scan points.
"""


import pandas as pd
import commonPlot as plotr


def load_dataframe(filename):
    """Read Daniele's dat file into pandas dataframe"""
    return pd.read_csv(filename, sep="\t", names=["m_a", "xsec_br_4tau"])


def make_all_2HDM_plots():
    # h = h(125)
    df_2hdm_type2_h125 = load_dataframe("Daniele_2HDMType2_Plots/sigma_4tau_mh125_type2.dat")

    # H = h(125)
    df_2hdm_type2_H125 = load_dataframe("Daniele_2HDMType2_Plots/sigma_4tau_mH125_type2-2.dat")

    # Scan contributions to put on plot
    scan_dicts = [
        {'df': df_2hdm_type2_h125, 'label': r"$h_{125}$", 'color': 'dodgerblue'},
        {'df': df_2hdm_type2_H125, 'label': r"$H_{125}$", 'color': 'indigo'},
    ]

    # Get experimental limits
    with pd.HDFStore('exp_limits.h5') as store:
        df_hig_14_019 = store['CMS_HIG_14_019']
        df_hig_14_022 = store['CMS_HIG_14_022']
        df_atlas_higg_2014_02 = store['ATLAS_HIGG_2014_02']

    # Experimental contributions to put on plot
    experimental_dicts = [
        {'df': df_hig_14_019, 'label': 'CMS HIG-14-019 ' + r'$(4\tau)$', 'color': 'blue'},
        {'df': df_hig_14_022, 'label': 'CMS HIG-14-022 ' + r'$(4\tau)$', 'color': 'green'},
        {'df': df_atlas_higg_2014_02, 'label': 'ATLAS HIGG-2014-02 ' + r'$(2\tau2\mu)$', 'color': 'red'},
    ]

    # Make plots
    title = 'Observed exclusion limits ' + r'$\left(\sqrt{s}\ =\ 8\ \mathrm{TeV}\right)$'
    common_text = '2HDM\nType II'
    str_mA = r'$m_A\ \mathrm{[GeV]}$'
    str_xsec_4tau = r'$\sigma\ \times\ BR\ (h_i\ \to\ 2A\ \to\ 4\tau)\ \mathrm{[pb]}$'

    plotr.save_scan_exclusions_xsec("Daniele_2HDMType2_Plots/xsec_br_4tau_type2", ["pdf", "svg"],
                                    scan_dicts, experimental_dicts,
                                    y_var='xsec_br_4tau',
                                    x_label=str_mA,
                                    y_label=str_xsec_4tau,
                                    x_range=[2, 14],
                                    y_range=[0.05, 5E2],
                                    title=title,
                                    text=common_text, text_coords=[0.82, 0.1])


if __name__ == "__main__":
    make_all_2HDM_plots()
