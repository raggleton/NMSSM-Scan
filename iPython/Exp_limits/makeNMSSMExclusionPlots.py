#!/usr/bin/env python

"""
Make exclusion plots using NMSSM scan points.
"""


import pandas as pd
import commonPlot as plotr
import os
import matplotlib.pyplot as plt


def make_all_NMSSM_plots():
    for cdir in ['range_all_final_relaxed',
                 'range_large_final_relaxed',
                 'range_all_final_relaxed_smallAlambdaMuEff_largeTanBeta',
                 'range_large_final_relaxed_DMASS2',
                 'range_large_final_relaxed_DMASS2_fixedAssignMass'][3:]:
        make_NMSSM_plot(cdir)

def make_NMSSM_plot(csv_dir):
    df_fail_NT_pass_HS_pass_HB = pd.read_csv(os.path.join('NMSSM_Plots', csv_dir, 'df_fail_NT_pass_HS_pass_HB.csv'))
    df_pass_NT_pass_HS_pass_HB = pd.read_csv(os.path.join('NMSSM_Plots', csv_dir, 'df_pass_NT_pass_HS_pass_HB.csv'))
    df_pass_NT_fail_HS_pass_HB = pd.read_csv(os.path.join('NMSSM_Plots', csv_dir, 'df_pass_NT_fail_HS_pass_HB.csv'))

    scan_dicts = [
        {'df': df_fail_NT_pass_HS_pass_HB, 'label': "Fail NT, Pass HS", 'color': 'dodgerblue', 'shape': '^'},
        {'df': df_pass_NT_fail_HS_pass_HB, 'label': "Pass NT, Fail HS", 'color': 'green', 'shape': '^'},
        {'df': df_pass_NT_pass_HS_pass_HB, 'label': "Pass NT, Pass HS", 'color': 'orange', 'shape': '^'},
    ]

    # Get experimental limits
    with pd.HDFStore('exp_limits.h5') as store:
        df_hig_14_019 = store['CMS_HIG_14_019']
        df_hig_14_022 = store['CMS_HIG_14_022']
        df_hig_14_041 = store['CMS_HIG_14_041']
        df_hig_15_011 = store['CMS_HIG_15_011']
        df_atlas_higg_2014_02 = store['ATLAS_HIGG_2014_02']


    # Experimental contributions to put on plot
    # < 10 GeV specific
    experimental_dicts = [
        {'df': df_hig_14_019, 'label': 'CMS HIG-14-019 ' + r'$(4\tau)$', 'color': 'blue'},
        {'df': df_hig_14_022, 'label': 'CMS HIG-14-022 ' + r'$(4\tau)$', 'color': 'green'},
        {'df': df_atlas_higg_2014_02, 'label': 'ATLAS HIGG-2014-02 ' + r'$(2\tau2\mu)$', 'color': 'red'},
    ]

    experimental_dicts_all = [
        {'df': df_hig_14_019, 'label': 'CMS HIG-14-019 ' + r'$(4\tau)$', 'color': 'blue'},
        {'df': df_hig_14_022, 'label': 'CMS HIG-14-022 ' + r'$(4\tau)$', 'color': 'green'},
        {'df': df_hig_14_041, 'label': 'CMS HIG-14-041 ' + r'$(2b2\mu)$', 'color': 'fuchsia', 'yvar': 'xsec_br_4tau_type1_tb1'},
        {'df': df_hig_15_011, 'label': 'CMS HIG-15-011 ' + r'$(2\tau2\mu)$', 'color': 'orange'},
        {'df': df_atlas_higg_2014_02, 'label': 'ATLAS HIGG-2014-02 ' + r'$(2\tau2\mu)$', 'color': 'red'},
    ]

    # Make plots
    title = 'Observed exclusion limits ' + r'$( \sqrt{s}\ =\ 8\ \mathrm{TeV})$'
    common_text = 'NMSSM\nRelaxed constraints'
    str_ma = r'$m_{a_1}\ \mathrm{[GeV]}$'
    y_strings = {
        "xsec_br_4tau": r'$\sigma\ \times\ BR\ (h_i\ \to\ 2a_1\ \to\ 4\tau)\ \mathrm{[pb]}$',
        "br_4tau": r'$\frac{\sigma}{\sigma_{SM}} \times BR\ (h\ \to\ 2a_1\ \to\ 4\tau)$',
        "xsec_br_2tau2mu": r'$\sigma\ \times\ BR\ (h_i\ \to\ 2a_1\ \to\ 2\tau2\mu)\ \mathrm{[pb]}$',
        "br_2tau2mu": r'$\frac{\sigma}{\sigma_{SM}} \times BR\ (h\ \to\ 2a_1\ \to\ 2\tau2\mu)$',
        "xsec_br_4mu": r'$\sigma\ \times\ BR\ (h_i\ \to\ 2a_1\ \to\ 4\mu)\ \mathrm{[pb]}$',
        "br_4mu": r'$\frac{\sigma}{\sigma_{SM}} \times BR\ (h\ \to\ 2a_1\ \to\ 4\mu)$',
    }
    final_states = ['4tau', '2tau2mu', '4mu']

    for fs in final_states:
        fvar = 'xsec_br_%s' % fs

        label_app = r', $h_i\ =\  h_1$'
        for d in scan_dicts:
            d['label'] += label_app

        if fs == '4tau':
            ylim = [5E-3, 50]
        elif fs == '2tau2mu':
            ylim = [1E-4, 5E-1]
        elif fs == '4mu':
            ylim = [1E-7, 1E-1]

        xlim = [2, 25]
        # split into scan plots and experimental plotting
        # h_i = h_1
        plotr.plot_scan_exclusions(scan_dicts, None,
                                   y_var='xsec_8_ggf_h1_2a1_%s' % fs,
                                   x_label=str_ma, y_label=y_strings[fvar],
                                   x_range=xlim, y_range=ylim, shade=False,
                                   title=None, text=None)
        # h_i = h_2
        new_label_app = r', $h_i\ =\  h_2$'
        for d in scan_dicts:
            d['shape'] = 'v'
            d['label'] = d['label'].replace(label_app, new_label_app)
        plotr.plot_scan_exclusions(scan_dicts, None,
                                   y_var='xsec_8_ggf_h2_2a1_%s' % fs,
                                   x_label=str_ma, y_label=y_strings[fvar],
                                   x_range=xlim, y_range=ylim, shade=False,
                                   title=None, text=None)

        # experimental exclusion regions
        plotr.plot_scan_exclusions(None, experimental_dicts,
                                   y_var=fvar,
                                   x_label=str_ma, y_label=y_strings[fvar],
                                   x_range=xlim, y_range=ylim,
                                   title=title, text=common_text, text_coords=[0.56, 0.05],
                                   leg_loc='upper right')

        for ofmt in ['eps', 'png', 'pdf']:
            plt.savefig(os.path.join('NMSSM_Plots', csv_dir, fvar + '.' + ofmt))
        plt.clf()

        # reset
        for d in scan_dicts:
            d['shape'] = '^'
            d['label'] = d['label'].replace(new_label_app, '')


if __name__ == "__main__":
    make_all_NMSSM_plots()
