import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
# import matplotlib.patches as patches


pd.set_option('precision',7)
mpl.rcParams['figure.figsize'] = (9.0, 6.0)  # default size of plots
mpl.rcParams['font.size'] = 16
mpl.rcParams['axes.labelsize'] = 16

mpl.rcParams['xtick.labelsize'] = 14
mpl.rcParams['ytick.labelsize'] = 14
mpl.rcParams['xtick.major.size'] = 10
mpl.rcParams['ytick.major.size'] = 10
mpl.rcParams['xtick.minor.size'] = 5
mpl.rcParams['ytick.minor.size'] = 5

mpl.rcParams['legend.fontsize'] = 16
mpl.rcParams['legend.framealpha'] = 0.95
mpl.rcParams['legend.scatterpoints'] = 1
mpl.rcParams['legend.numpoints'] = 1

mpl.rcParams.update({'font.size': 24, 'font.family': 'STIXGeneral', 'mathtext.fontset': 'stix'})


XSEC_SM = 19.27  # SM Higgs CrossSection in pb

M_a_STR = r'$m_a\ \mathrm{[GeV]}$'

M_A_STR = r'$m_A\ \mathrm{[GeV]}$'


def save_plt(filename, ext):
    """Save current figure to file.

    Parameters
    ----------
    filename : str
        Plot filename, without extension
    ext : str or list[str]
        Format extenstion(s) to save plot to

    """
    if isinstance(ext, str):
        plt.savefig(filename + "." + ext, format=ext)
    for ex in ext:
        plt.savefig(filename + "." + ex, format=ex)
    plt.clf()


def save_scan_exclusions_xsec(filename, ext, *args, **kwargs):
    """Plot & save scan + exclusions for total xsec * BR"""
    plot_scan_exclusions(*args, **kwargs)
    if plt.ylim()[1] > XSEC_SM:
        draw_xsec_sm()
    save_plt(filename, ext)


def save_scan_exclusions_br(filename, ext, *args, **kwargs):
    """Plot & save scan + exclusions for BR"""
    plot_scan_exclusions(*args, **kwargs)
    if plt.ylin()[1] > 1.:
        draw_hline_1()
    save_plt(filename, ext)


def plot_scan_exclusions(scan_dicts, experimental_dicts, y_var, x_label, y_label,
                         x_var='ma1', x_range=None, y_range=None,
                         title=None, shade=True,
                         text=None, text_coords=[0.6, 0.1], leg_loc=0):
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

    leg_loc : int or string or pair of floats
        See http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.legend
        Default is 'best'
    """
    if scan_dicts:
        for entry in scan_dicts:
            df = entry['df']
            if len(df.index) == 0:
                continue
            mass_key_default = 'm_a' if 'm_a' in df.columns.values else 'ma1'
            mass_key = x_var or mass_key_default
            colname = entry.get('yvar', y_var)
            plt.plot(df[mass_key].values, df[colname].values,
                     entry.get('shape', 'o'),
                     label=entry['label'], mew=0,
                     color=entry['color'], alpha=0.8)

    if experimental_dicts:
        for entry in experimental_dicts:
            df = entry['df']
            colname = entry.get('yvar', y_var)
            plt.plot(df['m_a'].values, df[colname].values,
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
            colname = entry.get('yvar', y_var)
            upper_edge = np.ones_like(df[colname]) * y_top
            plt.fill_between(df['m_a'], df[colname],
                             y2=upper_edge,
                             color=entry['color'],
                             alpha=0.2)

    plt.minorticks_on()
    # plt.xlabel(r'$m_a\ \mathrm{[GeV]}$', fontsize=20, labelpad=1)
    plt.xlabel(x_label, fontsize=20, labelpad=1)
    plt.ylabel(y_label, fontsize=20)
    plt.legend(loc=leg_loc, fontsize=14)
#     plt.xscale('log')

    if title:
        plt.suptitle(title)

    if text:
        plt.text(*text_coords, s=text, transform=plt.gca().transAxes,
                 bbox=dict(color='white', alpha=0.9, boxstyle='round,rounding_size=0.05'))

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
    plt.hlines(XSEC_SM, *xlim, linestyle='dashed')
    plt.annotate(r'$\sigma_{SM}$', xy=(xlim[0], XSEC_SM),
                 xytext=(5, 5), xycoords='data',
                 textcoords='offset points', fontsize=16)


def draw_hline_1():
    """Draw a horizontal line at y = 1"""
    plt.hlines(1, *plt.xlim(), linestyle='dashed')
