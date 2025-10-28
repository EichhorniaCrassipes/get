from r2r_adc import R2R_ADC
from adc_plot import plot_voltage_vs_time as plot, plot_sampling_period_hist as hist
from time import time, sleep

voltage_values = list()
time_values = list()
sampling_periods = list()
duration = 3.
max_voltage = 3.56

if __name__ == "__main__":
    try:
        adc = R2R_ADC(3.29)
        for _ in range(3, 0, -1):
            print(f"Установка готова, начало измерений через {_}...", end='\b\r')
            sleep(1)
        print("Установка готова, измеряем...                  ")

        exp_start = time()
        while time() - exp_start <= duration:
            voltage_values.append(adc.get_sc_voltage())
            time_values.append(time() - exp_start)

        for i in range(1, len(time_values)):
            sampling_periods.append(time_values[i] - time_values[i-1])

        print("Измерения завершены.")

        plot(time_values, voltage_values, max_voltage, duration)
        hist(sampling_periods, max(sampling_periods))  # 
    except KeyboardInterrupt:
        print("Выключение...")
    except Exception as e:
        print(f"Ошибка: \"[{e.__class__.__name__}]: {e.args if len(e.args) > 0 else '<no args>'}\"")
