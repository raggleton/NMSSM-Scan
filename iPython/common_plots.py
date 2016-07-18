"""
Fns to make common types of plots
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.cm as cmx
import matplotlib.colors as mplcolors
from matplotlib.ticker import MultipleLocator
from itertools import izip
from collections import namedtuple, OrderedDict
import re
from bisect import bisect
import os


# NMSSM params with various associated attributes, such as latex equivalents
# for axis labels, colours, binning for histograms, etc
Param = namedtuple('Param', ['label', 'color', 'bins', 'range', 'interval'])

nmssm_params = {
    "lambda_": Param(label=r"$\lambda$", color="orange", bins=25, range=[0, 0.7], interval=0.1),
    "mueff": Param(label=r"$\mu_{eff}\ \mathrm{[GeV]}$", color="green", bins=25, range=[100, 300], interval=25),
    "kappa": Param(label=r"$\kappa$", color="steelblue", bins=25, range=[0, 0.7], interval=0.1),
    "alambda": Param(label=r"$A_{\lambda}\ \mathrm{[GeV]}$", color="salmon", bins=25, range=[-1000, 4000], interval=1000),
    "akappa": Param(label=r"$A_{\kappa}\ \mathrm{[GeV]}$", color="red", bins=25, range=[-15, 2.5], interval=10),
    "tgbeta": Param(label=r"$\tan\beta$", color="purple", bins=25, range=[0, 50], interval=10),
}

nmssm_params_extended = nmssm_params.copy()
nmssm_params_extended.update({
    "m3": Param(label=r"$M_3\ \mathrm{[GeV]}$", color="olive", bins=25, range=[0, 2000], interval=500),
    "mq3": Param(label=r"$MQ3\ \mathrm{[GeV]}$", color="darksage", bins=25, range=[0, 2000], interval=500),
    "mu3": Param(label=r"$MU3\ \mathrm{[GeV]}$", color="darksage", bins=25, range=[0, 2000], interval=500),
    "au3": Param(label=r"$AU3\ \mathrm{[GeV]}$", color="cyan", bins=25, range=[0, 2000], interval=1000),
    "md3": Param(label=r"$MD3\ \mathrm{[GeV]}$", color="purple", bins=25, range=[0, 2000], interval=500),
    "ad3": Param(label=r"$AD3\ \mathrm{[GeV]}$", color="purple", bins=25, range=[0, 2000], interval=500),
    # "m0": Param(label=r"$M0$", color="purple", bins=25, range=[0, 2000], interval=-1),
    # "m12": Param(label=r"$M12$", color="purple", bins=25, range=[0, 2000], interval=-1),
})

nmssm_params_all = nmssm_params.copy()
nmssm_params_all.update({
    "m3": Param(label=r"$M_3$", color="olive", bins=25, range=[500, 3000], interval=-1),
    "m2": Param(label=r"$M_2$", color="olive", bins=25, range=[50, 1000], interval=-1),
    "m1": Param(label=r"$M_1$", color="olive", bins=25, range=[50, 500], interval=-1),
    "mq3": Param(label=r"$MQ3$", color="darksage", bins=25, range=[0, 2000], interval=-1),
    "mq2": Param(label=r"$MQ2$", color="darksage", bins=25, range=[0, 2000], interval=-1),
    "mu3": Param(label=r"$MU3$", color="darksage", bins=25, range=[0, 2000], interval=-1),
    "mu2": Param(label=r"$MU2$", color="darksage", bins=25, range=[0, 2000], interval=-1),
    "md3": Param(label=r"$MD3$", color="purple", bins=25, range=[0, 2000], interval=-1),
    "md2": Param(label=r"$MD2$", color="purple", bins=25, range=[0, 2000], interval=-1),
    "au3": Param(label=r"$AU3$", color="cyan", bins=25, range=[0, 2000], interval=-1),
    "ad3": Param(label=r"$AD3$", color="purple", bins=25, range=[0, 2000], interval=-1),
    "ml3": Param(label=r"$ML3$", color="purple", bins=25, range=[0, 2000], interval=-1),
    "ml2": Param(label=r"$ML2$", color="purple", bins=25, range=[0, 2000], interval=-1),
    "me3": Param(label=r"$ME3$", color="purple", bins=25, range=[0, 2000], interval=-1),
    "me2": Param(label=r"$ME2$", color="purple", bins=25, range=[0, 2000], interval=-1),
    "ae3": Param(label=r"$AE3$", color="purple", bins=25, range=[0, 2000], interval=-1),
    "ae2": Param(label=r"$AE2$", color="purple", bins=25, range=[0, 2000], interval=-1),
    # "m0": Param(label=r"$M0$", color="purple", bins=25, range=[0, 2000], interval=-1),
    # "m12": Param(label=r"$M12$", color="purple", bins=25, range=[0, 2000], interval=-1),
})

param_dict = dict(lambda_=r"$\lambda$", mueff=r"$\mu_{eff}\ \mathrm{[GeV]}$",
                  kappa=r"$\kappa$", alambda=r"$A_{\lambda}\ \mathrm{[GeV]}$",
                  akappa=r"$A_{\kappa}\ \mathrm{[GeV]}$", tgbeta=r"$\tan\beta$")


def save_plot(filename):
    """Save the plot. Auto creates dirs if necessary."""
    filename = os.path.abspath(filename)
    plot_dir = os.path.dirname(filename)
    if not os.path.isdir(plot_dir):
        os.makedirs(plot_dir)
    plt.savefig(filename)


def generate_fig(size=[6, 6]):
    """
    Simple figure generator, cos I'm really lazy.

    Makes a figure, can pass in a custom size.
    """
    fig = plt.figure()
    fig.set_size_inches(size[0], size[1])
    return fig


# legacy, remove me
def generate_axes(fig=None):
    """
    Simple axes generator, cos I'm super lazy.

    Puts 1 Axes object onto the figure (which is optional)
    """
    if not fig:
        fig = generate_fig()
    ax = fig.add_subplot(1, 1, 1)
    return ax


def generate_fig_axes(fig=None, size=[8, 6]):
    """
    Simple axes generator, cos I'm super lazy.

    Puts 1 Axes object onto the figure (which is optional)
    """
    if not fig:
        fig = generate_fig(size)
    ax = fig.add_subplot(1, 1, 1)
    return fig, ax


def set_major_tick_interval(which, interval):
    """Sets major tick intervals on an axis, cos I never remember this snippet"""
    if which.upper() == 'X':
        plt.gca().xaxis.set_major_locator(MultipleLocator(interval))
    elif which.upper() == 'Y':
        plt.gca().yaxis.set_major_locator(MultipleLocator(interval))
    else:
        raise RuntimeError('Cannot use %s to specify axis' % which)


def plot_histogram(ax=None, array=None, var=None, df=None,
                   label="", xlabel="", ylabel="N", title="",
                   errorbars=True, normed=False, **kwargs):
    """
    Generic histogram plotter. Can either plot variable var in DataFrame df,
    or plot a numpy array.

    ax: Axes object to plot on. If you don't pass one, it will make one for you.
    errorbars: can optionally show error bars
    normed: can optionally normalise so sum of bin contents = 1
    (irrespective of bin width)
    kwargs: other keyword args to pass to pyplot.histogram()
    """
    if not ax:
        ax = generate_axes()

    if array is not None:
        vals = array
    elif var is not None and df is not None:
        vals = df[var].dropna().values
    else:
        raise Exception("plot_histogram needs a numpy array or variable name + dataframe")

    weights = None
    if normed:
        weights = np.ones_like(vals) / len(vals)
    y, bins, patches = ax.hist(vals, weights=weights, label=label, **kwargs)
    if errorbars:
        # put error bars on
        bincenters = 0.5 * (bins[1:] + bins[:-1])
        menStd = np.sqrt(y)
        if normed:
            # need to do this otherwise it does errors incorrectly as
            # sqrt(normalised bin), not sqrt(bin)/sum of all bins
            menStd = menStd / np.sqrt(len(vals))
        width = 0.0
        ecolor = 'black' if 'color' not in kwargs.keys() else kwargs['color']
        ax.bar(bincenters, y, width=width, yerr=menStd, alpha=0,
               ecolor=ecolor, error_kw=dict(elinewidth=2, capthick=2))
    if xlabel == "":
        xlabel = var
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, y=1.04)
    plt.minorticks_on()
    plt.tight_layout()
    return ax, y, bins, patches


def plot_scatter(ax=None, xarray=None, yarray=None, xvar=None, yvar=None, df=None,
                 xlabel="", ylabel="", title="", **kwargs):
    """
    Generic scatter plot method. Can either plot variables yvar vs xvar from
    DataFrame df, or numpy arrays xarray vs yarray.

    ax: Axes object to plot on. If you don't pass one, it will make one for you.
    kwargs: other keyword args to pass to pyplot.scatter()
    """
    if not ax:
        ax = generate_axes()

    if xarray is not None and yarray is not None:
        vals_x, vals_y = xarray, yarray
    elif xvar is not None and yvar is not None and df is not None:
        vals_x, vals_y = df[xvar].values, df[yvar].values
    else:
        raise Exception("plot_scatter needs numpy arrays or variable names + dataframe")

    paths = ax.scatter(vals_x, vals_y, **kwargs)
    if xlabel == "":
        xlabel = xvar
    ax.set_xlabel(xlabel)
    if ylabel == "":
        ylabel = yvar
    ax.set_ylabel(ylabel)
    ax.set_title(title, y=1.04)
    plt.minorticks_on()
    plt.tight_layout()
    return ax, paths


def plot_histogram2d(ax=None,
                     df=None, xvar=None, yvar=None,
                     xarray=None, yarray=None,
                     bins=[25, 25], range=None,
                     xlabel=None, ylabel=None, zlabel=None,
                     norm_axis=None, **kwargs):
    """Make 2D histogram, with optional axis normalisation"""
    if ax is None:
        fig, ax = generate_fig_axes()

    if (xarray is not None and yarray is not None
        and df is None and xvar is None and yvar is None):
        vals_x, vals_y = xarray, yarray
    elif (xvar is not None and yvar is not None and df is not None
          and xarray is None and yarray is None):
        vals_x, vals_y = df[xvar].values, df[yvar].values
    else:
        raise Exception("plot_hist2d needs numpy arrays or variable names + dataframe")

    arr, xedges, yedges = np.histogram2d(vals_x.copy(), vals_y.copy(), bins=bins, range=range)


    # normalise bins along one axis,
    # so that the coloring highlights the "hot spot"
    # in each bin of that axis.
    if norm_axis not in [None, 'X', 'x', 'y', 'Y']:
        raise RuntimeError("norm_axis must be one of None, 'x', 'y' ")
    if norm_axis:
        if norm_axis.lower() == 'y':
            arr = arr.T
        # now set so the maximum in each bin is the same,
        # scale other bins accordingly
        for ind, xbin in enumerate(arr):
            if xbin.max() > 0:
                arr[ind] = xbin / xbin.max()
        if norm_axis.lower() == 'y':
            arr = arr.T

    qm = ax.pcolormesh(xedges, yedges, arr.T, edgecolors='None', **kwargs)

    xlabel = xlabel or ''
    ylabel = ylabel or ''
    zlabel = zlabel or ''
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.gcf().colorbar(qm, ax=ax, label=zlabel)
    plt.minorticks_on()
    plt.tight_layout()

    return ax, qm, arr


def add_median_line(df=None, var=None, array=None, **kwargs):
    """Add line showing median. Takes in numpy array, or Series val from DataFrame"""
    if array is not None:
        plt.axvline(x=np.median(array), **kwargs)
    elif df is not None and var:
        plt.axvline(x=df[var].median(), **kwargs)


def add_mean_line(df=None, var=None, array=None, **kwargs):
    """Add line showing mean. Takes in numpy array, or Series val from DataFrame"""
    if array is not None:
        plt.axvline(x=np.mean(array), **kwargs)
    elif df is not None and var:
        plt.axvline(x=df[var].mean(), **kwargs)


def plot_many_hists_compare(var, dfs, title, labels, xlabel, ylabel,
                            colors, errorbars=False, normed=False, **kwargs):
    """
    Plot hists of same var on same set of axes, to compare the distributions
    Note that normed here normalises the bins such that total bin contents
    sum to 1, irrespective of the bin width.
    """
    ax = generate_axes()
    max_y = 0
    for i, df in enumerate(dfs):
        y, bins, patches = plot_histogram(ax=ax, df=df, var=var, xlabel=xlabel,
                                          ylabel=ylabel, title=title,
                                          errorbars=errorbars, normed=normed,
                                          edgecolor=colors[i], **kwargs)
        max_y = max(max_y, max(y))
    ax.set_y(top=max_y)

    return plt.gcf(), ax


def plot_many_scatters_compare(varx, vary, dfs, title,
                               labels, xlabel, ylabel, colors, **kwargs):
    """
    Plot scatters of same var x & y on same set of axes, to compare distributions
    """
    # ax = dfs[0].plot(kind="scatter", x=varx, y=vary, title=title, color=colors[0], label=labels[0], **kwargs)
    ax = generate_axes()
    fig = plt.figure()
    plt.title(title)
    for i, df in enumerate(dfs):
        plt.scatter(x=df[varx].values, y=df[vary].values, color=colors[i], **kwargs)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # return ax


def plot_many_scatters(varx, vary, dfs, titles, xlabel, ylabel, **kwargs):
    """
    Make several side-by-side scatter plots to compare varx Vs vary for
    several dataframes

    dfs is a list of dataframes
    titles is a list of titles
    """
    if len(dfs) != len(titles):
        raise IndexError("len(dfs) != len(titles)")

    cols = 2
    rows = (len(dfs) / 2) + (len(dfs) % 2)
    if len(dfs) % 3 == 0:
            cols = 3
            rows = len(dfs) / 3
    fig, ax = plt.subplots(nrows=rows, ncols=cols)
    fig.set_size_inches(24, 8 * rows)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)

    axes = ax.reshape(-1)
    for i, [df, title] in enumerate(izip(dfs, titles)):
        df.plot(kind="scatter", x=varx, y=vary, ax=axes[i], **kwargs)
        axes[i].set_xlabel(xlabel)
        axes[i].set_ylabel(ylabel)
        axes[i].set_title(title, y=1.05)

    return fig, ax


def plot_many_hists(var, dfs, titles, xlabel, ylabel, same_y=True, **kwargs):
    """
    Make several side-by-side scatter plots to compare the same quantity for
    several dataframes

    dfs is a list of dataframes
    titles is a list of titles
    """
    if len(dfs) != len(titles):
        raise IndexError("len(dfs) != len(titles)")

    cols = 2
    rows = (len(dfs) / 2) + (len(dfs) % 2)
    if len(dfs) % 3 == 0:
            cols = 3
            rows = len(dfs) / 3
    fig, ax = plt.subplots(nrows=rows, ncols=cols)
    fig.set_size_inches(24, 8 * rows)
    plt.subplots_adjust(wspace=0.2)

    axes = ax.reshape(-1)
    for i, [df, title] in enumerate(izip(dfs, titles)):
        df[var].plot(kind="hist", x=varx, y=vary, ax=axes[i], title=title, **kwargs)
        axes[i].set_xlabel(xlabel)
        axes[i].set_ylabel(ylabel)

    if same_y:
        y_mins = [a.get_ylim()[0] for a in axes]
        y_maxs = [a.get_ylim()[1] for a in axes]
        miny = min(y_mins)
        maxy = max(y_maxs)
        for a in axes:
            a.set_ylim([miny, maxy])
    return fig, ax


def paper_compare_plot1(df, title):
    """
    Make a pair of plots a la Fig2 in the NEB/Moretti/et al paper

    The LH plot is mh1 Vs ma1, coloured by tan(beta)
    The RH plot is mh1 Vs kappa, coloured by lambda
    """
    import matplotlib as mpl
    fig, ax = plt.subplots(nrows=1, ncols=2)
    fig.set_size_inches(24, 8)
    plt.subplots_adjust(wspace=0.2)

    col_map = mpl.cm.cool

    fig.suptitle(r"$h_{SM}\ =\ h_1$", fontsize=34, y=1.05)

    df.plot(kind="scatter", x="ma1", y="mh1", marker="+", ax=ax[0],
            c=df.tgbeta, cmap=col_map, vmin=0, vmax=50)
    ax[0].set_xlim([0, 150])
    ax[0].set_ylim([122, 129])
    ax[0].set_xlabel(r"$m_{a_1}\ \mathrm{[GeV]}$")
    ax[0].set_ylabel(r"$m_{h_1}\ \mathrm{[GeV]}$")
    ax[0].set_title(title, y=1.03)

    df.plot(kind="scatter", x="kappa", y="mh1", marker="+", ax=ax[1],
            c=df["lambda_"], cmap=col_map, vmin=0, vmax=0.7, title=title)
    ax[1].set_xlim([0, 0.7])
    ax[1].set_ylim([122, 129])
    ax[1].set_xlabel(r"$\kappa$")
    ax[1].set_ylabel(r"$m_{h_1}\ \mathrm{[GeV]}$")
    ax[1].set_title(title, y=1.03)

    return fig, ax


def texify_str(p):
    # Make the labels tex-friendly
    p = "$\mathrm{" + p + "}$"
    p = p.replace(r"_s", r"}_{s}\mathrm{")
    p = p.replace(r"_d", r"}_{d}\mathrm{")
    # p = p.replace(r"_", r"\_")
    p = p.replace(r"gamma", r"}\gamma\mathrm{")
    p = p.replace(r"->gg", r"}\to\gamma\gamma\mathrm{")
    p = p.replace(r">>", r"}\gg\mathrm{")
    p = p.replace(r"->", r"}\to\mathrm{")
    # p = p.replace(r">", r"\gt")
    p = p.replace(r"~~~", r"\ ")
    p = p.replace(r"~~", r"\ ")
    # p = p.replace(r"too", r"too ")
    # p = p.replace(r"to", r"to ")
    p = p.replace(r"chi2", r"}\chi^2\mathrm{")
    p = p.replace(r"Delta", r"}\Delta\mathrm{")
    p = p.replace(r"Msusy", r"}M_{SUSY}\mathrm{")
    p = p.replace(r"MGUT", r"}M_{GUT}\mathrm{")
    p = p.replace(r"tautau", r"}\tau\tau\mathrm{")
    p = p.replace(r" tau nu", r"}\tau \nu\mathrm{")
    p = p.replace(r"mu+ mu-", r"}\mu^+\mu^-\mathrm{")
    p = p.replace(r"mu +mu-", r"}\mu^+\mu^-\mathrm{")
    # p = p.replace(r" nu", r"\nu")
    p = p.replace(r" ", r"\ ")
    return p


def plot_constraints(df, title, num=10, failing_only=True):
    """
    This plots a bar chart of the most popular reasons
    for points failing experimental constraints, in a given DataFrame.
    It will plot the top X% of reasons (see below)
    """

    c = df["constraints"].tolist()
    cons = []
    for cc in c:
        if cc:
            cons.extend(cc.split("|"))
        else:
            cons.extend('None')

    s = pd.Series(cons)
    vc = s.value_counts()
    if failing_only:
        vc /= 0.01 * float(len(df[df.constraints != ''].index))
    else:
        vc /= 0.01 * float(len(df.index))

    # find out how many points make up the top X%
    # last_i = next(x[0] for x in enumerate(vc_cum) if x[1] > fraction)

    vc.index = [texify_str(x) for x in vc.index]

    # make the graph here
    fig = generate_fig([8, 6])
    ax = generate_axes(fig)
    vc[:num][::-1].plot(kind="barh")  # this ensures most common at top
    ax.set_xlabel("% of points that fail given constraint",
                  multialignment='center', fontsize=22)
    ax.set_title(title, y=1.03)
    return ax, vc

# make a map of channel numbers Vs channel names from HiggsBounds
HB_MAP = {}
with open('Key.dat') as hb_file:
    for line in hb_file:
        if line.startswith("process"):
            channel = int(line.split()[1])
            line = next(hb_file)
            channel_name = line.strip()
            HB_MAP[channel] = channel_name


def plot_constraints_HB(df, title, num=10):
    """Plot bar chart of most popular reasons for points failing HiggsBounds.
    Note that each HiggsBounds only tells you the most sensitive experimental
    result the point failed (unlike NMSSMTools, which tells you all the reasons
    a point failed).
    """

    c = df["HBchannel"].tolist()
    cons = []
    for cc in c:
        if cc:
            cons.append(HB_MAP[int(cc)])
    # print cons

    s = pd.Series(cons)
    vc = s.value_counts()
    vc /= float(len(df.index))
    # vc_cum = vc.cumsum()

    # find out how many points make up the top X%
    # last_i = next(x[0] for x in enumerate(vc_cum) if x[1] > fraction)

    # make the graph here
    # fig, ax = plt.subplots(nrows=1, ncols=1)
    # fig.set_size_inches(6, 4)
    fig = generate_fig([8, 6])
    ax = generate_axes(fig)
    vc[:num][::-1].plot(kind="barh", color='green', fontsize=14)
    ax.set_xlabel("Most sensitive channel for HB",
                  multialignment='center', fontsize=22)
    # ax.set_xlabel("Fraction of failing points that fail given HiggsBounds constraint\n"
    #               "(encompassing " + str(fraction * 100) + " % of all failing points)",
    #               multialignment='center', fontsize=22)
    ax.set_title(title, y=1.03)
    return ax


def plot_input_params_hists(df, ylabel, title, errorbars=True, param_dict=nmssm_params, cols=3, **kwargs):
    """Make histograms for each input parameter using dataframe df"""
    # Calculate sensible number of rows & columns.
    rows = (len(param_dict.keys()) / cols) + (len(param_dict.keys()) % cols)
    # Setup plotting ares
    fig = plt.figure()
    fig.suptitle(title)
    fig.set_size_inches(6 * cols, 6 * rows)
    plt.subplots_adjust(wspace=0.3)
    plt.subplots_adjust(hspace=0.3)

    # Make a subplot for each param, then plot it
    # Need to use Series (aka numpy array), can't use df.plot() as x labels
    # do not show up except on final row.
    # And since the np array must be indexed properly, we use .values to
    # get out a raw array.
    for i, (param, attr) in enumerate(param_dict.items()):
        ax = fig.add_subplot(rows, cols, i + 1)
        y, bins, patches = plt.hist(df[param].values, color=attr.color, **kwargs)
        if errorbars:
            # put error bars on
            bincenters = 0.5 * (bins[1:] + bins[:-1])
            menStd = np.sqrt(y)
            width = 0.0
            plt.bar(bincenters, y, width=width, yerr=menStd, alpha=0, ecolor="black", error_kw=dict(elinewidth=2, capthick=2))
        ax.set_xlabel(attr.label)
        ax.set_ylabel(ylabel)
        plt.minorticks_on()


def plot_input_params_hists_multiple(dfs, ylabel, title, errorbars=True, param_dict=nmssm_params, cols=3, kwargs=None):
    """Make histograms for each input parameter using dataframe df"""
    # Calculate sensible number of rows & columns.
    rows = (len(param_dict.keys()) / cols) + (len(param_dict.keys()) % cols)
    # Setup plotting ares
    fig = plt.figure()
    fig.suptitle(title)
    fig.set_size_inches(6 * cols, 6 * rows)
    plt.subplots_adjust(wspace=0.3)
    plt.subplots_adjust(hspace=0.3)

    # Make a subplot for each param, then plot it
    # Need to use Series (aka numpy array), can't use df.plot() as x labels
    # do not show up except on final row.
    # And since the np array must be indexed properly, we use .values to
    # get out a raw array.
    for i, (param, attr) in enumerate(param_dict.items()):
        ax = fig.add_subplot(rows, cols, i + 1)
        for df, kw in zip(dfs, kwargs):
            if 'color' not in kw:
                kw['color'] = attr.color
            if 'range' not in kw:
                kw['range'] = attr.range
            vals = df.query('%f<%s<%f' % (attr.range[0], param, attr.range[1]))[param].values
            if len(vals) > 0:
                # y, bins, patches = ax.hist(vals, **kw)
                plot_histogram(ax=ax, array=vals, **kw)

        # # put error bars on
        # bincenters = 0.5 * (bins[1:] + bins[:-1])
        # menStd = np.sqrt(y)
        # width = 0.0
        # plt.bar(bincenters, y, width=width, yerr=menStd, alpha=0, ecolor="black", error_kw=dict(elinewidth=2, capthick=2))
        ax.set_xlabel(attr.label)
        ax.set_ylabel(ylabel)
        plt.minorticks_on()


def plot_input_params_scatters(df, yvar, ylabel, yrange=None, title="", param_dict=nmssm_params, cols=3, **kwargs):
    """Make scatter plots for each input parameter against variable var,
    using dataframe df"""

    # Calculate sensible number of rows & columns.
    rows = (len(param_dict.keys()) / cols) + (len(param_dict.keys()) % cols)
    # Setup plotting ares
    fig = plt.figure()
    fig.suptitle(title)
    fig.set_size_inches(6 * cols, 6 * rows)
    plt.subplots_adjust(wspace=0.3)
    plt.subplots_adjust(hspace=0.3)

    # Make a subplot for each param, then plot it
    # Need to use Series (aka numpy array), can't use df.plot() as x labels
    # do not show up except on final row.
    # And since the np array must be indexed properly, we use .values to
    # get out a raw array.
    for i, (param, attr) in enumerate(param_dict.iteritems()):
        ax = fig.add_subplot(rows, cols, i + 1)
        plt.scatter(x=df[param].values, y=df[yvar].values, color=attr.color, **kwargs)
        ax.set_xlabel(attr.label)
        # ax.set_xlim(attr.range)
        ax.set_ylabel(ylabel)
        if yrange:
            ax.set_ylim(yrange)
        plt.minorticks_on()
        if attr.interval != -1:
            set_major_tick_interval('X', attr.interval)


def plot_input_params_scatters_multiple(dfs, yvar, ylabel, yrange=None, title="",
                                        param_dict=nmssm_params, cols=3, kwargs=None):
    """Make scatter plots for each input parameter against variable var,
    using dataframe df"""

    # Calculate sensible number of rows & columns.
    rows = (len(param_dict.keys()) / cols) + (len(param_dict.keys()) % cols)
    # Setup plotting ares
    fig = plt.figure()
    fig.suptitle(title)
    fig.set_size_inches(6 * cols, 6 * rows)
    plt.subplots_adjust(wspace=0.3)
    plt.subplots_adjust(hspace=0.3)

    # Make a subplot for each param, then plot it
    # Need to use Series (aka numpy array), can't use df.plot() as x labels
    # do not show up except on final row.
    # And since the np array must be indexed properly, we use .values to
    # get out a raw array.
    for i, (param, attr) in enumerate(param_dict.iteritems()):
        ax = fig.add_subplot(rows, cols, i + 1)
        for df, kw in zip(dfs, kwargs):
            if kw and 'color' not in kw:
                kw['color'] = attr.color
            plt.scatter(x=df[param].values, y=df[yvar].values, **kw)

        ax.set_xlabel(attr.label)
        # ax.set_xlim(attr.range)
        ax.set_ylabel(ylabel)
        if yrange:
            ax.set_ylim(yrange)
        plt.minorticks_on()
        if attr.interval != -1:
            set_major_tick_interval('X', attr.interval)


def plot_input_params_hexbin(df, yvar, ylabel, yrange=None, title="", param_dict=nmssm_params, cols=3, **kwargs):
    """Make scatter plots for each input parameter against variable var,
    using dataframe df"""

    # Calculate sensible number of rows & columns.
    rows = (len(param_dict.keys()) / cols) + (len(param_dict.keys()) % cols)
    # Setup plotting ares
    fig = plt.figure()
    fig.suptitle(title)
    fig.set_size_inches(6 * cols, 6 * rows)
    plt.subplots_adjust(wspace=0.3)
    plt.subplots_adjust(hspace=0.3)

    # Make a subplot for each param, then plot it
    # Need to use Series (aka numpy array), can't use df.plot() as x labels
    # do not show up except on final row.
    # And since the np array must be indexed properly, we use .values to
    # get out a raw array.
    for i, (param, attr) in enumerate(param_dict.iteritems()):
        ax = fig.add_subplot(rows, cols, i + 1)
        # plt.scatter(x=df[param].values, y=df[yvar].values, color=attr.color, **kwargs)
        plt.hexbin(x=df[param].values, y=df[yvar].values, **kwargs)
        ax.set_xlabel(attr.label)
        # ax.set_xlim(attr.range)
        ax.set_ylabel(ylabel)
        if yrange:
            ax.set_ylim(yrange)
        plt.minorticks_on()
        if attr.interval != -1:
            set_major_tick_interval('X', attr.interval)


def plot_input_params_hist2d(df, yvar, ylabel, yrange=None, title="", param_dict=nmssm_params, cols=3, **kwargs):
    """Make 2d histogram plots for each input parameter against variable var,
    using dataframe df"""

    # Calculate sensible number of rows & columns.
    rows = (len(param_dict.keys()) / cols) + (len(param_dict.keys()) % cols)
    # Setup plotting ares
    fig = plt.figure()
    fig.suptitle(title)
    fig.set_size_inches(6 * cols, 6 * rows)
    plt.subplots_adjust(wspace=0.3)
    plt.subplots_adjust(hspace=0.3)

    # Make a subplot for each param, then plot it
    # Need to use Series (aka numpy array), can't use df.plot() as x labels
    # do not show up except on final row.
    # And since the np array must be indexed properly, we use .values to
    # get out a raw array.
    for i, (param, attr) in enumerate(param_dict.iteritems()):
        ax = fig.add_subplot(rows, cols, i + 1)

        plot_histogram2d(ax=ax, df=df, xvar=param, yvar=yvar, **kwargs)

        ax.set_xlabel(attr.label)
        # ax.set_xlim(attr.range)
        ax.set_ylabel(ylabel)
        if yrange:
            ax.set_ylim(yrange)
        plt.minorticks_on()
        if attr.interval != -1:
            set_major_tick_interval('X', attr.interval)


def make_highlight_region(ax, limits, axis, **kwargs):
    """
    Make a semi-transparent patch to highlight a region on a given axis.

    ax is the Axes object you want to plot it on.
    limits is a list of [min, max] for the variable
    axis is the axis that represents the variable in question, e.g. 'x'
    kwargs passes keyword arguments to patches.Rectagle
    """
    xmin, xmax = 0, 0
    ymin, ymax = 0, 0
    if axis.lower() == 'x':
        xmin, xmax = limits
        ymin, ymax = ax.get_ylim()
    else:
        ymin, ymax = limits
        xmin, xmax = ax.get_xlim()
    if not kwargs:
        kwargs = dict(color='grey', alpha=0.5)
    patch = patches.Rectangle((xmin, ymin), xmax - xmin, ymax - ymin, **kwargs)
    ax.add_patch(patch)
    return patch

# LIMITS
# -----------------------------------------------------------------------------
# HIG 14 019 limit:
cms_limits_4tau_xsec = {4: 7.1, 5: 10.3, 6: 8.6, 7: 5.0, 8: 4.5}


def plot_cms_limit(ax=None, color='red', **kwargs):
    """
    Plot limits from the CMS 4tau paper (HIG-14-019), at 8TeV.
    """
    # mass: xsec*BR limit
    limits = OrderedDict(sorted(cms_limits_4tau_xsec.items(), key=lambda t: t))
    masses = limits.keys()
    xsecs = limits.values()
    if not ax:
        ax = plt.gca()
    ax.plot(masses, xsecs, label='CMS 8 TeV limit (HIG-14-019)', color=color, **kwargs)
    upper_edge = np.ones_like(xsecs) * ax.get_ylim()[1]
    ax.fill_between(masses, xsecs, y2=upper_edge, where=xsecs < upper_edge,
                    label='CMS 8 TeV limit (HIG-14-019)', alpha=0.3, color=color)


# The boosted tau ID analysis:
cms_limits_4tau_boostedTau_xsec = {5: 558.84, 7: 10.5535, 9: 4.9436, 11: 3.5465, 13: 3.6754, 15: 5.4594}


def plot_cms_boostedTau_limit(ax=None, color='red', **kwargs):
    """
    Plot limits from the CMS 4tau bboosted tau ID paper (HIG-14-022), at 8TeV.
    """
    # mass: xsec*BR limit
    limits = OrderedDict(sorted(cms_limits_4tau_boostedTau_xsec.items(), key=lambda t: t))
    masses = limits.keys()
    xsecs = limits.values()
    if not ax:
        ax = plt.gca()
    ax.plot(masses, xsecs, label='CMS 8 TeV limit (HIG-14-022)', color=color, **kwargs)
    upper_edge = np.ones_like(xsecs) * ax.get_ylim()[1]
    ax.fill_between(masses, xsecs, y2=upper_edge, where=xsecs < upper_edge,
                    label='CMS 8 TeV limit (HIG-14-022)', alpha=0.3, color=color)


# these are limits having divided by sigma_SM(ggh) = 19.27
atlas_limits_br = {3.7: 3.59E-2, 4: 4.93E-2, 5: 8.61E-2, 6: 1.27E-1, 7: 1.59E-1, 8: 1.02E-1, 9: 1.20E-1, 10: 4.19E-1, 11: 1.25E-1, 12: 2.73E-1, 13: 3.05E-1, 14: 3.48E-1, 15: 3.35E-1, 16: 3.75E-1, 17: 3.35E-1, 18: 5.34E-1, 19: 3.11E-1, 20: 5.86E-1, 25: 5.97E-1, 30: 7.46E-1, 35: 1.19, 40: 7.6E-1}
atlas_limits_xsec = {4: 0.950011, 5: 1.659147, 6: 2.44729, 7: 3.06393, 8: 1.96554, 9: 2.3124, 10: 8.07413, 11: 2.40875, 12: 5.26071, 13: 5.87735, 14: 6.70596, 15: 6.45545, 16: 7.22625, 17: 6.45545, 18: 10.29018, 19: 5.99297, 20: 11.29222, 25: 11.50419, 30: 14.37542, 35: 22.9313, 40: 14.6452, 3.7: 0.691793}


def plot_atlas_limit(ax=None, color='red', **kwargs):
    """
    Plot limits from the ATLAS mumutautau paper, at 8TeV.
    """
    # mass: xsec*BR/xsec_SM, so need to * SM
    limits = OrderedDict(sorted(atlas_limits_xsec.items(), key=lambda t: t))
    masses = limits.keys()
    xsecs = limits.values()
    if not ax:
        ax = plt.gca()
    ax.plot(masses, xsecs, label='ATLAS 8 TeV limit', color=color, **kwargs)
    upper_edge = np.ones_like(xsecs) * ax.get_ylim()[1]
    ax.fill_between(masses, xsecs, y2=upper_edge, where=xsecs < upper_edge,
                    label='ATLAS 8 TeV limit', alpha=0.3, color=color)


def pass_limit(m_a, xsec, limits_dict):
    """Return bool as to whether cross-section for xsec * BR(h -> aa -> 4tau)
    passes given limits.

    m_a: mass of a
    xsec: total xsec * BR(h -> aa ->4tau)
    limits: ordered dict of {mass: limit}
    """
    # limits = OrderedDict(sorted(limits_dict.items(), key=lambda t: t))
    if m_a > max(limits_dict.keys()) or m_a < min(limits_dict.keys()):
        # outside of range of limits - pass
        return True
    else:
        masses = limits_dict.keys()
        xsecs = limits_dict.values()
        ind_upper = bisect(masses, m_a)
        # do linear interpolation to get limit based on closest mass points
        xsec_interp = np.interp(m_a, masses[ind_upper - 1:ind_upper + 1],
                                xsecs[ind_upper - 1:ind_upper + 1])
        return xsec < xsec_interp


def pass_new_limits_4tau(m_a, xsec):
    """Return bool as to whether cross-section for xsec * BR(h -> aa -> 4tau) passes CMS & ATLAS limits.
    m_a: mass of a
    xsec: total xsec * BR(h -> aa ->4tau)
    """
    return (pass_limit(m_a, xsec, atlas_limits_xsec) and
            pass_limit(m_a, xsec, cms_limits_4tau_xsec) and
            pass_limit(m_a, xsec, cms_limits_4tau_boostedTau_xsec))



