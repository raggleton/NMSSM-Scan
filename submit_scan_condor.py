#!/usr/bin/env python

"""
This script submits a new set of scan jobs on HTCondor.

1) User should make any edits to the card template file, and param range JSON
2) The user should change NUM_JOBS, NUM_POINTS, JOB_DESC, CARD and PARAM_RANGE.
3) Check Proto_files/runScan_dag.condor to ensure paths/versions correct.
4) Run me!

This will create a job directory both here and on HDFS, and submit jobs as a
DAG for ease of monitoring/maintaining.
"""

import os
from subprocess import call
import shutil
from time import strftime
import common_utils as cu

# Number of parallel jobs to submit
NUM_JOBS = 10
# Number of points to scan per job
NUM_POINTS = 100
# Shorthand description for this batch of jobs
JOB_DESC = "MICRO_SCAN_I42_NTv480_HBv421_TEST"
# Input card to use as template for NMSSMTools
CARD = "Proto_files/inp_PROTO.dat"
# JSON file with range of params to scan over
PARAM_RANGE = "paramRange.json"


def submit_scans(num_jobs, num_points, job_description, card, param_range):
    """Submit a set of scan jobs to HTCondor as a DAG, using NMSSMScan.py.

    num_jobs: int
        Number of jobs to submit.
    num_points: int
        Number of points to scan per job.
    job_description: str
        Description for the jobs, used in job & output directories.
    card: str
        Location of template input card for NMSSMTools.
    param_range: str
        Location of JSON with parameters to scan over and their ranges.
    """
    # Setup some directories:
    date_str = strftime("%d_%b_%y_%H%M")
    job_dir = 'jobs_%d_%s_%s' % (num_jobs, job_description, date_str)

    # For output from jobs (e.g. spectrum files)
    oDir_hdfs = os.path.join(out_dir, job_dir)
    cu.check_create_dir(oDir_hdfs)

    # For local files (e.g. DAG & status)
    oDir_local = os.path.join('jobs', job_dir)
    cu.check_create_dir(oDir_local)

    # For log files
    oDir_local_log = '%s/logs' % (oDir_local)
    cu.check_create_dir(oDir_local_log)

    # Make DAG script
    dag_file = os.path.join(oDir_local, 'scan.dag')
    write_dag_file(dag_file, num_jobs, num_points, oDir_hdfs, oDir_local_log, job_description)

    # Copy files to HDFS to sandbox them/keep a copy
    cp_dict = {
        PARAM_RANGE: os.path.join(oDir_hdfs, "paramRange.json"),
        "NMSSMScan.py": os.path.join(oDir_hdfs, "NMSSMScan.py"),
        "common_utils.py": os.path.join(oDir_hdfs, "common_utils.py"),
        CARD: os.path.join(oDir_hdfs, "inp_PROTO.dat")
    }
    for src, dest in cp_dict.iteritems():
        shutil.copy(src, dest)

    # Submit jobs
    condor_cmds = ['condor_submit_dag', dag_file]
    call(condor_cmds)


def write_dag_file(dag_filename, num_jobs, num_points, out_dir, log_dir,
                   job_description, condor_file='HTCondor/runScan_dag.condor'):
    """Write a DAG file.

    dag_filename: str
        Location of DAG file to write
    num_jobs: int
        Number of jobs to submit.
    num_points: int
        Number of points to scan per job.
    out_dir: str
        Directory for output spectrum files.
    log_dir: str
        Directory for log files.
    job_description: str
        Shorthand description of jobs, used for job naming.
    condor_file: Optional[str]
        Condor job description file to use for each job
    """
    print 'Writing DAG file to', dag_filename
    # TODO: maybe pass in job vars as dict if they don't depend on job ID number?
    with open(dag_filename, "w") as dag:
        dag.write('# DAG for jobs %s\n' % job_description)
        dag.write('# Output to %s\n' % (out_dir))
        for job_id in xrange(num_jobs):
            job_name = '%d_%s' % (job_id, job_description)
            dag.write('JOB %s %s\n' % (job_name, condor_file))
            dag_vars = {'logDir': log_dir, 'oDir': out_dir, 'nPoints': str(num_points), 'jobId': str(job_id)}
            vars_str = ' '.join(['%s="%s"' % (k, v) for k, v in dag_vars.items()])
            dag.write('VARS %s %s\n' % (job_name, vars_str))
        dag.write('NODE_STATUS_FILE %s 30' % dag_filename.replace(".dag", ".status"))

    print 'Check status with:'
    print 'DAGstatus.py', dag_filename.replace(".dag", ".status")

if __name__ == "__main__":
    submit_scans(NUM_JOBS, NUM_POINTS, JOB_DESC, CARD, PARAM_RANGE)
