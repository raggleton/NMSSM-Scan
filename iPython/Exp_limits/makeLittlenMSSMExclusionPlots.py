#!/usr/bin/env python

"""
Make exclusion plots using Daniele's nMSSM scan points.
"""


import pandas as pd
import commonPlot as plotr


def load_dataframe(filename):
    return pd.read_csv(filename, sep="\t", names=["m_a", "xsec_br_4tau"])


def make_all_nMSSM_plots():
    df_nMSSM_ma = load_dataframe("Daniele_Little_nMSSM_Plots/sigma_4tau_nMSSM_1ma.dat")
    df_nMSSM_mb = load_dataframe("Daniele_Little_nMSSM_Plots/sigma_4tau_nMSSM_1mb.dat")
    df_nMSSM_pam = load_dataframe("Daniele_Little_nMSSM_Plots/sigma_4tau_nMSSM_1pam.dat")
    df_nMSSM_pap = load_dataframe("Daniele_Little_nMSSM_Plots/sigma_4tau_nMSSM_1pap.dat")
    df_nMSSM_pbm = load_dataframe("Daniele_Little_nMSSM_Plots/sigma_4tau_nMSSM_1pbm.dat")
    df_nMSSM_pbp = load_dataframe("Daniele_Little_nMSSM_Plots/sigma_4tau_nMSSM_1pbp.dat")

    df_nMSSM_A = pd.concat([df_nMSSM_ma, df_nMSSM_pam, df_nMSSM_pap], ignore_index=True)
    df_nMSSM_B = pd.concat([df_nMSSM_mb, df_nMSSM_pbm, df_nMSSM_pbp], ignore_index=True)

    # Scan contributions to put on plot
    scan_dicts = [
        {'df': df_nMSSM_B, 'label': r"$m_0\ \sim\ 4\ \mathrm{TeV},\ m_{1/2}\ \lesssim\ 500\ \mathrm{GeV}$", 'color': 'mediumvioletred'},
        {'df': df_nMSSM_A, 'label': r"$m_0\ \lesssim\ 1\ \mathrm{TeV},\ m_{1/2}\ \sim\ 1\ \mathrm{TeV}$", 'color': 'royalblue'},
        # {'df': df_nMSSM_pam, 'label': "1PAM", 'color': 'chocolate'},
        # {'df': df_nMSSM_pap, 'label': "1PAP", 'color': 'goldenrod'},
        # {'df': df_nMSSM_pbm, 'label': "1PBM", 'color': 'sage'},
        # {'df': df_nMSSM_pbp, 'label': "1PBP", 'color': 'maroon'},
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
    common_text = 'nMSSM'
    str_ma = r'$m_{a_1}\ \mathrm{[GeV]}$'
    str_xsec_4tau = r'$\sigma\ \times\ BR\ (h_2\ \to\ 2a_1\ \to\ 4\tau)\ \mathrm{[pb]}$'

    plotr.save_scan_exclusions_xsec("Daniele_Little_nMSSM_Plots/xsec_br_4tau_nMSSM_all", ["pdf", "svg"],
                                    scan_dicts, experimental_dicts,
                                    x_var='m_a',
                                    y_var='xsec_br_4tau',
                                    x_label=str_ma,
                                    y_label=str_xsec_4tau,
                                    x_range=[2, 18],
                                    y_range=[0.001, 1E3],
                                    title=title, leg_loc=1,
                                    text=common_text, text_coords=[0.75, 0.1])

    # make inidivdual plots for each dataframe
    # for entry in scan_dicts:
    #     name = entry['label']
    #     plotr.save_scan_exclusions_xsec("Daniele_Little_nMSSM_Plots/xsec_br_4tau_nMSSM_%s" % name, ["pdf", "svg"],
    #                                     [entry], experimental_dicts,
    #                                     y_var='xsec_br_4tau',
    #                                     x_label=str_ma,
    #                                     y_label=str_xsec_4tau,
    #                                     x_range=[2, 18],
    #                                     y_range=[0.005, 1E3],
    #                                     title=title,
    #                                     text=common_text, text_coords=[0.75, 0.1])


if __name__ == "__main__":
    make_all_nMSSM_plots()
