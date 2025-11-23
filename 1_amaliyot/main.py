import time
import os

def count_up(limit=None):
    seconds = 0
    try:
        while True:
            os.system("cls" if os.name == "nt" else "clear")
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            print("=" * 30)
            print("   ⏱️ TIMER (Count Up)   ")
            print("=" * 30)
            print(f"   {h:02d}:{m:02d}:{s:02d}")
            print("=" * 30)

            time.sleep(1)
            seconds += 1
            if limit and seconds > limit:
                break
    except KeyboardInterrupt:
        print("\nTimer to‘xtatildi.")

count_up(limit=int(input("Qancha vaqtga o'tishni xohlaysiz? "))) 
    