# -*- coding: utf-8 -*-

# Each of n maintenance jobs (numbered 1,...,n) is to be processed without 
# interruption on a sequence of windmills that can handle no more than one job at a time.
# We ttherefore make a link btween maintenance jobs and windmills, on which jobs need to be carried out in sequence.
# (analogy with a sequence of jobs on one machine: one cannot start before the previous one has finished)
# job j (j= 1,...,n) becomes available for processing at time zero, 
# requires an uninterrupted positive processing time p(j), 
# has a positive weight w(j), and 
# has a due date d(j) by which it should ideally be finished. 
# For a given processing order of the jobs, the 
# earliest completion time C(j) (= for example, C(2) is sum of production times of job 0, 1 en 2)
# and the tardiness T(j)=max{C(j)-d(j),0} of 
# job j (j=1,...,n) can readily be computed. The problem
# is to find a processing order of the jobs with minimum
# total weighted tardiness SUM{j=1,...,n}w(j)T(j)

# importing required modules
import numpy as np
import time
import copy

# setting the parameters
#num_job=int(input('Please input the number of maintenance jobs: ')) # number of maintenance jobs
num_job=26

p=[10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10] #production time for 10 jobs in minutes
d=[20,75,90,60,50,40,95,60,80,90,45,70,50,35,40,45,40,50,60,60,20,50,45,60,90,70] # due date/time for 10 jobs in minutes
w=[1,2,3,4,2,2,1,4,1,3,4,1,2,1,2,5,1,3,4,2,1,5,1,3,2,3] #weight factors for importance indication
# raw_input is used in python 2

population_size=1

#Initial population

random_num=list(np.random.permutation(num_job)) # generate a random permutation of 0 to num_job-1
# Fitness calculation
ptime=0
tardiness=0
for j in range(num_job):
    ptime=ptime+p[random_num[j]]
    tardiness=tardiness+w[random_num[j]]*max(ptime-d[random_num[j]],0)

    
# Printing the result
print("Random sequence",random_num)
print("Tardiness:%f"%tardiness)
print("average tardiness:%f"%(tardiness/num_job))

