"""
Fns to make common types of plots
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from itertools import izip
from collections import namedtuple


# NMSSM params with various associated attributes, such as latex equivalents
# for axis labels, colours, binning for histograms, etc
Param = namedtuple('Param', ['label', 'color', 'bins', 'range'])

nmssm_params = {"lambda_": Param(label=r"$\lambda$", color="orange", bins=25, range=[0, 0.7]),
                "mueff": Param(label=r"$\mu_{eff}\ \mathrm{[GeV]}$", color="green", bins=25, range=[100, 300]),
                "kappa": Param(label=r"$\kappa$", color="steelblue", bins=25, range=[0, 0.7]),
                "alambda": Param(label=r"$A_{\lambda}\ \mathrm{[GeV]}$", color="salmon", bins=25, range=[-1000, 4000]),
                "akappa": Param(label=r"$A_{\kappa}\ \mathrm{[GeV]}$", color="red", bins=25, range=[-30, 2.5]),
                "tgbeta": Param(label=r"$\tan\beta$", color="purple", bins=25, range=[0, 50])
                }


def plot_many_hists_compare(var, dfs, title, labels, xlabel, ylabel, colors, **kwargs):
    """
    Plot hists of same var on same set of axes, to compare the distributions
    """
    # ax = dfs[0][var].plot(kind="hist", title=title, color=colors[0], label=labels[0], edgecolor=colors[0], **kwargs)
    plt.title(title)
    for i, df in enumerate(dfs):
        plt.hist(df[var].values, color=colors[i], label=labels[i], edgecolor=colors[i], **kwargs)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    # return ax


def plot_many_scatters_compare(varx, vary, dfs, title, labels, xlabel, ylabel, colors, **kwargs):
    """
    Plot scatters of same var x & y on same set of axes, to compare the distributions
    """
    # ax = dfs[0].plot(kind="scatter", x=varx, y=vary, title=title, color=colors[0], label=labels[0], **kwargs)
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
    fig.set_size_inches(24, 8*rows)
    plt.subplots_adjust(wspace=0.3, hspace=0.3)

    axes = ax.reshape(-1)
    for i, [df,title] in enumerate(izip(dfs, titles)):
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
    fig.set_size_inches(24, 8*rows)
    plt.subplots_adjust(wspace=0.2)

    axes = ax.reshape(-1)
    for i, [df,title] in enumerate(izip(dfs, titles)):
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
    ax[0].set_ylim([122,129])
    ax[0].set_xlabel(r"$m_{a_1}\ \mathrm{[GeV]}$")
    ax[0].set_ylabel(r"$m_{h_1}\ \mathrm{[GeV]}$")
    ax[0].set_title(title, y=1.03)

    df.plot(kind="scatter", x="kappa", y="mh1", marker="+", ax=ax[1],
            c=df["lambda_"], cmap=col_map, vmin=0, vmax=0.7, title=title)
    ax[1].set_xlim([0, 0.7])
    ax[1].set_ylim([122,129])
    ax[1].set_xlabel(r"$\kappa$")
    ax[1].set_ylabel(r"$m_{h_1}\ \mathrm{[GeV]}$")
    ax[1].set_title(title, y=1.03)

    return fig, ax


def plot_constraints(df, title):
    """
    This plots a bar chart of the most popular reasons
    for points failing experimental constraints, in a given DataFrame.
    It will plot the top X% of reasons (see below)
    """

    c = df["constraints"].tolist()
    cons = []
    for cc in c:
        if cc:
            for p in cc.split("/"):
                p = "$\mathrm{"+p+"}$"
                p = p.replace(r"_", r"\_")
                p = p.replace(r"_s", r"\_{s}")
                p = p.replace(r"_d", r"\_{d}")
                p = p.replace(r"gamma", r"\gamma")
                p = p.replace(r"->gg", r"->\gamma\gamma")
                p = p.replace(r">>", r"\gg")
                p = p.replace(r"->", r"\to")
                # p = p.replace(r">", r"\gt")
                p = p.replace(r" ", r"\ ")
                p = p.replace(r"~~~", r"\ ")
                p = p.replace(r"~~", r"\ ")
                p = p.replace(r"to", r"to ")
                p = p.replace(r"chi2", r"}\chi^2 \mathrm{")
                p = p.replace(r"Delta", r"}\Delta \mathrm{")
                p = p.replace(r"Msusy", r"M_{SUSY}")
                p = p.replace(r"MGUT", r"M_{GUT}")
                p = p.replace(r"tautau", r"\tau\tau")
                cons.append(p)


    # use Series
    s = pd.Series(cons)
    vc = s.value_counts(normalize=True)
    vc_cum = vc.cumsum()

    # find out how many points make up the top X%
    limit = 0.9
    last_i = next(x[0] for x in enumerate(vc_cum) if x[1] > limit)

    # make the graph here
    fig, ax = plt.subplots(nrows=1, ncols=1)
    fig.set_size_inches(6, 4)
    vc[:last_i].plot(kind="barh")
    ax.set_xlabel("Fraction of failing points that fail given experimental constraint\n(encompassing " + str(limit*100) + " % of all failing points)",
                multialignment='center', fontsize=22)
    ax.set_title(title, y=1.03)
    return ax


def plot_input_params_hists(df, ylabel, title, errorbars=True, **kwargs):
    """Make histograms for each input parameter using dataframe df"""
    # Calculate sensible number of rows & columns.
    cols = 2
    rows = (len(nmssm_params.keys()) / 2) + (len(nmssm_params.keys()) % 2)
    if len(nmssm_params.keys()) % 3 == 0:
        cols = 3
        rows = len(nmssm_params.keys()) / 3
    # Setup plotting ares
    fig = plt.figure()
    fig.suptitle(title, fontsize=30)
    fig.set_size_inches(24, 8*rows)
    plt.subplots_adjust(wspace=0.3)
    plt.subplots_adjust(hspace=0.3)

    # Make a subplot for each param, then plot it
    # Need to use Series (aka numpy array), can't use d.fplot() as x labels
    # do not show up except on final row.
    # And since the np array must be indexed properly, we use .values to
    # get out a raw array.
    for i, (param, attr) in enumerate(nmssm_params.items()):
        ax = fig.add_subplot(rows, cols, i+1)
        y, bins, patches = plt.hist(df[param].values, color=attr.color, **kwargs)
        # put error bars on
        bincenters = 0.5*(bins[1:]+bins[:-1])
        menStd = np.sqrt(y)
        width = 0.0
        plt.bar(bincenters, y, width=width, yerr=menStd, alpha=0, ecolor="black", error_kw=dict(elinewidth=2, capthick=2))
        ax.set_xlabel(attr.label)
        ax.set_ylabel(ylabel)
        plt.minorticks_on()



def plot_input_params_scatters(df, yvar, ylabel, yrange=None, title="", **kwargs):
    """Make scatter plots for each input parameter against variable var,
    using dataframe df"""

    # Calculate sensible number of rows & columns.
    cols = 2
    rows = (len(nmssm_params.keys()) / 2) + (len(nmssm_params.keys()) % 2)
    if len(nmssm_params.keys()) % 3 == 0:
        cols = 3
        rows = len(nmssm_params.keys()) / 3
    # Setup plotting ares
    fig = plt.figure()
    fig.suptitle(title, fontsize=30)
    fig.set_size_inches(24, 8*rows)
    plt.subplots_adjust(wspace=0.3)
    plt.subplots_adjust(hspace=0.3)

    # Make a subplot for each param, then plot it
    # Need to use Series (aka numpy array), can't use d.fplot() as x labels
    # do not show up except on final row.
    # And since the np array must be indexed properly, we use .values to
    # get out a raw array.
    for i, (param, attr) in enumerate(nmssm_params.items()):
        ax = fig.add_subplot(rows, cols, i+1)
        plt.scatter(x=df[param].values, y=df[yvar].values, color=attr.color, **kwargs)
        ax.set_xlabel(attr.label)
        ax.set_xlim(attr.range)
        ax.set_ylabel(ylabel)
        if yrange:
            ax.set_ylim(yrange)
        plt.minorticks_on()


def plot_xsec_scatter():
    """Plot"""
    pass
