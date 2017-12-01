#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

import os

from CrySPY.BO import BO_init, BO_restart
from CrySPY.interface import select_code
from CrySPY.job import ctrl_job
from CrySPY.IO import pkl_data
from CrySPY.IO import read_input as rin
from CrySPY.start import cryspy_init, cryspy_restart


# ---------- initialize
if not os.path.isfile('cryspy.stat'):
    # ------ cryspy_init
    stat, init_struc_data, opt_struc_data, rslt_data = cryspy_init.initialize()
    if rin.algo == 'RS':
        RS_id_data = cryspy_init.RS_init(stat)
    elif rin.algo == 'BO':
        rslt_data, BO_id_data, BO_data = BO_init.initialize(stat, init_struc_data, rslt_data)
    if rin.kpt_flag:
        kpt_data = cryspy_init.kpt_init()
    if rin.energy_step_flag:
        energy_step_data = cryspy_init.energy_step_init()
    if rin.struc_step_flag:
        struc_step_data = cryspy_init.struc_step_init()
    if rin.fs_step_flag:
        fs_step_data = cryspy_init.fs_step_init()

# ---------- restart
else:
    # ------ cpsy_restart
    stat = cryspy_restart.restart()

    # ------ load data
    init_struc_data = pkl_data.load_init_struc()
    opt_struc_data = pkl_data.load_opt_struc()
    rslt_data = pkl_data.load_rslt()
    if rin.algo == 'RS':
        RS_id_data = pkl_data.load_RS_id()
    elif rin.algo == 'BO':
        BO_id_data = pkl_data.load_BO_id()
        BO_data = pkl_data.load_BO_data()
    if rin.kpt_flag:
        kpt_data = pkl_data.load_kpt()
    if rin.energy_step_flag:
        energy_step_data = pkl_data.load_energy_step()
    if rin.struc_step_flag:
        struc_step_data = pkl_data.load_struc_step()
    if rin.fs_step_flag:
        fs_step_data = pkl_data.load_fs_step()

    # ------ append structures
    if len(init_struc_data) < rin.tot_struc:
        init_struc_data = cryspy_restart.append_struc(init_struc_data)
    elif rin.tot_struc < len(init_struc_data):
        raise ValueError('tot_struc < len(init_struc_data)')
    # -- BO
    if rin.algo == 'BO':
        if BO_id_data[1] < len(init_struc_data):    # BO_id_data[1] is next_BO_id
            BO_id_data, BO_data = BO_restart.restart(init_struc_data, BO_id_data, BO_data)
#
#
# ---------- check point 1
#
#
if rin.stop_chkpt == 1:
    print('Stop at check point 1')
    raise SystemExit()

# ---------- check calc files in ./calc_in
select_code.check_calc_files()

#
#
# ---------- check point 2
#
#
if rin.stop_chkpt == 2:
    print('Stop at check point 2')
    raise SystemExit()

# ---------- make working directory
if not os.path.isdir('work{:04d}'.format(rin.njob - 1)):
    for i in range(rin.njob):
        if not os.path.isdir('work{:04d}'.format(i)):
            os.mkdir('work{:04d}'.format(i))

# ---------- instantiate Ctrl_job class
jobs = ctrl_job.Ctrl_job(stat, init_struc_data, opt_struc_data, rslt_data)
if rin.algo == 'RS':
    jobs.RS_init(RS_id_data)
elif rin.algo == 'BO':
    jobs.BO_init(BO_id_data, BO_data)
if rin.kpt_flag:
    jobs.kpt_data = kpt_data
if rin.energy_step_flag:
    jobs.energy_step_data = energy_step_data
if rin.struc_step_flag:
    jobs.struc_step_data = struc_step_data
if rin.fs_step_flag:
    jobs.fs_step_data = fs_step_data

# ---------- check job status
jobs.check_job()

# ---------- control job
print('\n# ---------- job status')
for work_id, jstat in enumerate(jobs.job_stat):
    # ------ set work_id and work_path
    jobs.work_id = work_id
    jobs.work_path = './work{:04d}/'.format(work_id)

    # ------ handle job
    if jstat == 'submitted':
        print('work{:04d}: still queuing or runnning'.format(work_id))
    elif jstat == 'done':
        jobs.handle_done()
    elif jstat == 'skip':
        jobs.ctrl_skip()
    elif jstat == 'else':
        raise ValueError('Wrong job_stat in ' +
                         jobs.work_path +
                         'stat_job. To skip this structure, write "skip" in stat_job line 3')
    elif jstat == 'no_file':
        jobs.ctrl_next_struc()
    else:
        raise ValueError('Unexpected error in '+jobs.work_path+'stat_job')

# ---------- BO
if rin.algo == 'BO':
    if jobs.logic_next_gen:
        # ------ log and out
        with open('cryspy.out', 'a') as fout:
            fout.write('\nDone generation {}\n\n'.format(jobs.gen))
        print('\nDone generation {}\n'.format(jobs.gen))

        # ------ done all structures
        if len(jobs.rslt_data) == rin.tot_struc:
            with open('cryspy.out', 'a') as fout:
                fout.write('\nDone all structures!\n')
            print('\nDone all structures!')
            raise SystemExit()

        # ------ check job status
        jobs.check_job()

        # ------ next generation
        if 'submitted' not in jobs.job_stat:

            # ---------- check point 3
            if rin.stop_chkpt == 3:
                print('Stop at check point 3: BO is ready')
                raise SystemExit()

            jobs.ctrl_next_gen()
