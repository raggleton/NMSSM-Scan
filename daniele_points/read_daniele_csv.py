"""
Remake the input cards from Daniele's scan points, so can rerun with newer
version of NMSSMTools and check more things.
"""


import sys
import csv
# import shutil
import re


def main(start, end):
    print start, end
    with open('/hdfs/user/ra12451/NMSSM-Scan/daniele_points/ma1_10_br.dat') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=' ')
        # make a new card for each parameter point
        hdfs_dir = "/hdfs/user/ra12451/NMSSM-Scan/daniele_points/"
        input_proto = "/hdfs/user/ra12451/NMSSM-Scan/daniele_points/input_PROTO_daniele.dat"

        # read in input prototype card
        with open(input_proto, 'r') as inp:
            inp_proto_lines = inp.readlines()

        for i, line in enumerate(reader):
            if i < int(start):
                continue
            elif i > int(end):
                break

            # put input cards on hdfs and replace the necessary fields:
            # tan beta, lambda, kappa, alambda, akappa, mueff
            output_file = hdfs_dir + "inp_%d.dat" % i
            with open(output_file, 'w')as output:
                for inp_line in inp_proto_lines:
                    new_inp_line = re.sub(r'SED_TGBETA', line['tb'], inp_line)
                    new_inp_line = re.sub(r'SED_LAMBDA', line['lambda'], new_inp_line)
                    new_inp_line = re.sub(r'SED_KAPPA', line['kappa'], new_inp_line)
                    new_inp_line = re.sub(r'SED_ALAMBDA', line['alambda'], new_inp_line)
                    new_inp_line = re.sub(r'SED_AKAPPA', line['akappa'], new_inp_line)
                    new_inp_line = re.sub(r'SED_MUEFF', line['mueff'], new_inp_line)
                    output.write(new_inp_line)
            if i < 10 or i % 500 == 0:
                print output_file


if __name__ == "__main__":
    main(start=sys.argv[1], end=sys.argv[2])