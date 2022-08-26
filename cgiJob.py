#!/usr/bin/python3.6
# -*- coding: utf-8 -*-
from classFile import FileTable

listJob = FileTable ('b/cgi.csv', '\n', ',')
listJob.read()
listJob.delCol (14)
listJob.delCol (11)
listJob.delCol (10)
listJob.delCol (7)
listJob.delCol (3)
listJob.delCol (2)
print (listJob[0])

listJobGood = FileTable ('b/jobs.tsv', '\n', '\t')
listJobGood.append (listJob[0])

for job in listJob:
	if '2022' in job[1] and ('2022' in job[2] or '2023' in job[2]) and '"France"' == job[4] and 'java' not in job[7] and 'java' not in job[9] and job[8] not in '"confirmé" "expérimenté"': listJobGood.append (job)

listJobGood.delCol (8)
listJobGood.delCol (4)
listJobGood.delCol (1)
listJobGood.write()