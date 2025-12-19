#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IoT sensor simulyatsiyasi (Tkinter, standart kutubxonalar).
Har 2 soniyada yangi o'lchovlar, real vaqt grafika, CSVga yozish.
Java versiyasiga moslashtirilgan layout.
"""

import tkinter as tk
from tkinter import font
import random
from datetime import datetime
import os

# ---------------- CONFIG ----------------
UPDATE_INTERVAL_MS = 2000
MAX_POINTS = 60

CSV_PATH = "sensor_malumotlari.csv"
TIME_FORMAT = "%d.%m.%Y %H:%M:%S"

BG_COLOR = "#0F1428"       # Color(15, 20, 40)
PANEL_COLOR = "#28324A"    # Color(40, 50, 80)
TEXT_COLOR = "#D6DCE6"

COL_TEMP = "#FF5A5A"       # Color(255, 90, 90)
COL_HUM = "#50B4FF"        # Color(80, 180, 255)
COL_PRESS = "#64FF8C"      # Color(100, 255, 140)

# Ranges (original units)
TEMP_MIN, TEMP_MAX = 20.0, 32.0
HUM_MIN, HUM_MAX = 35.0, 65.0
PRESS_HPA_MIN, PRESS_HPA_MAX = 990.0, 1050.0
# convert hPa -> mm (1 hPa ≈ 0.75006 mmHg)
HPA_TO_MM = 0.75006
PRESS_MIN = PRESS_HPA_MIN * HPA_TO_MM  # ~742.5
PRESS_MAX = PRESS_HPA_MAX * HPA_TO_MM  # ~787.5

# ---------------- Data buffers ----------------
temps = []
hums = []
presses = []
times = []

# ---------------- CSV init ----------------
def init_csv():
    header = f"{'Vaqt':<20} | {'Harorat (°C)':<12} | {'Namlik (%)':<10} | {'Bosim (mm)':<12}\n"
    sep = "-" * (len(header) - 1) + "\n"
    # If file doesn't exist or is empty, write header
    write_header = not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0
    with open(CSV_PATH, "a", encoding="utf-8") as f:
        if write_header:
            f.write(header)
            f.write(sep)

def append_csv(now, t, h, p):
    # Format: vaqt | temp | hum | press
    line = f"{now} | {t:.2f} | {h:.1f} | {p:.1f}\n"
    with open(CSV_PATH, "a", encoding="utf-8") as f:
        f.write(line)

# ---------------- Main App ----------------
class IoTMonitorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("10-amaliy ish • IoT Sensor Simulyatsiyasi")
        self.configure(bg=BG_COLOR)
        self.geometry("1400x950")
        self.minsize(1000, 700)

        # Fonts (Java versiyasiga mos)
        self.font_title = font.Font(family="Consolas", size=38, weight="bold")
        self.font_sub = font.Font(family="Segoe UI", size=18)
        self.font_big = font.Font(family="Consolas", size=52, weight="bold")
        self.font_legend = font.Font(family="Segoe UI", size=22, weight="bold")
        self.font_label = font.Font(family="Segoe UI", size=22, weight="bold")

        # Canvas for entire window (like Java Canvas)
        self.canvas = tk.Canvas(self, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.on_resize)

        # initialize csv
        init_csv()

        # start updates
        self.updating = True
        self.after(1000, self.update_once)  # start after 1s

    def on_resize(self, event=None):
        # Redraw everything on resize
        self.redraw_all()

    def redraw_all(self):
        self.canvas.delete("all")
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        
        if w <= 0 or h <= 0:
            return

        # Background
        self.canvas.create_rectangle(0, 0, w, h, fill=BG_COLOR, outline=BG_COLOR)

        # Title
        self.canvas.create_text(
            w//2, 90, 
            text="IoT Sensor Monitoring", 
            font=self.font_title, 
            fill="#64C8FF", 
            anchor="center"
        )

        # Real-time clock
        now_text = datetime.now().strftime(TIME_FORMAT)
        self.canvas.create_text(
            w//2, 130, 
            text=f"Real vaqt rejimida • {now_text}", 
            font=self.font_sub, 
            fill="#E0E0E0", 
            anchor="center"
        )

        if not temps:
            return

        # === YUQORIDA KATTA RAQAMLAR (Java: 120, 250/350/450) ===
        t = temps[-1]
        hu = hums[-1]
        p = presses[-1]

        self.canvas.create_text(
            120, 250, 
            text=f"{t:.2f} °C", 
            font=self.font_big, 
            fill=COL_TEMP, 
            anchor="w"
        )
        self.canvas.create_text(
            120, 350, 
            text=f"{hu:.1f} %", 
            font=self.font_big, 
            fill=COL_HUM, 
            anchor="w"
        )
        self.canvas.create_text(
            120, 450, 
            text=f"{p:.1f} mm", 
            font=self.font_big, 
            fill=COL_PRESS, 
            anchor="w"
        )

        # === ENG PASTDA TO'RTBURCHAK ICHIDA GRAFIK ===
        box_x = 80
        box_y = 520
        box_w = w - 160
        box_h = h - box_y - 80

        # To'rtburchak ramka (rounded rectangle simulation)
        self.canvas.create_rectangle(
            box_x - 15, box_y - 50, 
            box_x + box_w + 15, box_y + box_h + 60, 
            fill=PANEL_COLOR, 
            outline="#3C4A66", 
            width=2
        )

        # Title above graph
        self.canvas.create_text(
            box_x + 20, box_y - 10, 
            text="Vaqt o'tishi bilan o'zgarish", 
            font=self.font_label, 
            fill="white", 
            anchor="w"
        )

        # Inner graph area (dark background)
        self.canvas.create_rectangle(
            box_x, box_y, 
            box_x + box_w, box_y + box_h, 
            fill="#0F1626", 
            outline="#55607C", 
            width=2
        )

        # Draw graphs with clipping (using create_rectangle clipping region)
        # Tkinter doesn't have setClip, but we can use canvas clipping by drawing only inside bounds
        if len(temps) >= 2:
            self._draw_graphs(box_x, box_y, box_w, box_h)

        # === AFSONA — O'NG YUQORI BURCHAKDA (grafikdan tashqarida!) ===
        legend_x = w - 380
        legend_y = 180
        self._draw_legend(legend_x, legend_y, COL_TEMP, "Harorat")
        self._draw_legend(legend_x, legend_y + 40, COL_HUM, "Namlik")
        self._draw_legend(legend_x, legend_y + 80, COL_PRESS, "Bosim")

    def _draw_legend(self, x, y, color, text):
        # Draw circle
        self.canvas.create_oval(
            x, y - 12, 
            x + 24, y + 12, 
            fill=color, 
            outline=color
        )
        # Draw text
        self.canvas.create_text(
            x + 35, y, 
            text=text, 
            font=self.font_legend, 
            fill="white", 
            anchor="w"
        )

    def _draw_graphs(self, box_x, box_y, box_w, box_h):
        # Draw graph lines (clipped to box area by ensuring coords are within bounds)
        self._draw_graph_line(temps, TEMP_MIN, TEMP_MAX, COL_TEMP, box_x, box_y, box_w, box_h)
        self._draw_graph_line(hums, HUM_MIN, HUM_MAX, COL_HUM, box_x, box_y, box_w, box_h)
        self._draw_graph_line(presses, PRESS_MIN, PRESS_MAX, COL_PRESS, box_x, box_y, box_w, box_h)

    def _draw_graph_line(self, data, vmin, vmax, color, x, y, w, h):
        points = min(len(data), MAX_POINTS)
        if points < 2:
            return

        # Draw lines connecting points (like Java version)
        for i in range(1, points):
            idx1 = len(data) - points + i - 1
            idx2 = len(data) - points + i

            # Calculate x positions
            px1 = x + (i - 1) * w // (points - 1)
            px2 = x + i * w // (points - 1)

            # Calculate y positions (inverted: larger value -> smaller y)
            if vmax == vmin:
                py1 = py2 = y + h // 2
            else:
                py1 = y + h - int((data[idx1] - vmin) / (vmax - vmin) * h)
                py2 = y + h - int((data[idx2] - vmin) / (vmax - vmin) * h)

            # Clamp to box bounds (simulating clipping)
            py1 = max(y, min(y + h, py1))
            py2 = max(y, min(y + h, py2))

            # Draw line with thick stroke (width=7 like Java)
            self.canvas.create_line(
                px1, py1, px2, py2,
                fill=color,
                width=7,
                capstyle=tk.ROUND,
                joinstyle=tk.ROUND
            )

    def update_once(self):
        # Generate new values (like Java version)
        t = 20 + random.random() * 12
        hu = 35 + random.random() * 30
        p_hpa = 990 + random.random() * 60
        p = p_hpa * HPA_TO_MM

        # Round values
        t = round(t * 100) / 100.0
        hu = round(hu * 10) / 10.0
        p = round(p * 10) / 10.0

        now = datetime.now().strftime(TIME_FORMAT)

        # Append to buffers
        temps.append(t)
        hums.append(hu)
        presses.append(p)
        times.append(now)

        # Keep only last MAX_POINTS
        if len(temps) > MAX_POINTS:
            temps.pop(0)
            hums.pop(0)
            presses.pop(0)
            times.pop(0)

        # Write to CSV
        append_csv(now, t, hu, p)

        # Redraw canvas
        self.redraw_all()

        # Schedule next update
        if self.updating:
            self.after(UPDATE_INTERVAL_MS, self.update_once)

    def on_close(self):
        self.updating = False
        self.destroy()

# ---------------- Run ----------------
if __name__ == "__main__":
    app = IoTMonitorApp()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
