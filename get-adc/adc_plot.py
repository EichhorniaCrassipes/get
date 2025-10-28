import matplotlib.pyplot as plt

def plot_voltage_vs_time(time, voltage, max_voltage: float, max_time: float):
    plt.figure(figsize=(10, 6))
    plt.plot(time, voltage)
    plt.grid(True, alpha=.3)
    plt.ylim(0, max_voltage)
    plt.xlim(0, max_time)
    plt.xlabel("time, s")
    plt.ylabel("voltage, V")
    plt.title("График зависимости напряжения на входе АЦП от времени")
    plt.show()
    plt.close()


def plot_sampling_period_hist(sampling_periods, max_period):
    plt.figure(figsize=(10, 6))
    plt.hist(sampling_periods)
    plt.grid(True, alpha=.3)
    plt.xlim(0, max_period)
    plt.xlabel("period, s")
    plt.ylabel("number of measurements")
    plt.title("Распределение периодов дискретизации измерений по времени на одно измерение")
    plt.show()
    plt.close()
