"""
Remake the input cards from Daniele's scan points, so can rerun with newer
version of NMSSMTools and check more things.
"""


import csv
# import shutil
import re


with open('ma1_10_br.dat') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ')

    headings = reader.next()
    print headings

    # make a new card for each parameter point
    hdfs_dir = "/hdfs/user/ra12451/NMSSM-Scan/daniele_points/"
    input_proto = "/users/ra12451/NMSSM-Scan/daniele_points/input_PROTO_daniele.dat"

    # read in input prototype card
    with open(input_proto, 'r') as inp:
        inp_proto_lines = inp.readlines()

    for i, line in enumerate(reader):
        if i > 10:
            break
        lineDict = dict(zip(headings, line))

        # put input card on hdfs
        # and replace the necessary fields:
        # tan beta, lambda, kappa, alambda, akappa, mueff
        output_file = hdfs_dir + "inp_%d.dat" % i
        with open(output_file, 'w')as output:
            for inp_line in inp_proto_lines:
                new_inp_line = re.sub(r'SED_TGBETA', lineDict['tb'], inp_line)
                new_inp_line = re.sub(r'SED_LAMBDA', lineDict['lambda'], new_inp_line)
                new_inp_line = re.sub(r'SED_KAPPA', lineDict['kappa'], new_inp_line)
                new_inp_line = re.sub(r'SED_ALAMBDA', lineDict['alambda'], new_inp_line)
                new_inp_line = re.sub(r'SED_AKAPPA', lineDict['akappa'], new_inp_line)
                new_inp_line = re.sub(r'SED_MUEFF', lineDict['mueff'], new_inp_line)
                output.write(new_inp_line)
        print output_file
