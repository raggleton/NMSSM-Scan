#!/usr/bin/env python

"""
Run SusHi over output from NMSSMTools.
"""


import sys
import argparse
import re


SUSHI_BLOCK = """Block SUSHI
    1   3       # model: 0 = SM, 1 = MSSM, 2 = 2HDM, 3 = NMSSM
    2   21      # 11,12,13 = H1,H2,H3, 21,22=A1,A2
    3   0       # collider: 0 = p-p, 1 = p-pbar
    4   8.00000000e+03  # center-of-mass energy in GeV
    5   2       # order ggh: -1 = off, 0 = LO, 1 = NLO, 2 = NNLO
    6   2       # order bbh: -1 = off, 0 = LO, 1 = NLO, 2 = NNLO
    7   1       # electroweak cont. for ggh:
                # 0 = no, 1 = light quarks at NLO, 2 = SM EW factor
    19  1       # 0 = silent mode of SusHi, 1 = normal output
    20  0       # ggh@nnlo subprocesses: 0=all, 10=ind. contributions
"""


COMMON_SUSHI = """Block DISTRIB
    1   0       # distribution : 0 = sigma_total, 1 = dsigma/dpt,
                #                2 = dsigma/dy,   3 = d^2sigma/dy/dpt
                #                (values for pt and y: 22 and 32)
    2   0       # pt-cut: 0 = no, 1 = pt > ptmin, 2 = pt < ptmax,
                #         3 = ptmin < pt < ptmax
    21  0.30000000e+02  # minimal pt-value ptmin in GeV
    22  1.00000000e+02  # maximal pt-value ptmax in GeV
    3   0       # rapidity-cut: 0 = no, 1 = Abs[y] < ymax,
                #    2 = Abs[y] > ymin, 3 = ymin < Abs[y] < ymax
    31  0.50000000e+00  # minimal rapidity ymin
    32  1.50000000e+00  # maximal rapidity ymax
    4   0       # 0 = rapidity, 1 = pseudorapidity
Block SCALES
    1   1.00000000e+00  # renormalization scale muR/mh
    2   1.00000000e+00  # factorization scale muF/mh
    11  1.00000000e+00  # renormalization scale muR/mh for bbh
    12  0.25000000e+00  # factorization scale muF/mh for bbh
    3   0       # 1 = Use (muR,muF)/Sqrt(mh^2+pt^2) for dsigma/dpt and d^2sigma/dy/dpt
Block RENORMBOT # Renormalization of the bottom sector
    1   0   # m_b used for bottom Yukawa:  0 = OS, 1 = MSbar(m_b), 2 = MSbar(muR)
    2   1   # tan(beta)-res. of Y_b: 0 = no, 1 = naive, 2 = full (for OS only)
Block RENORMSBOT # Renormalization of the sbottom sector
    1   2   # m_b:     0 = OS, 1 = DRbar, 2 = dep; recommended: 2
    2   0   # A_b:     0 = OS, 1 = DRbar, 2 = dep; recommended: 0
    3   0   # theta_b: 0 = OS, 1 = DRbar         ; recommended: 0
Block PDFSPEC
    1   MSTW2008lo68cl.LHgrid   # name of pdf (lo)
    2   MSTW2008nlo68cl.LHgrid  # name of pdf (nlo)
    3   MSTW2008nnlo68cl.LHgrid # name of pdf (nnlo)
    4   0   # set number - if different for LO, NLO, NNLO use entries 11, 12, 13
Block VEGAS
# parameters for NLO SusHi
    1   10000   # Number of points
    2   5   # Number of iterations
    3   10  # Output format of VEGAS integration
# parameters for ggh@nnlo:
    4   2000    # Number of points
    5   5   # Number of iterations
    14  5000    # Number of points in second run
    15  2   # Number of iterations in second run
    6   0   # Output format of VEGAS integration
# parameters for bbh@nnlo:
    7   2000    # Number of points
    8   5   # Number of iterations
    17  5000    # Number of points in second run
    18  2   # Number of iterations in second run
    9   0   # Output format of VEGAS integration
Block FACTORS
    1   0.00000000e+00  # factor for yukawa-couplings: c
    2   1.00000000e+00  # t
    3   1.00000000e+00  # b
    4   1.00000000e+00  # st
    5   1.00000000e+00  # sb
"""


def nmssmtools_to_sushi(nmssm_spectrum, sushi_card, higgs_id=11):
    """Converts NMSSMTools spectrum file to card suitable for SusHi

    nmssm_spectrum: str
        Spectrum file from NMSSMTools
    sushi_card: str
        Card for use with SusHi
    higgs_id: int
        ID of HIggs to use in production cross-section.
        11,12,13 = H1,H2,H3, 21,22=A1,A2
    """
    if higgs_id not in [11, 12, 13, 21, 22]:
        raise RuntimeError('Not acceptable higgs id. Must use: 11,12,13 = H1,H2,H3, 21,22=A1,A2')

    # Get input card
    with open(nmssm_spectrum) as nmssm:
        template = nmssm.readlines()

    # Make changes:
    # Set the right Higgs to calculate for
    new_sushi_block = re.sub(r'\s+2\s+\d\d\s+', '\n    2  %d\t' % higgs_id, SUSHI_BLOCK)
    print new_sushi_block
    # Modify NMAMIX matrix as different conventions in the programs
    modify = False
    for i, line in enumerate(template):
        if 'BLOCK NMAMIX' in line.upper():
            modify = True
            continue
        if 'BLOCK' in line.upper() and modify:
            break
        if modify:

            p = re.compile(r'^  (\d)  (\d.*)')
            result = p.match(line)
            if not result:
                continue
            template[i] = p.sub('  %d  %s' % (int(result.group(1)) + 1, result.group(2)), line)

    # Save
    with open(sushi_card, 'w') as sushi:
        sushi.write(new_sushi_block)
        for line in template:
            sushi.write(line)
        sushi.write(COMMON_SUSHI)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('nmssm_spectrum',
                        help='NMSSMTools spectrum file')
    parser.add_argument('sushi_card',
                        help='Name for SusHi input card to make')
    parser.add_argument('--higgs',
                        help='Higgs ID to use for production cross-section. '
                        '11,12,13 = H1,H2,H3; 21,22 = A1,A2',
                        type=int,
                        choices=[11, 12, 13, 21, 22],
                        default=11)
    args = parser.parse_args(args=sys.argv[1:])
    nmssmtools_to_sushi(args.nmssm_spectrum, args.sushi_card, args.higgs)
