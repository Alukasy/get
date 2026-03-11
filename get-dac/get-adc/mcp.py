from mcp3021_driver import MCP3021
import matplotlib.pyplot as plt 
import time 

def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize = (10,6))
    plt.plot(time, voltage, label = "U(t)")
    plt.xlabel("Время")
    plt.ylabel("Напряжение")
    plt.xlim(0, max(time) if time else 1)
    plt.ylim(0, max_voltage+0.5)
    plt.grid(True)
    plt.show()

def plot_sampling_period_hist(time):
    sampling_periods = [time[i] - time[i-1] for i in range(1, len(time))]
    plt.figure(figsize = (10,6))
    plt.hist(sampling_periods)
    plt.xlim(0,0.06)
    plt.grid(True)
    plt.show()

mcp = MCP3021()
voltage_values = []
time_values = []
time_periods = []
duration = 3
print("Пошла возня")

try:
    start = time.time()
    while time.time() - start < duration:
        last_time = time.time()
        time_values.append(time.time())
        voltage_values.append(mcp.get_voltage())
        time_periods.append(abs(last_time - time.time()))
    plot_voltage_vs_time(time_values, voltage_values, 3.3)
    plot_sampling_period_hist(time_periods)
finally:
    mcp.deinit()