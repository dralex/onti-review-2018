#!/usr/bin/python3
# -*- coding: utf-8 -*-

import glob
import math
import numpy as np

def read_file(name, rows, columns = None):
    f = open(name)
    data_array = []
    for line in f:
        if line[0:2] == 'А':
            continue
        data_row = map(lambda x: (int(x) if len(x) > 0 else -1), line.strip().split(':'))
        assert columns == None or len(data_row) == columns
        data_array.append(data_row)
    assert rows == None or len(data_array) == rows
    return data_array

def print_results(profiles, res, precision = 1):
    print_results = []
    for i in xrange(len(res)):
        print_results.append((profiles[i], res[i]))
    i = 1
    for r in sorted(list(print_results), key=lambda x: x[1], reverse=True):
        print '{0:>2}. {1:<8}\t{2}'.format(i, r[0], np.round(r[1], precision))
        i += 1

def print_matrix(profiles, m, precision = 1):
    rows = len(m[0])
    print(':' + ':'.join(profiles))
    for i in xrange(rows):
        a = ["{0}".format(i)]
        for prof in m:
            a.append("{0}".format(np.round(prof[i], precision)))
        print ':'.join(a)
        
profiles = 'Космоснимки:AR:Аэрокосминж:Геном:ИТБез:Кибер:Когнит:Композ:НаучКом:Ракеты'.split(':')
profiles_cnt = len(profiles)
scores_exp = (3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 4)
experts_params_cnt = len(scores_exp)

experts = []
for exp_file in glob.glob('exp-*.csv'):
    f = open(exp_file)
    exp_data = read_file(exp_file, experts_params_cnt, profiles_cnt)
    experts.append(exp_data)
exp_averages = []
exp_votes = []
for profile_idx in xrange(profiles_cnt):
    exp_averages.append([])
    v = 0
    for param in xrange(experts_params_cnt):
        a = []
        for e in experts:
            x = e[param][profile_idx]
            if x >= 0: 
                a.append(x)
                v += 1
        npa = np.array(a)
        exp_averages[-1].append(np.average(npa))
    exp_votes.append(v)
print 'Общая оценка профилей:'
print '----------------------'

results1 = np.dot(np.array(exp_averages), np.array(scores_exp))
print 'Средние оценки экспертов:'
print_matrix(profiles, exp_averages)
print
print 'Оценка экспертов:'
print_results(profiles, results1)

print
print
print 'Практики будущего:'
print '------------------'

prof_averages = []
practices_prof = read_file('pract-prof.csv', None, profiles_cnt)
for profile_idx in xrange(profiles_cnt):
    a = []
    for p in practices_prof:
        x = p[profile_idx]
        if x >= 0:
            a.append(x)
    avg = np.average(np.array(a))
    prof_averages.append(avg)
print
print 'Оценка профилей:'
print_results(profiles, prof_averages, 2)

practices_po = read_file('pract-po.csv', 1, profiles_cnt)[0]
print
print 'Оценка Программного комитета ПО:'
print_results(profiles, practices_po, 0)

exp_averages = []
practices_exp = read_file('pract-exp.csv', None, profiles_cnt)
for profile_idx in xrange(profiles_cnt):
    a = []
    for p in practices_exp:
        x = p[profile_idx]
        if x >= 0:
            a.append(x)
    avg = np.average(np.array(a))
    exp_averages.append(avg)
print
print 'Оценка экспертов:'
print_results(profiles, exp_averages, 1)

results_pr = np.array(prof_averages) / 3.0 + np.array(practices_po) / 3.0 + np.array(exp_averages) / 3.0
print
print 'Общая оценка:'
print_results(profiles, results_pr, 2)

print
for i in xrange(profiles_cnt):
    print "{0}:{1}:{2}:{3}:{4}:{5}".format(profiles[i],
                                           round(results1[i], 1),
                                           round(prof_averages[i], 2),
                                           round(practices_po[i], 2),
                                           round(exp_averages[i], 2),
                                           round(results_pr[i], 2))
    
