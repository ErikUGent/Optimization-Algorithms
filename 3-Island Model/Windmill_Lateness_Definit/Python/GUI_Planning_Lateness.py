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

population_size=int(input('Please input the size of population: ') or 30) # default value is 30
crossover_rate=float(input('Please input the size of Crossover Rate: ') or 0.9) # default value is 0.8
mutation_rate=float(input('Please input the size of Mutation Rate: ') or 0.1) # default value is 0.1
mutation_selection_rate=float(input('Please input the mutation selection rate: ') or 0.5)
num_mutation_jobs=round(num_job*mutation_selection_rate)
num_iteration=int(input('Please input number of iteration: ') or 2000) # default value is 2000

start_time = time.time()

#Initial population

Tbest=999999999999999
best_list,best_obj=[],[]
population_list=[]
for i in range(population_size):
    random_num=list(np.random.permutation(num_job)) # generate a random permutation of 0 to num_job-1
    population_list.append(random_num) # add to the population_list
        
for n in range(num_iteration):
    Tbest_now=99999999999           
    # cross-over
    parent_list=copy.deepcopy(population_list)
    offspring_list=copy.deepcopy(population_list)
    S=list(np.random.permutation(population_size)) # generate a random sequence to select the parent chromosome to crossover
    
    for m in range(int(population_size/2)):
        crossover_prob=np.random.rand()
        if crossover_rate>=crossover_prob:
            parent_1= population_list[S[2*m]][:]
            parent_2= population_list[S[2*m+1]][:]
            child_1=['na' for i in range(num_job)]
            child_2=['na' for i in range(num_job)]
            fix_num=round(num_job/2)
            g_fix=list(np.random.choice(num_job, fix_num, replace=False))
            
            for g in range(fix_num):
                child_1[g_fix[g]]=parent_2[g_fix[g]]
                child_2[g_fix[g]]=parent_1[g_fix[g]]
            c1=[parent_1[i] for i in range(num_job) if parent_1[i] not in child_1]
            c2=[parent_2[i] for i in range(num_job) if parent_2[i] not in child_2]
            
            for i in range(num_job-fix_num):
                child_1[child_1.index('na')]=c1[i]
                child_2[child_2.index('na')]=c2[i]
            offspring_list[S[2*m]]=child_1[:]
            offspring_list[S[2*m+1]]=child_2[:]
        
    # Mutation 
    for m in range(len(offspring_list)):
        mutation_prob=np.random.rand()
        if mutation_rate >= mutation_prob:
            m_chg=list(np.random.choice(num_job, num_mutation_jobs, replace=False)) # chooses the position to mutation
            t_value_last=offspring_list[m][m_chg[0]] # save the value which is on the first mutation position
            for i in range(num_mutation_jobs-1):
                offspring_list[m][m_chg[i]]=offspring_list[m][m_chg[i+1]] # displacement
            
            offspring_list[m][m_chg[num_mutation_jobs-1]]=t_value_last # move the value of the first mutation position to the last mutation position
    
    
    # Fitness calculation
    total_chromosome=copy.deepcopy(parent_list)+copy.deepcopy(offspring_list) # parent and offspring chromosomes combination
    chrom_fitness,chrom_fit=[],[]
    total_fitness=0
    for i in range(population_size*2):
        ptime=0
        tardiness=0
        for j in range(num_job):
            ptime=ptime+p[total_chromosome[i][j]]
            tardiness=tardiness+w[total_chromosome[i][j]]*max(ptime-d[total_chromosome[i][j]],0)
        chrom_fitness.append(1/tardiness)
        chrom_fit.append(tardiness)
        total_fitness=total_fitness+chrom_fitness[i]
    
    # Selection
    pk,qk=[],[]
    
    for i in range(population_size*2):
        pk.append(chrom_fitness[i]/total_fitness)
    for i in range(population_size*2):
        cumulative=0
        for j in range(0,i+1):
            cumulative=cumulative+pk[j]
        qk.append(cumulative)
    
    selection_rand=[np.random.rand() for i in range(population_size)]
    
    for i in range(population_size):
        if selection_rand[i]<=qk[0]:
            population_list[i]=copy.deepcopy(total_chromosome[0])
        else:
            for j in range(0,population_size*2-1):
                if selection_rand[i]>qk[j] and selection_rand[i]<=qk[j+1]:
                    population_list[i]=copy.deepcopy(total_chromosome[j+1])
                    break

    # Comparison
    for i in range(population_size*2):
        if chrom_fit[i]<Tbest_now:
            Tbest_now=chrom_fit[i]
            sequence_now=copy.deepcopy(total_chromosome[i])
    
    if Tbest_now<=Tbest:
        Tbest=Tbest_now
        sequence_best=copy.deepcopy(sequence_now)

    job_sequence_ptime=0
    num_tardy=0
    for k in range(num_job):
        job_sequence_ptime=job_sequence_ptime+p[sequence_best[k]]
        if job_sequence_ptime>d[sequence_best[k]]:
            num_tardy=num_tardy+1

# Printing the result
print("optimal sequence",sequence_best)
print("optimal value:%f"%Tbest)
print("average tardiness:%f"%(Tbest/num_job))
print("number of tardy:%d"%num_tardy)
print('the elapsed time:%s'% (time.time() - start_time))
