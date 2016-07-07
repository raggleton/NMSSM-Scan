#!/usr/bin/env python

"""
This script submits a new set of HDF5-maker jobs on HTCondor. These will parse
the CSV files, and output a HDF5 file.

This will use a job directory both here and on HDFS.

Usage:

    ./submit_make_hdf5_condor_new.py <jobs_A_B_C> <jobs_D_E_F> ...

where <jobs_X_Y_Z> are local dir names that have a corresponding dir on /hdfs
"""


import os
import sys
from glob import iglob
import htcondenser as ht
import logging


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
log = logging.getLogger(__name__)


HDFS_DIR = '/hdfs/user/%s/NMSSM-Scan/' % (os.environ['LOGNAME'])

STORAGE_DIR = "/storage/%s/NMSSM-Scan/" % (os.environ['LOGNAME'])


def submit(job_dirs, storage_dir, hdfs_dir):
    """Submit the make_hdf5 job"""
    common_input_files = ['iPython/parton_lumi_ratio.csv', 'iPython/YR3_cross_sections.csv']

    log_stem = 'makeHDF5.$(cluster).$(process)'

    status_files = []

    for jdir in job_dirs:
        if not os.path.isdir(jdir):
            raise IOError('No such directory %s' % jdir)

        jdir = jdir.strip('/')
        log_dir = os.path.join(storage_dir, jdir, 'logs')
        csv_dir = os.path.join(hdfs_dir, jdir)

        # remove old files
        for f in iglob(os.path.join(storage_dir, jdir, 'make*')):
            log.debug('Removing %s', f)
            os.remove(f)

        maker_jobset = ht.JobSet(exe='iPython/make_hdf5.py',
                                 copy_exe=True,
                                 setup_script='HTCondor/setupPyEnv.sh',
                                 filename=os.path.join(storage_dir, jdir, 'makeHDF5.condor'),
                                 out_dir=log_dir, out_file=log_stem + '.out',
                                 err_dir=log_dir, err_file=log_stem + '.err',
                                 log_dir=log_dir, log_file=log_stem + '.log',
                                 share_exe_setup=True,
                                 common_input_files=common_input_files,
                                 transfer_hdfs_input=False,
                                 hdfs_store=csv_dir,
                                 memory='6GB', disk='6GB')

        maker_dag = ht.DAGMan(filename=os.path.join(storage_dir, jdir, 'makeHDF5.dag'),
                              status_file=os.path.join(storage_dir, jdir, 'makeHDF5.status'))

        final_filename = os.path.basename(jdir).replace("jobs_", "points_") + '.h5'
        job = ht.Job(name='maker_%s' % jdir,
                     args=[final_filename, csv_dir],
                     hdfs_mirror_dir=csv_dir,
                     output_files=[final_filename])

        maker_jobset.add_job(job)
        maker_dag.add_job(job)
        maker_dag.submit()
        status_files.append(maker_dag.status_file)

    print 'Check status with:'
    print 'DAGstatus.py', ' '.join(status_files)

    return 0


if __name__ == "__main__":
    sys.exit(submit(sys.argv[1:], STORAGE_DIR, HDFS_DIR))
