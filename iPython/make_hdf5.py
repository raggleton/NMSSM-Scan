#!/usr/bin/env python

"""

Make a HDF5 binary from lots of CSV files so it can be easily used in pandas

"""

import sys
import argparse
import pandas as pd
import numpy as np
import glob
import math
from itertools import product, chain, permutations
from shutil import copyfile


def load_df(folders, filestem):
    """Load dataframe with CSV files from several folders in directory arg,
    from CSV files named <filestem>[0-9]*.dat

    Works by first making a large CSV file from all the consituent CSV files,
    and then reading that into a dataframe.

    I did try using the concat() and merge() methods, however their performance
    is much worse - appending is numpy's slow point, and it consumed a lot
    of memory to keep all those individual dataframes open and then concat them.
    """
    file_list = []
    for fo in folders:
        print "Getting CSVs from:", fo
        file_list += [fi for fi in glob.glob(fo + "/%s[0-9]*.dat" % filestem)]

    if not file_list:
        raise IndexError("file_list is empty - are you sure you've input the correct folders?")

    # Make a copy of the first file (so we can keep the column headers)
    copyfile(file_list[0], "merge.csv")

    # Now add the data rows of the rest of the files to the massive csv file
    with open("merge.csv", "a") as fout:
        for csv in file_list[1:]:
            with open(csv, "r") as fin:
                print "Adding", csv
                next(fin)  # skip header
                for line in fin:
                    fout.write(line)

    print "Making dataframe..."
    df = pd.read_csv("merge.csv", delimiter=",")

    # rename from column "lambda" to "lambda_"
    df.rename(columns={'lambda':'lambda_'}, inplace=True)

    # Fix the constraints column, such that the ones that pass (i.e. == "",
    # which pandas interprets as NaN) have NaN replaced by something sensible
    df.fillna({"constraints":""}, axis=0, inplace=True)

    print "Entries:", len(df.index)
    print "Columns:", df.columns.values
    return df


def store_channel_xsec(df):
    """
    Calculate total cross-section & scaled cross-sections
    for gg->h1->a1a1, gg->h2->a1a1, gg->h2->h1h1,
    with final states 4tau, 2b2tau, 4b.
    Denoted as gg -> X -> YY ->f1f1f2f2
    """
    process_scaled = [] # Store them for later
    process = []

    # low mass channels, gg - X -> 2Y -> 4F/2F+2F'
    # prod = {'ggf': 'ggrc2', 'vbf': 'vvrc2', 'zh':'vvrc2', 'wh':'vvrc2'}
    prod = {'ggf': 'ggrc2'}
    X = ["h1", "h2", 'h3']
    Y = ["a1", "h1"]
    F = ["tautau", "bb"]
    for production, coupling in prod.iteritems():
        for x, y in product(X,Y):
            if x == y:
                continue
            for f1, f2 in product(F,F):
                ff = ""
                factor = 1
                if f1 == f2 == "tautau":
                    ff = "4tau"
                elif f1 == f2 == "bb":
                    ff = "4b"
                else:
                    factor = 2
                    ff = "2b2tau"
                name = "xsec_scaled_"+production+"_"+x+"_"+"2"+y+"_"+ff
                if not name in process_scaled:
                    # store scaled total XS * BR
                    process_scaled.append(name)
                    df[name] = df[x+coupling] * df["Br"+x+y+y] * df["Br"+y+f1] * df["Br"+y+f2] * factor
                    # store actual XS * BR
                    # we store it twice for backwards-compatibility otherwise old script break
                    name = name.replace("_scaled", "")
                    process.append(name)
                    df[name] = df["xsec_"+production+"13_"+x] * df[x+coupling] * df["Br"+x+y+y] * df["Br"+y+f1] * df["Br"+y+f2] * factor
                    # name_new = name.replace("xsec", "xsec13")
                    # df[name_new] = df[name]
                    # name = name_new.replace("13", "8")
                    # df[name] = df["xsec_ggf8_"+x] * df[x+"ggrc2"] * df["Br"+x+y+y] * df["Br"+y+f1] * df["Br"+y+f2] * factor

    # More for middle mass channels, ZA1, etc
    prod = {'ggf': 'ggrc2', 'vbf': 'vvrc2', 'zh':'vvrc2', 'wh':'vvrc2'}
    br_z_ll = (3.363 + 3.366)/100.  # for Z->ee/mumu, taken frmo PDG




def subset_pass_constraints(df):
    """Return dataframe where points pass all constraints, except ones we select

    We take the constraints string, then do a replace() with each constraint
    and see what's left over.
    """
    # All the constraints strings to test against. Must follow regex.
    constraints = [
        r"Muon magn\. mom\. more than 2 sigma away",
        r"Relic density too small \(Planck\)"
        # r"Excluded by sparticle searches at the LHC",
        # r"Excluded by ggF/bb\->H/A\->tautau at the LHC",
        # r"Excluded H_125\->AA\->4mu \(CMS\)",
        # r"Excluded by ggF\->H/A\->gamgam \(ATLAS\)"
    ]

    # We want a bitmask, so for each entry we simply want a True or False
    # First make a copy of the constraints Series
    con_series = df.constraints.copy(deep=True)
    # Now for each entry we remove the constraints we don't mind failing
    for c in constraints:
        con_series = con_series.str.replace(c, "")
    con_series = con_series.str.replace(r"^/+$", "") # Any leftover separators
    # Now figure out which ones are empty
    mask = con_series.str.match("^$")
    # Return those entries, allowing for a +ve muon mag moment contribution
    return df[mask & (df.Del_a_mu > 0)]


def subset_var(df, min_var, max_var, var):
    """Make subset based on range of object value"""
    var_max = df[var] < max_var
    var_min = df[var] > min_var
    return df[var_min & var_max]


def make_dataframes(folders, file_stem):
    """Load files into Panda dataframes

    CSV files are read in from the folders listed in the arg.
    Certain columns are dropped.
    Cross-section information is added, both scaled (relative to SM) and absolute.
    A subset dataframe is made for points passing experimental contraints.
    Subsets of this are made for bosons with a particular mass range.

    All these dataframes are returned.
    """

    print "Making one big dataframe..."
    df_orig = load_df(folders, file_stem)
    # df_orig = load_df(folders, "output")
    # df_orig = load_df(folders, "output_ma1Lt11")
    # df_orig = load_df(folders, "output_good")

    # Drop columns tp save space
    drop_cols = ['h1u', 'h1d', 'h1b', 'h1V', 'h1G', 'h1A',
                 'h2u', 'h2d', 'h2b', 'h2V', 'h2G', 'h2A',
                 # 'Brh3gg', 'Brh3tautau', 'Brh3bb', 'Brh3ww',
                 # 'Brh3zz', 'Brh3gammagamma', 'Brh3zgamma', 'Brh3h1h1', 'Brh3h2h2', 'Brh3h1h2',
                 # 'Brh3a1a1', 'Brh3a1z',
                 'bsgamma', 'bsmumu', 'btaunu', 'delms', 'delmd']
    for col in drop_cols:
        if col in df_orig.columns.values:
            df_orig.drop(col, inplace=True, axis=1)
    print "After dropping columns:", df_orig.columns.values, len(df_orig.columns.values), "columns"

    # Remove any duplicate entries
    df_orig.drop_duplicates(inplace=True)

    # Load up the glu-glu cross sections for 13 TeV
    print "Adding in cross-sections..."
    # cs = pd.read_csv("parton_lumi_ratio.csv")
    cs = pd.read_csv("YR3_cross_sections.csv")
    masses = cs["MH [GeV]"]
    n_masses = len(masses)
    xsec_ggf13 = cs["ggF 13TeV Cross Section [pb]"]
    xsec_vbf13 = cs["VBF 13TeV Cross Section [pb]"]
    xsec_wh13 = cs["WH 13TeV Cross Section [pb]"]
    xsec_zh13 = cs["ZH 13TeV Cross Section [pb]"]
    xsec_ggf8 = cs["ggF 8TeV Cross Section [pb]"]

    def find_xsec(mass, xsec):
        """
        Return cross-section for the Higgs masses closest to the mass argument.
        xsec is a list of cross-sections, corresponding to masses in masses list.
        """
        # use numpy arrays to your advantage and do it all so much faster
        # get vector of absolute difference between masses in CSV and argument mass
        # then get the index of the smallest difference
        # then get the xsec corrresponding to that index
        # this fn takes ~ 310 us, the old one took ~ 4.4ms -> 10x faster!
        m_ind = np.absolute(masses - np.ones_like(n_masses) * mass).argmin()
        return xsec[m_ind]

    # Store SM cross section for gg fusion at 13 TeV for production of h1 and h2
    df_orig["xsec_ggf13_h1"] = df_orig.apply(lambda row: find_xsec(row['mh1'], xsec_ggf13), axis=1)
    df_orig["xsec_ggf13_h2"] = df_orig.apply(lambda row: find_xsec(row['mh2'], xsec_ggf13), axis=1)
    df_orig["xsec_ggf13_h3"] = df_orig.apply(lambda row: find_xsec(row['mh3'], xsec_ggf13), axis=1)

    df_orig["xsec_vbf13_h1"] = df_orig.apply(lambda row: find_xsec(row['mh1'], xsec_vbf13), axis=1)
    df_orig["xsec_vbf13_h2"] = df_orig.apply(lambda row: find_xsec(row['mh2'], xsec_vbf13), axis=1)
    df_orig["xsec_vbf13_h3"] = df_orig.apply(lambda row: find_xsec(row['mh3'], xsec_vbf13), axis=1)

    df_orig["xsec_zh13_h1"] = df_orig.apply(lambda row: find_xsec(row['mh1'], xsec_zh13), axis=1)
    df_orig["xsec_zh13_h2"] = df_orig.apply(lambda row: find_xsec(row['mh2'], xsec_zh13), axis=1)
    df_orig["xsec_zh13_h3"] = df_orig.apply(lambda row: find_xsec(row['mh3'], xsec_zh13), axis=1)

    df_orig["xsec_wh13_h1"] = df_orig.apply(lambda row: find_xsec(row['mh1'], xsec_wh13), axis=1)
    df_orig["xsec_wh13_h2"] = df_orig.apply(lambda row: find_xsec(row['mh2'], xsec_wh13), axis=1)
    df_orig["xsec_wh13_h3"] = df_orig.apply(lambda row: find_xsec(row['mh3'], xsec_wh13), axis=1)

    # Store SM cross section for gg fusion at 8 TeV for production of h1 and h2
    df_orig["xsec_ggf8_h1"] = df_orig.apply(lambda row: find_xsec(row['mh1'], xsec_ggf8), axis=1)
    df_orig["xsec_ggf8_h2"] = df_orig.apply(lambda row: find_xsec(row['mh2'], xsec_ggf8), axis=1)

    # Now add in individual channel xsec
    # store_channel_xsec(df_orig)
    print df_orig.columns.values

    # Make some subsets here:
    print "Making subsets..."

    # Points passing all experimental constraints chosen
    df_pass_all = subset_pass_constraints(df_orig)

    # subset with 2m_tau < ma1 < 10
    df_ma1Lt10 = None
    # df_ma1Lt10 = subset_var(df_pass_all, 3.554, 10.5, "ma1")

    mhmin, mhmax = 122.1, 128.1
    # subset with h1 as h_125
    # df_h1SM = subset_var(df_pass_all, mhmin, mhmax, "mh1")
    df_h1SM = None

    # subset with h2 as h_125
    # df_h2SM = subset_var(df_pass_all, mhmin, mhmax, "mh2")
    df_h2SM = None

    n_orig = len(df_orig.index)
    n_pass_all = len(df_pass_all.index)

    def percent_str(numerator, denominator):
        return "%.3f %% +- %.3f %%" % (100*numerator/float(denominator), 100*math.sqrt(numerator)/float(denominator))

    print "Running over", n_orig, "points"
    print n_pass_all, "points passing all constraints (= %s)" % percent_str(n_pass_all, n_orig)
    # print len(df_ma1Lt10.index), "of these have 2m_tau < ma1 < 10 GeV (= %s)" % percent_str(len(df_ma1Lt10.index), n_pass_all)
    # print len(df_h1SM.index), "points in the h1 = h(125) subset (= %s)" % percent_str(len(df_h1SM.index), n_pass_all)
    # print len(df_h2SM.index), "points in the h2 = h(125) subset (= %s)" % percent_str(len(df_h2SM.index), n_pass_all)
    print ""

    return df_orig, df_pass_all, df_ma1Lt10, df_h1SM, df_h2SM


#---------------------------------------------
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", help="output HDF5 filename")
    parser.add_argument("input", nargs="*", help="folders with CSV files")
    args = parser.parse_args()

    if not args.input:
        print "You need to specify an input directory"
        sys.exit(1)

    df_orig, df_pass_all, df_ma1Lt10, df_h1SM, df_h2SM = make_dataframes(args.input, file_stem='output')

    print "Saving as HDF5..."
    store = pd.HDFStore(args.output, complevel=9, comlib='bzip2')

    if isinstance(df_orig, pd.DataFrame):
        store.put('full12loop_all', df_orig, format='table', data_columns=True)
    if isinstance(df_pass_all, pd.DataFrame):
        store.put('full12loop_good_posMuMagMom_planckUpperOnly', df_pass_all, format='table', data_columns=True)
    if isinstance(df_ma1Lt10, pd.DataFrame):
        store.put('full12loop_good_posMuMagMom_planckUpperOnly_maLt10', df_ma1Lt10, format='table', data_columns=True)
    if isinstance(df_h1SM, pd.DataFrame):
        store.put('full12loop_good_posMuMagMom_planckUpperOnly_h1SM', df_h1SM, format='table', data_columns=True)
    if isinstance(df_h2SM, pd.DataFrame):
        store.put('full12loop_good_posMuMagMom_planckUpperOnly_h2SM', df_h2SM, format='table', data_columns=True)

