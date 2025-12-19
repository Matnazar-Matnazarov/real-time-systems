import psutil
from collections import deque
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime as dt

max_points = 30
cpu_data = deque(maxlen=max_points)
ram_data = deque(maxlen=max_points)
timestamps = deque(maxlen=max_points)

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9,6))
fig.tight_layout(pad=3.0)

# Dastlabki chiziqlar
cpu_line, = ax1.plot([], [], 'r-o', label="CPU")
ram_line, = ax2.plot([], [], 'b-o', label="RAM")

ax1.set_title("CPU foydalanish (%)")
ax2.set_title("RAM foydalanish (%)")

ax1.set_ylim(0, 100)
ax2.set_ylim(0, 100)

ax1.set_ylabel("CPU %")
ax2.set_ylabel("RAM %")
ax2.set_xlabel("Vaqt")

ax1.legend(loc="upper right")
ax2.legend(loc="upper right")

def update(frame):
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory().percent
    t = dt.datetime.now().strftime("%H:%M:%S")

    cpu_data.append(cpu)
    ram_data.append(ram)
    timestamps.append(t)

    cpu_line.set_data(timestamps, cpu_data)
    ram_line.set_data(timestamps, ram_data)

    ax1.set_xlim(timestamps[0], timestamps[-1])
    ax2.set_xlim(timestamps[0], timestamps[-1])

    return cpu_line, ram_line

ani = FuncAnimation(fig, update, interval=2000, blit=False)
plt.show()
