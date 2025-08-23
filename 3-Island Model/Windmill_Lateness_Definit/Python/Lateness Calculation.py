
num_job=26
p=[10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]#production time for 10 jobs in minutes
d=[40, 95, 50, 50, 75, 50, 90, 40, 60, 20, 50, 35, 60, 45, 70, 60, 90, 40, 45, 60, 45, 60, 70, 80, 20, 90] # due date/time for 10 jobs in minutes
w=[2 , 1 , 2 , 2 , 2 , 3 , 2 , 1 , 4 , 1 , 5 , 1 , 2 , 1 , 1 , 3 , 3 , 2 , 4 , 4 , 5 , 4 , 3 , 1 , 1 , 3] #weight factors for importance indication

ptime=0
tardiness=0
for j in range(num_job):
    ptime=ptime+p[j]
    tardiness=tardiness+w[j]*max(ptime-d[j],0)
print(tardiness)
print("average tardiness:%f"%(tardiness/num_job))