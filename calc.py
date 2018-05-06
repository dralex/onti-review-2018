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

profiles = 'АТС-1:АТС-2:БАС:БДиМО:ВРС:ИБС:ИРС:ИЭС:Нано:НМиС:ППТ:Финтех:VR:Космос:Нейро:Телеком:УД:ЯТ'.split(':')
profiles_cnt = len(profiles)
scores_exp = (3, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1)
experts_params_cnt = len(scores_exp)
scores_po = (2, 1, 1.5, 1.5, 1, 1, 1, 1, 1.5, 0.5, 2, 5)
po_params_cnt = len(scores_po)
scores_places = (3, 3)
places_params_cnt = len(scores_places)
scores_kids = 6

experts = []
for exp_file in glob.glob('exp-*.csv'):
    f = open(exp_file)
    exp_data = read_file(exp_file, experts_params_cnt, profiles_cnt)
    experts.append(exp_data)
exp_averages = []
for profile_idx in xrange(profiles_cnt):
    exp_averages.append([])
    for param in xrange(experts_params_cnt):
        a = []
        for e in experts:
            x = e[param][profile_idx]
            if x >= 0: 
                a.append(x)
        npa = np.array(a)
        exp_averages[-1].append(np.average(npa))
      
po = read_file('po.csv', po_params_cnt, profiles_cnt)

kids = read_file('kids.csv', profiles_cnt)
kids_averages = []
for p_idx in xrange(profiles_cnt):
    avg = np.average(np.array(kids[p_idx]))
    kids_averages.append(avg)

print 'Общая оценка профилей:'
print '----------------------'

results1 = np.dot(np.array(exp_averages), np.array(scores_exp))
print
print 'Оценка экспертов:'
print_results(profiles, results1)

results2 = np.dot(np.array(po).transpose(), np.array(scores_po))
print
print 'Оценка ПО:'
print_results(profiles, results2)

places_avg_1 = []
places_avg_2 = []
places1 = read_file('places1.csv', None, profiles_cnt)
places2 = read_file('places2.csv', None, profiles_cnt)
assert len(places1) == len(places2)
for profile_idx in xrange(profiles_cnt):
    a = []
    for p in places1:
        x = p[profile_idx]
        if x >= 0:
            a.append(x)
    if len(a) > 0:
        avg = np.average(np.array(a))
    else:
        avg = 5
    places_avg_1.append(avg)
    a = []
    for p in places2:
        x = p[profile_idx]
        if x >= 0:
            a.append(x)
    if len(a) > 0:
        avg = np.average(np.array(a))
    else:
        avg = 5
    places_avg_2.append(avg)
results3 = np.array(places_avg_1).transpose() * scores_places[0] + np.array(places_avg_2).transpose() * scores_places[1]
print
print 'Оценка площадок подготовки:'
print_results(profiles, results3)

results4 = scores_kids * np.array(kids_averages)
print
print 'Оценка участников:'
print_results(profiles, results4)
    
results = results1 + results2 + results4
print
print 'Общая оценка:'
print_results(profiles, results)
    
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
    print "{0}:{1}:{2}:{3}:{4}:{5}:{6}:{7}:{8}:{9}".format(profiles[i],
                                                           round(results1[i], 1),
                                                           round(results2[i], 1),
                                                           round(results3[i], 1),
                                                           round(results4[i], 1),
                                                           round(results[i], 1),
                                                           round(prof_averages[i], 2),
                                                           round(practices_po[i], 2),
                                                           round(exp_averages[i], 2),
                                                           round(results_pr[i], 2))
