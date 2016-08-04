#!/usr/bin/env python

"""
Make exclusion plots using Daniele's 2HDM Type 2 scan points.
"""


import pandas as pd
import commonPlot as plotr


def load_dataframe(filename):
    """Read Daniele's dat file into pandas dataframe"""
    return pd.read_csv(filename, sep="\s+", names=["m_a", "xsec_br_4tau"])


def make_all_2HDM_plots():
    # Type I
    df_2hdm_type1_h125 = load_dataframe("Daniele_2HDM/little_h/sigma_4tau_typeI_mh125.dat")
    df_2hdm_type1_H125 = load_dataframe("Daniele_2HDM/big_H/sigma_4tau_typeI_mH125.dat")

    # Type II
    df_2hdm_type2_h125 = load_dataframe("Daniele_2HDM/little_h/sigma_4tau_typeII_mh125.dat")
    df_2hdm_type2_H125 = load_dataframe("Daniele_2HDM/big_H/sigma_4tau_typeII_mH125.dat")

    # Scan contributions to put on plot
    type1_scan_dicts = [
        {'df': df_2hdm_type1_h125, 'label': r"$h_{125}$", 'color': 'dodgerblue', 'shape': 'o'},
        {'df': df_2hdm_type1_H125, 'label': r"$H_{125}$", 'color': 'indigo', 'shape': 's'},
    ]

    type2_scan_dicts = [
        {'df': df_2hdm_type2_h125, 'label': r"$h_{125}$", 'color': 'dodgerblue', 'shape': 'o'},
        {'df': df_2hdm_type2_H125, 'label': r"$H_{125}$", 'color': 'indigo', 'shape': 's'},
    ]

    # Get experimental limits
    with pd.HDFStore('exp_limits.h5') as store:
        df_hig_14_019 = store['CMS_HIG_14_019']
        df_hig_14_022 = store['CMS_HIG_14_022']
        df_atlas_higg_2014_02 = store['ATLAS_HIGG_2014_02']
        df_hig_14_041 = store['CMS_HIG_14_041']
        df_hig_15_011 = store['CMS_HIG_15_011']

    # Experimental contributions to put on plot
    # < 10 GeV specific
    experimental_dicts = [
        {'df': df_hig_14_019, 'label': 'CMS HIG-14-019 ' + r'$(4\tau)$', 'color': 'blue'},
        {'df': df_hig_14_022, 'label': 'CMS HIG-14-022 ' + r'$(4\tau)$', 'color': 'turquoise'},
        {'df': df_atlas_higg_2014_02, 'label': 'ATLAS HIGG-2014-02 ' + r'$(2\tau2\mu)$', 'color': 'red'},
    ]

    experimental_dicts_all = [
        {'df': df_hig_14_019, 'label': 'CMS HIG-14-019 ' + r'$(4\tau)$', 'color': 'blue'},
        {'df': df_hig_14_022, 'label': 'CMS HIG-14-022 ' + r'$(4\tau)$', 'color': 'turquoise'},
        {'df': df_hig_14_041, 'label': 'CMS HIG-14-041 ' + r'$(2b2\mu)$', 'color': 'fuchsia', 'yvar': 'xsec_br_4tau_type1_tb1'},
        {'df': df_hig_15_011, 'label': 'CMS HIG-15-011 ' + r'$(2\tau2\mu)$', 'color': 'orange'},
        {'df': df_atlas_higg_2014_02, 'label': 'ATLAS HIGG-2014-02 ' + r'$(2\tau2\mu)$', 'color': 'red'},
    ]

    # Make plots
    title = 'Observed exclusion limits ' + r'$\left(\sqrt{s}\ =\ 8\ \mathrm{TeV}\right)$'
    str_mA = r'$m_A\ \mathrm{[GeV]}$'
    str_xsec_4tau = r'$\sigma\ \times\ BR\ (h_i\ \to\ 2A\ \to\ 4\tau)\ \mathrm{[pb]}$'

    plotr.save_scan_exclusions_xsec("Daniele_2HDM/xsec_br_4tau_type1", ["pdf"],
                                    type1_scan_dicts, experimental_dicts,
                                    x_var='m_a',
                                    y_var='xsec_br_4tau',
                                    x_label=str_mA,
                                    y_label=str_xsec_4tau,
                                    x_range=[2, 15],
                                    y_range=[0.001, 5E2],
                                    title=title, leg_loc='upper right',
                                    text='2HDM\nType I', text_coords=[0.82, 0.1])

    plotr.save_scan_exclusions_xsec("Daniele_2HDM/xsec_br_4tau_type1_allMA", ["pdf"],
                                    type1_scan_dicts, experimental_dicts_all,
                                    x_var='m_a',
                                    y_var='xsec_br_4tau',
                                    x_label=str_mA,
                                    y_label=str_xsec_4tau,
                                    x_range=[2, 50],
                                    y_range=[0.0001, 5E2],
                                    title=title, leg_loc='upper right',
                                    text='2HDM\nType I', text_coords=[0.82, 0.1])

    plotr.save_scan_exclusions_xsec("Daniele_2HDM/xsec_br_4tau_type2", ["pdf"],
                                    type2_scan_dicts, experimental_dicts,
                                    x_var='m_a',
                                    y_var='xsec_br_4tau',
                                    x_label=str_mA,
                                    y_label=str_xsec_4tau,
                                    x_range=[2, 15],
                                    y_range=[0.01, 5E2],
                                    title=title,
                                    text='2HDM\nType II', text_coords=[0.82, 0.1])

    plotr.save_scan_exclusions_xsec("Daniele_2HDM/xsec_br_4tau_type2_allMA", ["pdf"],
                                    type2_scan_dicts, experimental_dicts_all,
                                    x_var='m_a',
                                    y_var='xsec_br_4tau',
                                    x_label=str_mA,
                                    y_label=str_xsec_4tau,
                                    x_range=[2, 50],
                                    y_range=[0.001, 5E2],
                                    title=title,
                                    text='2HDM\nType II', text_coords=[0.82, 0.1])


if __name__ == "__main__":
    make_all_2HDM_plots()
