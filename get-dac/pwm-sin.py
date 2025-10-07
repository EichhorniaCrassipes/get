import pwm_dac as pwm
import signal_generator as sg
import time

amplitude = 3.2         
signal_frequency = 5    
sampling_frequency = 100

PWM_PIN = 12
PWM_FREQUENCY = 1000

if __name__ == "__main__":
    dac = None
    try:
        dac = pwm.PWM_DAC(
            gpio_pin=PWM_PIN,
            pwm_frequency=PWM_FREQUENCY,
            dynamic_range=3.3,
            verbose=False
        )

        start_time = time.time()

        while True:
            t = time.time() - start_time
            normalized_amp = sg.get_sin_wave_amplitude(signal_frequency, t)
            voltage = normalized_amp * amplitude

            dac.set_voltage(voltage)
            sg.wait_for_sampling_period(sampling_frequency)

    finally:
        if dac is not None:
            dac.deinit()
