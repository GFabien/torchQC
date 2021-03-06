#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
script to generate jobs
"""
import pandas as pd
from script.create_jobs import create_jobs
from utils_file import get_parent_path

# parameters
root_dir = '/network/lustre/iss01/cenir/analyse/irm/users/romain.valabregue/QCcnn/NN_regres_motion/'
prefix = "/network/lustre/iss01/cenir/analyse/irm/users/romain.valabregue/QCcnn/job/job_eval/"

name = 'cati_all_ms_ela1_train200'
name = 'cati_all_ms_train_cati_ms'
name = 'cati_all_T1_train_cati_T1'

model = root_dir+'RegMotNew_ela1_train200_hcp400_ms_B4_nw0_Size182_ConvN_C16_256_Lin40_50_D0_BN_Loss_L1_lr0.0001/model_ep3_it9500.pt'
model = root_dir+'RegMotNew_ela1_train_cati_ms_B4_nw0_Size182_ConvN_C16_256_Lin40_50_D0_BN_Loss_L1_lr0.0001/model_ep8_it1249.pt'
model = root_dir+'RegMotNew_ela1_train_cati_T1_B4_nw0_Size182_ConvN_C16_256_Lin40_50_D0_BN_Loss_L1_lr0.0001/model_ep8_it1249.pt'

split = 10

model_name = get_parent_path(model)[1][:-3]
if 'cati_all_ms' in name:
    res = pd.read_csv('/home/romain.valabregue/datal/QCcnn/CATI_datasets/cati_cenir_all_ms.csv')
elif 'cati_all_T1' in name:
    res = pd.read_csv('/home/romain.valabregue/datal/QCcnn/CATI_datasets/cati_cenir_all_T1.csv')

fin_all = res.filename

nb_jobs = len(fin_all)//split + 1
jobs = []
for njob in range(0, nb_jobs):
    fin = fin_all[njob*split:(njob+1)*split]

    scriptsDir = '/network/lustre/iss01/cenir/software/irm/toolbox_python/romain/torchQC'

    py_options = '--use_gpu 0 --saved_model {} --out_name {} --val_number {}'.format(model, name, njob)

    job_id = name + model_name
    params = dict()
    params['output_directory'] = prefix + '/jobs/' + job_id
    params['scripts_to_copy'] = scriptsDir #+ '/*.py'

    cmd_init = '\n'.join(["#source /network/lustre/iss01/cenir/software/irm/bin/python_path3.6",
                          "#source activate pytorch1.2",
                          "python " + scriptsDir + "/do_eval_model.py \\",
                          py_options + " \\"] )

    inputs = ','.join(list(fin))

    job = '\n'.join([cmd_init, ' -i ' + inputs ])
    jobs.append(job)

params['jobs'] = jobs
params['job_name'] = job_id
params['cluster_queue'] = 'bigmem,normal'
params['cpus_per_task'] = 1
params['mem'] = 4000
params['walltime'] = '12:00:00'
params['job_pack'] = 1

create_jobs(params)

