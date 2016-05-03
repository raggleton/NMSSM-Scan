#!/usr/bin/env python

"""
This runs make_hdf5.py locally, to overcome the /software issue on condor.
"""


from analyse_scans import analyse_scans
import os
import sys
from glob import glob, iglob
import tarfile


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print 'Only do 1 folder at a time'
        exit(1)
    if len(sys.argv) < 2:
        print 'Must specify a folder to do'
        exit(1)

    job_dir = sys.argv[1]
    tmp_dir = os.path.join(job_dir, 'scratch')
    if not os.path.isdir(tmp_dir):
        os.makedirs(tmp_dir)

    hdfs_dir = '/hdfs/user/%s/NMSSM-Scan/' % os.environ['LOGNAME']

    spectr_tars = glob(os.path.join(hdfs_dir, job_dir, 'spectr*tgz'))
    for s_tar in spectr_tars:
        print 'Doing', s_tar

        with tarfile.open(s_tar) as tar:
            tar.extractall(tmp_dir)

        pid = os.path.basename(s_tar)
        pid = pid.replace('spectr', '')
        pid = pid.split('.')[0]

        analyse_scans([tmp_dir, '--oDir', job_dir, '--ID', pid])

        for f in iglob(os.path.join(tmp_dir, '*')):
            os.remove(f)
