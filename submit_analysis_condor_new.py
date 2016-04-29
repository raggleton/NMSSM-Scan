#!/usr/bin/env python

"""
This script submits a new set of analysis jobs on HTCondor. These will parse
the spectrum files, and output them as CSV files.

This will use a job directory both here and on HDFS, and submit jobs as a
DAG for ease of monitoring/maintaining.
"""


import os
import sys
from glob import glob
import htcondenser as ht
import logging


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


ODIR = '/hdfs/user/%s/NMSSM-Scan/' % os.environ['LOGNAME']

STORAGE_DIR = "/storage/%s/NMSSM-Scan/" % (os.environ['LOGNAME'])


def submit_all_analyses(job_dirs, storage_dir, hdfs_dir):
    """Submit all CSV-making jobs, with a DAG for each entry in job_dirs.
    Each job within a DAG is for 1 spectr*.tgz

    Probably could be designed better. Paths rely on many assumptions.
    """

    common_input_files = ['analyse_scans.py', 'NMSSMToolsFields.py',
                          'SuperIsoFields.py', 'NMSSMCalcFields.py']

    log_stem = 'analysis.$(cluster).$(process)'

    for jdir in job_dirs:
        jdir = jdir.strip('/')
        log_dir = os.path.join(storage_dir, jdir, 'logs')

        analysis_jobset = ht.JobSet(exe='HTCondor/analyse_condor.sh',
                                    copy_exe=True,
                                    setup_script=None,
                                    filename=os.path.join(storage_dir, jdir, 'analysis.condor'),
                                    out_dir=log_dir, out_file=log_stem + '.out',
                                    err_dir=log_dir, err_file=log_stem + '.err',
                                    log_dir=log_dir, log_file=log_stem + '.log',
                                    share_exe_setup=True,
                                    common_input_files=common_input_files,
                                    transfer_hdfs_input=False,
                                    hdfs_store=os.path.join(hdfs_dir, jdir),
                                    memory='500MB', disk='2GB')

        analysis_dag = ht.DAGMan(filename=os.path.join(storage_dir, jdir, 'analysis.dag'),
                                 status_file=os.path.join(storage_dir, jdir, 'analysis.status'))

        # add a job to analyse each spectr*.tgz
        spectr_tars = glob(os.path.join(hdfs_dir, jdir, 'spectr*tgz'))
        for tar in spectr_tars:
            ind = int(os.path.basename(tar).split('.')[0].replace("spectr", ''))
            job = ht.Job(name='%d_%s_analysis' % (ind, jdir.strip('/')),
                         args=[jdir, str(ind)],
                         hdfs_mirror_dir=os.path.join(hdfs_dir, jdir))
            analysis_jobset.add_job(job)
            analysis_dag.add_job(job)

        analysis_dag.submit()

        print 'Check status with:'
        print 'DAGstatus.py', analysis_dag.status_file

    return 0


if __name__ == "__main__":
    sys.exit(submit_all_analyses(sys.argv[1:], STORAGE_DIR, ODIR))
