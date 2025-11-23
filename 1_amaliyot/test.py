import psutil

# CPU foiz yuklanishi
print("CPU ishlatilishi (%):", psutil.cpu_percent(interval=1))

# Har bir yadroning yuklanishi
print("Yadro bo‘yicha CPU:", psutil.cpu_percent(interval=1, percpu=True))

# RAM ma’lumotlari
mem = psutil.virtual_memory()
print("Umumiy RAM:", mem.total // (1024 * 1024), "MB")
print("Band RAM:", mem.used // (1024 * 1024), "MB")
print("Bo‘sh RAM:", mem.available // (1024 * 1024), "MB")
