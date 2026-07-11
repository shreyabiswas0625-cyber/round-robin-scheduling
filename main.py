# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.



import matplotlib.pyplot as plt
from collections import deque

#Process class defines what a process contains
class Process:
    def __init__(self, pid, at, bt):
        self.pid = pid #process ID
        self.at = at #arrival time
        self.bt = bt #burst time
        self.remaining_bt = bt #remaining burst time
        self.ct = 0 #completion time
        self.tat = 0 #turnaround time
        self.wt = 0 #waiting time
        self.rt = -1  # response time


def round_robin(processes, tq):
    #INITIALIZATION
    time = 0
    queue = deque()
    gantt = [] #stores execution timeline
    completed = []
    n = len(processes)

#ensuring processes are handled in correct arrival order
    processes.sort(key=lambda x: x.at)
    i = 0

#loop runs until all processes are done
    while len(completed) < n:

        # Adds processes to queue when they arrive
        while i < n and processes[i].at <= time:
            queue.append(processes[i]) #add this process to deque
            i += 1 #move to next process

#If no process is ready then CPU waits.
        if not queue:
            time += 1
            continue

#take first item and return it
        current = queue.popleft()

        # Response Time
        #if this is process's first time running
        if current.rt == -1:
            current.rt = time - current.at

#how much time the process runs in its turn
        exec_time = min(tq, current.remaining_bt)
        #store in gantt chart (process, start time, end time)
        gantt.append((current.pid, time, time + exec_time))

#update time and remaining bt
        time += exec_time
        current.remaining_bt -= exec_time

        # Add newly arrived during execution
        while i < n and processes[i].at <= time:
            queue.append(processes[i])
            i += 1
#check for completion (if not finished send back to queue)
        if current.remaining_bt > 0:
            queue.append(current)
            #if finished calculate CT, TAT, WT
        else:
            current.ct = time
            current.tat = current.ct - current.at
            current.wt = current.tat - current.bt
            completed.append(current)

    return completed, gantt

#DISPLAY RESULTS
#table to show performance metrics of all processes
def display_results(processes):
    print("\nPID\tAT\tBT\tCT\tTAT\tWT\tRT")
    for p in processes:
        print(f"{p.pid}\t{p.at}\t{p.bt}\t{p.ct}\t{p.tat}\t{p.wt}\t{p.rt}")

#AVERAGES
    avg_wt = sum(p.wt for p in processes) / len(processes)
    avg_tat = sum(p.tat for p in processes) / len(processes)
    #Processes completed per unit time
    throughput = len(processes) / max(p.ct for p in processes)

    print(f"\nAverage WT: {avg_wt:.2f}")
    print(f"Average TAT: {avg_tat:.2f}")
    print(f"Throughput: {throughput:.2f}")

#GANNT CHART
def gantt_chart(gantt):
    for pid, start, end in gantt:
        plt.barh(1, end - start, left=start) #draws horizontal bars for each process
        plt.text((start + end) / 2, 1, pid, ha='center')

    plt.xlabel("Time")
    plt.title("Gantt Chart")
    plt.yticks([])
    plt.show()

#BAR GRAPHS
#graph 1: WT and graph 2: TAT
def bar_graph(processes):
    pids = [p.pid for p in processes]
    wt = [p.wt for p in processes]
    tat = [p.tat for p in processes]

    plt.figure()
    plt.bar(pids, wt)
    plt.title("Waiting Time vs Process")
    plt.show()

    plt.figure()
    plt.bar(pids, tat)
    plt.title("Turnaround Time vs Process")
    plt.show()

#LINE GRAPH
def line_graph(gantt, processes):
    time_points = []
    remaining_bt = []

#keeps track of remaining BT
    temp = {p.pid: p.bt for p in processes}

    for pid, start, end in gantt:
        for t in range(start, end):
            temp[pid] -= 1
            time_points.append(t)
            remaining_bt.append(temp[pid])

    plt.plot(time_points, remaining_bt)
    plt.title("Remaining Burst Time vs Time")
    plt.xlabel("Time")
    plt.ylabel("Remaining BT")
    plt.show()

#TIME QUANTUM COMPARISON
def compare_tq(original_processes):
    tqs = [2, 4, 6] #for each tq run algorithm, calculate avg wt & tat, plot graph
    avg_wts = []
    avg_tats = []

    for tq in tqs:
        # deep copy
        processes = [Process(p.pid, p.at, p.bt) for p in original_processes]
        completed, _ = round_robin(processes, tq)

        avg_wt = sum(p.wt for p in completed) / len(completed)
        avg_tat = sum(p.tat for p in completed) / len(completed)

        avg_wts.append(avg_wt)
        avg_tats.append(avg_tat)

    plt.plot(tqs, avg_wts, marker='o')
    plt.plot(tqs, avg_tats, marker='o')
    plt.title("Performance Comparison")
    plt.xlabel("Time Quantum")
    plt.ylabel("Time")
    plt.show()


#MAIN INPUT

n = int(input("Enter number of processes: "))
processes = []

for i in range(n):
    pid = input(f"Enter Process ID {i+1}: ")
    at = int(input("Arrival Time: "))
    bt = int(input("Burst Time: "))
    processes.append(Process(pid, at, bt))

tq = int(input("Enter Time Quantum: "))

completed, gantt = round_robin(processes, tq)

display_results(completed)
gantt_chart(gantt)
bar_graph(completed)
line_graph(gantt, completed)
compare_tq(processes)