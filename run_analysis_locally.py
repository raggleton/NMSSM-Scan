#!/usr/bin/env python

"""
This runs analyse_scans.py locally, to overcome the /software issue on condor.
Does it in multiprocessing mode as it's an embaressing parallel task.
"""


from analyse_scans import analyse_scans
import os
import sys
from glob import glob, iglob
from subprocess import check_call
from multiprocessing import Pool
import contextlib
from functools import partial


N_CPUS = 4

HDFS_DIR = '/hdfs/user/%s/NMSSM-Scan/' % os.environ['LOGNAME']


def do_one_dir(tar_file, job_dir):
    print 'Doing', tar_file

    pid = os.path.basename(tar_file).replace('spectr', '').split('.')[0]

    tmp_dir = os.path.join(job_dir, 'scratch%s' % pid)
    if not os.path.isdir(tmp_dir):
        print 'Making dir', tmp_dir
        os.makedirs(tmp_dir)

    check_call(['tar', 'xzf', tar_file, '-C', tmp_dir])

    analyse_scans([tmp_dir, '--oDir', job_dir, '--ID', pid])

    for f in iglob(os.path.join(tmp_dir, '*')):
        os.remove(f)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        print 'Only do 1 folder at a time'
        exit(1)
    if len(sys.argv) < 2:
        print 'Must specify a folder to do'
        exit(1)

    local_job_dir = sys.argv[1]

    spectr_tars = glob(os.path.join(HDFS_DIR, local_job_dir, 'spectr*tgz'))

    do_one_dir_partial = partial(do_one_dir, job_dir=local_job_dir)

    with contextlib.closing(Pool(processes=N_CPUS)) as pool:
        pool.map(do_one_dir_partial, spectr_tars)

    # non-parallel version
    # for s_tar in spectr_tars[0:1]:
    #     print 'Doing', s_tar
    #     do_one_dir_partial(tar_file=s_tar)
