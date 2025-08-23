import collections
from ortools.sat.python import cp_model


def main():
    # Data.
    
    jobs_data = [  # windmill = (worker_id, processing_time).
        [(0, 0), (1, 2), (2, 1), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (2, 6), (1, 2)],  # Service_Schedule 0 = between brackets, per windmill, how long a certain worker works on it
        [(1, 3), (0, 0), (0, 0), (0, 0), (0, 0), (1, 2), (2, 3), (1, 1), (1, 2), (0, 0), (0, 0), (0, 0), (2, 2), (2, 1), (0, 0), (0, 0)],  # Service_Schedule 1
        [(0, 0), (0, 0), (0, 0), (2, 2), (1, 4), (0, 0), (0, 0), (0, 0), (0, 0), (2, 4), (1, 3), (2, 1), (0, 0), (0, 0), (0, 0), (0, 0)],  # Service_Schedule 2
    ]
    
    workers_count = 1 + max(windmill[0] for job in jobs_data for windmill in job)
    all_workers = range(workers_count)
    # Computes horizon dynamically as the sum of all durations.
    horizon = sum(windmill[1] for job in jobs_data for windmill in job)

    # Create the model.
    model = cp_model.CpModel()

    # Named tuple to store information about created variables.
    windmill_type = collections.namedtuple('windmill_type', 'start end interval')
    # Named tuple to manipulate solution information.
    assigned_windmill_type = collections.namedtuple('assigned_windmill_type',
                                                'start job index duration')

    # Creates job intervals and add to the corresponding worker lists.
    all_windmills = {}
    workers_to_intervals = collections.defaultdict(list)

    for job_id, job in enumerate(jobs_data):
        for task_id, windmill in enumerate(job):
            worker = windmill[0]
            duration = windmill[1]
            suffix = '_%i_%i' % (job_id, task_id)
            start_var = model.NewIntVar(0, horizon, 'start' + suffix)
            end_var = model.NewIntVar(0, horizon, 'end' + suffix)
            interval_var = model.NewIntervalVar(start_var, duration, end_var,
                                                'interval' + suffix)
            all_windmills[job_id, task_id] = windmill_type(start=start_var,
                                                   end=end_var,
                                                   interval=interval_var)
            workers_to_intervals[worker].append(interval_var)

    # Create and add disjunctive constraints.
    for worker in all_workers:
        model.AddNoOverlap(workers_to_intervals[worker])

    # Precedences inside a job.
    for job_id, job in enumerate(jobs_data):
        for task_id in range(len(job) - 1):
            model.Add(all_windmills[job_id, task_id +
                                1].start >= all_windmills[job_id, task_id].end)

    # Makespan objective.
    obj_var = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(obj_var, [
        all_windmills[job_id, len(job) - 1].end
        for job_id, job in enumerate(jobs_data)
    ])
    model.Minimize(obj_var)

    # Creates the solver and solve.
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print('Solution:')
        # Create one list of assigned windmills per worker.
        assigned_jobs = collections.defaultdict(list)
        for job_id, job in enumerate(jobs_data):
            for task_id, windmill in enumerate(job):
                worker = windmill[0]
                assigned_jobs[worker].append(
                    assigned_windmill_type(start=solver.Value(
                        all_windmills[job_id, task_id].start),
                                       job=job_id,
                                       index=task_id,
                                       duration=windmill[1]))

        # Create per worker output lines.
        output = ''
        for worker in all_workers:
            # Sort by starting time.
            assigned_jobs[worker].sort()
            sol_line_tasks = 'worker ' + str(worker) + ': '
            sol_line = '          '

            for assigned_windmill in assigned_jobs[worker]:
                name = 'Service plan_%i_windmill_%i  ' % (assigned_windmill.job,
                                           assigned_windmill.index)
                # Add spaces to output to align columns.
                sol_line_tasks += '%-27s' % name

                start = assigned_windmill.start
                duration = assigned_windmill.duration
                sol_tmp = '[%i,%i]' % (start, start + duration)
                # Add spaces to output to align columns.
                sol_line += '%-27s' % sol_tmp

            sol_line += '\n'
            sol_line_tasks += '\n'
            output += sol_line_tasks
            output += sol_line

        # Finally print the solution found.
        print(f'Optimal Schedule Length: {solver.ObjectiveValue()}')
        print(output)
    else:
        print('No solution found.')

    # Statistics.
    print('\nStatistics')
    print('  - conflicts: %i' % solver.NumConflicts())
    print('  - branches : %i' % solver.NumBranches())
    print('  - wall time: %f s' % solver.WallTime())


if __name__ == '__main__':
    main()