import matplotlib.pyplot as plt 

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