#!/usr/bin/env python
"""
Script to run over output from NMSSMTools, etc, and pull relevant info.

The relevant info from ALL spectrum files in the input directory is put into
some CSV files:
- all points
- all points passing all constraints except g-2 (must have +ve contribution)
and relic density
- all points with ma1 < 11
"""


import os
import sys
import argparse
import logging
import glob
import re
from collections import defaultdict
import NMSSMToolsFields, SuperIsoFields, NMSSMCalcFields


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)

# fileextension for output files - may need to be used in further processing
OFMT = 'csv'


class AnalysisParser(argparse.ArgumentParser):
    """Class to handle arg parsing"""
    def __init__(self, *args, **kwargs):
        super(AnalysisParser, self).__init__(*args, **kwargs)
        self.add_arguments()

    def add_arguments(self):
        self.add_argument('input',
                          help='Directory with sample names and locations')
        self.add_argument('--oDir',
                          help='Output directory for files. If one is not '
                          'specified, uses $PWD.',
                          default=os.getcwd())
        self.add_argument('--ID',
                          help='Unique identifier to append to output filenames',
                          default='')
        self.add_argument('--superiso',
                          help='Include SuperIso output files',
                          action='store_true')
        self.add_argument('--nmssmcalc',
                          help='Include NMSSMCalc output files',
                          action='store_true')
        self.add_argument('-n',
                          help='Number of files to run over (default is all)',
                          type=int)
        # Some generic script options
        self.add_argument("-v",
                          help="Display debug messages.",
                          action='store_true')


def analyse_scans(in_args=sys.argv[1:]):
    """Main routine to loop over spectrum files in a directory and produce CSVs"""
    parser = AnalysisParser(description=__doc__)
    args = parser.parse_args(args=in_args)
    if args.v:
        log.setLevel(logging.DEBUG)
        log.debug(args)

    log.info('Getting spectrum files from %s' % args.input)

    # Do some checks
    # ------------------------------------------------------------------------
    check_create_dir(args.oDir)

    num_spectr_files = len(glob.glob(os.path.join(args.input, 'spectr_*')))
    if not args.n:
        args.n = num_spectr_files

    # Figure out if we are also including SuperIso output
    if args.superiso:
        if len(glob.glob(os.path.join(args.input, 'superiso_*'))) != num_spectr_files:
            args.superiso = False
            log.warning('Not enough SuperIso output files - will not analyse.')

    # Figure out if we are also including NMSSMCalc output
    if args.nmssmcalc:
        if len(glob.glob(os.path.join(args.input, 'nmssmcalc_*'))) != num_spectr_files:
            args.nmssmcalc = False
            log.warning('Not enough NMSSMCalc output files - will not analyse.')

    # Create output filenames
    # ------------------------------------------------------------------------
    outfile = os.path.join(args.oDir, 'output%s.%s' % (args.ID, OFMT))
    outfile_good = os.path.join(args.oDir, 'output_good%s.%s' % (args.ID, OFMT))
    outfile_ma1Lt11 = os.path.join(args.oDir, 'output_ma1Lt11%s.%s' % (args.ID, OFMT))
    log.info('Writing CSV to %s' % ', '.join([outfile, outfile_good, outfile_ma1Lt11]))

    # Analyse SLHA files
    # ------------------------------------------------------------------------
    # Counters
    n_all, n_good, n_ma1Lt11 = 0, 0, 0

    # ignore any points with ma1 > mass_cut
    mass_cut = 60

    done_cols = False

    with open(outfile, 'w') as f, \
         open(outfile_good, 'w') as f_good, \
         open(outfile_ma1Lt11, 'w') as f_ma1Lt11:

        columns = []  # to hold column order - important as dict not sorted

        # Loop through each spectrum file
        for i, spectr in enumerate(glob.iglob(os.path.join(args.input, 'spectr_*.dat'))):
            if i == args.n:
                break

            log.debug('Parsing %s', spectr)

            # Look for failing constraints.
            # If un-physical point (M_H^2 < 1 or M_A^2 < 1), skips file.
            nmssmtools_constraints = get_nmssmtools_constraints(spectr)
            if isinstance(nmssmtools_constraints, type(None)):
                continue
            results_dict = get_slha_dict(spectr, NMSSMToolsFields.nmssmtools_fields)
            # need joiner as CSV file
            results_dict['constraints'] = '|'.join(nmssmtools_constraints)
            # log.debug(results_dict)

            if args.superiso:
                # Get matching SuperIso output file and parse
                superiso = os.path.basename(spectr.replace("spectr", "superiso"))
                superiso = os.path.join(os.path.dirname(spectr), superiso)
                superiso_dict = get_slha_dict(superiso, SuperIsoFields.superiso_fields)
                results_dict.update(superiso_dict)
                log.debug(superiso_dict)

            if args.nmssmcalc:
                # Get matching NMSSMCalc output file and parse
                nmssmcalc = os.path.basename(spectr.replace("spectr", "nmssmcalc"))
                nmssmcalc = os.path.join(os.path.dirname(spectr), nmssmcalc)
                nmssmcalc_dict = get_slha_dict(nmssmcalc, NMSSMCalcFields.nmssmcalc_fields)
                results_dict.update(nmssmcalc_dict)
                log.debug(nmssmcalc_dict)

            # First time, write out column headers
            if not done_cols:
                # This defines the output column order & writes headers
                columns = sorted(results_dict.keys())
                log.debug('Columns: %s', columns)
                for o in f, f_good, f_ma1Lt11:
                    o.write(','.join(columns) + '\n')
                done_cols = True

            # Now write to file if we want this result
            if 0 < results_dict['ma1'] < mass_cut:
                # everything goes into the general output file - must keep
                # same order as header columns
                results_str = ','.join([str(results_dict[x]) for x in columns])
                f.write(results_str + '\n')
                n_all += 1

                if pass_constraints(results_dict, strict=False):
                    # "good" points
                    f_good.write(results_str + '\n')
                    n_good += 1

                if results_dict['ma1'] < 11:
                    # specifically for low mass points
                    f_ma1Lt11.write(results_str + '\n')
                    n_ma1Lt11 += 1

    # Finish by printing some stats
    log.info('#' * 60)
    log.info('# N. input points: %d' % num_spectr_files)
    log.info('# N. with 0 < ma1 < %g: %d' % (mass_cut, n_all))
    log.info('# N. with 0 < ma1 < %g + passing exp. constraints: %d' % (mass_cut, n_good))
    log.info('# N. with 0 < ma1 < 11: %d' % n_ma1Lt11)
    log.info('# Fraction useful: %.3f' % (float(n_all) / float(num_spectr_files)))
    log.info('# Fraction good: %.3f' % (float(n_good) / float(num_spectr_files)))
    log.info('#' * 60)


def get_slha_dict(filename, fields):
    """Pull information from SLHA file and store in a dict.

    filename: str
        Filepath to analyse
    fields: list of Field objects/namedtuples
        List of Fields to scan for. Each Field has properties:
        - a block e.g. 'EXTPAR', to define which BLOCK to search in.
          This is case-sensitive.
        - a name e.g. 'mh1', to be used as the dict key.
        - a type e.g. float, to convert from a string.
        - a regex pattern, to be used when trying to match lines.
          This is case-sensitive.

        A Field looks like:

        Field(block='MINPAR', name="tgbeta", type=float,
              regex=re.compile(r' +3 +([E\d\.\-\+]+) +\# TANBETA\(MZ\)'))
    """
    # For each BLOCK, we assign a list of pairs of field name + compiled regex pattern
    # Means we can only go through the patterns pertinent to that block
    scan_dict = defaultdict(list)
    for f in fields:
        if isinstance(f.regex, re._pattern_type):
            scan_dict[f.block].append(f)
        else:
            new_field = NMSSMToolsFields.Field(name=f.name,
                                               block=f.block,
                                               type=f.type,
                                               regex=re.compile(f.regex))
            scan_dict[f.block].append(new_field)

    results = defaultdict(str)
    results['file'] = filename

    # Now go through the file, line by line. If we encounter a BLOCK line,
    # then we loop through the block contents, checking each line against all
    # of the user's regexes. If there is a match, it is stored in the results
    # dict.
    # Note that we cannot use 'for line in f' as it skips alternate 'BLOCK' lines
    with open(filename) as f:
        try:
            line = f.next()
            while True:
                if line.startswith('#'):
                    line = f.next()
                    continue

                if line.upper().startswith('BLOCK'):
                    block = re.search(r'BLOCK +(\w+)', line, re.I).group(1).strip()
                    log.debug(block)

                    line = f.next()
                    if block in scan_dict.keys():
                        # Now loop over contents of this block and try matching
                        # against the regexes
                        while 'BLOCK' not in line.upper():
                            for field in scan_dict[block]:
                                result = field.regex.search(line)
                                if result:
                                    results[field.name] = field.type(result.group(1))
                                    log.debug('%s: %s', field.name, result.group(1))
                            line = f.next()
                    else:
                        line = f.next()
                else:
                    line = f.next()
        except StopIteration:
            pass

    return results


# put these outside to get ocmpiled once, then used lots of times
p_id = re.compile(r' *3 *# *')  # needed to remove identifier
p_space = re.compile(r'\s{2,}')  # needed to remove surplus spaces


def get_nmssmtools_constraints(filename):
    """Get a list of failed constraints from the NMSSMTools spectrum file.

    If un-physical point (M_H^2 < 1 or M_A^2 < 1), returns None object
    Otherwise, returns a list of constraints it failed. Note that if it passes
    all constraints, the output will be an empty list. Therefore you CANNOT
    use the output in a bool, since both un-physical points and perfect points
    will both give the same result. Instead, use isinstance(result, list)
    to distinguish.
    """
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue

            if line.upper().startswith('BLOCK SPINFO'):
                line = f.next().strip()
                constraints = []
                while 'BLOCK' not in line.upper():
                    if line.startswith('3'):
                        # store failed experimantal/theory constraints
                        log.debug(line)
                        line = p_id.sub('', line)
                        line = line.replace(',', '')  # important as CSV file
                        line = p_space.sub(' ', line)
                        constraints.append(line)
                    if line.startswith('4'):
                        # see if there was any show-stoppers in the constraints
                        return None
                    line = f.next().strip()

                return constraints


def pass_constraints(results_dict, strict=False):
    """Return bool to see if point passes constraints. Make an exception
    for certain constraints.

    strict: bool
        If True, require it passes ALL constraints.
    """
    if results_dict['constraints'] == '':
        return True

    if strict:
        # if it got this far, the constraints string wasn't empty
        return False
    else:
        # we can still accept it if it fails certain constraints
        # (only need +ve contribution to g-2, and a too-small relice density)
        cons = results_dict['constraints'].split('/')
        if results_dict['Del_a_mu'] < 0:
            return False
        return ((len(cons) == 2 and
                 "Relic density too small (Planck)" in cons and
                 "Muon magn. mom. more than 2 sigma away" in cons) or
                (len(cons) == 1 and
                 ("Relic density too small (Planck)" in cons or
                  "Muon magn. mom. more than 2 sigma away" in cons)))


def check_create_dir(directory):
    """Check to see if directory exists, if not make it."""
    if not os.path.isdir(directory):
        if os.path.isfile(directory):
            raise RuntimeError("Cannot create directory %s, already "
                               "exists as a file object" % directory)
        os.makedirs(directory)
        log.debug("Making dir %s" % directory)


if __name__ == "__main__":
    analyse_scans()
