import r2r_dac as r2r
import signal_generator as sg
import time

# Параметры генерируемого сигнала
amplitude = 3.2          # Амплитуда в вольтах (максимальное напряжение)
signal_frequency = 10    # Частота синусоиды, Гц
sampling_frequency = 1000  # Частота дискретизации, Гц

if __name__ == "__main__":
    dac = None
    try:
        # Создаём объект R2R-ЦАП
        # Предполагается, что в r2r_dac.R2R_DAC конструктор принимает:
        # (gpio_bits, dynamic_range, verbose)
        dac = r2r.R2R_DAC(
            gpio_bits=[16, 20, 21, 25, 26, 17, 27, 22],
            dynamic_range=3.3,
            verbose=False
        )

        # Запоминаем начальное время для синхронизации сигнала
        start_time = time.time()

        while True:
            # Текущее время относительно старта
            t = time.time() - start_time

            # Получаем нормализованную амплитуду синуса в диапазоне [0, 1]
            normalized_amp = sg.get_sin_wave_amplitude(signal_frequency, t)

            # Масштабируем до реального напряжения
            voltage = normalized_amp * amplitude

            # Подаем напряжение на ЦАП
            dac.set_voltage(voltage)

            # Ждём до следующего отсчёта
            sg.wait_for_sampling_period(sampling_frequency)

    finally:
        # Вызываем "деструктор" (метод deinit)
        if dac is not None:
            dac.deinit()
