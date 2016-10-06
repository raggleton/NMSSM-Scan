#!/usr/bin/env python

"""
This script runs NMSSMTools over parameter ranges, with optional depenence
between parameters.

This allows for running on a batch system, where each worker node can scan
randomly over a given range, improving efficiency.

"""

import os
import sys
import argparse
import logging
import random
from subprocess import call
import json
import re
from time import strftime
import common_utils as cu


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


def NMSSMScan(in_args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--card",
                        help="Input card template",
                        required=True)
    parser.add_argument("--oDir",
                        help="Output directory for spectrum/MicrOMEGAs files")
    parser.add_argument("--param",
                        help='JSON file with parameter range to run over.',
                        required=True)
    parser.add_argument('-n', '--number',
                        help='Number of points to run over',
                        type=int,
                        default=1)
    parser.add_argument('--NT',
                        help='NMSSMTools directory',
                        required=True,
                        type=str)
    parser.add_argument('--HB',
                        help='HiggsBounds directory',
                        type=str)
                        # action='store_true')
    parser.add_argument('--HS',
                        help='HiggsSignals irectory',
                        type=str)
                        # action='store_true')
    parser.add_argument('--sushi',
                        help="sushi directory (don't include /bin",
                        type=str)
                        # action='store_true')
    parser.add_argument("--dry",
                        help="Dry run, don't run programs.",
                        action='store_true')
    parser.add_argument("-v",
                        help="Display debug messages.",
                        action='store_true')

    args = parser.parse_args(args=in_args)

    if args.v:
        log.setLevel(logging.DEBUG)
        log.debug(args)

    log.debug('program args: %s' % args)

    # do some checks
    cu.check_file_exists(args.card)
    cu.check_file_exists(args.param)
    if args.number < 1:
        log.error('-n|--number must have an argument >= 1')
    if not args.oDir:
        # generate output directory if one not specified
        args.oDir = generate_odir()
    cu.check_create_dir(args.oDir, args.v)

    # read template card
    with open(args.card) as template_file:
        template = template_file.readlines()

    # read in JSON file with parameters and bounds
    with open(args.param) as json_file:
        param_dict = json.load(json_file)
        # remove any comments
        rm_keys = []
        for k in param_dict.iterkeys():
            if k.startswith('_'):
                rm_keys.append(k)
        for k in rm_keys:
            log.debug('Removing entry %s' % k)
            del param_dict[k]

    # loop over number of points requested, making an input card for each
    num_physical = 0
    for ind in xrange(args.number):

        if ind % 200 == 0:
            log.info('Processing %dth point at %s', ind, strftime("%H%M%S"))

        # generate a random point within the range
        for v in param_dict.itervalues():
            v['value'] = random.uniform(v['min'], v['max'])

        # replace values in the card text
        # eurgh stupid string in python
        new_card_text = template[:]
        for i in range(len(new_card_text)):
            for k, v in param_dict.iteritems():
                s_match = r'(\s+\d+\s+)[\w.]+(\s+#\s%s.*)' % k
                s_repl = r'\g<1>' + str(v['value']) + 'D0\g<2>'
                new_card_text[i] = re.sub(s_match, s_repl, new_card_text[i])

        # write a new card
        new_card_path = generate_new_card_path(args.oDir, args.card, ind)
        log.debug('New card: %s' % new_card_path)
        with open(new_card_path, 'w') as new_card:
            for line in new_card_text:
                new_card.write(line)

        base_dir = os.getcwd()

        if args.dry:
            continue

        # Run your tools!
        # --------------------------------------------------------------------
        # run NMSSMTools with the new card
        # NMSSMTools requires relpath NOT abspath!
        os.chdir(args.NT)
        ntools_cmds = ['./run', os.path.relpath(new_card_path)]
        log.debug(ntools_cmds)
        call(ntools_cmds)
        os.chdir(base_dir)

        spectr_name = new_card_path.replace('inp', 'spectr')
        if not os.path.isfile(spectr_name):
            print 'File %s not produced - skipping' % spectr_name
            continue

        if not check_if_physical(spectr_name):
            print 'Removing %s as unphysical' % spectr_name
            os.remove(spectr_name)
            continue

        num_physical += 1

        if args.HB or args.HS:
            # need to add in DMASS block for HB/HS
            # this is somewhat aribitrary
            add_dmass_block(spectr=spectr_name, dmh1=2, dmh2=2)

        # run HiggsBounds and HiggsSignals
        if args.HB:
            os.chdir(args.HB)
            hb_cmds = ['./HiggsBounds', 'LandH', 'SLHA', '5', '1', os.path.relpath(spectr_name)]
            log.debug(hb_cmds)
            call(hb_cmds)
            os.chdir(base_dir)

        if args.HS:
            os.chdir(args.HS)
            hs_cmds = ['./HiggsSignals', 'latestresults', 'peak', '2', 'SLHA', '5', '1', os.path.relpath(spectr_name)]
            log.debug(hs_cmds)
            call(hs_cmds)
            os.chdir(base_dir)

        if args.sushi:
            pass
            # os.chdir(args.sushi, 'bin'))
            # sushi_cmds = ['./sushi', input, output]
            # log.debug(sushi_cmds)
            # call(sushi_cmds)
            # os.chidr(base_dir)

    # print some stats
    print '*' * 40
    print '* Num iterations:', args.number
    print '* Num physical:', num_physical
    print '*' * 40


def check_if_physical(spectr):
    with open(spectr) as f:
        contents = f.read()
        constraints = [
            'M_A1^2<1',
            'M_H1^2<1',
            'M_HC^2<1',
            'Negative sfermion mass squared',
            'Disallowed parameters: lambda or tan(beta)=0',
            'Integration problem in RGES',
            'Integration problem in RGESOFT',
            'Convergence Problem']
        if any((x in contents for x in constraints)):
            return False
    return True


def add_dmass_block(spectr, dmh1=2, dmh2=2):
    """Add DMASS block to spectrum file so can be used with
    HiggsBounds/HiggsSignals correctly.

    spectr : str
        Spectrum filepath
    dmh1 : int / float
        Uncertainty on mh1
    dmh2 : int/float
        Uncertainty on mh2
    """
    block = 'BLOCK DMASS\n  25  %.8E\n  35  %.8E\n' % (dmh1, dmh2)
    with open(spectr, 'a') as f:
        f.write(block)


def generate_odir():
    """Generate an output directory"""
    return os.path.join(os.getcwd(), 'jobs_%s' % (strftime("%d_%b_%y_%H%M")))


def generate_new_card_path(oDir, card, ind):
    """Generate a new filepath for the output card.

    Use absolute path, as important for NMSSMTools.

    oDir: str
        Output directory for card.
    card: str
        Name of the card to be used as a basis.
    ind: int
        Index to be added to end of filename.
    """
    stem = os.path.splitext(os.path.basename(card))[0]
    return os.path.abspath(os.path.join(oDir, '%s_%d.dat' % (stem, ind)))


if __name__ == "__main__":
    NMSSMScan()
