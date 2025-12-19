import heapq
import time

class EDFTask:
    def __init__(self, deadline, name):
        self.deadline = deadline
        self.name = name

    def __lt__(self, other):
        return self.deadline < other.deadline

tasks = []
heapq.heappush(tasks, EDFTask(3, "Sensor o‘qish"))
heapq.heappush(tasks, EDFTask(1, "Favqulodda signal"))
heapq.heappush(tasks, EDFTask(5, "Ma’lumot yozish"))

while tasks:
    task = heapq.heappop(tasks)
    print(f"{task.name} bajarilmoqda (deadline={task.deadline})")
    time.sleep(1)
