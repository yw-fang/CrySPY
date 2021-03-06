#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import read_input as rin


def out_rslt(rslt_data):
    # ---------- asc in Struc_ID or Gen
    with open('./data/cryspy_rslt', 'w') as frslt:
        if rin.algo == 'RS' or rin.algo == 'LAQA':
            frslt.write(rslt_data.sort_values(by=['Struc_ID'], ascending=True).to_string(index=False))
        elif rin.algo == 'BO':
            frslt.write(rslt_data.sort_values(by=['Gen', 'Struc_ID'], ascending=True).to_string(index=False))

    # ---------- asc in energy
    with open('./data/cryspy_rslt_energy_asc', 'w') as fasc:
        fasc.write(rslt_data.sort_values(by=['Energy'], ascending=True).to_string(index=False))


# ---------- LAQA
def out_kpts(kpt_data):
    # ------ asc in ID
    with open('./data/kpts_rslt', 'w') as frslt:
        frslt.write('{0:>10}  {1:>10}\n'.format('Struc_ID', 'k-points'))
        for key, value in sorted(kpt_data.items()):
            frslt.write('{0:10d}  {1}\n'.format(key, value))


def out_LAQA_status(LAQA_step, LAQA_score, LAQA_energy, LAQA_bias):
    # ------ desc in score
    with open('./data/LAQA_status', 'w') as frslt:
        frslt.write('{0:>10}  {1:>14}  {2:>14}  {3:>14}  {4:>12}  {5:>12}\n'.format(
            'Struc_ID', 'Score', 'E(eV/atom)', 'Bias', 'Selection', 'Step'))
        for key, value in sorted(LAQA_score.items(), key=lambda x: -x[1][-1]):
            if LAQA_energy[key]:    # whether list is vacant or not?
                frslt.write('{0:10d}  {1: 14.8f}  {2: 14.8f}  {3: 14.8f}  {4:12d}  {5:12d}\n'.format(
                    key, value[-1], LAQA_energy[key][-1], LAQA_bias[key][-1],
                    len(LAQA_step[key]), sum(LAQA_step[key])))
            else:
                frslt.write('{0:10d}  {1: 14.8f}  {2:>14}  {3:>14}  {4:12d}  {5:12d}\n'.format(
                    key, value[-1], LAQA_energy[key], LAQA_bias[key], len(LAQA_step[key]), sum(LAQA_step[key])))


def out_LAQA_step(LAQA_step):
    # ------ asc in ID
    with open('./data/LAQA_step', 'w') as frslt:
        frslt.write('{0:>10}  {1:>4}\n'.format('Struc_ID', 'Step'))
        for key, value in sorted(LAQA_step.items()):
            frslt.write('{0:10d}'.format(key))
            for x in value:
                frslt.write('  {:4d}'.format(x))
            frslt.write('\n')


def out_LAQA_score(LAQA_score):
    # ------ asc in ID
    with open('./data/LAQA_score', 'w') as frslt:
        frslt.write('{0:>10}  {1:>14}\n'.format('Struc_ID', 'Score'))
        for key, value in sorted(LAQA_score.items()):
            frslt.write('{0:10d}'.format(key))
            for x in value:
                frslt.write('  {: 14.8f}'.format(x))
            frslt.write('\n')


def out_LAQA_energy(LAQA_energy):
    # ------ asc in ID
    with open('./data/LAQA_energy', 'w') as frslt:
        frslt.write('{0:>10}  {1:>12}\n'.format('Struc_ID', 'E(eV/atom)'))
        for key, value in sorted(LAQA_energy.items()):
            frslt.write('{0:10d}'.format(key))
            for x in value:
                frslt.write('  {: 12.8f}'.format(x))
            frslt.write('\n')


def out_LAQA_bias(LAQA_bias):
    # ------ asc in ID
    with open('./data/LAQA_bias', 'w') as frslt:
        frslt.write('{0:>10}  {1:>14}\n'.format('Struc_ID', 'Bias'))
        for key, value in sorted(LAQA_bias.items()):
            frslt.write('{0:10d}'.format(key))
            for x in value:
                frslt.write('  {: 14.8f}'.format(x))
            frslt.write('\n')


def out_LAQA_id_hist(id_select_hist):
    with open('./data/LAQA_select_id', 'w') as frslt:
        frslt.write('{0:>10}  {1:>5}\n'.format('Selection', 'ID'))
        for i, j in enumerate(id_select_hist):
            frslt.write('{0:10d}'.format(i+1))
            for x in j:
                frslt.write('  {:5d}'.format(x))
            frslt.write('\n')
