#!/usr/bin/env python

"""
This script submits a new set of scan jobs on HTCondor.

1) User should make any edits to the card template file, and param range JSON
2) The user should change NUM_JOBS, NUM_POINTS, JOB_DESC, CARD and PARAM_RANGE.
3) Run me!

Requires htcondenser: https://github.com/raggleton/htcondenser
"""


import os
import sys
from time import strftime
import htcondenser as ht
import logging


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


# Number of parallel jobs to submit
NUM_JOBS = 1000

# Number of points to scan per job
NUM_POINTS = 5000

# Shorthand description for this batch of jobs
JOB_DESC = "MICRO_SCAN_NTv491_HBv431_HSv140_all_smallAlambdaMuEff_largeTanBeta"
# JOB_DESC = "test"

# Input card to use as template for NMSSMTools
# CARD = "Proto_files/inp_PROTO.dat"
CARD = "Proto_files/inp_PROTO_all.dat"

# JSON file with range of params to scan over
# PARAM_RANGE = "paramRange_largeRange.json"
PARAM_RANGE = "paramRange_all.json"

# Output directory for results - will create a subdiretory for this set of jobs
ODIR = "/hdfs/user/%s/NMSSM-Scan/" % (os.environ['LOGNAME'])

# Directory for log file & condor scripts on /storage
STORAGE_DIR = "/storage/%s/NMSSM-Scan/" % (os.environ['LOGNAME'])


def submit_scans(num_jobs, num_points, job_description, card, param_range, storage_dir, hdfs_dir):
    """Submit a set of scan jobs to HTCondor as a DAG, that run NMSSMScan.py.

    Parameters
    ----------
    num_jobs : int
        Number of jobs to submit.
    num_points : int
        Number of points to scan per job.
    job_description : str
        Description for the jobs, used in job & output directories.
    card : str
        Location of template input card for NMSSMTools.
    param_range : str
        Location of JSON with parameters to scan over and their ranges.
    storage_dir : str
        Location on /storage for logs, and condor/DAG files
    hdfs_dir : str
        Location on /hdfs for storing output of scans
    """
    # Setup some directories:
    date_str = strftime("%d_%b_%y_%H%M")
    job_dir = 'jobs_%d_%s_%s' % (num_jobs, job_description, date_str)

    if not os.path.isdir(job_dir):
        os.makedirs(job_dir)  # local copy of directory for eventual output

    log_dir = os.path.join(storage_dir, job_dir, 'logs')
    log_stem = 'scan.$(cluster).$(process)'

    hdfs_store = os.path.join(hdfs_dir, job_dir)

    common_input_files = [param_range, 'NMSSMScan.py', 'common_utils.py', card,
                          'patches/NT.patch', 'patches/NT_clean.patch',
                          'patches/HB.patch', 'patches/HS_datatables.patch',
                          'patches/HS_subroutines.patch', 'patches/HS_assignmass.patch']

    scan_jobset = ht.JobSet(exe='HTCondor/runScan_condor.sh',
                            copy_exe=True,
                            setup_script=None,
                            filename=os.path.join(storage_dir, job_dir, 'scan.condor'),
                            out_dir=log_dir, out_file=log_stem + '.out',
                            err_dir=log_dir, err_file=log_stem + '.err',
                            log_dir=log_dir, log_file=log_stem + '.log',
                            share_exe_setup=True,
                            common_input_files=common_input_files,
                            transfer_hdfs_input=False,
                            hdfs_store=hdfs_store,
                            memory='1GB', disk='7GB')

    scan_dag = ht.DAGMan(filename=os.path.join(storage_dir, job_dir, 'scan.dag'),
                         status_file=os.path.join(storage_dir, job_dir, 'scan.status'))

    for ind in xrange(num_jobs):
        scan_job = ht.Job(name='%d_scan' % ind,
                          args=[hdfs_store, str(ind), str(num_points)],
                          hdfs_mirror_dir=hdfs_store)
        scan_jobset.add_job(scan_job)
        scan_dag.add_job(scan_job)

    scan_dag.submit(submit_per_interval=25)

    print 'Check status with:'
    print 'DAGstatus.py', scan_dag.status_file

    return 0


if __name__ == "__main__":
    sys.exit(submit_scans(NUM_JOBS, NUM_POINTS, JOB_DESC, CARD, PARAM_RANGE, STORAGE_DIR, ODIR))
