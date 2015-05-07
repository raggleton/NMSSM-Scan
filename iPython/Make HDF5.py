
# coding: utf-8

# This makes a HDF5 binary store for the dataframes. MUCH quicker than reading in the CSVs by hand. Only need ot run this once, then use the hdf5 in your script.

# In[ ]:

import pandas as pd
import numpy as np

folders_LOMass = [
"jobs_50_MICRO_LOMASS_17_Apr_15_0835",
"jobs_50_MICRO_LOMASS_17_Apr_15_0836",
"jobs_50_MICRO_LOMASS_17_Apr_15_0837",
"jobs_50_MICRO_LOMASS_17_Apr_15_0840",
"jobs_50_MICRO_LOMASS_17_Apr_15_0841",
"jobs_50_MICRO_LOMASS_17_Apr_15_0842",
"jobs_50_MICRO_LOMASS_17_Apr_15_2318",
"jobs_50_MICRO_LOMASS_17_Apr_15_2319",
"jobs_50_MICRO_LOMASS_17_Apr_15_2320",
"jobs_50_MICRO_LOMASS_17_Apr_15_2321",
"jobs_50_MICRO_LOMASS_17_Apr_15_2322",
"jobs_50_MICRO_LOMASS_17_Apr_15_2323",
"jobs_50_MICRO_LOMASS_18_Apr_15_0957",
"jobs_50_MICRO_LOMASS_18_Apr_15_0958",
"jobs_50_MICRO_LOMASS_18_Apr_15_0959",
"jobs_50_MICRO_LOMASS_18_Apr_15_1000",
"jobs_50_MICRO_LOMASS_18_Apr_15_1001",
"jobs_50_MICRO_LOMASS_18_Apr_15_1002",
"jobs_50_MICRO_LOMASS_18_Apr_15_1211",
"jobs_50_MICRO_LOMASS_18_Apr_15_1212",
"jobs_50_MICRO_LOMASS_18_Apr_15_1213",
"jobs_50_MICRO_LOMASS_18_Apr_15_1214",
"jobs_50_MICRO_LOMASS_18_Apr_15_1215",
"jobs_50_MICRO_LOMASS_18_Apr_15_1216"
# "jobs_50_MICRO_LOMASS_17_Apr_15_1814",
# "jobs_50_MICRO_LOMASS_17_Apr_15_1815",
# "jobs_50_MICRO_LOMASS_17_Apr_15_1816",
# "jobs_50_MICRO_LOMASS_17_Apr_15_1817",
# "jobs_50_MICRO_LOMASS_17_Apr_15_1818",
# "jobs_50_MICRO_LOMASS_17_Apr_15_1819",
# "jobs_50_MICRO_LOMASS_17_Apr_15_2116",
# "jobs_50_MICRO_LOMASS_17_Apr_15_2117",
# "jobs_50_MICRO_LOMASS_17_Apr_15_2118",
# "jobs_50_MICRO_LOMASS_17_Apr_15_2119",
# "jobs_50_MICRO_LOMASS_17_Apr_15_2120",
# "jobs_50_MICRO_LOMASS_17_Apr_15_2121"
]

# NMSSMTools calculates Higgs mass with corrections
folders = [
# "jobs_50_MICRO_11_Apr_15_0005",
# "jobs_50_MICRO_11_Apr_15_0006",
# "jobs_50_MICRO_11_Apr_15_0007",
# "jobs_50_MICRO_11_Apr_15_0008",
# "jobs_50_MICRO_11_Apr_15_0009",
# "jobs_50_MICRO_11_Apr_15_0010",
# "jobs_50_MICRO_11_Apr_15_0952",
# "jobs_50_MICRO_11_Apr_15_0953",
# "jobs_50_MICRO_11_Apr_15_0957",
# "jobs_50_MICRO_11_Apr_15_1009",
"jobs_50_MICRO_11_Apr_15_1036",
"jobs_50_MICRO_11_Apr_15_1038",
"jobs_50_MICRO_11_Apr_15_1157",
"jobs_50_MICRO_11_Apr_15_1158",
"jobs_50_MICRO_11_Apr_15_1203",
"jobs_50_MICRO_09_Apr_15_2049",
"jobs_50_MICRO_09_Apr_15_2046",
"jobs_50_MICRO_09_Apr_15_2340",
"jobs_50_MICRO_09_Apr_15_2048",
"jobs_50_MICRO_09_Apr_15_1857",
"jobs_50_MICRO_09_Apr_15_1856",
"jobs_50_MICRO_09_Apr_15_2047",
"jobs_50_MICRO_09_Apr_15_1500",
"jobs_50_MICRO_09_Apr_15_1458",
"jobs_50_MICRO_09_Apr_15_1457",
"jobs_50_MICRO_09_Apr_15_1446",
"jobs_50_MICRO_09_Apr_15_1443",
"jobs_50_MICRO_09_Apr_15_2050",
"jobs_50_MICRO_09_Apr_15_2108",
"jobs_50_MICRO_09_Apr_15_2333",
"jobs_50_MICRO_09_Apr_15_2335",
"jobs_50_MICRO_09_Apr_15_2337",
"jobs_50_MICRO_09_Apr_15_2338"
]


# Load files into Panda data frame
def load_df(folders):
    """Load data frame with CSV files from several folders"""
    df_list = []
    for fo in folders:
#         print fo
        for fi in glob.glob("/users/robina/Dropbox/4Tau/NMSSM-Scan/data/" + fo + "/output_good*.dat"):
            df_temp = pd.read_csv(fi, delimiter=",")#, keep_default_na=True, na_values="")
            df_list.append(df_temp)
    df_orig = pd.concat(df_list)
    return df_orig

df_orig = load_df(folders)
n_orig = len(df_orig.index)

df_orig_loMass = load_df(folders_LOMass)
n_orig_loMass = len(df_orig_loMass.index)

# Fix the constraints column, such that the ones that pass have NaN replaced by something more sensible
df_orig.fillna({"constraints":""}, axis=0, inplace=True)
df_orig_loMass.fillna({"constraints":""}, axis=0, inplace=True)

# Load up the glu-glu cross sections for 13 TeV
cs = pd.read_csv("/Users/robina/Dropbox/4Tau/NMSSM-Scan/iPython/parton_lumi_ratio.csv")
masses = cs["MH [GeV]"].tolist()
xsec_ggf13 = cs["ggF 13TeV cross section [pb]"].tolist()

def find_xsec(mass):
    m = min(range(len(masses)), key=lambda x: abs(masses[x]-mass))
    return xsec_ggf13[m]

# Store SM cross section for gg fusion at 13 TeV for production of m1 and m2
df_orig["xsec_ggf13_h1"] = df_orig.apply(lambda row: find_xsec(row['mh1']), axis=1)
df_orig["xsec_ggf13_h2"] = df_orig.apply(lambda row: find_xsec(row['mh2']), axis=1)
df_orig_loMass["xsec_ggf13_h1"] = df_orig_loMass.apply(lambda row: find_xsec(row['mh1']), axis=1)
df_orig_loMass["xsec_ggf13_h2"] = df_orig_loMass.apply(lambda row: find_xsec(row['mh2']), axis=1)


def store_xsec(df):
    """
    Calculate total cross-section & scaled cross-sections 
    for gg->h1->a1a1, gg->h2->a1a1, gg->h2->h1h1, 
    with final states 4tau, 2b2tau, 4b. 
    Denoted as gg -> X -> YY ->f1f1f2f2
    """
    process_scaled = [] # Store them for later
    process = []

    # (no constraint on if ggh is hSM)
    X = ["h1", "h2"]
    Y = ["a1", "h1"]
    F = ["tautau", "bb"]

    for x,y in itprod(X,Y):
        if x == y:
            continue
        for f1, f2 in itprod(F,F):
            ff = ""
            factor = 1
            if f1 == f2 == "tautau":
                ff = "4tau"
            elif f1 == f2 == "bb":
                ff = "4b"
            else:
                factor = 2
                ff = "2b2tau"    
            name = "xsec_scaled_"+x+"_"+"2"+y+"_"+ff
            if not name in process_scaled:
                # store scaled total XS * BR
                process_scaled.append(name) 
                df[name] = df[x+"ggrc2"] * df["Br"+x+y+y] * df["Br"+y+f1] * df["Br"+y+f2] * factor
                # store actual XS * BR
                name = name.replace("_scaled", "")
                process.append(name)
                df[name] = df["xsec_ggf13_"+x] * df[x+"ggrc2"] * df["Br"+x+y+y] * df["Br"+y+f1] * df["Br"+y+f2] * factor


store_xsec(df_orig)
store_xsec(df_orig_loMass)
# df_orig[0:5]["constraints"]

# Make some subsets here:

# subset based on passing all constraints
def pass_all(df):
    """
    return dataframe where points pass all constraints,
     or fail g-2, but have +ve contribution
    """
    pass_all_str = df["constraints"] == ""
    del_a_mu_str = df["constraints"] == r"Muon magn. mom. more than 2 sigma away"
    pass_del_a_mu = df["Del_a_mu"] > 0

    return df[pass_all_str | (del_a_mu_str & pass_del_a_mu)]

df = pass_all(df_orig)
df_loMass = pass_all(df_orig_loMass)
n_total = len(df.index)
n_total_loMass = len(df_loMass.index)


def subset_mass(df, min_mass, max_mass, mass):
    """Make subset based on range of object mass"""
    mass_max = df[mass] < max_mass
    mass_min = df[mass] > min_mass
    return df[mass_min & mass_max]

# subset with 2m_tau < ma1 < 10
df_ma1Lt10 = subset_mass(df, 3.554, 10, "ma1")
df_loMass_ma1Lt10 = subset_mass(df_loMass, 3.554, 10, "ma1")

mhmin = 122.1
mhmax = 128.1

# subset with h1 as h_SM
df_h1SM = subset_mass(df, mhmin, mhmax, "mh1")
df_loMass_h1SM = subset_mass(df_loMass, mhmin, mhmax, "mh1")

# subset with h2 as h_SM
df_h2SM = subset_mass(df, mhmin, mhmax, "mh2")
df_loMass_h2SM = subset_mass(df_loMass, mhmin, mhmax, "mh2")

print "MASS WITH FULL 1+2 LOOPS:"
print "Running over", n_orig, "points"
print n_total, "points passing all constraints (=", 100*n_total/float(n_orig), "%)"
print len(df_ma1Lt10.index), "of these have 2m_tau < ma1 < 10 GeV (=",100*len(df_ma1Lt10.index)/float(n_total), "%)"
print len(df_h1SM.index), "points in the h1 = h(125) subset (=", 100*len(df_h1SM.index)/float(n_total), "%)"
print len(df_h2SM.index), "points in the h2 = h(125) subset (=", 100*len(df_h2SM.index)/float(n_total), "%)"
print ""
print "DEFAULT MASS:"
print "Running over", n_orig_loMass, "points"
print n_total_loMass, "points passing all constraints (=", 100*n_total_loMass/float(n_orig_loMass), "%)"
print len(df_loMass_ma1Lt10.index), "of these have 2m_tau < ma1 < 10 GeV (=",100*len(df_loMass_ma1Lt10.index)/float(n_total_loMass), "%)"
print len(df_loMass_h1SM.index), "points in the h1 = h(125) subset (=", 100*len(df_loMass_h1SM.index)/float(n_total_loMass), "%)"
print len(df_loMass_h2SM.index), "points in the h2 = h(125) subset (=", 100*len(df_loMass_h2SM.index)/float(n_total_loMass), "%)"

# check constraints
# df[10:15].T

# Make some subsets here:

# subset based on passing all constraints
def pass_all(df):
    """
    return dataframe where points pass all constraints,
     or fail g-2, but have +ve contribution
    """
    pass_all_str = df["constraints"] == ""
    del_a_mu_str = df["constraints"] == r"Muon magn. mom. more than 2 sigma away"
    pass_del_a_mu = df["Del_a_mu"] > 0

    return df[pass_all_str | (del_a_mu_str & pass_del_a_mu)]

df = pass_all(df_orig)
df_loMass = pass_all(df_orig_loMass)
n_total = len(df.index)
n_total_loMass = len(df_loMass.index)


def subset_mass(df, min_mass, max_mass, mass):
    """Make subset based on range of object mass"""
    mass_max = df[mass] < max_mass
    mass_min = df[mass] > min_mass
    return df[mass_min & mass_max]

# subset with 2m_tau < ma1 < 10
df_ma1Lt10 = subset_mass(df, 3.554, 10, "ma1")
df_loMass_ma1Lt10 = subset_mass(df_loMass, 3.554, 10, "ma1")

mhmin = 122.1
mhmax = 128.1

# subset with h1 as h_SM
df_h1SM = subset_mass(df, mhmin, mhmax, "mh1")
df_loMass_h1SM = subset_mass(df_loMass, mhmin, mhmax, "mh1")

# subset with h2 as h_SM
df_h2SM = subset_mass(df, mhmin, mhmax, "mh2")
df_loMass_h2SM = subset_mass(df_loMass, mhmin, mhmax, "mh2")

print "MASS WITH FULL 1+2 LOOPS:"
print "Running over", n_orig, "points"
print n_total, "points passing all constraints (=", 100*n_total/float(n_orig), "%)"
print len(df_ma1Lt10.index), "of these have 2m_tau < ma1 < 10 GeV (=",100*len(df_ma1Lt10.index)/float(n_total), "%)"
print len(df_h1SM.index), "points in the h1 = h(125) subset (=", 100*len(df_h1SM.index)/float(n_total), "%)"
print len(df_h2SM.index), "points in the h2 = h(125) subset (=", 100*len(df_h2SM.index)/float(n_total), "%)"
print ""
print "DEFAULT MASS:"
print "Running over", n_orig_loMass, "points"
print n_total_loMass, "points passing all constraints (=", 100*n_total_loMass/float(n_orig_loMass), "%)"

# check constraints
# df[10:15].T

store = pd.HDFStore('points_store.h5')
store.put('full12loop', df, format='table', data_columns=True)
store.put('default', df_loMass, format='table', data_columns=True)

